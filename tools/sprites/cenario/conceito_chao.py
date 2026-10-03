"""Chão e muro de esboço pras três direções de arte (só pra PARADA 1: ver o caçador no lugar).

O tileset de verdade é desenhado depois, à mão, na direção escolhida.
"""
import os
import random
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit import paleta as pal  # noqa: E402

H = pal.de_hexa

DIRECOES = {
    # junta, pedra (3 tons), luz da aresta, sombra da aresta, musgo/mancha (2), reflexo (2)
    "A": dict(junta=H("#0d1517"), pedra=[H("#1b2627"), H("#212d2e"), H("#283535")], luz=H("#33433f"),
              sombra=H("#141e20"), mancha=[H("#22361f"), H("#2f4826")], reflexo=None,
              muro=[H("#111a1d"), H("#18242a"), H("#203038"), H("#2b3e45")], janela=H("#e09a38")),
    "B": dict(junta=H("#100810"), pedra=[H("#1f1119"), H("#25141e"), H("#2b1823")], luz=H("#3a2130"),
              sombra=H("#170c13"), mancha=[H("#2a1218"), H("#3a1820")], reflexo=[H("#4a1a24"), H("#7a2a34")],
              muro=[H("#120910"), H("#1b0f18"), H("#251521"), H("#331d2b")], janela=H("#d8c8a0")),
    "C": dict(junta=H("#292220"), pedra=[H("#49413c"), H("#4f4742"), H("#58514b")], luz=H("#68625c"),
              sombra=H("#39312e"), mancha=[H("#3f2f28"), H("#42381d")], reflexo=None,
              muro=[H("#1c1414"), H("#271c1a"), H("#332521"), H("#43312a")], janela=H("#f0b860")),
}


