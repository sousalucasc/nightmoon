"""Legenda dos carimbos do caçador: caractere -> (rampa, tom). Rampas em paleta.py."""
LEG = {
    "o": ("contorno", 0),
    "0": ("casaco", 0), "1": ("casaco", 1), "2": ("casaco", 2), "3": ("casaco", 3), "4": ("casaco", 4),
    "t": ("casaco", 0), "T": ("casaco", 1),       # linha interna = tom escuro do casaco
    "r": ("forro", 0), "R": ("forro", 1), "y": ("forro", 2),
    "p": ("pele", 0), "P": ("pele", 1), "Q": ("pele", 2), "q": ("pele", 2),
    "w": ("marfim", 0), "W": ("marfim", 1), "V": ("marfim", 2),
    "b": ("casaco", 0), "B": ("couro", 1), "n": ("couro", 2), "N": ("couro", 3),
    "g": ("ouro", 0), "G": ("ouro", 1), "Y": ("ouro", 2),
    "h": ("casaco", 0), "H": ("casaco", 1), "j": ("casaco", 2),     # cabelo = escuro do casaco
    "c": ("recorte", 0), "C": ("recorte", 1),
    "v": ("sangue", 0), "x": ("sangue", 1), "X": ("sangue", 2), "Z": ("sangue", 3),
    "i": ("vidro", 0), "I": ("vidro", 1), "J": ("vidro", 2),
    "_": (None, 0),   # apaga (usado em remendos)
}
