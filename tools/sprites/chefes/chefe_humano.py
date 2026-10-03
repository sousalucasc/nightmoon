"""CHEFE 1, fase humana — o caçador da Igreja Branca, direção sépia e ouro. (2ª rodada, refeito do zero)

BRIEF
- Chefe da arena. Machadada dupla (machado = spr_arma_machado, girado pelo código a partir da
  mão em (28, 33): mao_x=4, mao_y=12, em todos os quadros menos o tiro), tiro de bacamarte
  (desenhado no corpo; boca do sino em (44, 23): boca_x=20, boca_y=22, nos 3 quadros) e salto.
- Escala: 48×48, origem (24, 45); figura de 41 px: capuz pontudo, manto largo, pesado.
- Gancho: o CAPUZ pontudo com o rosto na sombra (só o olho vermelho e o queixo aparecem) +
  o manto em sino sobre os ombros. Traços: sobretudo branco até a canela com a abertura escura
  na frente, faixa vermelha na cintura com a ponta caída do lado, luvas e botas de couro.
- Família de cor: alvo (branco sujo, quente) contra o casaco escuro do jogador: o caçador da
  igreja oposta. Acentos: a faixa vermelha e o olho (a besta já está lá dentro). Nada do chefe
  antigo (cabelo branco, venda, estola marfim, ardósia).
- Animações: idle 4, walk 6, ataque 3 (o corpo gira em volta da mão parada), tiro 3 (o cano
  fica; no disparo o corpo recua), salto 3 (agacha / no ar / pouso), stagger 2, caído 2 (um
  joelho no chão, a mão do machado no joelho).
- Pintado à mão na bancada chefe_humano_pinta.py. Sem sombreamento automático.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import paleta as P  # noqa: E402
from kit.boneco import Boneco  # noqa: E402

W = H = 48
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


def _sh(txt, dx=0, dy=0, de=0, ate=99):
    """Desloca as linhas de 'de' a 'ate' (as outras ficam)."""
    out = []
    for lin in txt.strip().splitlines():
        y, resto = lin.split(":", 1)
        x0, t = resto.strip().split(" ", 1)
        y, x0 = int(y), int(x0)
        if de <= y <= ate:
            y, x0 = y + dy, x0 + dx
        out.append(f"{y}: {x0} {t}")
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

CAPUZ_BAIXO = _sh(CAPUZ.replace("11: 18 AbBBBBhHHEhB", "11: 18 AbBBBBhHHhhB"), 1, 2)

PERNA_TRAS = """
33: 25 h
34: 25 hH
35: 24 hH
36: 23 hHH
37: 23 hHh
38: 23 hHh
39: 22 hHHh
40: 21 hHHh
41: 20 vHHHh
42: 19 vVHHHh
43: 18 vVVVHHh
44: 18 hhhhhhh
"""
PERNA = """
33: 26 H
34: 27 h
35: 26 Hh
36: 26 Hh
37: 26 Hh
38: 27 hh
39: 27 hHh
40: 27 hHHh
41: 27 hHHHh
42: 27 hVVVHh
43: 27 hVVVVVh
44: 27 hhhhhhhh
"""


def _passo(txt, dx, dy=0):
    """A bota anda dx (a canela vai junto, a coxa fica sob o casaco); dy < 0 ergue o pé."""
    return _sh(_sh(txt, dx, dy, 39, 44), dx // 2, 0, 37, 38)


# joelho no chão: a perna de trás deita a canela, a da frente fica com o joelho pra cima
AJOELHA_TRAS = """
37: 23 hHh
38: 23 hHHh
39: 23 hHHh
40: 22 hHHh
41: 16 vvhhhHHHh
42: 14 vVVhhhhHHh
43: 14 vVVVhhhhhh
44: 14 hhhhhhhhh
"""
AJOELHA = """
36: 26 HHHHh
37: 26 HHHHHh
38: 30 HHh
39: 31 HHh
40: 31 hHh
41: 31 hHHh
42: 31 hVVHh
43: 31 hVVVVh
44: 31 hhhhhhh
"""

BRACO_VAR = {
    "normal": BRACO,
    # corpo recuado 2 px: o braço se inclina pra frente até a mão parada em (28, 33)
    "longo": _sh(_sh(BRACO, -2, 0, 22, 24), -1, 0, 25, 26),
    # corpo 2 px à frente: o braço se inclina pra trás
    "curto": _sh(_sh(BRACO, 2, 0, 22, 24), 1, 0, 25, 26),
    # corpo baixo (agacha, zonzo, de joelho): o manto cobre o alto do braço
    "baixo": "\n".join(l for l in BRACO.strip().splitlines() if int(l.split(":")[0]) >= 27),
    # no ar (corpo 3 px acima): o braço estica
    "estica": _sh(BRACO, 0, -3, 22, 26) + "\n26: 29 abBbAa\n27: 29 abBbAa\n",
    "tiro": TIRO,
}
CASACO_CURTO = "\n".join(l for l in CASACO.strip().splitlines() if int(l.split(":")[0]) <= 37) + """
38: 13 aAAAAAAAAa..aAAAAAa
"""

PECAS = {
    "capuz": {"normal": CAPUZ, "baixo": CAPUZ_BAIXO},
    "capa": {"normal": CAPA},
    "casaco": {"normal": CASACO, "curto": CASACO_CURTO},
    # windup do machado: o braço de trás sobe pra trás (silhueta própria no flash)
    "braco_tras": {"normal": BRACO_TRAS, "ergue": """
