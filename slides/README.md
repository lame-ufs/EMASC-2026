# Apresentação do minicurso · LAME / EMASC 2026

- [Apresentação integrada](minicurso-emasc-2026.pdf) · Introdução, Motivação, Python e Estatística.
- [Fonte Beamer de Python](python/introducao-python.tex) e [PDF de Python](python/introducao-python.pdf).
- [Notebook da apresentação](../notebooks/exemplos.ipynb) e [CSV de Estatística](../data/estatistica/alunos_redes_ia.csv).

O notebook integrado e o notebook de Estatística trazem as logos da LAME e da EMASC incorporadas no cabeçalho.

## Onde editar

Cada parte tem sua própria pasta. Edite apenas os arquivos da etapa sob sua responsabilidade.

| Parte | Fonte editável |
|---|---|
| Abertura e sumário | [`abertura/conteudo.tex`](abertura/conteudo.tex) |
| Introdução | [`introducao/conteudo.tex`](introducao/conteudo.tex) |
| Motivação | [`motivacao/conteudo.tex`](motivacao/conteudo.tex) |
| Python | [`python/secoes/`](python/secoes/) |
| Estatística | [`estatistica/introducao-estatistica.tex`](estatistica/introducao-estatistica.tex) (fonte de Gabriel) e [`estatistica/capa.tex`](estatistica/capa.tex) |
| Ciência de Dados | [`ciencia-de-dados/conteudo.tex`](ciencia-de-dados/conteudo.tex) |
| Exercícios | [`exercicios/conteudo.tex`](exercicios/conteudo.tex) |
| Processo Seletivo LAME 2027 | [`processo-seletivo/conteudo.tex`](processo-seletivo/conteudo.tex) |

As seis partes do bloco de Python ficam em `python/secoes/`, numeradas conforme o roteiro. A apresentação integrada utiliza a versão revisada de Estatística de Gabriel C. Souza em [`estatistica/`](estatistica/README.md). O [QR Code](motivacao/figuras/qr-code-dashboard-ufs-tre.png) do [dashboard UFS/TRE](https://dashboard-ufs-tre.streamlit.app/) recebido para Motivação está em `motivacao/figuras/`.

Para acrescentar um slide, adicione um ambiente `frame` ao arquivo de conteúdo correspondente. As capas já estão no início de cada bloco. Exemplo:

```latex
\begin{frame}[t]{Título do slide}
  Conteúdo do slide.
\end{frame}
```

Para slides com código, use `[fragile,t]` e o ambiente `lstlisting`. Para revelações progressivas, use os recursos de overlay do Beamer.

## Modelo dos slides

O [tema Beamer do EMASC 2026](modelo/beamerthemeEMASC.sty) concentra a tipografia, a paleta, a capa, as divisórias e o estilo dos blocos de código. A apresentação de Python carrega o tema a partir de `modelo/` e a marca a partir de `assets/`.

As aberturas usam o mesmo tema. O arquivo [aberturas.tex](modelo/aberturas.tex) reúne as partes editáveis por meio de `\input` e identifica cada bloco com `\section`. O arquivo `python/introducao-python.tex` reúne as subseções de Python da mesma forma. Esses dois arquivos contêm a configuração e a ordem de inclusão. O conteúdo fica nas pastas de cada parte.

O script de integração usa os marcadores das seções no PDF para localizar os blocos, atualizar os links do sumário e calcular a numeração. É possível acrescentar slides às partes sem alterar os índices manualmente. Preserve os identificadores das seções no arquivo de montagem e o rótulo `referencias-python` no primeiro slide de referências.

A paleta segue a referência visual da LAME, e as aberturas usam o motivo de grafos dos posts da EMASC, disponível em `assets/grafos-emasc.png`. O e-mail exibido na capa é `lame.ufs.mat@gmail.com`.

Durante a apresentação, avance uma página por vez para revelar exemplos e comentários. A numeração dos slides é contínua em todo o minicurso. As etapas de revelação (overlays do Beamer) de um mesmo slide compartilham o número, inclusive no rótulo de página do PDF.

## Gerar o PDF integrado

Com TeX Live (Beamer, pacote `qrcode` e `latexmk`) e Python instalados, execute a partir da raiz do repositório. As dependências de montagem estão em [`requirements.txt`](requirements.txt).

```text
python -m pip install -r slides/requirements.txt
cd slides/python
latexmk -pdf introducao-python.tex
cd ../modelo
latexmk -pdf aberturas.tex
cd ../estatistica
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build introducao-estatistica.tex
cd ../..
python slides/montar_apresentacao.py
```

Os arquivos auxiliares do LaTeX e os PDFs intermediários `modelo/aberturas.pdf` e `estatistica/build/introducao-estatistica.pdf` são gerados localmente e ignorados pelo Git. O PDF integrado e as fontes necessárias para reconstruí-lo permanecem no projeto.

O script aplica a capa padronizada de Estatística ao PDF integrado e incorpora os slides da fonte revisada com a navegação interna. As referências de Python ficam imediatamente antes do slide de agradecimento. O bloco de Ciência de Dados aguarda o material da equipe.
