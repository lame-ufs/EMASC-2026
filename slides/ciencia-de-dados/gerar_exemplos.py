"""Gera o notebook e os gráficos a partir dos exemplos dos slides.

Execução: python slides/ciencia-de-dados/gerar_exemplos.py
Requer NumPy, pandas e Matplotlib. Os exemplos são testados em um diretório
temporário; a exportação de CSV da aula não cria resíduos no repositório.
"""

import hashlib
import json
import re
import shutil
import tempfile
from copy import deepcopy
from pathlib import Path

PASTA = Path(__file__).resolve().parent
REPO = PASTA.parents[1]
NOTEBOOK = REPO / "notebooks" / "exemplos_ciencia_de_dados.ipynb"
NOTEBOOK_INTEGRADO = REPO / "notebooks" / "exemplos.ipynb"

# A célula de inicialização localiza a base tanto no VS Code quanto no Colab.
CONFIGURACAO = '''from pathlib import Path

# Restaura o estilo dos gráficos para este bloco de exemplos.
plt.rcdefaults()

candidatos = [
    Path("notas.csv"),
    Path("guia-de-apoio/dados/notas.csv"),
    Path("../guia-de-apoio/dados/notas.csv"),
]
fonte = next((c for c in candidatos if c.is_file()), None)
if fonte is None:
    fonte = (
        "https://raw.githubusercontent.com/lame-ufs/EMASC-2026/"
        "main/guia-de-apoio/dados/notas.csv"
    )
print("Fonte selecionada:", fonte)
'''

