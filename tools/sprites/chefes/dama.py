"""DAMA DO RELÓGIO (chefe 2, V1.1) — inspirada na Lady Maria; direção sépia e ouro.

BRIEF
- Caçadora jovem e esguia, MESMO tamanho e traço do caçador (32×32, origem 16,30, figura de
  ~28 px). Lâmina longa = spr_arma_dama_longa (girada pelo código a partir da mão em (18, 20):
  mao_x=2, mao_y=10); adaga na outra mão, desenhada no corpo.
- Gancho: pena branca subindo do tricórnio + rabo de cavalo prateado descendo pelas costas
  (silhueta diferente do caçador, que tem capa curta). Traços: casaco vinho acinturado com
  galão dourado na barra e na frente, babado branco no peito, punho de renda.
- Família de cor: vinho + prata + ouro (contra o escuro quente do caçador).
- Animações: idle 4, walk 6, ataque 3, estocada 3, passo 3 (esquiva pra trás), stagger 2,
  caído 2 (ajoelhada), transforma 6 (desperta o sangue: ergue a lâmina, o sangue escorre),
  morte 8 (ajoelha e crava a lâmina no chão — a lâmina entra no desenho, porque na morte o
  código não desenha a arma).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import paleta as P  # noqa: E402
from kit.boneco import Boneco  # noqa: E402

LEG = {
    "o": ("contorno", 0),
    "0": ("vinho", 0), "1": ("vinho", 1), "2": ("vinho", 2), "3": ("vinho", 3), "4": ("vinho", 4),
    "p": ("pele", 0), "P": ("pele", 1), "Q": ("pele", 2),
    "w": ("marfim", 0), "W": ("marfim", 1), "V": ("marfim", 2),
    "j": ("prata", 1), "J": ("prata", 2), "K": ("prata", 3), "i": ("prata", 0),
    "g": ("ouro", 0), "G": ("ouro", 1), "Y": ("ouro", 2),
    "b": ("casaco", 0), "B": ("couro", 1), "n": ("couro", 2), "N": ("couro", 3),
    "h": ("casaco", 1), "H": ("casaco", 2), "k": ("casaco", 0),
    "e": ("ferro", 2), "E": ("ferro", 4), "F": ("ferro", 5),
    "v": ("sangue", 0), "x": ("sangue", 1), "X": ("sangue", 2), "Z": ("sangue", 3),
    "t": ("vinho", 0),
}

PECAS = {
    "cab": {
        "normal": """
2: 7 WVWWw
3: 8 wWWw
4: 10 Wwhh
5: 11 HHH1.1HH1
6: 11 HHhh11hHHhh1
7: 11 hh0000000001
8: 11 GGGGtpppppGG
9: 13 jjPQPtP
10: 13 jjPQQQP
11: 13 jjjpPQPp
12: 13 jj.pPPp
""",
        "tras": """
2: 7 wWWw
3: 9 Wwhh
4: 10 HHH1.1HH1
5: 10 HHhh11hHHhh1
6: 10 hh0000000001
7: 10 GGGGtpppppGG
8: 12 jjPQPtP
9: 12 jjPQQQP
10: 12 jjjpPQtp
11: 12 jj.pPPp
""",
        "baixa": """
3: 7 WVWWw
4: 8 wWWw
5: 10 Wwhh
6: 11 HHH1.1HH1
7: 11 HHhh11hHHhh1
8: 11 hh0000000001
9: 11 GGGGtppppGGG
10: 13 jjtpPPp
11: 13 jjjpPQQP
12: 13 jj.pPQp
""",
    },
    "rabo": {
        "normal": """
13: 12 jJ
14: 11 jJ
15: 11 jJ
16: 10 jJ
17: 10 jK
18: 10 jj
19: 10 j
""",
        "vento": """
13: 12 jJ
14: 11 jJ
15: 10 jJ
16: 9 jJ
17: 8 jK
18: 7 jj
""",
    },
    "tronco": {
        "normal": """
13: 14 2WVW1
14: 13 32VWVw1
15: 13 332WVW11
16: 13 3321W1G1
17: 13 33211101
18: 13 2211G101
""",
        "frente": """
13: 15 2WVW1
14: 14 32VWVw1
15: 13 3332WVW1
16: 13 33321W1G
17: 13 33221110
18: 13 2211G101
""",
        "tras": """
13: 13 2WVW1
14: 12 32VWVw1
15: 12 332WVW11
16: 12 3321W1G11
17: 12 332111011
18: 13 2211G101
""",
    },
    "braco": {
        "baixo": """
