from enum import Enum

class Type(Enum):
    entier = "entier"
    liste = "liste"
    booleen = "booléen"
    texte = "texte"


def get_type(value):
    if isinstance(value, str):
        return Type.texte
    elif isinstance(value, bool):
        return Type.booleen
    elif isinstance(value, int):
        return Type.entier
    elif isinstance(value, list):
        return Type.liste
    else:
        return None