TEXTOS = {
    "Bibliotecas de Python": "NumPy realiza cálculos numéricos, pandas trabalha com tabelas e Matplotlib permite construir gráficos. As abreviações são usadas nos exemplos seguintes.",
    "1. Arrays": "Um array armazena valores do mesmo tipo e permite cálculos diretamente com seus elementos. O índice começa em zero. O recorte `notas[1:4]` retorna 6,7, 7,5 e 8,2, excluindo o índice 4.",
    "1.1. Matrizes": "Cada linha representa um estudante; as colunas contêm horas de estudo e nota. Em `matriz[i, j]`, o primeiro índice é a linha e o segundo, a coluna.",
    "1.2. Criação de arrays": "**Consulta complementar.** As funções `zeros` e `ones` inicializam arrays. `arange` utiliza um passo fixo e exclui o limite final; `linspace` gera a quantidade indicada de valores igualmente espaçados, incluindo os extremos.",
    "1.3. Operações vetorizadas": "As listas fictícias representam horas de estudo de três estudantes em duas semanas. Em listas, `+` concatena os elementos; em arrays, soma elemento a elemento. A comparação de notas com 7 retorna um array de valores booleanos.",
    "1.4. Medidas estatísticas com NumPy": "O parâmetro `ddof=0` utiliza o divisor n na variância para descrever a população completa. `ddof=1` utiliza n−1 quando a amostra é usada para estimar a variância populacional. O desvio padrão é a raiz quadrada da variância.",
    "2. Series e DataFrame": "Uma Series é uma sequência de valores, cada um com seu índice. Um DataFrame é uma tabela que pode reunir colunas de tipos distintos. A coluna `nota` do DataFrame é uma Series; o índice padrão começa em zero e não é a coluna `id`.",
    "2.1. Leitura de uma base de dados": "A sintaxe para ler um CSV local é `pd.read_csv('notas.csv')`. Quando o delimitador for ponto e vírgula, utiliza-se `sep=';'`. No exemplo, `fonte` contém o caminho ou endereço da base de notas.",
    "2.2. Inspeção dos dados": "Os comandos permitem reconhecer o formato (18 linhas e 5 colunas), os nomes, tipos e quantidade de valores presentes. `describe()` calcula medidas descritivas; o ID não entra nesse resumo porque é apenas um identificador.",
    "2.3. Seleção de linhas e colunas": "Uma coluna entre colchetes simples retorna uma Series; uma lista de colunas retorna um DataFrame. `loc` seleciona por rótulos e inclui o último rótulo de uma fatia. `iloc` seleciona por posições, excluindo a posição final. Os dois últimos comandos retornam as mesmas linhas e colunas.",
    "2.4. Filtros e ordenação": "O filtro `alto` seleciona notas de pelo menos 7 e frequência de pelo menos 80%. `atencao` seleciona notas abaixo de 7 ou ausentes, identificadas por `isna()`. Usa-se `&`, `|` e `~` no lugar de `and`, `or` e `not` para combinar condições linha a linha. `ascending=False` ordena da maior para a menor nota.",
    "3. Qualidade dos dados": "O pandas representa uma nota numérica ausente por `NaN`. `duplicated()` e `isna()` geram valores booleanos; `sum()` conta os verdadeiros como 1. O filtro `fora` procura notas registradas fora de 0 a 10. Uma tabela vazia indica que nenhuma nota atende ao filtro. Nesta base, as contagens de duplicatas e IDs repetidos são zero, e há duas notas ausentes.",
    "3.1. Tratamento de valores ausentes": "Uma nota ausente não é uma nota zero. `df` mantém os 18 registros; `df_com_notas` é uma cópia com as 16 notas disponíveis. O argumento `subset=['nota']` limita a exclusão às notas ausentes. `fillna()` permite substituir ausências quando existe uma justificativa; neste problema, não substituímos as notas.",
    "3.2. Criação de colunas": "A frequência original está entre 0 e 1; a multiplicação por 100 a expressa em percentual. `apply()` aplica a função a cada nota e classifica os valores com o limite didático de 7, sem representar uma regra oficial de aprovação. As novas colunas serão usadas no agrupamento e no gráfico de dispersão.",
    "4. Agrupamento dos dados": "`groupby('curso')` separa os registros por curso. Primeiro calculamos uma mediana para cada grupo. Com `agg()`, calculamos várias medidas de uma vez; `std` usa n−1 na variância por padrão. `value_counts()` conta as notas de cada categoria criada anteriormente. `round(2)` arredonda os valores exibidos.",
    "4.1. Frequência relativa de notas ausentes": "Ao sortear um registro de um curso nesta base, a probabilidade de a nota estar ausente é dada pela razão entre as notas ausentes e os registros desse curso. Em Matemática, 1/6 ≈ 16,67%. `size` conta todas as linhas; `count` conta apenas valores disponíveis. Multiplica-se a razão por 100 para expressá-la em percentual.",
    "5. Matplotlib / Gráfico de barras": "O eixo x contém os cursos (índice de `cobertura`), e o eixo y contém os percentuais de notas ausentes. `figsize` define largura e altura em polegadas, `color` define a cor e `bar_label` mostra os valores nas barras. `title`, `xlabel` e `ylabel` rotulam o gráfico, `ylim` limita o eixo y, `tight_layout()` ajusta o espaço e `show()` exibe a figura.",
    "5.2. Histograma": "O histograma resume a distribuição das notas em intervalos. O parâmetro `bins=5` divide o intervalo entre a menor e a maior nota em cinco classes de mesma largura.",
    "5.4. Gráfico de dispersão": "Cada ponto representa um estudante, com frequência em percentual no eixo x e nota no eixo y. O laço percorre os cursos; `label` define o nome de cada grupo e `legend()` exibe a legenda.",
    "6.1. Junção de tabelas": "O resultado final combina as medidas das notas com o percentual de notas ausentes. `reset_index()` transforma o índice de cursos em uma coluna. `merge()` junta as tabelas pela coluna indicada em `on='curso'`, mantendo as chaves presentes em ambas por padrão.",
    "6.2. Exportação dos resultados": "O arquivo `resumo_por_curso.csv` reúne as medidas de posição e dispersão e a proporção de notas ausentes. `to_csv()` exporta a tabela e `index=False` evita gravar o índice numérico como coluna extra.",
}

INTERPRETACOES = {
    "5.1. Comparação dos cursos": "Matemática e Estatística possuem uma nota ausente em seis registros (16,7%). Computação tem todas as notas disponíveis.",
    "5.3. Distribuição das notas": "As notas disponíveis variam de 5,5 a 9,6. Os quatro primeiros intervalos contêm três notas cada, e o último contém quatro.",
    "5.5. Relação entre frequência e nota": "Nesta base fictícia, as notas maiores tendem a acompanhar frequências mais altas. Essa associação, por si só, não demonstra uma relação de causa e efeito.",
    "6. Interpretação e proposta de ação": """| Curso | Notas disponíveis | Mediana | Desvio padrão | Ausentes |
|---|---:|---:|---:|---:|
| Computação | 6 | 7,85 | 1,29 | 0,0% |
| Estatística | 5 | 7,80 | 1,38 | 16,7% |
| Matemática | 5 | 7,50 | 1,25 | 16,7% |

As medianas e os desvios padrão das notas disponíveis são próximos entre os cursos.

**Ação proposta:** conferir os dois registros pendentes com os responsáveis e completar a base quando as notas reais estiverem disponíveis.

**Avaliação:** acompanhar o percentual de notas ausentes por curso, com meta de 0%, e repetir a análise após o registro.

As diferenças entre as medianas descrevem somente os registros disponíveis nesta base pequena e fictícia; não medem a qualidade dos cursos.""",
}

