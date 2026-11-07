#!/usr/bin/env python3
"""gerar.py — atalho para usar o GPT Image 2.6 pela API da OpenAI.

Gera imagem, SVG ou GIF, ou edita uma imagem (com markup opcional), já com os
ajustes novos do 2.6: complexity (quanto o modelo planeja) e quality (quanto detalhe).

Só usa a biblioteca padrão do Python 3.9+ (não precisa instalar nada).
Precisa da variável OPENAI_API_KEY com uma chave da API da OpenAI
(criada em https://platform.openai.com/api-keys; a API é cobrada à parte da assinatura do ChatGPT).
Use --seco para ver o pedido montado sem chamar a API nem gastar nada.

Exemplos:
  python3 gerar.py "Cartaz com o texto \"VERÃO 2027\"" --seco
  python3 gerar.py "Logo de padaria, formas simples" --formato svg --fundo transparente
  python3 gerar.py "Gato pisca e volta à pose inicial, câmera parada" --formato gif --quadros 9 --ms 200
  python3 gerar.py "Pinte de azul o vaso dentro do círculo vermelho. Não mude mais nada. Tire o círculo." \
      --editar exemplos/cozinha.webp --markup exemplos/circulo.png --complexity low
"""
import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path

API = "https://api.openai.com/v1/images/"
MODELOS = {"flare": "gpt-image-2.6-flare", "sunburst": "gpt-image-2.6-sunburst"}
FUNDOS = {"auto": "auto", "opaco": "opaque", "transparente": "transparent"}
TIPOS = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}


def montar(a):
    """Devolve (endpoint, campos) do pedido, sem abrir arquivos."""
    p = {"model": MODELOS[a.modelo], "prompt": a.prompt, "quality": a.quality,
         "size": a.tamanho, "output_format": a.formato}
    if a.complexity:
        p["complexity"] = a.complexity  # se omitir, o padrão do 2.6 é "high"
    if a.fundo != "auto":
        p["background"] = FUNDOS[a.fundo]
    if a.formato == "gif":
        p["frame_count"] = a.quadros
        p["frame_duration_ms"] = a.ms
    p["n"] = 1 if a.formato == "svg" else a.n  # SVG: sempre 1
    endpoint = "edits" if a.editar else "generations"
    if a.editar:
        p["image"] = a.editar
        if a.markup:
            p["markup"] = a.markup
    return endpoint, p


def validar(a):
    erros = []
    if a.formato == "svg" and a.editar:
        erros.append("SVG só sai em geração nova; a edição não devolve SVG.")
    if a.markup and not a.editar:
        erros.append("--markup só vale junto com --editar (vai na 1ª imagem).")
    if a.formato == "gif" and not (2 <= a.quadros <= 16):
        erros.append("GIF: --quadros de 2 a 16.")
    if a.formato == "gif" and not (20 <= a.ms <= 2000):
        erros.append("GIF: --ms de 20 a 2000 por quadro.")
    if a.tamanho != "auto":
        try:
            w, h = (int(x) for x in a.tamanho.lower().split("x"))
        except ValueError:
            erros.append("--tamanho no formato LARGURAxALTURA, ex.: 1024x1536.")
        else:
            if w % 16 or h % 16:
                erros.append("--tamanho: largura e altura em múltiplos de 16.")
            if a.formato != "gif" and max(w, h) / min(w, h) > 3:
                erros.append("--tamanho: proporção entre 1:3 e 3:1.")
    for f in (a.editar, a.markup):
        if f and not Path(f).exists():
            erros.append(f"arquivo não encontrado: {f}")
        elif f and Path(f).suffix.lower() not in TIPOS:
            erros.append(f"formato não aceito: {f} (use png, jpg ou webp)")
    if a.markup and Path(a.markup).suffix.lower() != ".png":
        erros.append("--markup tem de ser PNG transparente.")
    return erros


