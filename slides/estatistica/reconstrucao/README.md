# Introdução à Estatística — reconstrução editável

Autoria do material: Gabriel C. Souza (LAME/UFS).

Este projeto Beamer foi reconstruído a partir do PDF original, com 50 quadros e 66 páginas incluindo as revelações. O código-fonte original de Gabriel não estava no repositório. A reconstrução recupera os textos e seus posicionamentos nos arquivos LaTeX e conserva as figuras, elementos gráficos e expressões matemáticas complexas em um PDF vetorial.

## Onde editar

- `reconstrucao.tex`: documento principal e comandos de posicionamento.
- `inclusoes.tex`: ordem das partes.
- `secoes/`: conteúdos da abertura, das oito seções e do encerramento.
- `figuras/fundos.pdf`: camada vetorial extraída do PDF original, sem os textos recuperados. O número em `\Fundo{n}` seleciona a página dessa camada.

Os trechos de texto usam o comando:

~~~latex
\Texto{x}{y}{largura}{tamanho}{estilo}{cor}{Texto editável}
~~~

As coordenadas e as dimensões estão em pontos PDF (bp) a partir do canto superior esquerdo. A coordenada y é a linha de base. Os estilos são r (regular), b (negrito), i (itálico), t (monoespaçado) e c (comentário monoespaçado em itálico). A largura mantém a área ocupada no layout original; quando alterar o texto, ajuste a largura ou posição caso necessário. Os comandos `\only<...>{...}` indicam em quais etapas da revelação o texto aparece.

As fórmulas com tipografia matemática mista e os desenhos originais permanecem na camada vetorial. Para alterá-los, substitua a figura correspondente ou reescreva o trecho em LaTeX. Não é possível recuperar as macros originais apenas pelo PDF.

## Compilação

Execute a partir desta pasta, com TeX Live (Beamer, TikZ e Helvetica) e Python. A compactação utiliza a dependência registrada em `requirements.txt`:

~~~powershell
python -m pip install -r requirements.txt
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build reconstrucao.tex
python -m pymupdf clean -garbage 4 -compress -sanitize build/reconstrucao.pdf reconstrucao.pdf
~~~

O PDF compilado aparece em `build/reconstrucao.pdf`. O segundo comando Python gera a prévia local `reconstrucao.pdf` compactada sem perda visual. Ambos os PDFs gerados são ignorados pelo Git.

A reconstrução foi substituída na apresentação integrada pela [fonte revisada de Gabriel](../introducao-estatistica.tex), recebida em 22/11/2026. Esta pasta preserva a versão anterior para consulta histórica; não é necessária para compilar os slides atuais.
