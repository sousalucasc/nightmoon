"""Bancada do brutamontes novo (2ª rodada): o prisioneiro da gaiola, pintado à mão."""

LEG = {
    "o": ("contorno", 0),
    "p": ("pelecinza", 0), "q": ("pelecinza", 1), "Q": ("pelecinza", 2), "w": ("pelecinza", 3), "W": ("pelecinza", 4),
    "i": ("ferro", 3),
    "z": ("ferrugem", 0), "Z": ("ferrugem", 1), "y": ("ferrugem", 2), "Y": ("ferrugem", 3),
    "S": ("saco", 1), "d": ("saco", 2), "D": ("saco", 3),
    "E": ("olho", 0),
    "x": ("sangue", 1),
}

# camadas: braço de trás, tronco, pernas, pano, braço da frente, gaiola
BRACO_TRAS = """
16: 10 qwwQ
17: 9 qwwQQ
18: 9 qwwQq
19: 9 qwQQq
20: 9 qwQQq
21: 9 qwQqq
22: 9 qwQqp
23: 9 qQQqp
24: 8 qwQQqp
25: 8 qwQQqp
26: 8 qwQQqp
27: 8 qQQqqp
28: 8 iiiiip
29: 8 pZpZZp
30: 8 qwwQqp
31: 7 qwWwQqp
32: 7 qwwQQqp
33: 7 qQwQqqp
34: 8 qQqqp
35: 9 pqp
"""

TRONCO = """
9: 19 QwWWwQ
10: 16 QwwWWWwwQQ
11: 14 QwwWWWWwwwQq
12: 13 QwwWWWWwwwQQq
13: 12 qwwwWWwwwwQQQq
14: 12 qwwwwwwwwQQQqq
15: 12 qQwwwwwwQQQqqqq
16: 13 qQwwwwQQQQqqpp
17: 14 qQQwwQQQQqqqp
18: 15 qQQwwwwwwQQQqq
19: 15 qQwwwWWwwwQQqq
20: 15 qQQwwwwwwQQQqp
21: 15 qppQQwwwQQQqqp
22: 15 qQQppQQQQQQqqp
23: 16 qwQQppQQQQqqp
24: 16 qppQQQppQQqqp
25: 16 qQQppQQQQqqp
26: 16 qwQQQppQQqqp
27: 16 qQQQQQQQqqp
28: 16 qqQQQQQqqpp
"""

PANO = """
29: 15 DdDdDdDdDdDdDd
30: 15 SddddSdddddSdS
31: 15 SdddSddddSdddS
32: 16 SddSdddSdddS
33: 16 SddSddSSddS
34: 17 SdS.SdSS.dS
35: 17 S....S....S
"""

PERNAS = """
35: 16 qQ
36: 16 qwQq.....qwwQq
37: 15 qwwQq....qwWwQq
38: 15 qwQqp....qwwQqp
39: 15 qQQqp....qQwQqp
40: 15 qQqp.....qQQqqp
41: 15 qQqp.....qQQqp
42: 13 qwQQqp....qwwQQqp
43: 12 qwwwQpQp..qwwwwQpQp
44: 12 pqqqqqqp..pqqqqqqqqp
"""

BRACO = """
16: 27 wwWWwwQq
17: 26 qwwWWwwwQQq
18: 27 qwwwwwQQqq
19: 28 qwwwQQQqq
20: 29 qwwQQQqp
21: 30 qwQQQqp
22: 30 qwQQqqp
23: 30 qwQQqqp
24: 30 qwwQqqp
25: 30 qwwQQqqp
26: 30 qwwwQQqqp
27: 30 qwwwQQQqp
28: 31 qwwQQQqp
29: 31 iiiiiiip
30: 31 pZpZZpZp
31: 31 qwwWWwQqp
32: 31 qwWWwwQQqp
33: 31 qwwwwQQqqp
34: 31 qQwQwQqqp
35: 32 qQqQqqp
36: 33 pqpqp
29: 39 i
30: 39 Zi
31: 41 i
32: 41 Z
33: 41 i
34: 40 iZ
35: 41 p
36: 41 i
37: 41 Z
38: 40 iZ
"""

GAIOLA = """
5: 31 yZ
6: 29 zyYyZz
7: 28 zyYYyZZz
8: 27 zyYyyZZZZz
9: 27 ZppZqqZqqz
10: 27 yppyqQyQqZ
11: 27 yppyEqyEqZ
12: 27 ZppZqqZqQz
13: 27 ZppZpwZwpz
14: 27 zZyYyZyZZz
15: 27 piipppippp
"""

BASE = BRACO_TRAS + TRONCO + PERNAS + PANO + BRACO + GAIOLA

# ---- versão B: gigante esquelético (alto, magro, braços até abaixo do joelho) ----
LEG["t"] = ("trapo", 1)
LEG["T"] = ("trapo", 2)
LEG["u"] = ("trapo", 3)

B_BRACO_TRAS = """
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
"""

B_TRONCO = """
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
"""

B_TRAPO = """
27: 18 uuuTTTtt
28: 17 tuuTTTTttt
29: 17 tuTTTtTTtt
30: 17 tTTTtTTTtt
31: 17 tTt.tTt.tt
32: 18 t...tT..t
33: 22 t
"""