def multipart(campos):
    """Monta o corpo multipart/form-data (arquivos em image e markup)."""
    limite = uuid.uuid4().hex
    partes = []
    for k, v in campos.items():
        partes.append(f"--{limite}\r\n".encode())
        if k in ("image", "markup"):
            arq = Path(v)
            tipo = TIPOS.get(arq.suffix.lower()) or mimetypes.guess_type(arq.name)[0] or "application/octet-stream"
            partes.append(f'Content-Disposition: form-data; name="{k}"; filename="{arq.name}"\r\n'
                          f"Content-Type: {tipo}\r\n\r\n".encode())
            partes.append(arq.read_bytes())
            partes.append(b"\r\n")
        else:
            partes.append(f'Content-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    partes.append(f"--{limite}--\r\n".encode())
    return b"".join(partes), f"multipart/form-data; boundary={limite}"


def chamar(endpoint, p, chave):
    if endpoint == "edits":
        corpo, tipo = multipart(p)
    else:
        corpo, tipo = json.dumps(p).encode(), "application/json"
    req = urllib.request.Request(API + endpoint, data=corpo, method="POST",
                                 headers={"Authorization": f"Bearer {chave}", "Content-Type": tipo})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8", "replace")
        raise SystemExit(f"ERRO da API ({e.code}): {msg[:600]}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Gera ou edita imagem com o GPT Image 2.6.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("prompt", help="o que você quer (entre aspas)")
    ap.add_argument("--modelo", choices=MODELOS, default="flare",
                    help="flare = rápido (rascunho); sunburst = detalhe e edição precisa")
    ap.add_argument("--complexity", choices=["low", "medium", "high"],
                    help="quanto o modelo planeja antes de desenhar (se omitir, o modelo usa high)")
    ap.add_argument("--quality", choices=["auto", "low", "medium", "high", "xhigh", "max"],
                    default="medium", help="quanto detalhe visual")
    ap.add_argument("--tamanho", default="auto", help="auto ou LxA, ex.: 1024x1536")
    ap.add_argument("--formato", choices=["png", "jpeg", "webp", "svg", "gif"], default="png")
    ap.add_argument("--fundo", choices=FUNDOS, default="auto")
    ap.add_argument("--quadros", type=int, default=9, help="GIF: 2 a 16 quadros")
    ap.add_argument("--ms", type=int, default=200, help="GIF: milissegundos por quadro")
    ap.add_argument("--n", type=int, default=1, help="quantas versões (SVG é sempre 1)")
    ap.add_argument("--editar", help="imagem de entrada (png, jpg ou webp): liga o modo edição")
    ap.add_argument("--markup", help="PNG transparente do mesmo tamanho, com o círculo/risco")
    ap.add_argument("--saida", default="saida", help="nome base do arquivo gerado")
    ap.add_argument("--seco", action="store_true", help="só mostra o pedido, não chama a API")
    a = ap.parse_args(argv)

    erros = validar(a)
    if erros:
        for e in erros:
            print("ERRO:", e, file=sys.stderr)
        return 2

    endpoint, p = montar(a)
    if a.seco:
        print(f"POST /v1/images/{endpoint}")
        print(json.dumps(p, ensure_ascii=False, indent=2))
        return 0

    chave = os.environ.get("OPENAI_API_KEY")
    if not chave:
        print("ERRO: defina OPENAI_API_KEY (chave em https://platform.openai.com/api-keys).", file=sys.stderr)
        return 2
    r = chamar(endpoint, p, chave)
    ext = a.formato if a.formato != "jpeg" else "jpg"
    dados = r.get("data") or []
    for i, item in enumerate(dados, 1):
        nome = f"{a.saida}.{ext}" if len(dados) == 1 else f"{a.saida}-{i}.{ext}"
        Path(nome).write_bytes(base64.b64decode(item["b64_json"]))
        print("salvo:", nome)
    if "usage" in r:
        print("uso (tokens):", json.dumps(r["usage"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
