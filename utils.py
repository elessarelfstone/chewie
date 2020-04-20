import json
import os

from settings import CHARACTER_STYLE_TEMPALTE, TEMP_DIR


def read_file(fpath):
    with open(fpath, 'r', encoding="utf8") as f:
        data = f.read()

    return data


def load_characters_styles(movie):
    """ Load """
    data = read_file(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'characters', '{}.json'.format(movie))
    )

    return json.loads(data)


def find_character(ch_obj: dict, styles: dict) -> str:

    # chs = load_characters_styles()
    for k, v in styles.items():
        _d = {**CHARACTER_STYLE_TEMPALTE, **v}
        if _d == ch_obj:
            return k


def temp_fpath(fname):
    return os.path.join(TEMP_DIR, fname)
