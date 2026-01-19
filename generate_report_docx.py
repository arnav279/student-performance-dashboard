from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile


OUTPUT_PATH = Path("Minor_Project_Progress_Report_Styled_v2.docx")


def run_props(size=24, bold=False):
    parts = [
        '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>',
        f'<w:sz w:val="{size}"/>',
        f'<w:szCs w:val="{size}"/>',
    ]
    if bold:
        parts.append("<w:b/>")
    return "".join(parts)


def paragraph(text="", *, size=24, bold=False, align="both", before=0, after=120, page_break=False, indent=0):
    if page_break:
        return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
    if text == "":
        return '<w:p/>'
    escaped = escape(text)
    indent_xml = f'<w:ind w:left="{indent}"/>' if indent else ""
    return (
        f'<w:p><w:pPr><w:jc w:val="{align}"/><w:spacing w:before="{before}" w:after="{after}" '
        f'w:line="360" w:lineRule="auto"/>{indent_xml}</w:pPr>'
        f'<w:r><w:rPr>{run_props(size=size, bold=bold)}</w:rPr>'
        f'<w:t xml:space="preserve">{escaped}</w:t></w:r></w:p>'
    )


def bullet(text):
    return (
        '<w:p><w:pPr><w:jc w:val="both"/><w:spacing w:after="80" w:line="360" w:lineRule="auto"/>'
        '<w:ind w:left="720" w:hanging="360"/></w:pPr>'
        f'<w:r><w:rPr>{run_props(size=24, bold=False)}</w:rPr><w:t xml:space="preserve">• </w:t></w:r>'
        f'<w:r><w:rPr>{run_props(size=24, bold=False)}</w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'
    )


def title(text):
    return paragraph(text, size=30, bold=True, align="center", before=120, after=180)


def heading(text):
    return paragraph(text, size=28, bold=True, align="left", before=180, after=120)


def subheading(text):
    return paragraph(text, size=24, bold=True, align="left", before=120, after=80)


def table(rows, widths=None):
    if not widths:
        widths = [2400] * len(rows[0])
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    trs = []
    for row_index, row in enumerate(rows):
        cells = []
        for cell in row:
            fill = ' w:fill="D9E2F3"' if row_index == 0 else ""
            cells.append(
                '<w:tc>'
                f'<w:tcPr><w:tcW w:w="0" w:type="auto"/><w:shd w:val="clear" w:color="auto"{fill}/></w:tcPr>'
                f'{paragraph(cell, size=22, bold=row_index == 0, align="left", after=60)}'
                '</w:tc>'
            )
        trs.append(f'<w:tr>{"".join(cells)}</w:tr>')
    return (
        '<w:tbl>'
        '<w:tblPr><w:tblW w:w="0" w:type="auto"/>'
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        '<w:left w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        '<w:right w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        '<w:insideH w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        '<w:insideV w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        '</w:tblBorders></w:tblPr>'
        f'<w:tblGrid>{grid}</w:tblGrid>'
        f'{"".join(trs)}'
        '</w:tbl>'
    )


def build_document():
    parts = []

