"""BRUTAMONTES — inimigo pesado, Nightmoon, direção sépia e ouro. (2ª rodada, refeito do zero)

BRIEF
- O prisioneiro da gaiola: gigante esquelético, curvado, com uma gaiola de ferro enferrujada
  presa na cabeça (cadeado na gola) e os olhos vermelhos lá dentro; braços compridos que passam
  do joelho, grilhões nos pulsos e a corrente partida arrastando no chão; trapos na cintura.
  Referência: os gigantes da igreja de Bloodborne (altos, magros, braços longos) e as gaiolas
  dos alunos de Byrgenwerth. Nada do brutamontes antigo (carne crua, saco, corpo atarracado).
- Escala: 48×48, origem (24, 45); figura de 40 px (da argola da gaiola à sola), 4 cabeças.
- Gancho: a gaiola na cabeça projetada pra frente + os braços que chegam abaixo do joelho.
  Traços: costelas e coluna marcadas, grilhões com corrente, pés grandes.
- Família de cor: pelecinza (pele de defunto, cinza-violeta) + ferrugem + trapo; acento: os
  olhos vermelhos dentro da gaiola. 15 cores.
- Animações: idle 4 (respira, a cabeça dá um tranco), walk 6 (contato, descida e passagem, os
  braços balançam contra as pernas), pancada 3 (windup com os dois punhos erguidos acima da
  gaiola — silhueta alta pro flash; ativo: os punhos no chão; recovery), agarrão 3 (windup com
  os braços abertos em X; ativo: avança com a garra à frente; recovery), stagger 2, caído 2 (de
  joelhos, mãos no chão), morte 6 (cai de joelhos, tomba, deitado; os olhos apagam).
- Pintado à mão na bancada brutamontes_pinta.py: carimbos por peça (gaiola, tronco, trapos,
  braços por pose, pernas por passo) e o quadro deitado inteiro. Sem sombreamento automático.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import paleta as P  # noqa: E402
from kit.boneco import Boneco  # noqa: E402

LEG = {
    "o": ("contorno", 0),
    "p": ("pelecinza", 0), "q": ("pelecinza", 1), "Q": ("pelecinza", 2), "w": ("pelecinza", 3), "W": ("pelecinza", 4),
    "i": ("ferro", 3),
    "z": ("ferrugem", 0), "Z": ("ferrugem", 1), "y": ("ferrugem", 2), "Y": ("ferrugem", 3),
    "t": ("trapo", 1), "T": ("trapo", 2), "u": ("trapo", 3),
    "E": ("olho", 0),
}

PECAS = {
    "cab": {
        "normal": """
5: 33 yZ
6: 31 zyYyZz
7: 30 zyYYyZZz
8: 29 zyYyyZZZZz
9: 29 ZppZqqZqqz
10: 29 yppyqQyQqZ
11: 29 yppyEqyEqZ
12: 29 ZppZqqZqQz
13: 29 ZppZpwZwpz
14: 29 zZyYyZyZZz
15: 29 piipppippp
16: 28 qQq
16: 37 i
17: 36 yYZ
18: 36 ZZz
""",
    },
    "tronco": {
        "normal": """
10: 20 wWWw
11: 18 wwWWWwQ
12: 17 QwwWwwwQQq
13: 16 QwwwwwwQQQqq
14: 16 qwwwQQQQQQqq
15: 16 qwwQQQQQqqqp
16: 17 qwQQQwwQqqp
17: 17 qQQwwWwwQqp
18: 17 qQpQwwwQQqp
19: 17 qQQppQwQQqp
20: 17 qQwQQpQQQqp
21: 17 qQQppQQwQqp
22: 18 qQwQQppQqp
23: 18 qQQQQQQqp
24: 18 qqQQQQqqp
25: 18 qqQQwQqp
26: 18 qqQQQQqp
27: 18 qqQQQqqp
""",
    },
    "trapo": {
        "normal": """
27: 18 uuuTTTtt
28: 17 tuuTTTTttt
29: 17 tuTTTtTTtt
30: 17 tTTTtTTTtt
31: 17 tTt.tTt.tt
32: 18 t...tT..t
33: 22 t
""",
    },
    "braco": {
        "pende": """