14: 21 1
15: 21 1
16: 20 11
17: 19 11
18: 19 1
19: 18 WV
20: 17 BNn
21: 17 bB
""",
    },
    "adaga": {
        "baixa": """
17: 13 1
18: 13 1
19: 13 W
20: 12 Bn
21: 12 E
22: 12 e
""",
        "erguida": """
14: 11 1
15: 10 11
16: 9 1W
17: 8 Bn
18: 8 E
19: 7 E
20: 6 e
""",
    },
}

BOTA_TRAS = "0: 0 kBn\n1: 0 kkB"
BOTA_FRENTE = "0: 0 kBnnN\n1: 0 kBBnN"
BOTA_LONGE = "0: 0 kBnB\n1: 0 kkBn"
BOTA_ERG = "0: 0 kBn"
BOTA_ERG_L = "0: 0 kkB"

SAIA = {
    "y0": 19, "y1": 27, "cintura": (13, 19), "barra": (9, 23), "curva": 1.4,
    "faixas": [(0.12, ("vinho", 2)), (0.30, ("vinho", 3)), (0.42, ("vinho", 1)), (0.56, ("vinho", 2)),
               (0.70, ("vinho", 1)), (1.00, ("vinho", 0))],
    "topo": {("vinho", 3): ("vinho", 2), ("vinho", 2): ("vinho", 1)},
    # galão dourado na barra e na frente
    "barra_tons": {("vinho", 0): ("ouro", 0), ("vinho", 1): ("ouro", 0), ("vinho", 2): ("ouro", 1), ("vinho", 3): ("ouro", 1)},
    "abertura": (0.74, 0.07, ("ouro", 0)),
}

ORDEM = ["adaga", "rabo", "lista:botas", "saia", "tronco", "cab", "braco", "remendos"]
PADRAO = {"cab": ("normal", 0, 0), "tronco": ("normal", 0, 0), "braco": ("baixo", 0, 0), "rabo": ("normal", 0, 0),
          "adaga": ("baixa", 0, 0), "botas": [(BOTA_TRAS, 11, 28), (BOTA_FRENTE, 17, 28)]}

B = Boneco(32, 32, P.RAMPAS, LEG, PECAS, ORDEM, saia=SAIA, rel={"cab", "tronco", "rabo", "adaga"}, padrao=PADRAO)

IDLE = [
    {},
    {"tronco": ("normal", 0, 1), "rabo": ("normal", 0, 1), "saia": {"barra": (9, 22)}},
    {"tronco": ("normal", 0, 1), "rabo": ("normal", 0, 1), "cab": ("normal", 0, 1)},
    {"saia": {"barra": (9, 24)}},
]
WALK = [
    {"botas": [(BOTA_LONGE, 9, 28), (BOTA_FRENTE, 19, 28)], "saia": {"barra": (8, 24)}},
    {"y": 1, "cab": ("normal", 0, -1), "botas": [(BOTA_ERG_L, 11, 28), (BOTA_FRENTE, 18, 28)], "rabo": ("vento", 0, 0)},
    {"botas": [(BOTA_ERG_L, 13, 28), (BOTA_FRENTE, 16, 28)], "saia": {"barra": (10, 22)}, "rabo": ("vento", 0, 0)},
    {"botas": [(BOTA_FRENTE, 9, 28), (BOTA_LONGE, 19, 28)], "saia": {"barra": (8, 24)}},
    {"y": 1, "cab": ("normal", 0, -1), "botas": [(BOTA_ERG, 11, 28), (BOTA_LONGE, 18, 28)], "rabo": ("vento", 0, 0)},
    {"botas": [(BOTA_ERG, 13, 28), (BOTA_LONGE, 16, 28)], "saia": {"barra": (10, 22)}, "rabo": ("vento", 0, 0)},
]
ATAQUE = [
    {"x": -1, "y": 1, "tronco": ("tras", 0, 0), "adaga": ("erguida", 0, 0), "rabo": ("normal", 0, 0),
     "botas": [(BOTA_TRAS, 10, 28), (BOTA_FRENTE, 18, 28)]},
    {"x": 2, "y": 1, "tronco": ("frente", 0, 0), "cab": ("normal", 1, 0), "rabo": ("vento", 0, 0),
     "botas": [(BOTA_LONGE, 8, 28), (BOTA_FRENTE, 20, 28)], "saia": {"barra": (7, 24)}},
    {"x": 1, "tronco": ("frente", 0, 0), "botas": [(BOTA_TRAS, 10, 28), (BOTA_FRENTE, 19, 28)]},
]
ESTOCADA = [
    {"x": -2, "y": 2, "tronco": ("tras", 0, 0), "cab": ("normal", -1, 0), "adaga": ("erguida", 0, 0),
     "botas": [(BOTA_TRAS, 9, 28), (BOTA_FRENTE, 17, 28)], "saia": {"barra": (8, 23)}},
    {"x": 3, "y": 2, "tronco": ("frente", 0, 0), "cab": ("normal", 2, 0), "rabo": ("vento", 0, 0),
     "botas": [(BOTA_LONGE, 6, 28), (BOTA_FRENTE, 21, 28)], "saia": {"barra": (5, 24)}},
    {"x": 1, "y": 1, "tronco": ("frente", 0, 0), "botas": [(BOTA_TRAS, 9, 28), (BOTA_FRENTE, 19, 28)]},
]
PASSO = [
    {"y": 1, "botas": [(BOTA_TRAS, 10, 28), (BOTA_FRENTE, 17, 28)]},
    {"x": -2, "y": 0, "tronco": ("tras", 0, 0), "cab": ("normal", -1, 0), "rabo": ("vento", 2, -1),
     "botas": [(BOTA_ERG_L, 11, 27), (BOTA_ERG, 15, 27)], "saia": {"barra": (10, 25), "y1": 26}},
    {"x": -1, "y": 1, "botas": [(BOTA_TRAS, 8, 28), (BOTA_FRENTE, 16, 28)], "saia": {"barra": (8, 24)}},
]
STAGGER = [
    {"y": 2, "cab": ("baixa", 0, 0), "tronco": ("tras", 0, 0), "adaga": ("baixa", 0, 1),
     "botas": [(BOTA_TRAS, 10, 28), (BOTA_FRENTE, 16, 28)]},
    {"y": 2, "x": 1, "cab": ("baixa", 0, 1), "adaga": ("baixa", 0, 1),
     "botas": [(BOTA_TRAS, 10, 28), (BOTA_FRENTE, 16, 28)]},
]
CAIDO = [
    {"y": 5, "cab": ("baixa", 0, 0), "saia": {"barra": (7, 25), "y1": 28, "curva": 0.9},
     "botas": [(BOTA_ERG_L, 7, 28)], "braco": None},
    {"y": 6, "cab": ("baixa", 0, 0), "saia": {"barra": (7, 25), "y1": 28, "curva": 0.9},
     "botas": [(BOTA_ERG_L, 7, 28)], "braco": None},
]
# desperta o sangue: ergue a cabeça, a adaga corta a própria mão, o sangue escorre
TRANSFORMA = [
    {"y": 1, "cab": ("baixa", 0, 0), "adaga": ("erguida", 0, 0)},
    {"cab": ("tras", 0, 0), "adaga": ("erguida", 1, -1), "rabo": ("vento", 1, 0)},
    {"cab": ("tras", 0, 0), "adaga": ("erguida", 1, -1), "rabo": ("vento", 2, -1),
     "remendos": ["17: 9 X\n18: 9 X\n19: 9 X"]},
    {"y": 0, "cab": ("tras", 0, 0), "rabo": ("vento", 2, -2), "remendos": ["20: 17 X\n21: 18 X\n22: 18 X\n23: 18 X"]},
    {"cab": ("normal", 0, 0), "rabo": ("vento", 1, 0), "remendos": ["21: 18 X\n22: 18 X\n24: 18 X"]},
    {"remendos": ["22: 18 X\n24: 18 X"]},
]
# morte: ajoelha e crava a lâmina no chão (a lâmina é desenhada no corpo)
LAMINA_CRAVADA = """
15: 21 F
16: 21 E
17: 21 E
18: 21 E
19: 21 E
20: 21 E
21: 21 E
22: 21 E
23: 21 E
24: 21 e
25: 21 e
26: 21 e
14: 20 GYG
13: 21 G
"""
MORTE = [
    {"y": 1, "cab": ("baixa", 0, 0), "tronco": ("tras", 0, 0)},
    {"y": 3, "cab": ("baixa", 0, 0), "saia": {"barra": (8, 25), "y1": 28}},
    {"y": 5, "cab": ("baixa", 1, 0), "saia": {"barra": (7, 25), "y1": 28, "curva": 0.9},
     "botas": [(BOTA_ERG_L, 7, 28)], "remendos": [(LAMINA_CRAVADA, 1, 3)]},
    {"y": 6, "cab": ("baixa", 1, 1), "saia": {"barra": (7, 25), "y1": 28, "curva": 0.9},
     "botas": [(BOTA_ERG_L, 7, 28)], "braco": None, "remendos": [(LAMINA_CRAVADA, 1, 3), ("20: 21 BN\n21: 21 bB", 0, 0)]},
    {"y": 7, "cab": ("baixa", 1, 2), "saia": {"barra": (7, 26), "y1": 28, "curva": 0.8},
     "botas": [(BOTA_ERG_L, 7, 28)], "braco": None, "adaga": None, "rabo": ("normal", 0, 0),
     "remendos": [(LAMINA_CRAVADA, 1, 3), ("21: 21 BN\n22: 21 bB", 0, 0)]},
    {"y": 8, "cab": ("baixa", 1, 3), "saia": {"barra": (7, 26), "y1": 28, "curva": 0.8},
     "botas": [(BOTA_ERG_L, 7, 28)], "braco": None, "adaga": None, "rabo": ("normal", 0, 0),
     "remendos": [(LAMINA_CRAVADA, 1, 3), ("21: 21 BN\n22: 21 bB", 0, 0)]},
    {"y": 8, "cab": ("baixa", 1, 3), "saia": {"barra": (7, 26), "y1": 28, "curva": 0.8},
     "botas": [(BOTA_ERG_L, 7, 28)], "braco": None, "adaga": None, "rabo": ("normal", 0, 0),
     "remendos": [(LAMINA_CRAVADA, 1, 3), ("21: 21 BN\n22: 21 bB", 0, 0)]},
    {"y": 9, "cab": ("baixa", 1, 3), "saia": {"barra": (7, 26), "y1": 28, "curva": 0.8},
     "botas": [(BOTA_ERG_L, 7, 28)], "braco": None, "adaga": None, "rabo": ("normal", 0, 0),
     "remendos": [(LAMINA_CRAVADA, 1, 3), ("22: 21 BN\n23: 21 bB", 0, 0)]},
]

ANIMS = {
    "idle": (IDLE, 160),
    "walk": (WALK, 100),
    "ataque": (ATAQUE, 120),
    "estocada": (ESTOCADA, 140),
    "passo": (PASSO, 90),
    "stagger": (STAGGER, 150),
    "caido": (CAIDO, 300),
    "transforma": (TRANSFORMA, 160),
    "morte": (MORTE, 160),
}


def quadros(nome):
    return [B.montar(p).imagem() for p in ANIMS[nome][0]]


def aura():
    """spr_fx_aura_sangue: 32×32, origem (16,30), 4 quadros, desenhada ATRÁS dela na fase 2.
    Uma chama de sangue em volta do corpo: borda escura, miolo claro, línguas que sobem e
    trocam de lugar a cada quadro (forma estável + deslocamento, pra tremular sem chuviscar)."""
    import math
    from kit.tela import Tela
    out = []
    for q in range(4):
        t = Tela(32, 32, P.RAMPAS)
        for y in range(2, 31):
            for x in range(4, 28):
                dx, dy = (x - 16) / 9.5, (y - 18) / 13.5
                r = math.hypot(dx, dy)
                # línguas de chama no alto: a borda sobe onde o seno é alto
                ang = math.atan2(dy, dx)
                lingua = 0.18 * max(0.0, math.sin(ang * 5 + q * 1.6)) * (1 if dy < 0.2 else 0.3)
                borda = 1.0 + lingua
                if borda - 0.22 <= r <= borda:
                    k = (r - (borda - 0.22)) / 0.22
                    tom = 3 if k < 0.35 else (2 if k < 0.7 else 1)
                    t.pinta(x, y, "sangue", tom, grupo="fx")
        out.append(t.imagem())
    return out



AUDITORIA = {
    "teto_cores": "figurino de 4 materiais + ouro (até 25 cores), sem nenhuma gêmea",
    "pixel_solto": "olho, botões de ouro, punho de renda, gotas de sangue da transformação",
    "nos_1px": "ponta da pena, adaga, bico da bota",
    "furos_1px": "vão entre a pena e a aba, entre as botas",
    "aglomerados": "pena, babado e galão concentram detalhe pequeno (ponto de interesse)",
}

if __name__ == "__main__":
    from kit import previa as pv
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "previa")
    linhas = [(n, quadros(n)) for n in ANIMS] + [("aura", aura())]
    pv.folha(linhas, k=5, larg_rotulo=90, titulo="Dama").save(os.path.join(out, "dama_folha.png"))
    print("ok")
