# Guia de Apoio · LAME / EMASC 2026

O [guia em PDF](guia_lame.pdf) reúne explicações e exemplos comentados sobre preparação do ambiente, Python, Estatística, NumPy, pandas e Matplotlib.

## Dados dos exemplos

A [base simulada de notas](dados/notas.csv) contém 18 participantes fictícios. Em um notebook local, trabalhe a partir desta pasta. No [Google Colab](https://colab.research.google.com/), envie o CSV pelo painel **Arquivos**. O exemplo de leitura aceita o arquivo em `dados/notas.csv` ou em `notas.csv`.

## Ambiente local

O ambiente de referência usa Python 3.14.7. A instalação das bibliotecas nas versões registradas é feita com `python -m pip install -r requirements.txt`.

## Edição e compilação

- `guia_lame.tex` é o arquivo principal.
- `secoes/` contém os capítulos e os exemplos.
- `referencias.bib` reúne as fontes bibliográficas.
- `figuras/` contém a logo e os gráficos dos exemplos.

Compile a partir desta pasta com `latexmk`, `pdflatex` e `biber`. O `latexmk` resolve as referências automaticamente.

~~~powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build guia_lame.tex
Copy-Item build/guia_lame.pdf guia_lame.pdf
~~~

Para atualizar um gráfico, execute seu exemplo no capítulo de Matplotlib ou no de exemplos de análise de dados e chame `.savefig()` no objeto da figura antes de `plt.show()`, usando o arquivo indicado no comando `includegraphics` da mesma seção.