B_PERNAS = """
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
"""

B_BRACO = """
14: 26 wwWw
15: 25 qwwWwQ
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
"""

B_GAIOLA = """
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
"""

BASE_B = B_BRACO_TRAS + B_TRONCO + B_PERNAS + B_TRAPO + B_BRACO + B_GAIOLA


def sh(txt, dx=0, dy=0):
    out = []
    for l in txt.strip().splitlines():
        y, resto = l.split(":", 1)
        x0, t = resto.strip().split(" ", 1) if " " in resto.strip() else (resto.strip(), "")
        out.append(f"{int(y) + dy}: {int(x0) + dx} {t}")
    return "\n" + "\n".join(out) + "\n"


# ---- variantes de braço (pancada: erguidos; bate: no chão) ----
ERGUE = """
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
"""
ERGUE_TRAS = """
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
"""
BATE = """
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
"""
BATE_TRAS = """
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
"""
F_ERGUE = sh(B_PERNAS) + sh(B_BRACO_TRAS, 0, 99) + sh(ERGUE_TRAS, 0, 1) + sh(B_TRONCO, 0, 1) + sh(B_TRAPO, 0, 1) + sh(B_GAIOLA, -1, 0) + sh(ERGUE, 0, 1)
F_BATE = sh(B_PERNAS) + sh(BATE_TRAS, 3, 6) + sh(B_TRONCO, 3, 5) + sh(B_TRAPO, 2, 3) + sh(B_GAIOLA, 5, 9) + sh(BATE, 3, 6)

ABRE = """
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
"""
ABRE_TRAS = """
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
"""
ESTENDE = """
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
"""
PERNA_TRAS = {
    "base": B_PERNAS.split("31: 23")[0],
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
}
PERNA = {
    "base": "\n31: 23" + B_PERNAS.split("31: 23")[1],
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
}
AJOELHA = """
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
"""
DEITADO = """
35: 38 zZyY
36: 36 zZyYYyZ
37: 35 zyppqqqZz
38: 35 yppqEqEqZ
39: 34 ZyZZyZZyZZz
40: 35 yppqqwqwZ
41: 35 zpppqqqZz
42: 36 zZZyZZz
37: 17 wwWWWwwww
36: 21 wWWw
38: 15 qwwwwwwWwwwwwwwQ
39: 13 qwwQQwQQwQQwQQQq
40: 12 qQQQpQQpQQpQQQQqq
41: 12 qQQQQQQQQQQQQqqq
42: 13 qqqQQQQQQQqqqp
38: 10 TuuT
39: 8 tuuTTt
40: 7 tTTTtTt
41: 7 tTtTTtt
42: 8 t.tTt
40: 3 qQQq
41: 2 qQQQqq
42: 1 qQQQQqqp
43: 2 pqqqpp
42: 30 qwwQ
43: 22 qwwwwwwwQQq
44: 17 qQwQqiiwwwQQqp
44: 31 iZiZiZ
"""
F_ABRE = sh(PERNA_TRAS["tras"]) + sh(PERNA["base"]) + sh(ABRE_TRAS, -1, 0) + sh(B_TRONCO, -1, 0) + sh(B_TRAPO, -1, 0) + sh(B_GAIOLA, -2, -1) + sh(ABRE, -1, 0)
F_ESTENDE = sh(PERNA_TRAS["tras"]) + sh(PERNA["frente"], 1, 0) + sh(B_TRONCO, 3, 2) + sh(B_TRAPO, 2, 1) + sh(B_GAIOLA, 5, 4) + sh(ESTENDE, 3, 2)
F_PASSO_A = sh(PERNA_TRAS["tras"]) + sh(PERNA["frente"]) + sh(B_BRACO_TRAS, 1, 0) + sh(B_TRONCO) + sh(B_TRAPO) + sh(B_GAIOLA) + sh(B_BRACO, -1, 0)
F_MEIO_A = sh(PERNA_TRAS["ergue"]) + sh(PERNA["base"]) + sh(B_BRACO_TRAS) + sh(B_TRONCO, 0, -1) + sh(B_TRAPO, 0, -1) + sh(B_GAIOLA, 0, -1) + sh(B_BRACO, 0, -1)
F_PASSO_B = sh(PERNA_TRAS["frente"]) + sh(PERNA["tras"]) + sh(B_BRACO_TRAS, -1, 0) + sh(B_TRONCO) + sh(B_TRAPO) + sh(B_GAIOLA) + sh(B_BRACO, 1, 0)
F_MEIO_B = sh(PERNA_TRAS["base"]) + sh(PERNA["ergue"]) + sh(B_BRACO_TRAS) + sh(B_TRONCO, 0, -1) + sh(B_TRAPO, 0, -1) + sh(B_GAIOLA, 0, -1) + sh(B_BRACO, 0, -1)
F_JOELHO = sh(AJOELHA) + sh(BATE_TRAS, 3, 7) + sh(B_TRONCO, 0, 8) + sh(B_TRAPO, 0, 8) + sh(B_GAIOLA, 2, 11) + sh(BATE, 0, 7)
