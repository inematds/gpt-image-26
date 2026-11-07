# GPT Image 2.6 na prática

[![GPT Image 2.6 na prática](guia/assets/banner.jpg)](https://inematds.github.io/gpt-image-26/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

O GPT Image 2.6 é o modelo de imagem mais novo da OpenAI, que já roda dentro do ChatGPT e do Codex e também pode ser usado pela API. Este repositório é um guia para quem cria imagens para posts, anúncios, logos, histórias ou vídeos e quer tirar proveito das novidades: o ajuste de complexidade (quanto o modelo planeja antes de desenhar), GIF animado, logo em vetor (SVG) e edição só na área que você marca. Para usar basta uma conta do ChatGPT; para a API, uma chave da OpenAI (cobrada à parte da assinatura) e o script `gerar.py`, que só precisa do Python.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/gpt-image-26/guia/**

## Conteúdo

| Arquivo | O que é |
|---|---|
| `guia/` | Página do guia em PT, com `en/` e `es/` |
| `prompts.md` | 10 prompts prontos: estrutura, complexidade, instruções em sequência, cartaz, personagem, referência salva, GIF, SVG, markup e edição |
| `gerar.py` | Atalho para a API (só biblioteca padrão do Python): gera imagem, SVG ou GIF, ou edita com markup, já com `complexity` e `quality`; confere os limites antes de gastar |
| `exemplos/baixar.py` | Baixa a foto e o círculo de exemplo da OpenAI para testar a edição com markup |
| `tests/` | Testes do `gerar.py` sem chamar a API: `python3 -m unittest discover tests` |

## O processo, do início ao fim

| # | Passo | Comando | Quem faz |
|---|---|---|---|
| 1 | Escolher o modelo: Flare (rápido) ou Sunburst (detalhe) | — | 🧠 você |
| 2 | Escrever o pedido em seções (cena, sujeito, detalhes, restrições, texto entre aspas) | `prompts.md` | 🧠 você |
| 3 | Ver o pedido sem gastar | `python3 gerar.py "<prompt>" --seco` | ⚙️ script |
| 4 | Gerar e comparar: primeiro a complexidade, depois a qualidade | `python3 gerar.py "<prompt>" --complexity high --quality medium` | ⚙️ script (API, cobrado na sua conta) |
| 5 | Conferir mão, proporção, reflexo, contagem e texto | — | 🧠 você |
| 6 | Editar uma coisa por vez (ou circular com markup) | `python3 gerar.py "<mudança>" --editar exemplos/cozinha.webp --markup exemplos/circulo.png --complexity low` | ⚙️ script |

No ChatGPT os passos 3, 4 e 6 são só conversa: peça a imagem, o GIF ("sprite sheet 3x3 … em loop") ou o SVG.

## Uso rápido da API

```bash
export OPENAI_API_KEY="sua-chave"        # Windows PowerShell: $env:OPENAI_API_KEY="sua-chave"
python3 gerar.py 'Cartaz com o texto "VERÃO 2027"' --modelo sunburst --quality high --seco
python3 gerar.py "Logo de padaria, formas simples" --formato svg --fundo transparente
python3 gerar.py "Gato pisca e volta à pose inicial, câmera parada" --formato gif --quadros 9 --ms 200
python3 exemplos/baixar.py
python3 gerar.py "Pinte de azul o vaso no círculo. Não mude mais nada. Tire o círculo." --editar exemplos/cozinha.webp --markup exemplos/circulo.png --complexity low
```

A chave da API é criada em https://platform.openai.com/api-keys e cobrada à parte da assinatura do ChatGPT.

No Windows, use `py` no lugar de `python3`. Sem Git, baixe o [ZIP](https://github.com/inematds/gpt-image-26/archive/refs/heads/main.zip).

`python3 gerar.py --help` lista todas as opções e os padrões (modelo `flare`, qualidade `medium`). Cada pedido real é cobrado na sua conta da OpenAI.

## Custo (calculadora oficial, imagem 1024×1024)

| Qualidade | GPT Image 2.5 | GPT Image 2.6 |
|---|---|---|
| low | US$ 0,006 | US$ 0,025 (4,2×) |
| medium | US$ 0,013 | US$ 0,044 (3,3×) |
| high | US$ 0,053 | US$ 0,053 (igual) |
| xhigh | US$ 0,094 | US$ 0,094 (igual) |
| max | US$ 0,211 | US$ 0,211 (igual) |

## Fontes

Documentação oficial da OpenAI, consultada em 07/11/2026:
[guia de prompts do GPT Image 2.6](https://developers.openai.com/api/docs/guides/image-prompting?model=gpt-image-2.6),
[geração de imagem](https://developers.openai.com/api/docs/guides/image-generation) e
[preços](https://developers.openai.com/api/docs/pricing).
As imagens de exemplo do guia são da documentação da OpenAI.

---

Feito pelo [INEMA.CLUB](https://inema.club).
