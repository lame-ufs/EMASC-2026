# Notebooks do minicurso

- [Notebook de exemplos](exemplos.ipynb): exemplos de Python e Estatística, na ordem da apresentação.
- [Notebook de Estatística](exemplos_estatistica.ipynb): material preparado por Gabriel C. Souza.
- [Base de dados de Estatística](../data/estatistica/AI_SocialMedia_Student_Dataset.csv): arquivo CSV usado nos dois notebooks.

## Google Colab

Abra [os exemplos do minicurso](https://colab.research.google.com/github/lame-ufs/EMASC-2026/blob/main/notebooks/exemplos.ipynb) ou [os exemplos de Estatística](https://colab.research.google.com/github/lame-ufs/EMASC-2026/blob/main/notebooks/exemplos_estatistica.ipynb) pelo Colab e envie o CSV pelo painel **Arquivos**, mantendo o nome original. Execute as células em ordem. Se iniciar uma nova sessão, envie o CSV novamente.

## Jupyter local

O ambiente de referência é Python 3.14.7. Com o ambiente virtual ativado, instale as dependências a partir da raiz do repositório:

```text
python -m pip install -r notebooks/requirements.txt
jupyter notebook
```

Para os exemplos de Estatística, copie `data/estatistica/AI_SocialMedia_Student_Dataset.csv` para a pasta `notebooks/` e abra o notebook. Essa cópia de trabalho é ignorada pelo Git. O arquivo original permanece em `data/estatistica/`.

As células com `input()` aguardam uma resposta antes de continuar a execução.