14: 26 wwW
15: 25 qwwW
16: 26 qwwwQq
17: 27 qwwQq
18: 28 qwQq
19: 28 qwQq
20: 29 qwQq
21: 29 qwQq
22: 29 qwQq
23: 30 qwQq
24: 30 qwwQ
25: 30 qwwQq
26: 31 qwQq
27: 31 qwQq
28: 31 qwQqq
29: 32 qwQq
30: 32 qwQq
31: 32 qwQq
32: 31 iiiiip
33: 31 pZyZZp
34: 31 qwWWwq
35: 31 qwwwwQq
36: 31 qwQpQQq
37: 31 qQqpQqp
38: 31 qq.qQ.q
39: 32 p..p
33: 37 i
34: 37 Z
35: 37 i
36: 37 Z
37: 37 i
38: 38 Z
39: 38 i
40: 38 Z
41: 39 i
42: 39 Z
43: 39 iZi
""",
        # pancada, windup: os dois punhos acima da gaiola
        "ergue": """
2: 24 qwWWq
3: 23 qwWWwwq
4: 23 qwwwwQq
5: 23 qQwQqQq
6: 24 iiiip
7: 24 pZyZp
8: 25 qwQq
9: 25 qwQq
10: 26 qwQq
11: 26 qwwQ
12: 26 qwQq
13: 26 qwQq
14: 26 wwWw
15: 25 qwwWwQ
16: 26 qwwwQq
8: 23 i
9: 23 Z
10: 23 i
11: 22 Z
12: 22 i
""",
        # pancada, ativo: o punho no chão à frente
        "bate": """
14: 26 wwWw
15: 25 qwwWwQ
16: 26 qwwwQq
17: 27 qwwQq
18: 28 qwwQq
19: 29 qwQq
20: 30 qwQq
21: 30 qwwQ
22: 31 qwQq
23: 31 qwQq
24: 32 qwQq
25: 32 qwQq
26: 33 qwQq
27: 33 qwQq
28: 34 qwQq
29: 34 qwQq
30: 34 qwQqq
31: 33 iiiiiip
32: 33 pZyZZZp
33: 33 qwWWwwq
34: 33 qwwwwwQq
35: 33 qwwwQQqq
36: 33 qQwQwQqp
37: 34 pqpqpqp
""",
        # agarrão, windup: braços abertos em X
        "abre": """
16: 26 qwwwQq
15: 25 qwwWwwQ
14: 26 wwWwwwwQ
13: 31 qwwwwQ
12: 34 qwwQq
11: 36 qwwQ
10: 37 qwwQ
9: 38 iiip
8: 38 pZyp
7: 39 qwWq
6: 39 qwwwq
5: 39 qwQwQq
4: 40 q.q.q
""",
        # agarrão, ativo: a garra à frente
        "estende": """
14: 26 wwWw
15: 25 qwwWwQ
16: 26 qwwwwQq
17: 27 qwwwwQq
18: 29 qwwwQq
19: 30 qwwwQq
20: 32 qwwQq
21: 33 qwwQq
22: 34 qwwQq
23: 35 iiiip
24: 35 pZyZp
25: 36 qwWWq
26: 36 qwwwwq
27: 36 qwQqQq
28: 37 q.q.q
24: 34 i
25: 34 Z
26: 33 i
27: 33 Z
28: 32 i
""",
    },
    "braco_tras": {
        "pende": """
14: 14 qQQ
15: 14 qQq
16: 14 qQq
17: 13 qQq
18: 13 qQq
19: 13 qQq
20: 13 qQq
21: 13 qQq
22: 12 qQq
23: 12 qQQ
24: 12 qQq
25: 12 qQq
26: 12 qQq
27: 12 qQq
28: 12 qQq
29: 12 qQq
30: 11 iiiip
31: 11 pZZZp
32: 11 qQQqq
33: 11 qQqqq
34: 11 qqQqp
35: 11 q.q.q
32: 11 i
33: 10 Z
34: 10 i
35: 10 Z
36: 10 i
37: 10 Z
""",
        "ergue": """
