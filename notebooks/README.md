# Notebooks do minicurso

- [Notebook de exemplos](exemplos.ipynb): materiais de Motivação, Python, Estatística e Ciência de Dados, na ordem da apresentação.
- [Notebook de Estatística](exemplos_estatistica.ipynb): versão revisada de Gabriel C. Souza, integrada também em `exemplos.ipynb`.
- [Notebook de Ciência de Dados](exemplos_ciencia_de_dados.ipynb): versão independente, integrada também em `exemplos.ipynb`.
- [Notebook de exercícios](exercicios.ipynb): atividades práticas em níveis de dificuldade, com os dados necessários incluídos no próprio notebook.
- [Base de dados de Estatística](../data/estatistica/alunos_redes_ia.csv): arquivo CSV utilizado nos dois notebooks.
- [Base de dados de Ciência de Dados](../guia-de-apoio/dados/notas.csv): utilizada nos exemplos de Ciência de Dados e no Guia de Apoio.

## Google Colab

Abra [os exemplos do minicurso](https://colab.research.google.com/github/lame-ufs/EMASC-2026/blob/main/notebooks/exemplos.ipynb) ou [os exercícios](https://colab.research.google.com/github/lame-ufs/EMASC-2026/blob/main/notebooks/exercicios.ipynb) pelo Colab. Execute as células em ordem, preenchendo as lacunas propostas nos exercícios. Nos exemplos de Estatística e Ciência de Dados, as bases são carregadas diretamente do GitHub se não estiverem disponíveis localmente. Se isso falhar, baixe `alunos_redes_ia.csv` ou `notas.csv` e envie ao painel **Arquivos**, mantendo os nomes.

## Jupyter local

O ambiente de referência é Python 3.14.7. Com o ambiente virtual ativado, instale as dependências a partir da raiz do repositório:

```text
python -m pip install -r notebooks/requirements.txt
jupyter notebook
```

Os notebooks localizam automaticamente `data/estatistica/alunos_redes_ia.csv` e `guia-de-apoio/dados/notas.csv` ao serem executados na raiz do projeto ou na pasta `notebooks/`.

As células com `input()` aguardam uma resposta antes de continuar a execução.
