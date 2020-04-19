from itertools import groupby

from docx import Document
from docx.text.paragraph import Paragraph

from settings import DEFAULT_FONT, CHARACTER_STYLE_TEMPALTE
from utils import find_charcter, load_characters_styles

def transcript_parts(fpath):
    """ Break docx document into parts(paragraph objects)
        which are separated by empty line(s).
    """

    doc = Document(fpath)
    rows = []
    for p in doc.paragraphs:
        if p.text:
            rows.append(p)
        else:
            rows.append(None)
    parts = []
    for k, g in groupby(rows, lambda x: x is not None):
        if k:
            _p = filter(lambda x: x.text.strip(), g)
            parts.append(tuple(_p))

    return parts


def font(par: Paragraph) -> str:
    _all = [par.style.font.name] + [run.font.name for run in par.runs]
    fonts = list(filter(bool, _all))
    return fonts[0] if len(fonts) else None


def bold(par: Paragraph):
    """ Return whether paragraph's text is bold or not """
    _all = [par.style.font.bold] + [run.font.bold for run in par.runs]
    b = list(filter(bool, _all))
    return b[0] if len(b) else False


def italic(par: Paragraph) -> bool:
    """ Return whether paragraph's text is italic or not """
    _all = [par.style.font.italic] + [run.font.italic for run in par.runs]
    i = list(filter(bool, _all))
    return i[0] if len(i) else None


def underline(par: Paragraph) -> bool:
    """ Return whether paragraph's text is underline or not """
    _all = [par.style.font.underline] + [run.font.underline for run in par.runs]
    underlines = list(filter(bool, _all))
    return underlines[0] if len(underlines) else None


def style(par: Paragraph):
    """ Return style for paragraph as json"""
    d = dict()
    # _d =
    d['font'] = font(par) or DEFAULT_FONT
    if bold(par):
        d['bold'] = True

    if italic(par):
        d['italic'] = True

    if underline(par):
        d['underline'] = True

    return {**CHARACTER_STYLE_TEMPALTE, **d}


def show_styles(parts):
    chs = load_characters_styles('the_office')
    for p in parts:
        if len(p) == 1:
            print(style(p[0]), '>>>>', find_charcter(style(p[0]), chs))


show_styles(transcript_parts('C:\\Users\\elessar\\Documents\\The Office S03E8 - The Merger.docx'))


    # print(parts)

# docx_parse("c:\\Users\\elessar\\michael.docx")
