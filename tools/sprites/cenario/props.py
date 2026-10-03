"""OBJETOS DO CENÁRIO — Nightmoon, direção sépia e ouro.

Tamanhos, origens e a BASE (máscara de colisão do Apêndice A) são o contrato:
lanterna 16×32 ×4 (8,31) · poste 16×48 (8,47) base 5,43-10,47 · pilar 16×32 (8,32) base
0,22-15,31 · caixote 16×20 (8,19) base 1,10-14,19 · barril 16×20 (8,19) base 2,12-13,19 ·
carroça 48×32 (24,31) base 4,16-43,31 · caixão 16×28 (8,27) base 2,20-13,27 · cerca 16×24
(8,23) base 0,20-15,23 · boneco 16×24 (8,24) · atalho 32×16 (16,16) · névoa 16×16 ×4 (0,0) ·
mancha 16×16 ×4 (8,8) · luz 48×48 (24,24).

Luz de cima-esquerda; ferro frio de contraste alto, madeira com veio no comprimento; a chama
âmbar é o acento (lanterna e poste). Névoa, luz e mancha usam alfa parcial de propósito (o
código também as desenha com alfa ou blend aditivo).
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import paleta as P  # noqa: E402
from PIL import Image  # noqa: E402
from kit.tela import Tela, de_segmentos  # noqa: E402

LEG = {
    "o": ("contorno", 0),
    "f": ("ferro", 0), "F": ("ferro", 1), "e": ("ferro", 2), "E": ("ferro", 3), "D": ("ferro", 4), "d": ("ferro", 5),
    "m": ("madeira", 0), "M": ("madeira", 1), "j": ("madeira", 2), "J": ("madeira", 3), "k": ("madeira", 4),
    "c": ("chama", 0), "C": ("chama", 1), "a": ("chama", 2), "A": ("chama", 3),
    "p": ("muro", 1), "P": ("muro", 2), "q": ("muro", 3), "Q": ("muro", 4), "r": ("muro", 5),
    "s": ("saco", 0), "S": ("saco", 1), "t": ("saco", 2), "T": ("saco", 3),
    "x": ("sangue", 1), "X": ("sangue", 2), "v": ("sangue", 0),
    "g": ("ouro", 0), "G": ("ouro", 1), "Y": ("ouro", 2),
    "w": ("marfim", 0), "W": ("marfim", 1),
}


def _desenha(w, h, texto, contorno=True, grupo="corpo"):
    t = Tela(w, h, P.RAMPAS)
    de_segmentos(texto, LEG, P.RAMPAS, w, h, tela=t, grupo=grupo)
    if contorno:
        t.contorno(("contorno", 0))
    return t.imagem()


# --------------------------------------------------------------- lanterna -----
LANTERNA = """
3: 7 EE
4: 6 EDDE
5: 5 eEEEEF
6: 4 eEEEEEEF
7: 5 F%%%%F
8: 5 F%%%%F
9: 5 F%%%%F
10: 5 F%%%%F
11: 5 F%%%%F
12: 4 eEEEEEEF
13: 5 FFFFFF
14: 7 FF
15: 7 eF
16: 7 eF
17: 7 eF
18: 7 eF
19: 7 eF
20: 7 eF
21: 7 eF
22: 7 eF
23: 6 EeFF
24: 7 eF
25: 7 eF
26: 7 eF
27: 4 qQQQQQQp
28: 3 QrrrrrrqqP
29: 3 qQQQQQQPPp
30: 3 pPPPPPPPpp
"""
# vidro aceso: 4 quadros de chama tremulando (letras: brilho do vidro e da chama)
CHAMAS = [
    ["aaAa", "aAAa", "CaAC", "CaaC", "cCCc"],
    ["aAaa", "aAAa", "CAaC", "CaaC", "cCCc"],
    ["aaAa", "AAaa", "CaAC", "CaaC", "cCCc"],
    ["aAAa", "aAAa", "CAAC", "CaaC", "cCCc"],
]


def lanterna():
    out = []
    for q in CHAMAS:
        txt = LANTERNA
        for i, linha in enumerate(q):
            txt = txt.replace(f"{7 + i}: 5 F%%%%F", f"{7 + i}: 5 F{linha}F", 1)
        out.append(_desenha(16, 32, txt))
    return out


POSTE = """
1: 7 EE
2: 6 eDDE
3: 5 eEEEEF
4: 4 eEEEEEEF
5: 5 FaAAaF
6: 5 FaAAaF
7: 5 FCaaCF
8: 5 FCaaCF
9: 4 eEEEEEEF
10: 5 FFFFFF
11: 6 FeeF
12: 7 eF
13: 7 eF
14: 4 FFeeeFFF
15: 5 f.eF.f
16: 7 eF
17: 7 eF
18: 7 eF
19: 7 eF
20: 7 eF
21: 7 eF
22: 7 eF
23: 7 eF
24: 7 eF
25: 7 eF
26: 7 eF
27: 7 eF
28: 7 eF
29: 7 eF
30: 7 eF
31: 7 eF
32: 7 eF
33: 7 eF
34: 7 eF
35: 7 eF
36: 7 eF
37: 6 eEFF
38: 7 eF
39: 7 eF
40: 7 eF
41: 6 eEFF
42: 6 eEFF
43: 5 eEEFFF
44: 5 eEEFFf
45: 5 eFFFFf
46: 5 ffffff
"""


def poste():
    return _desenha(16, 48, POSTE)


PILAR = """
1: 1 rrrrrrrrrrrrrr
2: 1 QQQQQQQQQQQQqq
3: 1 qqqqqqqqqqqqPP
4: 2 QrQQQQQQQQqp
5: 3 QrQQQQQQqp
6: 3 QrQQQQQqqp
7: 3 QrQQQQQqqp
8: 3 QrQQQQQqqp
9: 3 QrQQQQQqqp
10: 3 QrQQQQQqqp
11: 3 QrQQQQQqqp
12: 3 QrQQQQQqqp
13: 3 QrQQQQQqqp
14: 3 QrQQQQQqqp
15: 3 QrQQQQQqqp
16: 3 QrQQQQQqqp
17: 3 QrQQQQQqqp
18: 3 QrQQQQQqqp
19: 3 QrQQQQQqqp
20: 3 QrQQQQQqqp
21: 2 rrrrrrrrrrqp
22: 1 QQQQQQQQQQQQqp
23: 1 QrrrrrrrrrrQqp
24: 1 QQQQQQQQQQQQqp
25: 1 qQQQQQQQQQQQqp
26: 1 qqqqqqqqqqqqPp
27: 1 qqqqqqqqqqqqPp
28: 1 PPPPPPPPPPPPPp
29: 1 PPPPPPPPPPPPpp
30: 1 pppppppppppppp
"""


def pilar():
    return _desenha(16, 32, PILAR)


CAIXOTE = """
1: 2 JJJJJJJJJJJJ
2: 1 JkkkkkkkkkkkJ
3: 1 JjjjjjjjjjjjJ
4: 1 JkkkkkkkkkkkJ
5: 1 JjjjjjjjjjjjJ
6: 1 EEEEEEEEEEEEE
7: 1 EjjjjjjjjjjjE
8: 1 FJjjMjjjjjjjF
9: 1 FjJjjMjjjjjjF
10: 1 FjjJjjMjjjjjF
11: 1 FjjjJjjMjjjjF
12: 1 FMMMMMMMMMMMF
13: 1 FjjjjjJjjMjjF
14: 1 FjjjjjjJjjMjF
15: 1 FjjjjjjjJjjMF
16: 1 FjjjjjjjjJjjF
17: 1 FMMMMMMMMMMMF
18: 1 fFFFFFFFFFFFf
"""


def caixote():
    return _desenha(16, 20, CAIXOTE)


BARRIL = """
1: 4 MMMMMMMM
2: 2 MjjJJJJJjjM
3: 2 MjJkkkkJjjM
4: 2 EEEEEEEEEEEE
5: 2 MJJkjjjjjMMm
6: 2 MJJkjjjjjMMm
7: 2 EEEEEEEEEEEE
8: 2 MJJkjjjjjMMm
9: 2 MJJkjjjjjMMm
10: 2 MJJkjjjjjMMm
11: 2 MJJkjjjjjMMm
12: 2 MJJkjjjjjMMm
13: 2 EEEEEEEEEEEE
14: 2 MJJkjjjjjMMm
15: 2 MJJjjjjjjMMm
16: 3 mMjjjjjjMm
17: 4 mmmmmmmm
"""


def barril():
    return _desenha(16, 20, BARRIL)


CAIXAO = """
1: 5 JJJJJJ
2: 4 JkkkkkkJ
3: 3 JkjjjjjjjJ
4: 2 JkjjjjjjjjjM
5: 2 JkjjjGjjjjjM
6: 2 JkjjGYGjjjjM
7: 2 JkjjjGjjjjjM
8: 2 EEEEEEEEEEEE
9: 3 JjjjjGjjjjM
10: 3 JjjjjGjjjjM
11: 3 JjjjjjjjjjM
12: 3 JjjjjjjjjjM
13: 3 EEEEEEEEEE
14: 3 JjjjjjjjjjM
15: 4 JjjjjjjjM
16: 4 JjjjjjjjM
17: 4 JjjjjjjjM
18: 4 EEEEEEEEE
19: 4 JjjjjjjjM
20: 4 JjjjjjjjM
21: 5 JjjjjjjM
22: 5 JjjjjjjM
23: 5 JjjjjjMM
24: 5 MMMMMMMm
25: 3 pPPPPPPPPPp
"""


def caixao():
    return _desenha(16, 28, CAIXAO)


CERCA = """
1: 2 D.....D.....D
2: 2 E.....E.....E
3: 1 eEe...eEe...eEe
4: 2 E.....E.....E
5: 2 E..D..E..D..E
6: 2 E.eEe.E.eEe.E
7: 2 E..E..E..E..E
8: 0 EEEEEEEEEEEEEEEE
9: 0 FFFFFFFFFFFFFFFF
10: 2 E..E..E..E..E
11: 2 E..E..E..E..E
12: 2 E..E..E..E..E
13: 2 E..E..E..E..E
14: 2 E..E..E..E..E
15: 2 E..E..E..E..E
16: 2 E..E..E..E..E
17: 2 E..E..E..E..E
18: 2 E..E..E..E..E
19: 0 EEEEEEEEEEEEEEEE
20: 0 FFFFFFFFFFFFFFFF
21: 0 pPPPPPPPPPPPPPPp
22: 0 pppppppppppppppp
"""


def cerca():
    return _desenha(16, 24, CERCA)


BONECO = """
1: 6 TTTT
2: 5 TtttTt
3: 5 tStSts
4: 5 tttttS
5: 6 sttS
6: 7 jJ
7: 3 tTTTTTTTTt
8: 2 tTttttttttT
9: 4 tSttttttS
10: 5 tStttSt
11: 5 tSttttS
12: 5 tSttttS
13: 5 tStttSt
14: 6 tSttS
15: 7 jJ
16: 7 jJ
17: 7 jJ
18: 7 jJ
19: 7 jJ
20: 4 MmmjJmmM
21: 3 MMmmmmmmMM
22: 3 mmmmmmmmmm
"""


def boneco():
    return _desenha(16, 24, BONECO)


ATALHO = """
1: 1 rrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
2: 1 QQQQQQQQQQQQQQQQQQQQQQQQQQQQqp
3: 1 Qd.D.E.E.E.E.E.E.E.E.E.E.D.dqp
4: 1 QD.D.E.E.E.E.E.E.E.E.E.E.D.Dqp
5: 1 QEEEEEEEEEEEEEEEEEEEEEEEEEEEqp
6: 1 QE.E.E.E.E.E.E.E.E.E.E.E.E.Eqp
7: 1 QE.E.E.E.E.E.E.E.E.E.E.E.E.Eqp
8: 1 QE.E.E.E.E.EGGGE.E.E.E.E.E.Eqp
9: 1 QE.E.E.E.E.EGYGE.E.E.E.E.E.Eqp
10: 1 QE.E.E.E.E.E.E.E.E.E.E.E.E.Eqp
11: 1 QEEEEEEEEEEEEEEEEEEEEEEEEEEEqp
12: 1 QF.F.F.F.F.F.F.F.F.F.F.F.F.Fqp
13: 1 QqqqqqqqqqqqqqqqqqqqqqqqqqqqPp
14: 1 pppppppppppppppppppppppppppppp
"""


def atalho():
    return _desenha(32, 16, ATALHO)


CARROCA = """
3: 11 MMMMMMMMMMMMMMMMMMMMMMMM
4: 10 MjjjjjjjjjjjjjjjjjjjjjjjjM
5: 10 MkkkkkkkkkkkkkkkkkkkkkkkkM
6: 10 MjjjjjjjjjjjjjjjjjjjjjjjjM
7: 10 MkkkkkkkkkkkkkkkkkkkkkkkkM
8: 10 EEEEEEEEEEEEEEEEEEEEEEEEEE
9: 10 MJJJJJJJJJJJJJJJJJJJJJJJJM
10: 10 MjjjjjjjjjjjjjjjjjjjjjjjjM
11: 10 MjjjjjjjjjjjjjjjjjjjjjjjjM
12: 10 MJJJJJJJJJJJJJJJJJJJJJJJJM
13: 10 MjjjjjjjjjjjjjjjjjjjjjjjjM
14: 2 jjjjjjjjMMMMMMMMMMMMMMMMMMMMMMMMMMjjjjjjjj
15: 2 MMMMMMMMmmmmmmmmmmmmmmmmmmmmmmmmmmMMMMMMMM
28: 4 pPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPp
29: 5 pppppppppppppppppppppppppppppppppppppp
"""


def _roda(t, cx, cy, r=6):
    """Roda de raios: aro de madeira, cubo de ferro, 4 raios; luz de cima-esquerda."""
    for y in range(cy - r - 1, cy + r + 2):
        for x in range(cx - r - 1, cx + r + 2):
            d = math.hypot(x - cx, y - cy)
            if r - 1.4 <= d <= r + 0.4:
                luz = (x - cx) + (y - cy) < 0
                t.pinta(x, y, "madeira", 3 if luz else 1)
    for k in range(4):
        ang = k * math.pi / 4 + math.pi / 8
        for rr in range(1, r - 1):
            x, y = int(round(cx + math.cos(ang) * rr)), int(round(cy + math.sin(ang) * rr))
            t.pinta(x, y, "madeira", 2)
            x, y = int(round(cx - math.cos(ang) * rr)), int(round(cy - math.sin(ang) * rr))
            t.pinta(x, y, "madeira", 2)
    for (x, y) in ((cx, cy), (cx - 1, cy), (cx, cy - 1), (cx - 1, cy - 1)):
        t.pinta(x, y, "ferro", 3 if (x, y) == (cx - 1, cy - 1) else 2)


def carroca():
    t = Tela(48, 32, P.RAMPAS)
    _roda(t, 15, 21)
    _roda(t, 33, 21)
    de_segmentos(CARROCA, LEG, P.RAMPAS, 48, 32, tela=t)
    t.contorno(("contorno", 0))
    return t.imagem()


def nevoa():
    """16×16 que se repete; 4 quadros com a textura andando 4 px pro lado (emenda nas bordas)."""
    n = P.RAMPAS["nevoa"]
    rnd = random.Random(9)
    # fiapos: elipses achatadas em posições periódicas
    fiapos = [(rnd.uniform(0, 16), rnd.uniform(0, 16), rnd.uniform(5, 9), rnd.uniform(0.9, 1.6), rnd.choice((0, 1, 2)))
              for _ in range(8)]
    out = []
    for q in range(4):
        im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        for y in range(16):
            for x in range(16):
                melhor = None
                for (cx, cy, rx, ry, tom) in fiapos:
                    for ox in (-16, 0, 16):
                        for oy in (-16, 0, 16):
                            dx = (x - (cx + q * 4 + ox)) / rx
                            dy = (y - (cy + oy)) / ry
                            d = dx * dx + dy * dy
                            if d <= 1 and (melhor is None or tom > melhor):
                                melhor = tom
                if melhor is not None:
                    im.putpixel((x, y), tuple(n[melhor]) + ((150, 180, 210)[melhor],))
                else:
                    im.putpixel((x, y), tuple(n[0]) + (90,))
        out.append(im)
    return out


def mancha():
    """A mancha de sangue com as almas: poça escura com brilhos dourados que trocam de lugar."""
    s, g = P.RAMPAS["sangue"], P.RAMPAS["ouro"]
    base = []
    for y in range(16):
        for x in range(16):
            d = ((x - 7.5) / 6.5) ** 2 + ((y - 8) / 4.2) ** 2
            if d <= 1:
                base.append((x, y, 0 if d > 0.7 else (1 if d > 0.3 else 2)))
    brilhos = [[(6, 7), (9, 9)], [(8, 6), (5, 9)], [(10, 7), (7, 10)], [(7, 8), (11, 9)]]
    out = []
    for q in range(4):
        im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        for x, y, tom in base:
            im.putpixel((x, y), tuple(s[tom]) + (255,))
        for (x, y) in brilhos[q]:
            im.putpixel((x, y), tuple(g[2]) + (255,))
            im.putpixel((x + 1, y), tuple(g[1]) + (255,))
        out.append(im)
    return out


def luz():
    """Brilho branco em degraus (o código tinge e soma com bm_add). Achatado: luz no chão."""
    im = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
    degraus = [(1.0, 30), (0.78, 60), (0.56, 100), (0.36, 145), (0.18, 190)]
    for y in range(48):
        for x in range(48):
            d = math.hypot((x - 23.5) / 23.5, (y - 23.5) / 19.5)
            a = 0
            for lim, alfa in degraus:
                if d <= lim:
                    a = alfa
            if a:
                im.putpixel((x, y), (255, 255, 255, a))
    return im


PROPS = {
    # nome: (função, origem, quadros?)
    "spr_lanterna": (lanterna, (8, 31)),
    "spr_poste": (lambda: [poste()], (8, 47)),
    "spr_pilar": (lambda: [pilar()], (8, 32)),
    "spr_caixote": (lambda: [caixote()], (8, 19)),
    "spr_barril": (lambda: [barril()], (8, 19)),
    "spr_carroca": (lambda: [carroca()], (24, 31)),
    "spr_caixao": (lambda: [caixao()], (8, 27)),
    "spr_cerca": (lambda: [cerca()], (8, 23)),
    "spr_boneco": (lambda: [boneco()], (8, 24)),
    "spr_atalho": (lambda: [atalho()], (16, 16)),
    "spr_nevoa": (nevoa, (0, 0)),
    "spr_mancha": (mancha, (8, 8)),
    "spr_luz": (lambda: [luz()], (24, 24)),
}

# base que bloqueia (Apêndice A): a arte não pode sair dela embaixo
MASCARAS = {"spr_poste": (5, 43, 10, 47), "spr_caixote": (1, 10, 14, 19), "spr_barril": (2, 12, 13, 19),
            "spr_carroca": (4, 16, 43, 31), "spr_caixao": (2, 20, 13, 27), "spr_cerca": (0, 20, 15, 23),
            "spr_pilar": (0, 22, 15, 31)}


def quadros(nome):
    return PROPS[nome][0]()


if __name__ == "__main__":
    from kit import previa as pv
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "previa")
    pv.folha([(n.replace("spr_", ""), quadros(n)) for n in PROPS], k=4, larg_rotulo=110,
             titulo="objetos do cenário").save(os.path.join(out, "props_folha.png"))
    print("ok")