def lajes(d, w=64, h=48, seed=1, alt=(5, 8), larg=(7, 14)):
    """Pedras em fiadas desencontradas (laje irregular), emendando nas bordas."""
    rnd = random.Random(seed)
    img = np.zeros((h, w, 3), np.uint8)
    img[:, :] = d["junta"]
    y = 0
    while y < h:
        hh = rnd.randint(*alt)
        x = -rnd.randint(0, larg[1])
        while x < w:
            ww = rnd.randint(*larg)
            base = rnd.choice(d["pedra"])
            for yy in range(y, min(h, y + hh - 1)):
                for xx in range(max(0, x), min(w, x + ww - 1)):
                    c = base
                    if yy == y or xx == x:
                        c = d["luz"]
                    elif yy == y + hh - 2 or xx == x + ww - 2:
                        c = d["sombra"]
                    img[yy, xx] = c
            # marcas: 1 risco de 2 px dentro de algumas pedras
            if rnd.random() < 0.5 and ww > 6 and hh > 5:
                mx, my = x + rnd.randint(2, ww - 4), y + rnd.randint(2, hh - 3)
                for k in range(2):
                    if 0 <= mx + k < w and 0 <= my < h:
                        img[my, mx + k] = d["sombra"]
            x += ww
        y += hh
    # mancha (musgo / sujeira) em algumas juntas
    for _ in range(w * h // 90):
        x, y = rnd.randrange(w), rnd.randrange(h)
        if tuple(img[y, x]) == d["junta"]:
            c = rnd.choice(d["mancha"])
            for dx in range(rnd.randint(1, 3)):
                if x + dx < w and tuple(img[y, x + dx]) == d["junta"]:
                    img[y, x + dx] = c
    if d["reflexo"]:
        for _ in range(4):
            x, y = rnd.randrange(w - 6), rnd.randrange(h)
            for dx in range(rnd.randint(3, 6)):
                if tuple(img[y, x + dx]) != d["junta"]:
                    img[y, x + dx] = d["reflexo"][0 if dx in (0, 5) else 1]
    a = np.dstack([img, np.full((h, w), 255, np.uint8)])
    return Image.fromarray(a, "RGBA")


def muro(d, w=64, h=24, seed=2):
    """Face de muro em blocos, mais escura embaixo (sombra do chão), com uma janela acesa."""
    rnd = random.Random(seed)
    img = np.zeros((h, w, 3), np.uint8)
    img[:, :] = d["muro"][0]
    bh = 6
    for row, y in enumerate(range(0, h - 2, bh)):
        off = (row % 2) * 6
        for x in range(-off, w, 12):
            for yy in range(y, min(h - 2, y + bh - 1)):
                for xx in range(max(0, x), min(w, x + 11)):
                    t = 2 if yy > y else 3
                    if xx == x + 10 or yy == y + bh - 2:
                        t = 1
                    if yy > h - 8:
                        t = max(1, t - 1)
                    img[yy, xx] = d["muro"][t]
    img[h - 2:, :] = d["muro"][0]
    # janela estreita, ogival
    jx = w // 2 - 2
    for yy in range(4, 14):
        for xx in range(jx, jx + 4):
            if yy == 4 and xx in (jx, jx + 3):
                continue
            img[yy, xx] = d["janela"] if (xx - jx) in (1, 2) or yy > 5 else d["muro"][1]
    a = np.dstack([img, np.full((h, w), 255, np.uint8)])
    return Image.fromarray(a, "RGBA")


def cena(direcao, w=96, h=72):
    d = DIRECOES[direcao]
    chao = lajes(d, w, h - 24, seed=ord(direcao))
    mur = muro(d, w, 24, seed=ord(direcao) + 1)
    t = Image.new("RGBA", (w, h))
    t.alpha_composite(mur, (0, 0))
    t.alpha_composite(chao, (0, 24))
    return t


def luz(cor, raio=22):
    n = raio * 2
    a = np.zeros((n, n, 4), np.uint8)
    for y in range(n):
        for x in range(n):
            r = ((x - raio + 0.5) ** 2 + (y - raio + 0.5) ** 2) ** 0.5 / raio
            if r < 1:
                k = (1 - r) ** 2 * 0.55
                a[y, x] = (*cor, int(255 * k))
    return Image.fromarray(a, "RGBA")


def voronoi(d, w=96, h=72, cel=(10, 8), metrica="euclid", estica=1.0, seed=3, tons_extra=0):
    """Pedras irregulares (Voronoi periódico, emenda nas bordas)."""
    rnd = random.Random(seed)
    cw, ch = cel
    nx, ny = max(1, w // cw), max(1, h // ch)
    pts = []
    for j in range(ny):
        for i in range(nx):
            pts.append(((i + rnd.uniform(0.2, 0.8)) * w / nx, (j + rnd.uniform(0.2, 0.8)) * h / ny))
    base_de = [rnd.randrange(len(d["pedra"])) for _ in pts]
    lab = np.zeros((h, w), np.int32)
    for y in range(h):
        for x in range(w):
            melhor, bi = 1e9, 0
            for k, (px, py) in enumerate(pts):
                dx = min(abs(x - px), w - abs(x - px)) / estica
                dy = min(abs(y - py), h - abs(y - py))
                dd = max(dx, dy) if metrica == "cheb" else (dx * dx + dy * dy) ** 0.5
                if dd < melhor:
                    melhor, bi = dd, k
            lab[y, x] = bi
    img = np.zeros((h, w, 3), np.uint8)
    for y in range(h):
        for x in range(w):
            k = lab[y, x]
            dir_ = lab[y, (x + 1) % w] != k
            baixo = lab[(y + 1) % h, x] != k
            esq = lab[y, (x - 1) % w] != k
            cima = lab[(y - 1) % h, x] != k
            if dir_ or baixo:
                img[y, x] = d["junta"]
            elif cima or esq:
                img[y, x] = d["luz"]
            elif lab[(y + 2) % h, x] != k or lab[y, (x + 2) % w] != k:
                img[y, x] = d["sombra"]
            else:
                img[y, x] = d["pedra"][base_de[k]]
    # musgo / mancha nas juntas
    for _ in range(w * h // 70):
        x, y = rnd.randrange(w), rnd.randrange(h)
        if tuple(img[y, x]) == tuple(d["junta"]):
            c = rnd.choice(d["mancha"])
            for dx in range(rnd.randint(1, 3)):
                xx = (x + dx) % w
                if tuple(img[y, xx]) == tuple(d["junta"]):
                    img[y, xx] = c
    if d["reflexo"]:
        for k in rnd.sample(range(len(pts)), max(1, len(pts) // 6)):
            ys, xs = np.nonzero(lab == k)
            if len(xs) < 12:
                continue
            cy, cx = int(ys.mean()), int(xs.mean())
            for dx in range(-2, 3):
                xx, yy = (cx + dx) % w, cy
                if lab[yy, xx] == k and tuple(img[yy, xx]) not in (tuple(d["junta"]), tuple(d["luz"])):
                    img[yy, xx] = d["reflexo"][1 if abs(dx) < 2 else 0]
    a = np.dstack([img, np.full((h, w), 255, np.uint8)])
    return Image.fromarray(a, "RGBA")


ESTILO_CHAO = {
    "A": dict(cel=(14, 9), metrica="euclid", estica=1.5),   # lajes grandes
    "B": dict(cel=(9, 9), metrica="cheb", estica=1.0),      # placas quadradas
    "C": dict(cel=(6, 5), metrica="euclid", estica=1.2),    # paralelepípedo miúdo
}


def cena2(direcao, w=96, h=72):
    d = DIRECOES[direcao]
    return voronoi(d, w, h, seed=ord(direcao) * 7, **ESTILO_CHAO[direcao])
