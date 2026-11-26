# Notebooks do minicurso

- [Notebook de exemplos](exemplos.ipynb): materiais de Motivação, Python, Estatística e Ciência de Dados, na ordem da apresentação.
- [Notebook de exercícios](exercicios.ipynb): atividades práticas organizadas em níveis de dificuldade.
- [Gabarito dos exercícios](gabarito.ipynb): soluções de referência das atividades práticas ([Abrir no Colab](https://colab.research.google.com/github/lame-ufs/EMASC-2026/blob/main/notebooks/gabarito.ipynb)).
- [Base de dados de Estatística](alunos_redes_ia.csv): arquivo CSV utilizado nos exemplos de Estatística.
- [Base de dados de Ciência de Dados](../guia-de-apoio/dados/notas.csv): utilizada nos exemplos de Ciência de Dados e no Guia de Apoio.
- [Base do Titanic](titanic.csv): utilizada no bloco de Ciência de Dados dos exercícios, obtida do [repositório de datasets do seaborn](https://github.com/mwaskom/seaborn-data/blob/master/titanic.csv).

## Google Colab

Abra [os exemplos do minicurso](https://colab.research.google.com/github/lame-ufs/EMASC-2026/blob/main/notebooks/exemplos.ipynb) ou [os exercícios](https://colab.research.google.com/github/lame-ufs/EMASC-2026/blob/main/notebooks/exercicios.ipynb) pelo Colab. Execute as células em ordem, preenchendo as lacunas propostas nos exercícios. Nos exemplos e exercícios, as bases são carregadas diretamente da internet se não estiverem disponíveis localmente. Se isso falhar, baixe o CSV indicado no notebook e envie ao painel **Arquivos**, mantendo o nome original.

## Jupyter local

O ambiente de referência é Python 3.14.7. Com o ambiente virtual ativado, instale as dependências a partir da raiz do repositório:

```text
python -m pip install -r notebooks/requirements.txt
jupyter notebook
```

Os notebooks localizam automaticamente `notebooks/alunos_redes_ia.csv` e `guia-de-apoio/dados/notas.csv` ao serem executados na raiz do projeto ou na pasta `notebooks/`.

Nos exercícios de Ciência de Dados, a base `notebooks/titanic.csv` é localizada automaticamente a partir da raiz do projeto ou da pasta `notebooks/`. No Colab, se a leitura automática pelo GitHub não funcionar, envie o arquivo `titanic.csv` pelo painel Arquivos.

As células com `input()` aguardam uma resposta antes de continuar a execução.

## Origem da base de Estatística

O arquivo `alunos_redes_ia.csv` foi fornecido por Gabriel C. Souza (16.000 registros e 10 colunas) e obtido da [fonte indicada no notebook original](https://drive.google.com/uc?export=download&id=10fEsPETcG27eItdHwG5D-mmovfG64S5c), sem alteração.