15: 9 vv
16: 8 vVVv
17: 8 vVVv
18: 8 aAAa
19: 9 aAAa
20: 10 aAAa
21: 11 aAA
"""},
    "apoio": {"tiro": TIRO_TRAS},
    "arma": {"bacamarte": BACAMARTE},
    "braco": BRACO_VAR,
    "perna_tras": {"base": PERNA_TRAS, "tras": _passo(PERNA_TRAS, -2), "frente": _passo(PERNA_TRAS, 3),
                   "ergue": _passo(PERNA_TRAS, 1, -2), "abre": _passo(PERNA_TRAS, -2),
                   "ar": _sh(PERNA_TRAS, 2, -4), "joelho": AJOELHA_TRAS},
    "perna": {"base": PERNA, "tras": _passo(PERNA, -3), "frente": _passo(PERNA, 2),
              "ergue": _passo(PERNA, -1, -2), "abre": _passo(PERNA, 2),
              "ar": _sh(PERNA, -1, -5), "joelho": AJOELHA},
}

ORDEM = ["braco_tras", "perna_tras", "perna", "casaco", "capa", "capuz", "apoio", "arma", "braco", "remendos"]
PADRAO = {"capuz": ("normal", 0, 0), "capa": ("normal", 0, 0), "casaco": ("normal", 0, 0),
          "braco_tras": ("normal", 0, 0), "braco": ("normal", 0, 0),
          "perna_tras": ("base", 0, 0), "perna": ("base", 0, 0)}
B = Boneco(W, H, P.RAMPAS, LEG, PECAS, ORDEM, rel={"capuz", "capa", "casaco", "braco_tras", "apoio"},
           padrao=PADRAO)


def _p(**k):
    return k


IDLE = [
    _p(),
    _p(y=1, braco=("baixo", 0, 0)),
    _p(y=1, capuz=("normal", 0, 0), braco=("baixo", 0, 0)),
    _p(capuz=("normal", 1, 0)),
]
WALK = [
    _p(perna_tras=("tras", 0, 0), perna=("frente", 0, 0), casaco=("normal", -1, 0)),
    _p(y=1, perna_tras=("tras", 0, 0), perna=("frente", 0, 0), casaco=("normal", -1, 0), braco=("baixo", 0, 0)),
    _p(perna_tras=("ergue", 0, 0), perna=("base", 0, 0)),
    _p(perna_tras=("frente", 0, 0), perna=("tras", 0, 0), casaco=("normal", 1, 0)),
    _p(y=1, perna_tras=("frente", 0, 0), perna=("tras", 0, 0), casaco=("normal", 1, 0), braco=("baixo", 0, 0)),
    _p(perna_tras=("base", 0, 0), perna=("ergue", 0, 0)),
]
# ataque: o corpo gira em volta da mão do machado (28, 33), que não sai do lugar
ATAQUE = [
    _p(x=-2, y=1, capuz=("normal", -1, 0), braco=("longo", 0, 0), braco_tras=("ergue", 0, 0), perna_tras=("tras", 0, 0)),
    _p(x=2, y=1, capuz=("normal", 1, 1), braco=("curto", 0, 0), perna_tras=("tras", 0, 0), perna=("frente", 0, 0)),
    _p(x=1, perna=("frente", 0, 0)),
]
# tiro: o bacamarte não sai do lugar (boca em 44, 23); no disparo o corpo recua
TIRO = [
    _p(braco=("tiro", 0, 0), braco_tras=None, apoio=("tiro", 0, 0), arma=("bacamarte", 0, 0)),
    _p(x=-1, capuz=("normal", -1, 0), braco=("tiro", -1, 0), braco_tras=None, apoio=("tiro", 1, 0),
       arma=("bacamarte", 0, 0), perna_tras=("tras", 0, 0)),
    _p(y=1, capuz=("normal", 0, 0), braco=("tiro", 0, 0), braco_tras=None, apoio=("tiro", 0, -1),
       arma=("bacamarte", 0, 0)),
]
SALTO = [
    _p(y=4, casaco=("curto", 0, 0), braco=("baixo", 0, 0), perna_tras=("abre", 0, 0), perna=("abre", 0, 0)),
    _p(y=-2, braco=("estica", 0, 0), perna_tras=("ar", 0, 1), perna=("ar", 0, 1)),
    _p(x=1, y=5, casaco=("curto", 0, 0), braco=("baixo", 0, 0), perna_tras=("abre", 0, 0), perna=("abre", 0, 0)),
]
STAGGER = [
    _p(x=-1, y=2, capuz=("baixo", 0, 0), braco=("baixo", 0, 0)),
    _p(x=-2, y=3, capuz=("baixo", 1, 1), braco=("baixo", 0, 0), perna_tras=("tras", 0, 0)),
]
# caído: um joelho no chão, a mão do machado descansa no joelho (28, 33)
CAIDO = [
    _p(y=6, casaco=("curto", 0, 0), capuz=("baixo", 0, 0), braco=("baixo", 0, 0), perna_tras=("joelho", 0, 0),
       perna=("joelho", 0, 0), braco_tras=("normal", 0, -1)),
    _p(y=6, casaco=("curto", 0, 0), capuz=("normal", 0, 1), braco=("baixo", 0, 0), perna_tras=("joelho", 0, 0),
       perna=("joelho", 0, 0), braco_tras=("normal", 0, -1)),
]

ANIMS = {
    "idle": (IDLE, 180),
    "walk": (WALK, 110),
    "ataque": (ATAQUE, 160),
    "tiro": (TIRO, 160),
    "salto": (SALTO, 200),
    "stagger": (STAGGER, 150),
    "caido": (CAIDO, 300),
}


def montar(p):
    return B.montar(p)


def quadros(nome):
    return [montar(p).imagem() for p in ANIMS[nome][0]]


AUDITORIA = {
    "pixel_solto": "olho vermelho na sombra do capuz e brilho do bacamarte",
    "furos_1px": "vãos entre as pernas e entre as pontas do manto",
    "pontilhado": "pontas do manto e faixa",
    "teto_cores": "tiro: o bacamarte soma ferro e madeira ao corpo",
}

if __name__ == "__main__":
    from kit import previa as pv
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "previa")
    linhas = [(n, quadros(n)) for n in ANIMS]
    pv.folha(linhas, k=4, larg_rotulo=90, titulo="chefe humano (2ª rodada)").save(
        os.path.join(out, "chefe_humano_folha.png"))
    print("ok")