3: 18 qQQq
4: 17 qQQQq
5: 17 qQqQq
6: 18 iiip
7: 18 pZZp
8: 18 qQq
9: 18 qQq
10: 17 qQq
11: 17 qQq
12: 16 qQq
13: 15 qQq
14: 14 qQQ
15: 14 qQq
16: 14 qQq
""",
        "bate": """
14: 14 qQQ
15: 14 qQq
16: 15 qQq
17: 16 qQq
18: 17 qQq
19: 18 qQq
20: 19 qQq
21: 20 qQq
22: 21 qQq
23: 22 qQq
24: 23 qQq
25: 24 qQq
26: 25 qQq
27: 26 qQq
28: 26 qQq
29: 27 qQq
30: 26 iiiip
31: 26 pZZZp
32: 26 qQQqq
33: 26 qQqqq
34: 26 qqQqp
""",
        "abre": """
14: 14 qQQ
13: 12 qQQq
12: 10 qQQq
11: 8 qQQq
10: 7 qQq
9: 6 qQq
8: 5 iiip
7: 5 pZZp
6: 4 qQQq
5: 3 qQqQq
4: 3 q.q.q
""",
    },
    "perna_tras": {
        "base": """
31: 19 qQQq
32: 20 qQQq
33: 20 qQQq
34: 21 qQQq
35: 21 qQwq
36: 21 qQQq
37: 20 qQQq
38: 20 qQq
39: 19 qQq
40: 19 qQq
41: 19 qQq
42: 18 qQQq
43: 16 qQQQqqp
44: 16 pqqqqqp
""",
        "tras": """
31: 19 qQQq
32: 19 qQQq
33: 19 qQQq
34: 19 qQQq
35: 19 qQwq
36: 19 qQQq
37: 18 qQQq
38: 18 qQq
39: 17 qQq
40: 17 qQq
41: 16 qQq
42: 15 qQQq
43: 13 qQQQqqp
44: 13 pqqqqqp
""",
        "frente": """
31: 19 qQQq
32: 20 qQQq
33: 21 qQQq
34: 22 qQQq
35: 23 qQwq
36: 23 qQQq
37: 23 qQQq
38: 23 qQq
39: 23 qQq
40: 23 qQq
41: 23 qQq
42: 22 qQQq
43: 21 qQQQqqp
44: 21 pqqqqqp
""",
        "ergue": """
31: 19 qQQq
32: 20 qQQq
33: 21 qQQq
34: 22 qQwq
35: 22 qQQq
36: 21 qQQq
37: 20 qQq
38: 19 qQq
39: 18 qQq
40: 17 qQQq
41: 15 qQQQqp
42: 15 pqqqp
""",
    },
    "perna": {
        "base": """
31: 23 QwwQ
32: 24 qwwQ
33: 24 qwwQ
34: 25 qwwQ
35: 26 qwWQ
36: 26 qwwQq
37: 26 qwQq
38: 25 qwQq
39: 25 qwQq
40: 25 qwQq
41: 25 qwQq
42: 25 qwwQq
43: 25 qwwwwQqp
44: 25 pqqqqqqp
""",
        "tras": """
31: 23 QwwQ
32: 23 qwwQ
33: 23 qwwQ
34: 23 qwwQ
35: 23 qwWQ
36: 23 qwwQ
37: 22 qwQq
38: 22 qwQq
39: 21 qwQq
40: 21 qwQq
41: 20 qwQq
42: 19 qwwQq
43: 19 qwwwwQqp
44: 19 pqqqqqqp
""",
        "frente": """
31: 23 QwwQ
32: 24 qwwQ
33: 25 qwwQ
34: 26 qwwQ
35: 27 qwWQ
36: 28 qwwQq
37: 28 qwQq
38: 28 qwQq
39: 28 qwQq
40: 29 qwQq
41: 29 qwQq
42: 29 qwwQq
43: 29 qwwwwQqp
44: 29 pqqqqqqp
""",
        "ergue": """
