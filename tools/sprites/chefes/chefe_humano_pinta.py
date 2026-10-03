"""Bancada do chefe humano novo (2ª rodada): o caçador da Igreja Branca, pintado à mão."""

LEG = {
    "o": ("contorno", 0),
    "a": ("alvo", 0), "A": ("alvo", 1), "b": ("alvo", 2), "B": ("alvo", 3), "C": ("alvo", 4),
    "h": ("casaco", 1), "H": ("casaco", 2),
    "v": ("couro", 1), "V": ("couro", 2),
    "p": ("pele", 0), "P": ("pele", 1),
    "r": ("forro", 0), "R": ("forro", 1), "Q": ("forro", 2),
    "E": ("olho", 0),
    "m": ("madeira", 2), "M": ("madeira", 3), "f": ("ferro", 2), "F": ("ferro", 3), "I": ("ferro", 4),
}


def sh(txt, dx=0, dy=0):
    out = []
    for l in txt.strip().splitlines():
        y, resto = l.split(":", 1)
        x0, t = resto.strip().split(" ", 1) if " " in resto.strip() else (resto.strip(), "")
        out.append(f"{int(y) + dy}: {int(x0) + dx} {t}")
    return "\n" + "\n".join(out) + "\n"


BRACO_TRAS = """
24: 12 aAa
25: 12 aAAa
26: 12 hvvh
27: 12 vVVv
28: 12 vVvv
29: 13 vv
"""

CASACO = """
22: 15 aAbbbbbbbbbbbbbbAa
23: 15 AbBBBBBBbhhbbbbbAa
24: 15 AbBBBBBBbhhbbbbAAa
25: 15 AbBBBBBbbhhbbbbAAa
26: 15 AbBBBBBbbhhbbbbAAa
27: 15 AbBBBBBbbhhbbbbAAa
28: 15 rRQQRRRRRRRrrrrrrr
29: 15 rRRRRRRRRRrrrrrrrr
30: 15 RrBBBBbbbhhbbbbAAa
31: 15 RrBBBBbbbhhbbbbAAa
32: 14 ARrBBBBbbbhhbbbbAAa
33: 14 AbRrBBbbbbhhbbbbAAa
34: 14 AbBRBBbbbbbhhbbbAAa
35: 13 AbBBBBbbbbb.hhbbbAAa
36: 13 AbBBBbbbbbA..hbbbAAa
37: 13 AbBBBbbbbA...hAbbbAa
38: 13 aAbBbbbbAa....AbbAAa
39: 12 aAbBbbbAAa.....AbAAa
40: 12 aAAbbAAAa......aAAa
41: 13 aaAAAaa
"""

PERNAS = """
33: 25 hH
34: 25 hHh
35: 24 hHHh
36: 23 hHHHh
37: 23 hHhHh
38: 23 hHh.hh
39: 22 hHHh.hHh
40: 21 hHHh..hHHh
41: 20 vHHHh..hHHHh
42: 19 vVHHHh..hVVVHh
43: 18 vVVVHHh..hVVVVVh
44: 18 hhhhhhh..hhhhhhhh
"""

CAPA = """
13: 15 AbBC
13: 29 CBbA
14: 13 AbBCCB
14: 29 BBBbA
15: 12 AbBCCCB
15: 28 BBBBbbA
16: 11 AbBCCCBBBBBBBBBBBBBBBbbA
17: 11 AbBCCBBBBBBBBBBBBBBBbbbAa
18: 10 AbBBCBBBABBBBBABBBBBbbbAAa
19: 10 AbBBBBBbABBBBbABBBBbbbAAAa
20: 10 aAbBBBbbAbBBbbAbBBbbbAAAaa
21: 10 aAAbbbAAaAbbAAaAbbAAAAaaa
22: 11 aaAAaa.aAAa.aAAa.aAAaaa
"""

CAPUZ = """
4: 22 AB
5: 21 AbBC
6: 20 AbBCCB
7: 19 AbBBCCBB
8: 19 AbBBBCCBBb
9: 18 AbBBBBCBBBbA
10: 18 AbBBBBBhhhhB
11: 18 AbBBBBhHHEhB
12: 18 AbBBBBhHHHhB
13: 18 aAbBBBhhPPhA
14: 18 aAbBBbhppPhA
15: 19 aAbbbAhhAa
"""

BRACO = """
22: 30 bBBA
23: 29 abBBA
24: 29 abBbA
25: 29 abBbAa
26: 29 abBbAa
27: 29 abBbAa
28: 29 abbAAa
29: 28 aAAAa
30: 27 vVVVv
31: 27 vVVVv
32: 27 VVvVv
33: 27 vVvvv
34: 28 vvv
"""

BASE = BRACO_TRAS + PERNAS + CASACO + CAPA + CAPUZ + BRACO

BACAMARTE = """
20: 43 FI
21: 41 fFFI
22: 28 mMMmffFFFFFFFfFFI
23: 28 mMMMmffffffffffFF
24: 29 mmMm........fffF
25: 43 fF
"""
TIRO = """
18: 30 bBBA
19: 30 bBBbA
20: 31 bBbA
21: 31 abbA
22: 31 vVVv
23: 31 vVVv
24: 32 vv
"""
TIRO_TRAS = """
23: 36 vVv
24: 35 avVVv
25: 34 aAvvv
26: 33 aAA
"""
F_TIRO = BRACO_TRAS + PERNAS + CASACO + CAPA + CAPUZ + TIRO_TRAS + BACAMARTE + TIRO
