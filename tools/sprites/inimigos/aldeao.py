"""ALDEÃO — inimigo comum (fodder), Nightmoon, direção sépia e ouro. (2ª rodada, refeito do zero)

BRIEF
- Morador que virou besta, da turba de tochas de Yharnam. Aparece em grupos de 2-3; ataca com
  a foice (sprite separado, girado pelo código a partir da mão em (19, 20): mao_x=3, mao_y=10).
- Escala: 32×32, origem (16, 30); figura de 28 px com a tocha (o corpo curvado tem 20).
- Gancho: a TOCHA acesa erguida na mão de trás + corcunda com a cabeça à frente. Traços: boina
  de aba curta (ardósia), rosto cinza-esverdeado com o olho vermelho na sombra da aba, cachecol
  vinho; colete de couro sobre camisa de linho, calça de ardósia, pés enrolados em pano.
- Família de cor: linho sujo + ardósia + pele doente; acentos: a chama (o ponto mais claro) e o
  olho vermelho. Nada a ver com o caçador (escuro quente e ouro) nem com o antigo (capuz de saco
  e bata oliva).
- Valores: massa escura no colete e na calça, plano de luz no rosto e na camisa, a chama como o
  único branco. 20 cores (o teto do tier).
- Animações: idle 4 (a chama tremula), walk 6 (contato, descida e passagem de cada perna, a
  tocha balança), ataque 3 (windup: empina e puxa a tocha pra trás — silhueta alta pro flash;
  ativo: mergulha), hit 2, stagger 2 (a tocha cai), caído 2, morte 6 (a chama apaga no chão).
- Pintado à mão (bancada `aldeao_pinta.py`): carimbos por peça (tocha, braço da tocha, cabeça,
  tronco, braço da foice, pernas por passo). Sem sombreamento automático.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import paleta as P  # noqa: E402
from kit.boneco import Boneco  # noqa: E402

LEG = {
    "o": ("contorno", 0),
    "b": ("ardosia", 1), "B": ("ardosia", 2), "n": ("ardosia", 3),
    "k": ("doente", 0), "K": ("doente", 1), "L": ("doente", 2), "l": ("doente", 3),
    "E": ("olho", 0),
    "r": ("forro", 0), "R": ("forro", 1),
    "v": ("couro", 1), "V": ("couro", 2), "u": ("couro", 3),
    "2": ("linho", 1), "3": ("linho", 2), "4": ("linho", 3),
    "C": ("chama", 1), "a": ("chama", 2), "A": ("chama", 3),
}

PECAS = {
    "chama": {
        "f0": "2: 8 a\n3: 7 aA\n4: 7 aAa\n5: 6 CaAaC\n6: 6 CaAAC",
        "f1": "2: 9 a\n3: 8 aA\n4: 7 aAAa\n5: 6 CaAaC\n6: 6 CaAAC",
        "f2": "3: 7 a.a\n4: 7 aAaC\n5: 6 CaAAa\n6: 6 CaAAC",
        # tocha caída: a chama sobe da ponta de baixo do cabo
        "baixa0": "18: 4 a\n19: 3 aAa\n20: 3 CAaC\n21: 4 CaC",
        "baixa1": "18: 5 a\n19: 4 aA\n20: 3 CaAa\n21: 4 CaC",
    },
    "braco_tras": {
        "ergue": """
7: 7 CVC
8: 8 uV
9: 8 uV
10: 7 KLL
11: 7 kKKk
12: 9 KK
13: 10 33
14: 11 2
""",
        # tocha caída (stagger, morte): o braço pende e o cabo aponta pra trás e pra baixo
        "baixo": """
14: 11 2
15: 10 33
16: 10 KK
17: 9 kKK
18: 8 KLLk
19: 7 uVk
20: 6 uV
21: 5 VCV
""",
    },
    "cab": {
        "normal": """
10: 18 nnnBB
11: 17 nnBBBBBb
12: 17 bBBBBbbbb
13: 17 bKKkEkK
14: 17 bkLlLLLK
15: 18 kKLKoK
16: 19 kKKk
""",
        # olhando pra cima (windup, dano): a aba levanta, o rosto aparece, a boca abre
        "tras": """
9: 17 nnnBB
10: 16 nnBBBBBb
11: 16 bBBBBbbbb
12: 17 bKLLkEK
13: 17 bkLlLLLK
14: 18 kKLooK
15: 19 kKoK
16: 20 kk
""",
        # cabeça pendendo (zonzo): a aba cobre o olho
        "baixa": """
12: 19 nnnBB
13: 18 nnBBBBBb
14: 18 bBBBBbbbb
15: 18 bKKkkkK
16: 18 bkLlLLK
17: 19 kKLoK
18: 20 kk
""",
    },
    "tronco": {
        "normal": """