31: 23 QwwQ
32: 24 qwwQ
33: 25 qwwQ
34: 26 qwWQ
35: 26 qwwQ
36: 25 qwwQ
37: 24 qwQq
38: 23 qwQq
39: 22 qwQq
40: 21 qwwQq
41: 21 qwwwwQqp
42: 21 pqqqqqqp
""",
        # de joelhos: as duas pernas, as canelas deitadas pra trás
        "ajoelha": """
36: 19 qQQq
37: 19 qQQq
38: 20 qQQq
39: 20 qQQq
40: 21 qQQq
41: 21 qQQq
42: 14 qQQQQQQqQQq
43: 12 qQQqqqqqqqqp
44: 12 pqqqqqqqqqp
36: 23 QwwQ
37: 24 qwwQ
38: 25 qwwQ
39: 25 qwwQ
40: 26 qwwQ
41: 26 qwWQq
42: 18 qwwwwwwwwqQq
43: 17 qwwwwQQQqqqqp
44: 17 pqqqqqqqqqqqp
""",
    },
}

ORDEM = ["braco_tras", "perna_tras", "perna", "tronco", "trapo", "cab", "braco", "remendos"]
PADRAO = {"cab": ("normal", 0, 0), "tronco": ("normal", 0, 0), "trapo": ("normal", 0, 0),
          "braco": ("pende", 0, 0), "braco_tras": ("pende", 0, 0),
          "perna_tras": ("base", 0, 0), "perna": ("base", 0, 0)}
B = Boneco(48, 48, P.RAMPAS, LEG, PECAS, ORDEM, rel={"cab", "tronco", "trapo", "braco", "braco_tras"},
           padrao=PADRAO)


def _p(**k):
    return k


IDLE = [
    _p(),
    _p(y=1),
    _p(y=1, cab=("normal", 1, 0)),
    _p(braco_tras=("pende", 0, 1), braco=("pende", 0, 1)),
]

# contato, descida, passagem; os braços balançam contra as pernas
WALK = [
    _p(perna_tras=("tras", 0, 0), perna=("frente", 0, 0), braco_tras=("pende", 1, 0), braco=("pende", -1, 0)),
    _p(y=1, perna_tras=("tras", 0, 0), perna=("frente", 0, 0), braco_tras=("pende", 1, 0), braco=("pende", -1, 0)),
    _p(y=-1, perna_tras=("ergue", 0, 0), perna=("base", 0, 0)),
    _p(perna_tras=("frente", 0, 0), perna=("tras", 0, 0), braco_tras=("pende", -1, 0), braco=("pende", 1, 0)),
    _p(y=1, perna_tras=("frente", 0, 0), perna=("tras", 0, 0), braco_tras=("pende", -1, 0), braco=("pende", 1, 0)),
    _p(y=-1, perna_tras=("base", 0, 0), perna=("ergue", 0, 0)),
]

PANCADA = [
    _p(y=1, cab=("normal", -1, -1), braco=("ergue", 0, 0), braco_tras=("ergue", 0, 0)),
    _p(x=3, y=5, trapo=("normal", -1, -2), cab=("normal", 2, 4), braco=("bate", 0, 1), braco_tras=("bate", 3, 0),
       perna_tras=("tras", 0, 0), perna=("frente", 0, 0)),
    _p(x=2, y=3, trapo=("normal", -1, -1), cab=("normal", 1, 2), braco=("bate", 0, 0), braco_tras=("bate", 3, -1),
       perna_tras=("tras", 0, 0), perna=("frente", 0, 0)),
]

AGARRAO = [
    _p(x=-1, cab=("normal", -1, -1), braco=("abre", 0, 0), braco_tras=("abre", 0, 0), perna_tras=("tras", 0, 0)),
    _p(x=3, y=2, trapo=("normal", -1, -1), cab=("normal", 2, 2), braco=("estende", 0, 0), braco_tras=("pende", -1, 0),
       perna_tras=("tras", 0, 0), perna=("frente", 1, 0)),
    _p(x=2, y=1, trapo=("normal", -1, 0), cab=("normal", 1, 1), braco=("estende", 0, 2), braco_tras=("pende", 0, 0),
       perna_tras=("tras", 0, 0), perna=("frente", 0, 0)),
]

STAGGER = [
    _p(x=-2, y=1, cab=("normal", -1, 2), braco=("pende", 1, 0), braco_tras=("pende", 1, 0), perna_tras=("tras", 0, 0)),
    _p(x=-1, y=2, cab=("normal", 0, 3)),
]

# deitado de bruços, a gaiola tombada à direita (pintado inteiro)
DEITADO = """
35: 39 zZyY
36: 37 zZyYYyZ
37: 36 zyppqqqZz
38: 36 yppqEqEqZ
39: 35 ZyZZyZZyZZz
40: 36 yppqqwqwZ
41: 36 zpppqqqZz
42: 37 zZZyZZz
37: 18 wwWWWwwww
36: 22 wWWw
38: 16 qwwwwwwWwwwwwwwQ
39: 14 qwwQQwQQwQQwQQQq
40: 13 qQQQpQQpQQpQQQQqq
41: 13 qQQQQQQQQQQQQqqq
42: 14 qqqQQQQQQQqqqp
38: 11 TuuT
39: 9 tuuTTt
40: 8 tTTTtTt
41: 8 tTtTTtt
42: 9 t.tTt
40: 4 qQQq
41: 3 qQQQqq
42: 2 qQQQQqqp
43: 3 pqqqpp
42: 31 qwwQ
43: 23 qwwwwwwwQQq
44: 18 qQwQqiiwwwQQqp
44: 32 iZiZiZ
"""
DEITADO_1 = DEITADO.replace("38: 36 yppqEqEqZ", "38: 36 yppqqqEqZ")
DEITADO_0 = DEITADO.replace("38: 36 yppqEqEqZ", "38: 36 yppqqqqqZ")

CAIDO = [
    _p(y=8, perna_tras=None, perna=("ajoelha", 0, 0), cab=("normal", 2, 3), braco=("bate", 0, -1),
       braco_tras=("bate", 3, -1)),
    _p(y=8, perna_tras=None, perna=("ajoelha", 0, 0), cab=("normal", 2, 2), braco=("bate", 0, -1),
       braco_tras=("bate", 3, -1)),
]
MORTE = [
    STAGGER[0],
    _p(y=8, perna_tras=None, perna=("ajoelha", 0, 0), cab=("normal", 1, 0), braco=("bate", 0, -1),
       braco_tras=("bate", 3, -1)),
    _p(x=2, y=10, perna_tras=None, perna=("ajoelha", 0, 0), cab=("normal", 3, 3), braco=("bate", 0, -3),
       braco_tras=("bate", 3, -3), trapo=("normal", -2, -2)),
    {"quadro": DEITADO},
    {"quadro": DEITADO_1},
    {"quadro": DEITADO_0},
]

ANIMS = {
    "idle": (IDLE, 180),
    "walk": (WALK, 130),
    "pancada": (PANCADA, 200),
    "agarrao": (AGARRAO, 200),
    "stagger": (STAGGER, 150),
    "caido": (CAIDO, 300),
    "morte": (MORTE, 110),
}


def quadros(nome):
    return [B.montar(p).imagem() for p in ANIMS[nome][0]]


AUDITORIA = {
    "pixel_solto": "olhos vermelhos dentro da gaiola, elos da corrente, dentes",
    "nos_1px": "elos da corrente e pontas dos dedos",
    "furos_1px": "vãos entre os dedos e entre os elos",
    "pontilhado": "barras da gaiola e elos da corrente alternam ferro e ferrugem de propósito",
    "aglomerados": "corrente e gaiola concentram o detalhe pequeno",
    "teto_cores": "deitado: a altura baixa derruba o teto do tier",
    "direcao": "quadros deitados e de joelhos",
}


if __name__ == "__main__":
    from kit import previa as pv
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "previa")
    linhas = [(n, quadros(n)) for n in ANIMS]
    pv.folha(linhas, k=4, larg_rotulo=90, titulo="brutamontes (2ª rodada)").save(
        os.path.join(out, "brutamontes_folha.png"))
    print("ok")
