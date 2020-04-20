import os
import enum

from itertools import groupby
from typing import List, Any, Dict

from docx import Document
from docx.text.paragraph import Paragraph

from db import upload_transcripts
from settings import DEFAULT_FONT, CHARACTER_STYLE_TEMPALTE
from utils import find_character, load_characters_styles


def transcript_parts(fpath: str) -> List:
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


def style(par: Paragraph) -> Dict:
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

    return d


def parse_movie(fpath: str) -> str:
    fname = os.path.basename(fpath)
    t = fname.split('-')[0]
    t = t.split(' ')[:-1]
    return '_'.join(t).lower()


def parse_transcripts(fpath: str) -> List[Any]:
    """ Return dict of transcripts"""
    transcripts = transcript_parts(fpath)
    _transcripts = []
    # meta = dict(movie=parse_movie(fpath))
    for transcript in transcripts:
        meta = dict(movie=parse_movie(fpath))

        # if we have only line in talk
        if len(transcript) == 1:
            line = transcript[0]

            # if it's just one single phrase
            if style(line) == dict(font=DEFAULT_FONT):
                d = dict(meta=meta, transcript=monolog(line.text))
            else:
                # or it's monolog to the camera
                meta.update(dict(style=style(line)))
                d = dict(meta=meta, transcript=monolog(line.text), is_monolog=1)
        else:
            # build dialog
            d = dict(meta=meta, transcript=dialog([p.text for p in transcript]))

        _transcripts.append(d)

    return _transcripts


def dialog(lines: List[str]):
    return '\n'.join([' - {}'.format(line) for line in lines])


def monolog(line: str) -> str:
    return ' - {}'.format(line)


def show_styles(parts):
    chs = load_characters_styles('the_office')
    for p in parts:
        if len(p) == 1:
            print(style(p[0]), '>>>>', find_character(style(p[0]), chs))

