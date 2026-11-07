#!/usr/bin/env python3
"""Baixa a foto e o círculo de exemplo da documentação da OpenAI para testar a edição com markup.
Uso (na raiz do repo): python3 exemplos/baixar.py   → exemplos/cozinha.webp e exemplos/circulo.png"""
import urllib.request
from pathlib import Path

B = "https://developers.openai.com/images/platform/guides/image-prompting/"
ARQ = {"cozinha.webp": "kitchen.webp", "circulo.png": "markup-vase-overlay-gpt-image-2-6.png"}
pasta = Path(__file__).resolve().parent
for local, remoto in ARQ.items():
    req = urllib.request.Request(B + remoto, headers={"User-Agent": "gpt-image-26-exemplos"})
    dados = urllib.request.urlopen(req, timeout=60).read()
    (pasta / local).write_bytes(dados)
    print(f"salvo: exemplos/{local} ({len(dados) // 1024} KB)")
