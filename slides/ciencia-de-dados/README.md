# Introdução à Ciência de Dados

Versão independente do bloco incorporado à apresentação completa.

## Materiais

- `introducao-ciencia-de-dados.pdf`: versão para apresentação.
- `introducao-ciencia-de-dados.tex` e `secoes/`: fontes Beamer, organizadas por assunto e vinculadas ao tema compartilhado da LAME.
- `figuras/`: gráficos gerados com os próprios códigos da apresentação.
- [Notebook de exemplos](../../notebooks/exemplos_ciencia_de_dados.ipynb): exemplos na mesma ordem dos slides.
- [Base de notas](../../guia-de-apoio/dados/notas.csv): base fictícia compartilhada com o Guia de Apoio.

O arquivo `conteudo.tex` fornece a capa utilizada na apresentação principal.

## Roteiro sugerido (45 minutos)

| Etapa | Tempo |
| --- | ---: |
| Problema e etapas da análise | 3 min |
| Bibliotecas e NumPy | 7 min |
| pandas: leitura, seleção e filtros | 8 min |
| Preparação dos dados | 8 min |
| Análise descritiva e gráficos | 14 min |
| Interpretação, proposta de ação e exportação | 5 min |

A abordagem segue os conteúdos introdutórios de Kaue Santos, com uma única base de dados para ilustrar a análise. Como o CSV utilizado no notebook recebido não foi disponibilizado, foi adotada a base de notas do Guia. A parte de predição foi substituída por uma análise descritiva e uma proposta de ação.

O frame de criação de arrays serve como consulta complementar; a junção e a exportação podem ser demonstradas rapidamente ou consultadas depois. Na apresentação, priorize a comparação entre listas e arrays, a leitura e preparação da base, os agrupamentos e a construção e interpretação dos gráficos. Os exemplos têm as saídas já registradas no notebook, mas podem ser executados novamente.

## Atualização dos materiais

Na raiz do repositório, execute:

```bash
python slides/ciencia-de-dados/gerar_exemplos.py --integrar
cd slides/ciencia-de-dados
latexmk -pdf introducao-ciencia-de-dados.tex
cd ../..
python slides/montar_apresentacao.py
```

O gerador extrai os blocos de código dos arquivos LaTeX, executa os exemplos em sequência, recria os gráficos e atualiza o notebook independente. Com `--integrar`, atualiza também somente o bloco de Ciência de Dados de `notebooks/exemplos.ipynb`. Ao acrescentar um novo frame com código, inclua sua explicação em `TEXTOS` no gerador. Os notebooks utilizam o CSV local ou o endereço público do repositório quando disponível.
