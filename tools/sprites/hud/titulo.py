"""LOGO e FUNDO DO TÍTULO — Nightmoon, direção sépia e ouro.

Logo (spr_logo 115×34, origem 57,17): "NIGHTMOON" em capitais de gravura douradas (serifa,
contorno escuro, brilho marfim na aresta de cima), com a lua crescente fazendo o primeiro O e
um filete com losango embaixo. Nada de sangue escorrendo (era o antigo).

Fundo (spr_fundo_titulo 320×180): céu sépia em faixas, lua grande e baixa atrás da catedral à
esquerda do centro, cidade em camadas (a de trás mais clara e chapada, a da frente quase preta
com janelas âmbar), neblina quente no pé. O centro de cima (logo, y 13-47) e o menu (y 60-74)
ficam sobre céu calmo.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import paleta as P  # noqa: E402
from PIL import Image  # noqa: E402
from kit.tela import Tela  # noqa: E402

R = P.RAMPAS

# letras do logo: 11×16, traço de 2 px, serifas
L = {
    "N": ["##.......##", "###......##", "####.....##", "##.##....##", "##..##...##", "##...##..##", "##....##.##",
          "##.....####", "##......###", "##.......##", "##.......##", "##.......##", "##.......##", "##.......##"],
    "I": ["######", "..##..", "..##..", "..##..", "..##..", "..##..", "..##..", "..##..", "..##..", "..##..", "..##..",
          "..##..", "..##..", "######"],
    "G": ["...######..", "..##....##.", ".##......##", "##.........", "##.........", "##.........", "##...######",
          "##......##.", "##......##.", "##......##.", ".##.....##.", "..##....##.", "...######..", "..........."],
    "H": ["##.......##", "##.......##", "##.......##", "##.......##", "##.......##", "##.......##", "###########",
          "###########", "##.......##", "##.......##", "##.......##", "##.......##", "##.......##", "##.......##"],
    "T": ["###########", "##...##...#", "#....##....", ".....##....", ".....##....", ".....##....", ".....##....",
          ".....##....", ".....##....", ".....##....", ".....##....", ".....##....", ".....##....", "...######.."],
    "M": ["###.......###", "####.....####", "##.##...##.##", "##..##.##..##", "##...###...##", "##....#....##",
          "##.........##", "##.........##", "##.........##", "##.........##", "##.........##", "##.........##",
          "##.........##", "##.........##"],
    "O": ["...#####...", "..##...##..", ".##.....##.", "##.......##", "##.......##", "##.......##", "##.......##",
          "##.......##", "##.......##", "##.......##", ".##.....##.", "..##...##..", "...#####...", "..........."],
    # o primeiro O vira lua: disco inteiro, iluminado à esquerda (marcas: L luz, s sombra)
    "C": ["...LLLss...", "..LLLLsss..", ".LLLLLssss.", "LLLLLLssss#", "LLLLLsssss#", "LLLLLsssss#", "LLLLLsssss#",
          "LLLLLsssss#", "LLLLLsssss#", "LLLLLLssss#", ".LLLLLsss#.", "..LLLLss#..", "...LLLs#...", "..........."],
}


def logo():
    w, h = 115, 34
    t = Tela(w, h, R)
    palavra = ["N", "I", "G", "H", "T", "M", "C", "O", "N"]
    larg = sum(len(L[c][0]) for c in palavra) + 2 * (len(palavra) - 1)
    x = (w - larg) // 2
    y0 = 5
    for c in palavra:
        linhas = L[c]
        for yy, linha in enumerate(linhas):
            for xx, ch in enumerate(linha):
                if ch == ".":
                    continue
                # ouro com luz de cima: as 4 primeiras linhas mais claras, o fio de cima marfim
                if c == "C":
                    tom = {"L": ("marfim", 2) if xx < 3 else ("marfim", 1), "s": ("nevoa", 0), "#": ("ouro", 0)}[ch]
                else:
                    tom = ("ouro", 2) if yy < 3 else (("ouro", 1) if yy < 10 else ("ouro", 0))
                    if yy == 0:
                        tom = ("marfim", 2)
                t.pinta(x + xx, y0 + yy, tom[0], tom[1])
        x += len(linhas[0]) + 2
    # filete com losango
    cx = w // 2
    for xx in range(10, w - 10):
        if abs(xx - cx) > 4:
            t.pinta(xx, 23, "ouro", 0)
    for k in range(5):
        for dx in range(-k, k + 1):
            pass
    losango = [(0, -2), (-1, -1), (0, -1), (1, -1), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (-1, 1), (0, 1), (1, 1), (0, 2)]
    for dx, dy in losango:
        t.pinta(cx + dx, 23 + dy, "ouro", 2 if (dx, dy) == (0, 0) else 1)
    for xx in (8, 9, w - 10, w - 9):
        t.pinta(xx, 23, "ouro", 1)
    t.contorno(("contorno", 0), diagonais=True)
    return t.imagem()


def fundo_titulo():
    w, h = 320, 180
    rnd = random.Random(7)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    px = im.load()
    # céu em faixas (de cima pra baixo: quase preto -> sépia quente perto do horizonte)
    ceu = [(18, 11, 14), (25, 16, 18), (34, 22, 23), (46, 31, 29), (60, 42, 36), (76, 55, 44)]
    limites = [40, 70, 92, 108, 120, 180]
    for y in range(h):
        for i, lim in enumerate(limites):
            if y < lim:
                c = ceu[i]
                break
        for x in range(w):
            px[x, y] = c + (255,)
    # estrelas raras (só no alto)
    for _ in range(40):
        x, y = rnd.randrange(w), rnd.randrange(60)
        px[x, y] = (150, 130, 110, 255) if rnd.random() < 0.7 else (220, 205, 180, 255)
    # lua grande e baixa, à esquerda do centro
    lx, ly, lr = 112, 104, 46
    lua = [(214, 196, 162), (232, 218, 190), (244, 236, 214)]
    for y in range(ly - lr - 8, ly + lr + 8):
        for x in range(lx - lr - 8, lx + lr + 8):
            d = math.hypot(x - lx, y - ly)
            if 0 <= x < w and 0 <= y < h:
                if d <= lr:
                    k = (x - lx) * 0.6 + (y - ly) * 0.4
                    c = lua[2] if k < -18 else (lua[1] if k < 16 else lua[0])
                    # manchas (mares)
                    if math.hypot(x - (lx + 12), y - (ly - 10)) < 9 or math.hypot(x - (lx - 14), y - (ly + 14)) < 7:
                        c = (198, 176, 140)
                    px[x, y] = c + (255,)
                elif d <= lr + 3:
                    r, g, b, _ = px[x, y]
                    px[x, y] = (min(255, r + 22), min(255, g + 16), min(255, b + 10), 255)
                elif d <= lr + 7:
                    r, g, b, _ = px[x, y]
                    px[x, y] = (min(255, r + 10), min(255, g + 7), min(255, b + 4), 255)

    def predio(x0, x1, topo, cor, telhado="reto", agulha=0):
        for x in range(max(0, x0), min(w, x1)):
            yy = topo
            if telhado == "duas":
                meio = (x0 + x1) / 2
                yy = topo + int(abs(x - meio) * 0.8)
            for y in range(max(0, yy), h):
                px[x, y] = cor + (255,)
        if agulha:
            cx = (x0 + x1) // 2
            for k in range(agulha):
                for dx in range(-(k // 6), k // 6 + 1):
                    if 0 <= cx + dx < w and 0 <= topo - agulha + k < h:
                        px[cx + dx, topo - agulha + k] = cor + (255,)

    # cidade de trás (mais clara, chapada)
    tras = (52, 36, 32)
    x = 0
    while x < w:
        lw = rnd.randint(14, 30)
        predio(x, x + lw, rnd.randint(118, 132), tras, telhado=rnd.choice(("reto", "duas")),
               agulha=rnd.choice((0, 0, 0, 10)))
        x += lw
    # catedral na frente da lua
    escura = (24, 15, 16)
    predio(86, 140, 112, escura, telhado="duas")
    predio(104, 122, 70, escura, agulha=32)          # torre central com agulha
    predio(90, 100, 96, escura, agulha=14)
    predio(126, 136, 96, escura, agulha=14)
    # rosácea acesa
    for y in range(116, 124):
        for x in range(109, 117):
            if math.hypot(x - 112.5, y - 119.5) < 3.6:
                px[x, y] = (200, 112, 40, 255) if (x + y) % 3 else (240, 170, 70, 255)
    # cidade da frente (quase preta) com janelas
    frente = (16, 10, 11)
    x = 0
    while x < w:
        lw = rnd.randint(18, 40)
        if not (80 < x < 150):
            predio(x, x + lw, rnd.randint(132, 150), frente, telhado=rnd.choice(("reto", "duas", "duas")),
                   agulha=rnd.choice((0, 0, 8, 16)))
            for _ in range(rnd.randint(1, 4)):
                jx, jy = rnd.randrange(x + 2, x + lw - 2), rnd.randrange(150, 172)
                if 0 <= jx < w - 1:
                    for (dx, dy) in ((0, 0), (1, 0), (0, 1), (1, 1)):
                        px[jx + dx, jy + dy] = (232, 154, 56, 255) if dy == 0 else (176, 98, 34, 255)
        x += lw
    predio(80, 150, 156, frente)
    # neblina quente no pé: três faixas chapadas, onduladas
    for y in range(156, h):
        for x in range(w):
            onda = int(2 * math.sin(x / 13.0) + 1.5 * math.sin(x / 5.3 + 1))
            faixa = (y - 156 - onda)
            if faixa >= 0:
                add = 14 if faixa < 8 else (24 if faixa < 16 else 32)
                r, g, b, _ = px[x, y]
                px[x, y] = (min(255, r + add), min(255, g + int(add * 0.75)), min(255, b + int(add * 0.55)), 255)
    return im


if __name__ == "__main__":
    from kit import previa as pv
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "previa")
    lg = logo()
    f = fundo_titulo()
    # composição do título como no jogo: fundo + véu 0.3 + logo em (160, 30) + menu
    from hud import fonte
    tela = f.copy()
    veu = Image.new("RGBA", f.size, (0, 0, 0, int(255 * 0.3)))
    tela.alpha_composite(veu)
    tela.alpha_composite(lg, (160 - 57, 30 - 17))
    for i, (txt, cor) in enumerate((("> Começar <", (255, 255, 0)), ("Sair", None))):
        im = fonte.escrever(txt, cor=cor)
        tela.alpha_composite(im, (160 - im.width // 2, 60 + i * 14))
    pv.amplia(tela, 3).save(os.path.join(out, "titulo_previa.png"))
    pv.amplia(lg, 5, (30, 22, 24, 255)).save(os.path.join(out, "logo_previa.png"))
    print("ok")
