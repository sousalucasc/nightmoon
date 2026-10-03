"""TILESET da rua (spr_tiles_rua, 128×96 = 8×6 tiles de 16) — direção sépia e ouro.

Os 48 lugares (e os nomes) são o contrato com o Apêndice A (dia 18): o dono pinta as rooms à
mão seguindo os guias, e a tabela de regras cita os tiles pelo nome. O desenho é todo novo:
- chão: paralelepípedo em fiadas desencontradas (pedras miúdas, quinas arredondadas, luz de
  cima-esquerda), mais claro e neutro que os personagens pra eles saltarem do chão;
- calçada de lajes grandes; meio-fio de granito com a face escura caindo pra rua;
- muro: blocos de pedra escura com a FACE em fiadas e um friso de pedra clara embaixo; a janela
  ogival acesa em âmbar é o acento do cenário; topo do muro com a borda clara do lado de dentro;
- detalhes com fundo transparente (sombra do muro e poça com alfa parcial de propósito).

Regras de cenário (conhecimento/13): contraste e saturação menores que os das sprites, mesma
luz, emenda sem costura (as 4 pedras compartilham as juntas das bordas, então misturam em
qualquer ordem), repetição quebrada pelos detalhes.
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import paleta as P  # noqa: E402
from PIL import Image  # noqa: E402

T = 16
R = P.RAMPAS


def nova(fundo=None):
    im = Image.new("RGBA", (T, T), (0, 0, 0, 0) if fundo is None else tuple(fundo) + (255,))
    return im


def put(im, x, y, cor, a=255):
    if 0 <= x < T and 0 <= y < T:
        im.putpixel((x, y), tuple(cor[:3]) + (a,))


# ------------------------------------------------------------------ chão ------
# Chão de LAJES de pedra gasta: uma laje grande por tile (ou duas, nas variantes 2 e 4), junta
# fina e de pouco contraste na direita e embaixo, bisel de luz em cima e à esquerda. Superfície
# quase lisa (área de descanso pro olho), com poucas marcas. Misturar as 4 dá um calçamento
# irregular sem desenho repetido; a variedade fina vem da camada de detalhes.
def pedras(var, grama=False, seed=0):
    rnd = random.Random(100 + var * 13 + seed)
    p = R["pedra"]
    im = nova(p[1])
    lajes = {1: [(0, 0, 16, 16)], 2: [(0, 0, 16, 8), (0, 8, 16, 8)],
             3: [(0, 0, 16, 16)], 4: [(0, 0, 9, 16), (9, 0, 7, 16)]}[var]
    for k, (x0, y0, w, h) in enumerate(lajes):
        base = {1: 3, 2: (3, 2)[k], 3: 2, 4: (2, 3)[k]}[var]
        for y in range(y0, y0 + h - 1):
            for x in range(x0, x0 + w - 1):
                tom = base
                if y == y0 or x == x0:
                    tom = min(5, base + 1)
                elif y == y0 + h - 2 or x == x0 + w - 2:
                    tom = max(2, base - 1) if base > 2 else 2
                put(im, x, y, p[tom])
        # desgaste: 1 ou 2 riscos horizontais de 2-3 px, um tom abaixo (seguem o plano da laje)
        for _ in range(rnd.randint(1, 2)):
            x = x0 + 2 + rnd.randrange(max(1, w - 6))
            y = y0 + 2 + rnd.randrange(max(1, h - 5))
            for dx in range(rnd.choice((2, 3))):
                put(im, x + dx, y, p[max(1, base - 1)])
    if var == 3:      # rachadura em Y
        for (x, y) in ((4, 3), (5, 4), (6, 5), (6, 6), (7, 7), (8, 8), (7, 9), (9, 8), (10, 9), (11, 9)):
            put(im, x, y, p[1])
        for (x, y) in ((5, 3), (7, 6), (9, 7)):
            put(im, x, y, p[4])
    if grama:
        m = R["mato"]
        for (x, y) in ((15, 3), (15, 4), (15, 9), (3, 15), (4, 15), (10, 15), (11, 15), (15, 12)):
            put(im, x, y, m[rnd.choice((1, 2))])
        for (x, y) in ((14, 4), (4, 14), (11, 14)):
            put(im, x, y, m[2])
    return im


def calcada(var):
    rnd = random.Random(200 + var)
    l = R["laje"]
    im = nova(l[0])
    # duas lajes de 16×8 (a de baixo desencontrada no 2: junta no meio)
    for (y0, y1) in ((0, 7), (8, 15)):
        juntas = [15] if (var == 1 or y0 == 0) else [7, 15]
        x0 = 0
        for xj in juntas:
            base = rnd.choice((2, 2, 3))
            for x in range(x0, xj):
                for y in range(y0, y1):
                    tom = base
                    if y == y0 or x == x0:
                        tom = base + 1
                    elif y == y1 - 1 or x == xj - 1:
                        tom = base - 1
                    put(im, x, y, l[tom])
            x0 = xj + 1
    # rachadura fina em Y numa das lajes
    if var == 2:
        for (x, y) in ((3, 2), (4, 3), (5, 3), (6, 4), (5, 5), (7, 4)):
            put(im, x, y, l[0])
    return im


def terra(seed=31):
    rnd = random.Random(seed)
    t = R["terra"]
    im = nova(t[1])
    for _ in range(26):
        x, y = rnd.randrange(T), rnd.randrange(T)
        c = rnd.choice((0, 2, 2))
        put(im, x, y, t[c])
        if c == 2:
            put(im, (x + 1) % T, y, t[2])
    for _ in range(4):        # pedrinhas
        x, y = rnd.randrange(T), rnd.randrange(T)
        put(im, x, y, t[3])
        put(im, x, (y + 1) % T, t[0])
    return im


def grama(seed):
    rnd = random.Random(seed)
    im = terra(seed + 7)
    m = R["mato"]
    for _ in range(9):
        x, y = rnd.randrange(T), rnd.randrange(3, T)
        h = rnd.randint(2, 4)
        for k in range(h):
            put(im, (x + (k // 2) * rnd.choice((-1, 0, 1))) % T, y - k, m[min(3, 1 + k)])
    return im


def meio_fio(rua):
    """Laje da calçada + pedra do meio-fio + a face caindo pra rua. rua: c/b/e/d (lado da rua)."""
    l, p = R["laje"], R["pedra"]
    im = calcada(1)
    # desenha como "rua embaixo" e gira
    for x in range(T):
        for y in range(10, 16):
            if y == 10:
                c = l[4]                     # topo do granito, na luz
            elif y in (11, 12):
                c = l[3]
            elif y == 13:
                c = l[1]                     # face do meio-fio
            elif y == 14:
                c = l[0]
            else:
                c = p[0]                     # sarjeta
            put(im, x, y, c)
        if x in (5, 13):                     # junta entre blocos do meio-fio
            for y in (10, 11, 12):
                put(im, x, y, l[1])
    giro = {"b": 0, "c": 180, "e": 270, "d": 90}[rua]
    return im.rotate(giro) if giro else im


# ------------------------------------------------------------------ muro ------
def face(esq=False, dir_=False, seed=1, janela=False, rachada=False):
    """Face do muro (de pé, virada pro sul): fiadas de blocos, friso claro embaixo."""
    rnd = random.Random(seed)
    m = R["muro"]
    im = nova(m[1])
    fiadas = [(0, 4), (5, 9), (10, 13)]
    for i, (y0, y1) in enumerate(fiadas):
        off = (4 if i % 2 else 0) + (seed % 3)
        x0 = -off
        while x0 < T:
            xb = x0 + rnd.choice((7, 8, 9))
            base = rnd.choice((2, 3, 3))
            for x in range(max(0, x0 + 1), min(T, xb)):
                for y in range(y0 + 1, y1 + 1):
                    tom = base
                    if y == y0 + 1:
                        tom = base + 1
                    elif y == y1:
                        tom = base - 1
                    put(im, x, y, m[tom])
            x0 = xb
    # friso de pedra no pé do muro (lê como base) e a sombra de contato
    for x in range(T):
        put(im, x, 14, m[4])
        put(im, x, 15, m[2])
    if esq:
        for y in range(T):
            put(im, 0, y, m[0])
            put(im, 1, y, m[4] if y < 14 else m[3])
            put(im, 2, y, m[3] if y < 14 else m[2])
    if dir_:
        for y in range(T):
            put(im, 15, y, m[0])
            put(im, 14, y, m[2] if y < 14 else m[1])
    if janela:
        # janela ogival estreita, acesa (o acento do cenário)
        ch = R["chama"]
        pts = [(7, 2), (8, 2)] + [(x, y) for y in range(3, 12) for x in (6, 7, 8, 9)]
        for (x, y) in pts:
            put(im, x, y, m[0])
        for y in range(4, 11):
            for x in (7, 8):
                put(im, x, y, ch[3] if y < 7 else ch[2])
        for y in range(5, 11):
            put(im, 7 if y % 2 else 8, y, ch[2] if y < 8 else ch[1])
        for x in (6, 7, 8, 9):
            put(im, x, 12, m[4])              # peitoril
    if rachada:
        for (x, y) in ((10, 1), (10, 2), (9, 3), (9, 4), (10, 5), (11, 6), (11, 7), (10, 8), (12, 7)):
            put(im, x, y, m[0])
    return im


def topo(bordas, seed=1, canto=None):
    """Topo do muro visto de cima: pedra de cobertura escura; a borda clara fica do lado que dá pra
    dentro da room (as setas do nome). canto: 'ce','cd','be','bd' = canto interno."""
    rnd = random.Random(300 + seed)
    m = R["muro"]
    im = nova(m[1])
    # cobertura: placas grandes, quase lisas
    for (y0, y1) in ((0, 7), (8, 15)):
        x0 = 0 if y0 == 0 else 6
        for xs in ((x0, x0 + 9),):
            pass
        for y in range(y0, y1 + 1):
            for x in range(T):
                junta = (y == y1) or ((x == (9 if y0 == 0 else 4)))
                put(im, x, y, m[0] if junta else m[rnd.choice((1, 2, 2))] if (x + y * 3) % 11 == 0 else m[2])
    lado = {"c": [(x, 0) for x in range(T)], "b": [(x, 15) for x in range(T)],
            "e": [(0, y) for y in range(T)], "d": [(15, y) for y in range(T)]}
    dentro = {"c": [(x, 1) for x in range(T)], "b": [(x, 14) for x in range(T)],
              "e": [(1, y) for y in range(T)], "d": [(14, y) for y in range(T)]}
    for b in bordas:
        for (x, y) in lado[b]:
            put(im, x, y, m[5])
        for (x, y) in dentro[b]:
            put(im, x, y, m[3])
    if canto:
        cx = 0 if "e" in canto else 15
        cy = 0 if "c" in canto else 15
        sx = 1 if cx == 0 else -1
        sy = 1 if cy == 0 else -1
        for k in range(3):
            put(im, cx + sx * k, cy, m[5])
            put(im, cx, cy + sy * k, m[5])
        put(im, cx + sx, cy + sy, m[3])
    return im


def escada(parte):
    """Degraus subindo pra porta do muro de cima: pisos claros, espelhos escuros."""
    l, m = R["laje"], R["muro"]
    im = nova(l[1])
    for i, y0 in enumerate((0, 4, 8, 12)):
        for x in range(T):
            put(im, x, y0, l[4 - (i // 2)])
            put(im, x, y0 + 1, l[3 - (i // 2)])
            put(im, x, y0 + 2, l[1])
            put(im, x, y0 + 3, m[1])
    if parte == "e":
        for y in range(T):
            put(im, 0, y, m[0])
            put(im, 1, y, m[3])
    if parte == "d":
        for y in range(T):
            put(im, 15, y, m[0])
            put(im, 14, y, m[2])
    return im


def passagem():
    im = nova()
    for y in range(T):
        for x in range(T):
            a = 230 if y < 6 else (170 if y < 11 else 110)
            put(im, x, y, R["muro"][0], a)
    return im


# --------------------------------------------------------------- detalhes -----
def sombra_muro():
    im = nova()
    for y in range(6):
        for x in range(T):
            put(im, x, y, R["muro"][0], (150, 120, 95, 70, 50, 30)[y])
    return im


def rachadura(seed):
    im = nova()
    c = R["pedra"][0]
    for (x, y) in ((3, 4), (4, 5), (5, 5), (6, 6), (7, 7), (7, 8), (8, 9), (9, 9), (6, 7), (5, 8), (10, 10)):
        put(im, x, y, c)
    for (x, y) in ((4, 4), (6, 5), (8, 8), (9, 8)):
        put(im, x, y, R["pedra"][4])
    return im


def folhas(seed):
    rnd = random.Random(seed)
    im = nova()
    cores = [R["madeira"][2], R["madeira"][3], R["ouro"][0], R["madeira"][1]]
    for _ in range(6):
        x, y = rnd.randrange(1, 14), rnd.randrange(1, 14)
        c = rnd.choice(cores)
        put(im, x, y, c)
        put(im, x + 1, y, c)
        put(im, x, y + 1, R["madeira"][1])
    return im


def sangue_chao(seed):
    rnd = random.Random(seed)
    s = R["sangue"]
    im = nova()
    for (x, y) in ((6, 7), (7, 7), (8, 7), (7, 8), (8, 8), (9, 8), (6, 8), (7, 6), (8, 9)):
        put(im, x, y, s[1])
    for (x, y) in ((7, 7), (8, 8)):
        put(im, x, y, s[2])
    for _ in range(6):
        x, y = rnd.randrange(2, 14), rnd.randrange(2, 14)
        put(im, x, y, s[0])
    return im


def poca():
    a = R["agua"]
    im = nova()
    for y in range(5, 12):
        for x in range(3, 13):
            if ((x - 7.5) / 5.2) ** 2 + ((y - 8.2) / 3.4) ** 2 <= 1:
                put(im, x, y, a[1], 220)
    for (x, y) in ((5, 7), (6, 7), (7, 7)):
        put(im, x, y, a[3], 230)          # reflexo do lampião
    for (x, y) in ((9, 9), (10, 9)):
        put(im, x, y, a[2], 220)
    return im


def bueiro():
    f = R["ferro"]
    im = nova()
    for y in range(4, 12):
        for x in range(3, 13):
            borda = x in (3, 12) or y in (4, 11)
            put(im, x, y, f[2] if borda else (f[0] if x % 2 else f[1]))
    for x in range(3, 13):
        put(im, x, 4, f[3])
    return im


def pedrinhas(seed):
    rnd = random.Random(seed)
    im = nova()
    p = R["pedra"]
    for _ in range(6):
        x, y = rnd.randrange(2, 14), rnd.randrange(2, 14)
        put(im, x, y, p[5])
        put(im, x + 1, y, p[3])
        put(im, x, y + 1, p[1])
    return im


TILES = [
    ("vazio", nova),
    ("pedra 1", lambda: pedras(1)), ("pedra 2", lambda: pedras(2)), ("pedra 3", lambda: pedras(3)), ("pedra 4", lambda: pedras(4)),
    ("calçada 1", lambda: calcada(1)), ("calçada 2", lambda: calcada(2)), ("terra", lambda: terra(31)),
    ("grama 1", lambda: grama(51)), ("grama 2", lambda: grama(52)),
    ("grama na pedra 1", lambda: pedras(1, grama=True, seed=5)), ("grama na pedra 2", lambda: pedras(3, grama=True, seed=6)),
    ("meio-fio (rua em cima)", lambda: meio_fio("c")), ("meio-fio (rua embaixo)", lambda: meio_fio("b")),
    ("meio-fio (rua à esquerda)", lambda: meio_fio("e")), ("meio-fio (rua à direita)", lambda: meio_fio("d")),
    ("face ponta esquerda", lambda: face(esq=True, seed=1)), ("face 1", lambda: face(seed=2)), ("face 2", lambda: face(seed=3)),
    ("face ponta direita", lambda: face(dir_=True, seed=4)), ("face sozinha", lambda: face(esq=True, dir_=True, seed=5)),
    ("face com janela", lambda: face(seed=6, janela=True)), ("face rachada", lambda: face(seed=7, rachada=True)),
    ("escada esquerda", lambda: escada("e")),
    ("topo ↖", lambda: topo({"c", "e"}, 1)), ("topo ↑", lambda: topo({"c"}, 2)), ("topo ↗", lambda: topo({"c", "d"}, 3)),
    ("canto interno ↖", lambda: topo(set(), 4, "ce")), ("canto interno ↗", lambda: topo(set(), 5, "cd")),
    ("escada meio", lambda: escada("m")), ("escada direita", lambda: escada("d")), ("passagem escura", passagem),
    ("topo ←", lambda: topo({"e"}, 6)), ("topo centro", lambda: topo(set(), 7)), ("topo →", lambda: topo({"d"}, 8)),
    ("canto interno ↙", lambda: topo(set(), 9, "be")), ("canto interno ↘", lambda: topo(set(), 10, "bd")),
    ("sombra do muro", sombra_muro), ("rachadura", lambda: rachadura(61)), ("folhas", lambda: folhas(62)),
    ("topo ↙", lambda: topo({"b", "e"}, 11)), ("topo ↓", lambda: topo({"b"}, 12)), ("topo ↘", lambda: topo({"b", "d"}, 13)),
    ("sangue no chão", lambda: sangue_chao(63)), ("poça", poca), ("bueiro", bueiro), ("pedrinhas", lambda: pedrinhas(64)),
    ("folhas 2", lambda: folhas(65)),
]


def montar():
    cols = 8
    folha = Image.new("RGBA", (cols * T, 6 * T), (0, 0, 0, 0))
    for i, (_n, fn) in enumerate(TILES):
        folha.alpha_composite(fn(), ((i % cols) * T, (i // cols) * T))
    return folha


def indice(nome):
    for i, (n, _) in enumerate(TILES):
        if n == nome:
            return i
    raise KeyError(nome)


if __name__ == "__main__":
    from kit import previa as pv
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "previa")
    f = montar()
    pv.amplia(f, 5, (30, 30, 34, 255)).save(os.path.join(out, "tiles_folha.png"))
    # emenda: 4 pedras misturadas 6×4
    rnd = random.Random(1)
    t = Image.new("RGBA", (T * 8, T * 5))
    for y in range(5):
        for x in range(8):
            t.alpha_composite(pedras(rnd.randint(1, 4)), (x * T, y * T))
    pv.amplia(t, 4).save(os.path.join(out, "tiles_emenda.png"))
    print("ok")
