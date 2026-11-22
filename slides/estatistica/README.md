# Introdução à Estatística

Material revisado de Gabriel C. Souza, recebido em 22/11/2026.

- [Fonte original Beamer](introducao-estatistica.tex): apresentação revisada.
- [Figuras](figuras/): imagens, logos e script de geração fornecidos pelo autor. Os nomes foram mantidos para preservar as referências do LaTeX.
- [Exemplos de Estatística](../../notebooks/exemplos_estatistica.ipynb): notebook que acompanha a apresentação.
- [Reconstrução anterior](reconstrucao/README.md): versão histórica, não utilizada na montagem atual.

## Compilar a nova apresentação

A partir da pasta `slides/estatistica/`, com TeX Live instalado:

```text
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build introducao-estatistica.tex
```

O PDF independente será gerado em `build/introducao-estatistica.pdf`. A pasta `build/` é ignorada pelo Git. O material utiliza a base [`alunos_redes_ia.csv`](../../data/estatistica/alunos_redes_ia.csv), também utilizada nos notebooks.