11: 13 uV
12: 12 uuV
13: 12 uVVV
14: 12 uVVVV
15: 12 vVVVVV
16: 12 vVVrRRr
17: 12 vVrRRR
18: 12 vV44Rr
19: 12 vV4332
20: 12 vv3322
21: 13 v2222
""",
        # empinado (windup, dano): as costas sobem, o peito abre
        "empina": """
10: 13 uV
11: 12 uuV
12: 12 uVVV
13: 12 uVVVV
14: 12 vVVVVV
15: 12 vVVrRRr
16: 12 vVrRRR
17: 12 vV44Rr
18: 12 vV4432
19: 12 vV4332
20: 12 vv3322
21: 13 v2222
""",
    },
    "braco": {
        "normal": "17: 18 43\n18: 18 43\n19: 18 2LK\n20: 18 2KL\n21: 19 kk",
        # corpo recuado (x -1/-2): o braço estica até a mão, que não sai do lugar
        "longo": "17: 16 443\n18: 17 433\n19: 18 2LK\n20: 18 2KL\n21: 19 kk",
        # corpo baixo (zonzo): o ombro desce, a mão continua em (19, 20)
        "zonzo": "18: 17 43\n19: 18 43\n20: 18 2KL\n21: 19 KL\n22: 19 kk",
    },
    # pernas: parado + contato e passagem de cada perna (a perna de perto é a clara)
    "pernas": {
        "base": """
22: 13 bBBBnBBb
23: 13 bBBbBBnBb
24: 13 bBb.bBnBb
25: 12 bBb...BnB
26: 12 bB....bBb
27: 12 kK.....KK
28: 12 k23....K34
29: 12 2233...3344
""",
        "passo_a": """
22: 13 bBBBnBBb
23: 12 bBBb.BBnBb
24: 11 bBb....bBnBb
25: 10 bBb......BnBb
26: 9 bB.........bBb
27: 8 kK...........KK
28: 8 k23..........K34
29: 8 2233.........3344
""",
        "passo_b": """
22: 13 bBBBnBBb
23: 13 BnBBbbBb
24: 12 BnBb...bBb
25: 11 BnB......bBb
26: 10 bBb.......bB
27: 10 KK........kK
28: 10 K34.......k23
29: 10 3344......2233
""",
        "meio_a": """
22: 13 bBBBnBBb
23: 13 bBBbBnBb
24: 13 bBBbBnB
25: 14 bBbBnB
26: 13 kKb.bBb
27: 12 k23..KK
28: 12 2233.K34
29: 17 3344
""",
        "meio_b": """
22: 13 bBBBnBBb
23: 13 bBBbBBnBb
24: 13 bBb.bBnBb
25: 14 bBb..BnBb
26: 14 bB...bBb
27: 14 kK...K34
28: 14 k23..3344
29: 14 2233
""",
    },
}

ORDEM = ["braco_tras", "chama", "pernas", "tronco", "cab", "braco", "remendos"]
PADRAO = {"chama": ("f0", 0, 0), "braco_tras": ("ergue", 0, 0), "cab": ("normal", 0, 0),
          "tronco": ("normal", 0, 0), "braco": ("normal", 0, 0), "pernas": ("base", 0, 0)}
B = Boneco(32, 32, P.RAMPAS, LEG, PECAS, ORDEM, rel={"chama", "braco_tras", "cab", "tronco"}, padrao=PADRAO)


def _p(**k):
    return k


IDLE = [
    _p(),
    _p(chama=("f1", 0, 0), tronco=("normal", 0, 1), braco_tras=("ergue", 0, 1), cab=("normal", 0, 1)),
    _p(chama=("f2", 0, 1), tronco=("normal", 0, 1), braco_tras=("ergue", 0, 1), cab=("normal", 0, 1)),
    _p(chama=("f1", 0, 0), cab=("normal", 1, 0)),           # tique: a cabeça dá um tranco pra frente
]

# contato, descida, passagem (a tocha atrasa um quadro em relação ao corpo)
WALK = [
    _p(pernas=("passo_a", 0, 0), chama=("f0", 0, 0)),
    _p(y=1, pernas=("passo_a", 0, 0), chama=("f1", -1, 0), braco_tras=("ergue", -1, 0)),
    _p(pernas=("meio_a", 0, 0), chama=("f2", -1, 0), braco_tras=("ergue", -1, 0), cab=("normal", 0, -1)),
    _p(pernas=("passo_b", 0, 0), chama=("f0", 0, 0)),
    _p(y=1, pernas=("passo_b", 0, 0), chama=("f1", 1, 0), braco_tras=("ergue", 1, 0)),
    _p(pernas=("meio_b", 0, 0), chama=("f2", 1, 0), braco_tras=("ergue", 1, 0), cab=("normal", 0, -1)),
]

ATAQUE = [
    # windup: empina, olha pra cima, puxa a tocha pra trás (silhueta alta e larga no flash)
    _p(x=-1, tronco=("empina", 0, 0), cab=("tras", 0, 0), braco_tras=("ergue", -2, 0), chama=("f1", -2, 0),
       braco=("longo", 0, 0), pernas=("passo_b", 0, 0)),
    # ativo: mergulha pra frente com a cabeça baixa
    _p(x=2, y=1, cab=("normal", 1, 1), braco_tras=("ergue", 1, 1), chama=("f2", 1, 1), pernas=("passo_a", 0, 0)),
    _p(x=1, pernas=("base", 0, 0), chama=("f0", 0, 0)),
]

HIT = [
    _p(x=-2, tronco=("empina", 0, 0), cab=("tras", -1, 0), braco_tras=("ergue", -2, 0), chama=("f2", -2, 0),
       braco=("longo", 0, 0), pernas=("passo_b", 0, 0)),
    _p(x=-1, y=1, chama=("f1", -1, 0), braco_tras=("ergue", -1, 0), braco=("longo", 0, 0)),
]

STAGGER = [
    _p(y=2, cab=("baixa", 0, 0), braco_tras=("baixo", 0, 0), chama=("baixa0", 0, 0), braco=("zonzo", 0, 0),
       pernas=("meio_b", 0, 0)),
    _p(y=2, x=1, cab=("baixa", 0, 1), braco_tras=("baixo", 0, 0), chama=("baixa1", 0, 0), braco=("zonzo", 0, 0),
       pernas=("meio_b", 0, 0)),
]

# no chão (caído e morte), pintado à mão: deitado de lado, cabeça à direita, tocha no chão
CHAO = """
23: 21 nnnBB
24: 11 uuuVV....nnBBBBb
25: 6 bBBbuVVVVVVVVbBBBBbbb
26: 4 bBBBnBvVVVrRRRrbKKkEkK
27: 3 kbBBnBBv4433322bkLlLLLK
28: 2 k23bBb.v3322222.kKLKoK
29: 2 2233....vvvvvv...kKKk
"""
CHAO_ERGUE = """
22: 21 nnnBB
23: 20 nnBBBBb
24: 11 uuuVV...bBBBBbbbb
25: 6 bBBbuVVVVVVVbKKkEkK
26: 4 bBBBnBvVVVrRRRrbkLlLLLK
27: 3 kbBBnBBv4433322.kKLKoK
28: 2 k23bBb.v3322222KLkKKk
29: 2 2233....vvvvvv.kk
"""
# a tocha cai atrás do corpo (era a mão de trás), com a ponta acesa pra esquerda
TOCHA_CHAO = {
    "acesa": """
