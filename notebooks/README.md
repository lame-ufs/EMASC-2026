# Notebooks do minicurso

- [Notebook de exemplos](exemplos.ipynb): materiais de Motivação, Python e Estatística, na ordem da apresentação.
- [Notebook de Estatística](exemplos_estatistica.ipynb): versão revisada de Gabriel C. Souza, integrada também em `exemplos.ipynb`.
- [Notebook de exercícios](exercicios.ipynb): atividades práticas em níveis de dificuldade, com os dados necessários incluídos no próprio notebook.
- [Base de dados de Estatística](../data/estatistica/alunos_redes_ia.csv): arquivo CSV utilizado nos dois notebooks.

## Google Colab

Abra [os exemplos do minicurso](https://colab.research.google.com/github/lame-ufs/EMASC-2026/blob/main/notebooks/exemplos.ipynb), [os exemplos de Estatística](https://colab.research.google.com/github/lame-ufs/EMASC-2026/blob/main/notebooks/exemplos_estatistica.ipynb) ou [os exercícios](https://colab.research.google.com/github/lame-ufs/EMASC-2026/blob/main/notebooks/exercicios.ipynb) pelo Colab. Execute as células em ordem, preenchendo as lacunas propostas nos exercícios. Nos exemplos de Estatística, a base é carregada diretamente do GitHub. Se isso falhar, baixe `alunos_redes_ia.csv` e envie ao painel **Arquivos**, mantendo o nome.

## Jupyter local

O ambiente de referência é Python 3.14.7. Com o ambiente virtual ativado, instale as dependências a partir da raiz do repositório:

```text
python -m pip install -r notebooks/requirements.txt
jupyter notebook
```

Os notebooks localizam automaticamente `data/estatistica/alunos_redes_ia.csv` ao serem executados na raiz do projeto ou na pasta `notebooks/`.

As células com `input()` aguardam uma resposta antes de continuar a execução.
