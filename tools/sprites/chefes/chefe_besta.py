"""CHEFE 1, fase besta — o caçador da Igreja Branca virado besta, direção sépia e ouro. (2ª rodada, refeito do zero)

BRIEF
- Fase 2 do chefe (abaixo de 50% de vida): garras em combo de 3, investida de 120 px e salto.
  Rápida (velocidade 2,0): a corrida é a animação de perseguição.
- Escala: 64×64, origem (32, 60); figura de 55 px: curvada, braços que passam do quadril,
  pernas digitígradas (joelho pra frente, jarrete pra trás).
- Gancho: o CRÂNIO de osso no lugar do focinho (osso exposto, dentes à mostra, olho aceso no
  buraco) + a corcunda com a crina em espinhos. Traços: orelhas varridas pra trás, garras de
  marfim, os restos do manto branco nas costas e a faixa vermelha ainda na cintura.
- Família de cor: pelosangue (pelo preto-avermelhado) + marfim (osso); o branco do manto e o
  vermelho da faixa ligam a besta ao caçador da Igreja Branca. O crânio é a massa mais clara
  (o olho cai nele primeiro). Nada da besta antiga (pelo cinza-marfim, focinho de pelo).
- Animações: idle 4, corrida 6 (contato, passagem e voo de cada perna), garra 3 (windup com a
  garra armada atrás da cabeça; ativo: bote com a garra embaixo e à frente), investida 3,
  salto 3 (agacha / no ar / pouso), stagger 2, caído 2 (de quatro), morte 8 (cai de joelhos,
  tomba, os olhos apagam). Transformação 8: o humano larga o machado, o manto incha, a crina
  rompe, o crânio cresce, RUGE no quadro 5 e termina igual ao idle 0.
- Pintado à mão na bancada chefe_besta_pinta.py. Sem sombreamento automático.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import paleta as P  # noqa: E402
from kit.boneco import Boneco  # noqa: E402
from kit.tela import Tela, de_segmentos  # noqa: E402

W = H = 64
LEG = {
    "o": ("contorno", 0),
    "0": ("pelosangue", 0), "1": ("pelosangue", 1), "2": ("pelosangue", 2), "3": ("pelosangue", 3),
    "4": ("pelosangue", 4), "5": ("pelosangue", 5),
    "w": ("marfim", 0), "W": ("marfim", 1), "V": ("marfim", 2),
    "e": ("olho", 1), "E": ("olho", 0),
    "A": ("alvo", 1), "b": ("alvo", 2), "B": ("alvo", 3),
    "x": ("sangue", 1), "X": ("sangue", 2),
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


def _so(txt, de=0, ate=99):
    return "\n" + "\n".join(l for l in txt.strip().splitlines() if de <= int(l.split(":")[0]) <= ate) + "\n"


BRACO_TRAS = """
28: 19 1210
29: 18 12210
30: 18 12110
31: 18 1211
32: 18 1210
33: 17 1210
34: 17 1210
35: 17 1210
36: 17 1110
37: 17 1110
38: 17 1100
39: 16 11100
40: 16 12110
41: 15 121100
42: 15 1211100
43: 15 0111100
44: 16 VW.VW.W
45: 17 VW.VW.W
46: 18 W..W
"""
PERNA_TRAS = """
38: 21 11110
39: 21 121110
40: 21 1221110
41: 22 1221110
42: 23 122110
43: 24 12110
44: 25 1211
45: 26 1211
46: 26 1110
47: 25 1110
48: 24 110
49: 23 110
50: 22 110
51: 22 110
52: 22 110
53: 22 110
54: 23 110
55: 23 1110
56: 23 11110
57: 23 111110
58: 23 1111100
59: 24 W.W.W
"""
PERNA = """
38: 28 2222211
39: 28 23332111
40: 28 233322111
41: 29 23332211
42: 30 2333211
43: 31 233211
44: 32 23321
45: 33 23321
46: 34 22321
47: 34 22211
48: 33 2211
49: 32 2211
50: 31 2211
51: 30 2211
52: 30 2211
53: 30 2211
54: 31 2211
55: 31 22211
56: 31 222211
57: 31 2232211
58: 31 22222211
59: 32 VW.VW.VW
"""
TRONCO = """
11: 28 43
12: 27 4332
13: 26 43322
14: 25 3433221
15: 24 43332210
16: 23 344332210
17: 22 4333332210
18: 21 34433322110
19: 20 4333332221100
20: 19 43333322221110
21: 19 333332222111100
22: 18 4333322221111100
23: 18 33332222111110000
24: 17 433322221111100000
25: 17 333322211110000000
26: 17 333222110011000000
27: 17 332221100111000000
28: 17 33222111001100000
29: 17 3222110011100000
30: 17 3222111100100000
31: 18 222110011000000
32: 18 22211110100000
33: 18 2221111000000
34: 19 221111000000
35: 19 22111100000
36: 20 2111100000
37: 21 111100000
38: 22 11110000
"""
ESPINHOS = """
9: 31 4
10: 30 43
12: 25 4
13: 24 43
15: 21 4
16: 20 43
19: 17 4
20: 16 43
23: 15 4
24: 14 43
28: 15 3
29: 15 2
"""
TRAPOS = """
17: 27 BB
18: 25 BBBb
19: 23 BBBbbA
20: 22 BBbbbA
21: 21 BBbbAA
22: 20 BBbbA
23: 20 BbbAA
24: 19 BbbA
25: 19 BbAA
26: 19 BbA
27: 19 bbA
28: 19 bA.A
29: 19 bA
30: 20 A
36: 21 xXXXXxxxxxxxxx
37: 21 xXXXXXxxxxxxxx
38: 22 xXx
39: 22 xXx
40: 22 xx
41: 23 x
"""
CAB = """
5: 35 4
6: 31 3
6: 35 43
7: 31 32
7: 35 4301
8: 32 321
8: 36 43011
9: 33 3211
9: 36 443011
10: 34 33221
10: 37 4330111
11: 35 3322211111
12: 35 33322221wWVW
13: 36 3332221wVVVVVVW
14: 36 33221110wVVVVVVVW
15: 37 3221100eWVVVVVVWw
16: 38 22110w0WWVVVVVW0
17: 39 2110wwWWWWWWWw0
18: 40 110wwwWWWWWWw
19: 42 VVoVVVoVVVo
20: 42 00000000000
21: 42 VVoVVoVVw
22: 42 wWWWWWww
23: 43 0wwww
"""
BRACO = """
19: 35 4332
20: 34 443322
21: 34 4333221
22: 34 33332210
23: 35 3332210
24: 35 3322110
25: 36 322110
26: 36 322110
27: 37 22110
28: 37 22110
29: 38 2210
30: 38 22110
31: 38 232110
32: 39 23210
33: 39 23210
34: 40 2310
35: 40 2310
36: 40 2210
37: 41 2210
38: 41 2210
39: 41 22110
40: 40 232110
41: 39 2332110
42: 39 23322110
43: 39 12221100
44: 40 VW.VW.VW
45: 41 VW.VW.VW
46: 42 W..W..W
"""

# rugido: a cabeça sobe e a mandíbula despenca (a boca aberta mostra os dentes)
CAB_RUGE = (_sh(_so(CAB, 0, 19), -1, -2) + """
17: 42 000000000
18: 42 0000000000
19: 43 000000000
20: 43 0X00000
21: 44 V0V00V0V
""" + _sh(_so(CAB, 21, 23), -1, 2))
# cabeça baixa (zonzo, caída): o crânio desce e o olho se apaga
CAB_BAIXA = _sh(CAB.replace("eW", "0W"), 2, 3)

# garra armada atrás da cabeça (windup)
BRACO_ERGUE = """
22: 34 44443321
21: 34 4444332
20: 34 443322
19: 33 44332
18: 32 4332
17: 31 4332
16: 30 4332
15: 30 4321
14: 29 4321
13: 29 4321
12: 28 4321
11: 28 3321
10: 27 34321
9: 26 344321
8: 25 3443211
7: 25 V.V.V
6: 24 W.W.W
5: 24 V..V
23: 35 3332210
24: 35 3322110
25: 36 322110
"""
# garra embaixo e à frente (ativo do golpe, investida)
BRACO_GOLPE = """
19: 35 4332
20: 34 443322
21: 34 4433221
22: 35 4433221
23: 36 443321
24: 37 443321
25: 38 43321
26: 39 43321
27: 40 433210
28: 41 433210
29: 42 43321
30: 43 43321
31: 44 43321
32: 45 4332
33: 45 43321
34: 45 344321
35: 45 3443321
36: 46 VW.VW.VW
37: 47 VW.VW.VW
38: 48 W..W..W
"""
BRACO_TRAS_ERGUE = """
24: 22 1210
23: 21 1210
22: 20 1210
21: 19 1210
20: 18 1210
19: 17 1210
18: 16 1210
17: 15 1210
16: 14 12110
15: 13 121100
14: 12 1211000
13: 12 V.V.V
12: 11 W.W.W
11: 11 V..V
"""


def _passo(txt, dx, dy=0):
    """Inclina a perna: cada linha anda proporcional à distância do quadril (0 no quadril, dx na
    pata), então a perna não quebra; dy < 0 ergue a perna inteira (o alto some sob o tronco)."""
    out = []
    for lin in txt.strip().splitlines():
        y, resto = lin.split(":", 1)
        x0, t = resto.strip().split(" ", 1)
        y, x0 = int(y), int(x0)
        k = max(0, y - 38) / 21
        out.append(f"{y + dy}: {x0 + round(dx * k)} {t}")
    return "\n" + "\n".join(out) + "\n"


# de quatro (caído): as coxas dobradas, os joelhos no chão, as canelas deitadas pra trás
AJOELHA = """
50: 22 111110
51: 21 1222110
52: 21 12221100
53: 20 122211000
54: 18 11122211000
55: 15 1111111110000
56: 13 11111111100000
57: 13 1111111100000
58: 13 W.W.W00000
50: 30 2222211
51: 29 23332111
52: 29 233322111
53: 29 233322211
54: 27 2223332211
55: 24 222222222211
56: 22 2222222222211
57: 22 222222222111
58: 22 VW.VW.V1111
"""

PECAS = {
    "cab": {"normal": CAB, "ruge": CAB_RUGE, "baixa": CAB_BAIXA},
    "tronco": {"normal": TRONCO},
    "espinhos": {"normal": ESPINHOS},
    "trapos": {"normal": TRAPOS},
    "braco": {"pende": BRACO, "ergue": BRACO_ERGUE, "golpe": BRACO_GOLPE},
    "braco_tras": {"pende": BRACO_TRAS, "ergue": BRACO_TRAS_ERGUE},
    "perna_tras": {"base": PERNA_TRAS, "tras": _passo(PERNA_TRAS, -7, -2), "frente": _passo(PERNA_TRAS, 7),
                   "ergue": _passo(PERNA_TRAS, 3, -6), "ar": _sh(_passo(PERNA_TRAS, -4, -3), 0, -6),
                   "estica": _passo(PERNA_TRAS, -9, -3)},
    "perna": {"base": PERNA, "tras": _passo(PERNA, -8, -2), "frente": _passo(PERNA, 7),
              "ergue": _passo(PERNA, 2, -6), "ar": _sh(_passo(PERNA, -3, -4), 0, -6),
              "estica": _passo(PERNA, -6, -2), "ajoelha": AJOELHA},
}

ORDEM = ["braco_tras", "perna_tras", "perna", "tronco", "espinhos", "trapos", "cab", "braco", "remendos"]
PADRAO = {"cab": ("normal", 0, 0), "tronco": ("normal", 0, 0), "espinhos": ("normal", 0, 0),
          "trapos": ("normal", 0, 0), "braco": ("pende", 0, 0), "braco_tras": ("pende", 0, 0),
          "perna_tras": ("base", 0, 0), "perna": ("base", 0, 0)}
B = Boneco(W, H, P.RAMPAS, LEG, PECAS, ORDEM,
           rel={"cab", "tronco", "espinhos", "trapos", "braco", "braco_tras"}, padrao=PADRAO)


def _p(**k):
    return k


IDLE = [
    _p(),
    _p(y=1, braco=("pende", 0, 0)),
    _p(y=1, cab=("normal", 1, 0)),
    _p(braco=("pende", 0, 1), braco_tras=("pende", 0, 1)),
]
# corrida inclinada: contato, passagem e voo de cada perna; os braços contra as pernas
CORRIDA = [
    _p(x=3, y=2, perna=("frente", 2, 0), perna_tras=("tras", 0, 0), braco=("pende", -2, 0), braco_tras=("pende", 2, 0)),
    _p(x=3, y=1, perna=("base", 1, -1), perna_tras=("ergue", 0, 0)),
    _p(x=3, y=0, perna=("tras", 0, -2), perna_tras=("ergue", 2, -2), cab=("normal", 0, -1)),
    _p(x=3, y=2, perna=("tras", 0, 0), perna_tras=("frente", 2, 0), braco=("pende", 2, 0), braco_tras=("pende", -2, 0)),
    _p(x=3, y=1, perna=("ergue", 0, 0), perna_tras=("base", 1, -1)),
    _p(x=3, y=0, perna=("ergue", 2, -2), perna_tras=("tras", 0, -2), cab=("normal", 0, -1)),
]
GARRA = [
    _p(x=-2, cab=("normal", -1, -1), braco=("ergue", 0, 0), perna_tras=("tras", 0, 0)),
    # bote: o corpo voa pra frente com a garra embaixo (a sola sai da linha)
    _p(x=4, y=1, cab=("normal", 1, 2), braco=("golpe", 0, 0), perna=("frente", 0, -2), perna_tras=("estica", 0, -1)),
    _p(x=3, y=2, cab=("normal", 1, 2), braco=("golpe", 0, 2), perna=("frente", 0, 0), perna_tras=("tras", 0, 0)),
]
INVESTIDA = [
    _p(x=-3, y=4, cab=("normal", 0, 1), braco=("pende", 1, -2), braco_tras=("pende", 1, -2), perna=("base", 0, 0),
       perna_tras=("tras", 0, 0)),
    _p(x=6, y=3, cab=("normal", 2, 3), braco=("golpe", -2, -3), perna=("estica", 0, -2), perna_tras=("estica", 0, -3)),
    _p(x=3, y=2, cab=("normal", 1, 2), braco=("golpe", -1, 1), perna=("frente", 0, 0), perna_tras=("tras", 0, 0)),
]
SALTO = [
    _p(y=6, cab=("normal", 1, 1), braco=("pende", 1, -3), braco_tras=("pende", 1, -3), perna=("base", 0, 0)),
    _p(y=-2, cab=("normal", 0, -1), braco=("ergue", 0, 0), braco_tras=("ergue", 0, 0), perna=("ar", 0, 0),
       perna_tras=("ar", 0, 0)),
    _p(x=2, y=6, cab=("normal", 1, 2), braco=("golpe", -2, 6), perna=("frente", 0, 0), perna_tras=("tras", 0, 0)),
]
STAGGER = [
    _p(x=-3, y=2, cab=("baixa", -1, 0), braco=("pende", 2, 0), braco_tras=("pende", 2, 0), perna_tras=("tras", 0, 0)),
    _p(x=-2, y=3, cab=("baixa", 0, 1), braco=("pende", 1, 0), braco_tras=("pende", 1, 0)),
]
# de quatro: a garra da frente apoiada no chão
_QUATRO = dict(y=12, perna_tras=None, perna=("ajoelha", 0, 0), braco=("golpe", -4, 9), braco_tras=("pende", 4, 2))
CAIDO = [
    _p(cab=("baixa", 0, 0), **_QUATRO),
    _p(cab=("normal", 1, 1), **_QUATRO),
]

# deitada de lado, o crânio à direita (pintada inteira)
DEITADA = """
44: 47 VVW
45: 44 wVVVVVW
46: 42 wwVVVVVVVW
47: 41 1w00VVVVVVW
48: 40 21we0WVVVVVV
49: 39 2210wWWWWWWW0
50: 38 22110wwWWWWWw
51: 39 110VVoVVoVVo
52: 40 1000000000
53: 40 0wVVoVVoVw
45: 35 4
46: 33 43
47: 30 4.4433
48: 26 4433443321
49: 22 44333333332211
50: 18 433333222222221110
51: 15 433322222222222111100
52: 13 4322222BBbbA2221111100
53: 11 432222BBbbbbA22111111000
54: 10 3222222BbbAA2222111110000
55: 9 32222221xXXXxx221111100000
56: 8 222222111xxxxx1111110000
57: 8 2221110111111110000000VW.VW
58: 9 W.W.W0000000000000VW.VW.V
59: 10 W.W.........W.W.W
"""
DEITADA_APAGA = DEITADA.replace("21we0W", "21w00W")


def deitada(apaga=False):
    t = Tela(W, H, P.RAMPAS)
    de_segmentos(DEITADA_APAGA if apaga else DEITADA, LEG, P.RAMPAS, W, H, tela=t)
    t.contorno(("contorno", 0))
    return t


MORTE = [
    STAGGER[0],
    _p(cab=("normal", 0, -1), **_QUATRO),
    _p(cab=("baixa", 0, 1), **_QUATRO),
    _p(x=4, y=16, perna_tras=None, perna=("ajoelha", -2, -4), cab=("baixa", 2, 2), braco=("golpe", -6, 6),
       braco_tras=("pende", 4, -2)),
    {"deitada": 0},
    {"deitada": 0},
    {"deitada": 1},
    {"deitada": 1},
]

ANIMS = {
    "idle": (IDLE, 180),
    "corrida": (CORRIDA, 90),
    "garra": (GARRA, 140),
    "investida": (INVESTIDA, 160),
    "salto": (SALTO, 200),
    "stagger": (STAGGER, 150),
    "caido": (CAIDO, 300),
    "morte": (MORTE, 140),
}


def montar(p):
    if "deitada" in p:
        return deitada(p["deitada"] == 1)
    return B.montar(p)


def quadros(nome):
    return [montar(p).imagem() for p in ANIMS[nome][0]]


# ---------------------------------------------------------------- transformação
def transforma():
    """8 quadros 64×64: o humano (48×48, mesma sola) vira a besta; termina no idle 0 da besta.
    0 em pé com o machado · 1 larga o machado e curva · 2 o manto incha e a crina rompe ·
    3 o crânio sai do capuz, garras · 4 levanta já besta, manto em tiras · 5 RUGE (frame 57 do
    código) · 6 assenta · 7 = idle 0 da besta."""
    from PIL import Image
    from armas import armas
    from chefes import chefe_humano as ch

    def no64(img48, dx=0, dy=0):
        c = Image.new("RGBA", (64, 64))
        c.alpha_composite(img48, (8 + dx, 15 + dy))
        return c

    def carimbo(texto, contorno=True):
        t = Tela(64, 64, P.RAMPAS)
        de_segmentos(texto, LEG, P.RAMPAS, 64, 64, tela=t)
        if contorno:
            t.contorno(("contorno", 0))
        return t.imagem()

    ax = armas.imagem("spr_arma_machado")
    ox, oy = armas.origem("spr_arma_machado")

    def machado_na_mao(img):
        # cabo na mão (28, 33) do humano = (36, 48) aqui; 30° horário: a cabeça do machado
        # apoiada no chão (a -40° do idle do código ela sairia pela borda de baixo)
        r = ax.rotate(-30, resample=Image.NEAREST, expand=True)
        dx, dy = ox - ax.width / 2, oy - ax.height / 2     # cabo em relação ao centro
        cx = r.width // 2 + round(dx * 0.866 - dy * 0.5)
        cy = r.height // 2 + round(dx * 0.5 + dy * 0.866)
        b = Image.new("RGBA", (64, 64))
        b.alpha_composite(img)
        b.alpha_composite(r, (max(0, 36 - cx), max(0, 48 - cy)))
        return b

    def machado_no_chao(img):
        b = Image.new("RGBA", (64, 64))
        b.alpha_composite(ax, (36, 59 - ax.height + 3))
        b.alpha_composite(img)
        return b

    hum = ch.quadros("idle")[0]
    zonzo = ch.quadros("stagger")
    out = [machado_na_mao(no64(hum))]
    out.append(machado_no_chao(no64(zonzo[1])))
    # 2: o manto incha por trás e a crina rompe; garras nas mãos
    # (a crina rompe atrás do ombro esquerdo do manto, por trás do capuz)
    crina = carimbo("""
