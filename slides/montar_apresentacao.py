from io import BytesIO
from pathlib import Path
import re

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, ByteStringObject, NameObject, TextStringObject
from reportlab.pdfgen.canvas import Canvas


def email_da_capa(capa):
    for anotacao in capa.get("/Annots", []):
        acao = anotacao.get_object().get("/A", {})
        uri = acao.get("/URI", "")
        if uri.startswith("mailto:"):
            return uri.removeprefix("mailto:")
    raise ValueError("Inclua um link de e-mail na capa geral antes de gerar o PDF integrado.")


def corrigir_email_no_encerramento(pagina, email):
    endereco_provisorio = "email-da-liga@dominio.br"
    if endereco_provisorio not in pagina.extract_text():
        return

    conteudo = pagina.get_contents()
    for operandos, operador in conteudo.operations:
        if operador != b"TJ":
            continue
        trechos = operandos[0]
        texto = "".join(trecho for trecho in trechos if isinstance(trecho, TextStringObject))
        if texto == endereco_provisorio:
            trechos[:] = [ByteStringObject(email.encode("ascii"))]
            pagina.replace_contents(conteudo)
            return

    raise ValueError("O endereço provisório de Estatística não está em um único trecho editável.")


def conectar_sumario(writer, destinos):
    for anotacao in writer.pages[1]["/Annots"]:
        acao = anotacao.get_object()["/A"]
        # Os identificadores emasc: emitidos pelo Beamer viram destinos deste PDF.
        secao = acao.pop("/URI").removeprefix("emasc:")
        pagina = writer.pages[destinos[secao]]
        acao[NameObject("/S")] = NameObject("/GoTo")
        acao[NameObject("/D")] = ArrayObject([pagina.indirect_reference, NameObject("/Fit")])


def remover_numeracao_local(pagina, texto):
    # Em overlays, o texto revelado pode ser extraído depois do rodapé.
    rodape = re.search(r"UFS\s*(\d+)\s*/\s*(\d+)(?=\s|$)", texto)
    if not rodape:
        return None

    atual, total = rodape.groups()
    conteudo = pagina.get_contents()
    trechos = [
        (i, "".join(str(t) for t in operandos[0] if isinstance(t, TextStringObject)))
        for i, (operandos, operador) in enumerate(conteudo.operations)
        if operador == b"TJ"
    ]
    for (_, anterior), (indice_atual, numero), (indice_total, denominador) in reversed(
        list(zip(trechos, trechos[1:], trechos[2:]))
    ):
        if (
            anterior.rstrip().endswith("UFS")
            and numero.strip() == atual
            and denominador.replace(" ", "") == f"/{total}"
        ):
            del conteudo.operations[indice_total]
            del conteudo.operations[indice_atual]
            pagina.replace_contents(conteudo)
            return atual, total
    raise ValueError("Não foi possível remover a numeração local do rodapé.")


def numerar_apresentacao(writer):
    paginacao = []
    numero = 0
    anterior = None
    for pagina in writer.pages:
        texto = pagina.extract_text()
        rodape = remover_numeracao_local(pagina, texto)
        # O mesmo número local em páginas consecutivas identifica overlays do mesmo slide.
        if rodape is None or rodape != anterior:
            numero += 1
        anterior = rodape
        fundo_claro = rodape is not None or texto.startswith(("Sumário", "Obrigado!"))
        paginacao.append((numero, fundo_claro))

    total = numero
    buffer = BytesIO()
    canvas = Canvas(buffer)
    for indice, (pagina, (numero, fundo_claro)) in enumerate(zip(writer.pages, paginacao)):
        largura, altura = float(pagina.mediabox.width), float(pagina.mediabox.height)
        canvas.setPageSize((largura, altura))
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor("#302181" if fundo_claro else "#FFFFFF")
        canvas.drawRightString(largura - 35.43, 4.8, f"{numero} / {total}")
        canvas.showPage()
        writer.set_page_label(indice, indice, style="/D", start=numero)
    canvas.save()

    numeros = PdfReader(buffer)
    for pagina, overlay in zip(writer.pages, numeros.pages):
        pagina.merge_page(overlay)
        pagina.compress_content_streams()