FRAME = re.compile(
    r"\\begin\{frame\}(?:\[[^\]]*\])?\{([^{}]+)\}(.*?)\\end\{frame\}",
    re.S,
)
LISTING = re.compile(r"\\begin\{lstlisting\}\s*\n(.*?)\\end\{lstlisting\}", re.S)


def celula(tipo, fonte, chave, **extras):
    resultado = {
        "cell_type": tipo,
        "id": hashlib.sha256(chave.encode()).hexdigest()[:12],
        "metadata": {},
        "source": fonte.strip().splitlines(keepends=True),
    }
    if tipo == "code":
        resultado.update(execution_count=None, outputs=[])
    resultado.update(extras)
    return resultado


def criar_notebook():
    base = json.loads(NOTEBOOK_INTEGRADO.read_text(encoding="utf-8"))
    logos = base["cells"][0]["attachments"]
    cabecalho = """![Logos da Liga Acadêmica Matemática e Empresa e da EMASC](attachment:logos-lame-emasc.png)

# Introdução à Ciência de Dados
**LAME · EMASC 2026**

Exemplos utilizados na apresentação de Ciência de Dados. As células de código devem ser executadas em ordem.

## Problema de estudo

Uma equipe acadêmica precisa acompanhar os registros de notas de três cursos. Em quais cursos existem notas pendentes e como se distribuem as notas já registradas?

A base fictícia `notas.csv`, disponível no Guia de Apoio, contém 18 registros de estudantes. Alguns exemplos:

| id | curso | horas_estudo | frequencia | nota |
|---:|---|---:|---:|---:|
| 1 | Matematica | 2,0 | 0,70 | 5,9 |
| 6 | Matematica | 3,5 | 0,80 | |

O ID identifica o estudante e não é uma medida de desempenho. A frequência é uma proporção de aulas frequentadas (0,70 = 70%). Neste estudo, supomos que uma nota em branco ainda não foi registrada.

As etapas são: entender o problema, obter os dados, prepará-los, explorá-los, interpretar os resultados e propor uma ação.
"""
    celulas = [celula("markdown", cabecalho, "cabecalho", attachments=logos)]
    codigos = []
    for arquivo in sorted((PASTA / "secoes").glob("*.tex")):
        for titulo, corpo in FRAME.findall(arquivo.read_text(encoding="utf-8")):
            if titulo in INTERPRETACOES:
                celulas.append(celula("markdown", f"### {titulo}\n\n{INTERPRETACOES[titulo]}", titulo))
            exemplos = LISTING.findall(corpo)
            if not exemplos:
                continue
            celulas.append(celula("markdown", f"## {titulo}\n\n{TEXTOS[titulo]}", titulo))
            if titulo == "2.1. Leitura de uma base de dados":
                celulas.append(celula("markdown", """**Configuração do ambiente (não é conteúdo da aula).** Execute a célula a seguir para localizar o CSV. No VS Code, ela procura o arquivo no repositório. No Colab, utiliza `notas.csv` se estiver disponível na sessão ou o endereço público do GitHub. Caso o repositório ainda esteja privado, carregue o CSV na aba Arquivos do Colab antes de executar.""", "fonte-explicacao"))
                celulas.append(celula("code", CONFIGURACAO, "configuracao"))
                codigos.append(("configuracao", CONFIGURACAO))
            for i, texto in enumerate(exemplos):
                codigo = texto.strip()
                celulas.append(celula("code", codigo, f"{titulo}-codigo-{i}"))
                codigos.append((titulo, codigo))
    celulas.append(celula("markdown", """## Referências

- [Documentação do NumPy](https://numpy.org/doc/)
- [Documentação do pandas](https://pandas.pydata.org/docs/)
- [Documentação do Matplotlib](https://matplotlib.org/stable/)
- Guia de Apoio da LAME (EMASC 2026).
""", "referencias"))
    notebook = {
        "cells": celulas,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "file_extension": ".py", "mimetype": "text/x-python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    return notebook, codigos


def integrar_notebook(notebook):
    """Substitui somente a seção de Ciência de Dados no notebook do minicurso."""
    integrado = json.loads(NOTEBOOK_INTEGRADO.read_text(encoding="utf-8"))
    celulas = integrado["cells"]
    ancora = '<a id="ciencia-de-dados"></a>'
    encontrados = [
        i for i, c in enumerate(celulas)
        if c["cell_type"] == "markdown" and ancora in "".join(c["source"])
    ]
    if len(encontrados) != 1:
        raise ValueError("O notebook integrado deve conter uma única seção de Ciência de Dados.")
    inicio = encontrados[0]
    fim = next(
        (i for i, c in enumerate(celulas[inicio + 1:], inicio + 1)
         if c["cell_type"] == "markdown" and "".join(c["source"]).startswith('<a id="')),
        len(celulas),
    )
    cabecalho = "".join(celulas[0]["source"]).replace(
        "[Introdução à Ciência de Dados](#ciencia-de-dados) · aguardando o material",
        "[Introdução à Ciência de Dados](#ciencia-de-dados)",
    )
    celulas[0]["source"] = cabecalho.splitlines(keepends=True)
    bloco = deepcopy(notebook["cells"])
    abertura = "".join(bloco[0]["source"])
    abertura = abertura[abertura.index("# Introdução à Ciência de Dados"):]
    abertura = ancora + "\n" + abertura.replace(
        "**LAME · EMASC 2026**\n\n",
        "",
        1,
    )
    abertura = abertura.replace(
        "As células de código devem ser executadas em ordem.",
        "As células de código devem ser executadas em ordem. Este bloco utiliza uma nova base em `df`. "
        "Ao retornar à Estatística, execute novamente a célula de carregamento daquela base.",
        1,
    )
    bloco[0]["source"] = abertura.splitlines(keepends=True)
    bloco[0].pop("attachments", None)  # As logos já aparecem na capa geral.
    for c in bloco:
        c["id"] = "cd-" + c["id"]
    integrado["cells"] = celulas[:inicio] + bloco + celulas[fim:]
    NOTEBOOK_INTEGRADO.write_text(
        json.dumps(integrado, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    print(f"Notebook integrado atualizado: {NOTEBOOK_INTEGRADO}")


def testar_e_gerar_figuras(notebook, codigos):
    import base64
    import contextlib
    import io
    import os

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    graficos = iter(["barras.pdf", "histograma.pdf", "dispersao.pdf"])
    pasta_figuras = PASTA / "figuras"
    pasta_figuras.mkdir(exist_ok=True)
    exibicoes = []

    def mostrar():
        destino = pasta_figuras / next(graficos)
        plt.gcf().savefig(destino, bbox_inches="tight", metadata={"CreationDate": None})
        imagem = io.BytesIO()
        plt.gcf().savefig(imagem, format="png", dpi=120, bbox_inches="tight")
        exibicoes.append({
            "output_type": "display_data",
            "data": {
                "image/png": base64.b64encode(imagem.getvalue()).decode("ascii"),
                "text/plain": ["Gráfico de Matplotlib"],
            },
            "metadata": {},
        })
        plt.close("all")

    plt.show = mostrar
    ambiente = {}
    atual = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="lame-ciencia-dados-") as pasta:
        shutil.copy2(REPO / "guia-de-apoio" / "dados" / "notas.csv", Path(pasta) / "notas.csv")
        os.chdir(pasta)
        try:
            celulas_codigo = [c for c in notebook["cells"] if c["cell_type"] == "code"]
            for numero, (cel, (titulo, codigo)) in enumerate(zip(celulas_codigo, codigos, strict=True), 1):
                exibicoes.clear()
                with contextlib.redirect_stdout(io.StringIO()) as saida:
                    exec(compile(codigo, titulo, "exec"), ambiente)
                cel["execution_count"] = numero
                if saida.getvalue():
                    cel["outputs"].append({
                        "output_type": "stream",
                        "name": "stdout",
                        "text": saida.getvalue().splitlines(keepends=True),
                    })
                cel["outputs"].extend(exibicoes)
                print(f"OK: {titulo}")
            assert ambiente["df"].shape == (18, 5)
            assert ambiente["df_com_notas"].shape[0] == 16
            assert ambiente["cobertura"]["sem_nota"].to_dict() == {
                "Computacao": 0, "Estatistica": 1, "Matematica": 1
            }
            assert ambiente["resumo"]["median"].round(2).to_dict() == {
                "Computacao": 7.85, "Estatistica": 7.8, "Matematica": 7.5
            }
            assert Path("resumo_por_curso.csv").is_file()
            assert len(ambiente["resultado"]) == 3
        finally:
            os.chdir(atual)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--integrar", action="store_true",
                        help="Atualiza também a seção de Ciência de Dados no notebook do minicurso.")
    args = parser.parse_args()
    notebook, codigos = criar_notebook()
    testar_e_gerar_figuras(notebook, codigos)
    NOTEBOOK.write_text(
        json.dumps(notebook, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Notebook gerado: {NOTEBOOK}")
    if args.integrar:
        integrar_notebook(notebook)