25: 22 4
26: 19 4.43
27: 17 4.4333
28: 16 433333.4
29: 15 4333333332
30: 14 433333332211
31: 14 3333333222111
32: 15 33333222211
33: 16 3322221
""")
    f2 = crina.copy()
    f2.alpha_composite(no64(zonzo[1], 0, 1))
    f2.alpha_composite(carimbo("""
54: 34 VW.V
55: 35 W..W
"""))
    out.append(machado_no_chao(f2))
    # 3: o corpo já é da besta, agachado; o capuz rasgado ainda nas costas
    f3 = B.montar(_p(y=8, cab=("baixa", 0, 0), braco=("pende", 0, -4), braco_tras=("pende", 0, -4),
                     perna=("base", 0, 0))).imagem()
    f3.alpha_composite(carimbo("""
18: 28 Bb
19: 27 BBbA
20: 26 BBBbA
21: 25 BBbbAA
22: 25 BbbAA
"""))
    out.append(machado_no_chao(f3))
    out.append(B.montar(_p(y=4, cab=("normal", 0, 1), braco=("pende", 0, -2), braco_tras=("pende", 0, -2))).imagem())
    out.append(B.montar(_p(y=1, cab=("ruge", 0, 0), braco=("ergue", 0, 2), braco_tras=("ergue", 0, 2))).imagem())
    out.append(B.montar(_p(y=2, cab=("normal", 0, 1))).imagem())
    out.append(quadros("idle")[0])
    return out


AUDITORIA = {
    "nos_1px": "pontas da crina, das orelhas e das garras",
    "furos_1px": "vãos entre as garras e entre os dentes",
    "pixel_solto": "olho aceso, dentes, pontas da crina",
    "pontilhado": "dentes e garras alternam marfim e vão",
    "aglomerados": "pelo e crina: borda serrilhada de propósito",
    "teto_cores": "deitada: a altura baixa derruba o teto do tier",
    "direcao": "quadros deitados",
}


if __name__ == "__main__":
    from kit import previa as pv
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "previa")
    linhas = [(n, quadros(n)) for n in ANIMS] + [("transforma", transforma())]
    pv.folha(linhas, k=3, larg_rotulo=90, titulo="besta (2ª rodada)").save(os.path.join(out, "chefe_besta_folha.png"))
    print("ok")