19: 3 a
20: 2 aAa
21: 2 CaAC
22: 2 CaCuVVV
""",
    "fraca": """
21: 3 a
22: 2 CaCuVVV
""",
    "brasa": "\n22: 3 CCuVVV\n",
    "apagada": "\n22: 3 vvuVVV\n",
}
CAIDO = [
    {"quadro": CHAO + TOCHA_CHAO["acesa"]},
    {"quadro": CHAO_ERGUE + TOCHA_CHAO["fraca"]},
]
MORTE = [
    _p(x=-2, tronco=("empina", 0, 0), cab=("tras", -1, 0), braco_tras=("ergue", -2, 0), chama=("f2", -2, 0),
       braco=None, pernas=("passo_b", 0, 0)),
    _p(y=3, cab=("baixa", 0, 0), braco_tras=("baixo", 0, -1), chama=("baixa0", 0, -1), braco=None,
       pernas=("meio_b", 0, 0)),
    _p(y=6, cab=("baixa", 1, 0), braco_tras=None, chama=None, braco=None, pernas=("base", 0, 0),
       remendos=[TOCHA_CHAO["acesa"]]),
    {"quadro": CHAO + TOCHA_CHAO["acesa"]},
    {"quadro": CHAO + TOCHA_CHAO["brasa"]},
    {"quadro": CHAO + TOCHA_CHAO["apagada"]},
]

ANIMS = {
    "idle": (IDLE, 170),
    "walk": (WALK, 110),
    "ataque": (ATAQUE, 180),
    "hit": (HIT, 120),
    "stagger": (STAGGER, 160),
    "caido": (CAIDO, 300),
    "morte": (MORTE, 110),
}


def quadros(nome):
    return [B.montar(p).imagem() for p in ANIMS[nome][0]]


AUDITORIA = {
    "pixel_solto": "olho vermelho (1 px), boca, ponta da chama",
    "nos_1px": "ponta da chama e do cabo da tocha",
    "furos_1px": "vão entre as pernas e entre a chama e o cabo",
    "aglomerados": "chama e rosto concentram o detalhe pequeno (ponto de interesse)",
    "direcao": "quadros deitados",
    "teto_cores": "deitado: a altura baixa derruba o teto do tier",
}


if __name__ == "__main__":
    from kit import previa as pv
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "previa")
    linhas = [(n, quadros(n)) for n in ANIMS]
    pv.folha(linhas, k=5, larg_rotulo=90, titulo="aldeão (2ª rodada)").save(os.path.join(out, "aldeao_folha.png"))
    print("ok")
