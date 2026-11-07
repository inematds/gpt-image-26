# Prompts prontos — GPT Image 2.6

Copie, troque o que está entre `< >` e cole no ChatGPT (ou passe para o `gerar.py`).
Funcionam em português ou em inglês; o que importa é a estrutura.

## 1. Estrutura que funciona para qualquer imagem

```
Crie <tipo de peça: foto de produto, anúncio, cartaz, infográfico> para <uso>.

Cena: <onde, luz, clima>
Sujeito: <quem/o quê, enquadramento, pose, olhar>
Detalhes: <materiais, cores, textura, estilo>
Restrições:
- <o que NÃO pode ter: texto extra, logo, marca d'água>
Texto (exatamente, entre aspas): "<texto>"
```

Por que funciona: a OpenAI recomenda separar cena, sujeito, detalhes e restrições em seções com rótulo,
pôr o texto exato entre aspas e dizer o que não quer.

## 2. Teste de complexidade (layout e várias pessoas)

```
Um grupo de quatro dançarinos na chuva, à noite, num terraço da cidade.
Cada dançarino forma uma letra com o corpo e juntos eles escrevem a palavra "LIKE".
Corpo inteiro visível, pés incluídos, anatomia correta, mãos com cinco dedos.
```

Rode em `low`, `medium` e `high` de complexidade **com a mesma qualidade**. Compare se a palavra
aparece certa e se os corpos fazem sentido. Depois, com a complexidade escolhida, compare qualidades.

## 3. Instruções em sequência (o 2.6 vai bem)

```
Foto de estúdio, fundo branco. Um homem de camiseta preta atrás de uma mesa de madeira.
Na mesa, da esquerda para a direita:
1. uma caneca vermelha com a alça virada para a esquerda;
2. uma maçã verde;
3. três livros empilhados com a lombada virada para a câmera;
4. um copo de água pela metade;
5. um par de óculos dobrado.
Ele segura outra maçã verde na mão direita, na altura do ombro.
```

Atenção: conta exata ("exatamente sete pincéis") ainda falha. Se o número importa, confira e peça de novo.

## 4. Texto miúdo e cartaz

```
Cartaz de festival de música, formato retrato.
Título no topo, em letras grandes: "FESTIVAL DO MAR 2027"
Abaixo, três colunas com os dias e as bandas:
SEXTA: "Maré Alta", "Sal Grosso"
SÁBADO: "Farol Norte", "Vento Sul"
DOMINGO: "Ilha Azul", "Concha"
Rodapé: "Ingressos a partir de R$ 89 · festivaldomar.com.br"
Mesma família de fonte no cartaz inteiro. Sem nenhum outro texto.
```

Letra pequena ilegível com o layout certo → suba a **qualidade** (não a complexidade).

## 5. Personagem consistente

```
Folha de personagem: o mesmo homem de 40 anos, barba curta grisalha, cicatriz pequena na sobrancelha
esquerda, em 9 quadros (grade 3x3): no escritório, correndo na chuva, cozinhando, de terno num palco,
de pijama, na praia, de capacete de obra, lendo na biblioteca, rindo num bar.
Mesmo rosto, mesmas proporções e mesma cicatriz em todos os quadros.
```

Para continuar a história, mande a imagem dele de volta e repita os traços que não podem mudar
("mesma cicatriz, mesma barba, não redesenhe o personagem").

## 6. Referência salva no ChatGPT

1. Envie a foto e escreva: `Salve esta imagem como referência com o nome "<nome>".`
2. Numa conversa nova: `Use a referência "<nome>" e crie uma capa de vídeo com o texto "<texto>".`

## 7. GIF a partir de um sprite sheet (ChatGPT)

```
Faça um sprite sheet 3x3 desta pessoa piscando e sorrindo, em loop.
O último quadro volta para a pose do primeiro. Câmera parada. Depois monte o GIF.
```

Quer mais suave? Peça "4x4" (mais quadros). Pela API, use `--formato gif --quadros 9 --ms 200`
(2 a 16 quadros, 20 a 2000 ms cada; 9 × 200 ms = loop de 1,8 s).

## 8. Logo em SVG (vetor)

```
Logo original para <nome>, <ramo>. Formas simples, silhueta forte, poucas cores, sem degradê,
legível pequeno e grande. Fundo totalmente transparente. Entregue em SVG.
```

Pela API: `python3 gerar.py "<prompt>" --formato svg --fundo transparente`. Abra o `.svg` num editor
vetorial (Inkscape, Figma) para mover e recolorir as formas.

## 9. Edição com markup (circula e pede)

No ChatGPT, use a ferramenta de marcar na imagem, circule a área e escreva:

```
Dentro do círculo vermelho, <mudança>. Não mude mais nada na imagem. Remova o círculo do resultado.
```

Pela API: `python3 gerar.py "<prompt>" --editar foto.jpg --markup circulo.png --complexity low`
(o `circulo.png` é um PNG transparente do MESMO tamanho da foto, só com o traço; para testar, `python3 exemplos/baixar.py`
baixa a foto e o círculo de exemplo da OpenAI).

## 10. Edição comum: uma mudança por vez

```
Troque a cor da lata de azul para verde-escuro. Mantenha o texto, a tampa, a xícara, os grãos,
a luz e o enquadramento exatamente iguais.
```

Depois, com a imagem nova: fundo → luz → ângulo, um pedido por vez, sempre repetindo o que deve ficar igual.