def intervalos_aberturas(capas):
    blocos = {
        "abertura": "Abertura",
        "introducao": "Introdução",
        "motivacao": "Motivação",
        "estatistica": "Introdução à Estatística",
        "ciencia-de-dados": "Introdução à Ciência de Dados",
        "exercicios": "Exercícios",
        "processo-seletivo": "Processo Seletivo LAME 2027",
    }
    marcadores = {
        item.title: capas.get_destination_page_number(item)
        for item in capas.outline
        if hasattr(item, "title")
    }
    if any(titulo not in marcadores for titulo in blocos.values()):
        raise ValueError("Faltam marcadores dos blocos no PDF de aberturas. Recompile aberturas.tex.")

    inicios = [marcadores[titulo] for titulo in blocos.values()]
    finais = inicios[1:] + [len(capas.pages)]
    if inicios[0] != 0 or any(inicio >= fim for inicio, fim in zip(inicios, finais)):
        raise ValueError("A ordem dos blocos em aberturas.tex é inválida.")
    return dict(zip(blocos, zip(inicios, finais)))


def main():
    slides = Path(__file__).resolve().parent
    capas = PdfReader(slides / "modelo" / "aberturas.pdf")
    intervalos = intervalos_aberturas(capas)

    python_pdf = PdfReader(slides / "python" / "introducao-python.pdf")
    paginas_python = len(python_pdf.pages)
    marcador_referencias = python_pdf.named_destinations.get("python.referencias-python")
    if marcador_referencias is None:
        raise ValueError("Recompile o PDF de Python com o marcador referencias-python.")
    indice_referencias = python_pdf.get_destination_page_number(marcador_referencias)
    titulo_referencias = "Referências"
    if titulo_referencias not in python_pdf.pages[indice_referencias].extract_text():
        raise ValueError("O marcador referencias-python deve apontar para o primeiro slide de referências.")

    fonte_estatistica = slides / "estatistica" / "build" / "introducao-estatistica.pdf"
    if not fonte_estatistica.is_file():
        raise FileNotFoundError(
            "Compile introducao-estatistica.tex conforme slides/README.md."
        )
    estatistica_pdf = PdfReader(fonte_estatistica)
    paginas_estatistica = len(estatistica_pdf.pages)
    indice_encerramento = paginas_estatistica - 1
    if "Obrigado!" not in estatistica_pdf.pages[indice_encerramento].extract_text():
        raise ValueError("O PDF de Estatística deve terminar com o slide de agradecimento.")

    writer = PdfWriter()
    writer.append(capas, pages=(0, intervalos["estatistica"][0]), import_outline=False)
    destinos = {
        "introducao": intervalos["introducao"][0],
        "motivacao": intervalos["motivacao"][0],
        "python": len(writer.pages),
    }
    writer.append(python_pdf, "Introdução a Python", pages=(0, indice_referencias))
    inicio_estatistica = len(writer.pages)
    destinos["estatistica"] = inicio_estatistica
    writer.append(capas, pages=intervalos["estatistica"], import_outline=False)
    offset_estatistica = len(writer.pages) - 1
    writer.append(estatistica_pdf, pages=(1, indice_encerramento), import_outline=False)
    marcador_estatistica = writer.add_outline_item("Introdução à Estatística", inicio_estatistica)
    for item in estatistica_pdf.outline:
        indice = estatistica_pdf.get_destination_page_number(item)
        writer.add_outline_item(item.title, offset_estatistica + indice, parent=marcador_estatistica)
    for secao in ("ciencia-de-dados", "exercicios", "processo-seletivo"):
        destinos[secao] = len(writer.pages)
        writer.append(capas, pages=intervalos[secao], import_outline=False)
    writer.append(python_pdf, titulo_referencias, pages=(indice_referencias, paginas_python))
    writer.append(estatistica_pdf, pages=(indice_encerramento, paginas_estatistica))
    corrigir_email_no_encerramento(writer.pages[-1], email_da_capa(capas.pages[0]))
    conectar_sumario(writer, destinos)
    numerar_apresentacao(writer)
    writer.add_metadata({"/Title": capas.metadata.title})
    writer.compress_identical_objects()
    writer.write(slides / "minicurso-emasc-2026.pdf")


if __name__ == "__main__":
    main()
