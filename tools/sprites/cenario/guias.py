"""Guias de pintura das rooms (arte/cenario/previa/guia_rm_*.png) e mapa do tileset.

As regras são as da tabela do Apêndice A, dia 18 (o dono pinta à mão seguindo o guia):
- muro com chão embaixo = face (pontas, janela e rachada espalhadas); o resto do muro = topo,
  com a borda clara do lado de dentro; cantos internos onde só a diagonal é chão;
- chão: pedra 1-4 misturadas, grama na pedra de vez em quando; nas 2 linhas abaixo do muro de
  cima, calçada com meio-fio (rua embaixo) na segunda;
- porta no muro de cima = escada; vão do atalho = pedra + passagem escura;
- detalhes: sombra do muro embaixo de toda face, e pouca coisa espalhada.
As posições dos objetos são as da tabela do Apêndice (POSICOES).
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PIL import Image, ImageDraw  # noqa: E402

from cenario import props, tiles  # noqa: E402

T = 16
AQUI = os.path.dirname(os.path.abspath(__file__))
ROOMS = json.load(open(os.path.join(AQUI, "rooms_tutorial.json"), encoding="utf-8"))

POSICOES = {
    "rm_praca": [("obj_poste", 190, 90), ("obj_poste", 300, 90), ("obj_barril", 330, 150), ("obj_barril", 342, 154),
                 ("obj_caixote", 356, 148), ("obj_carroca", 150, 200), ("obj_caixao", 290, 60)]
                + [("obj_cerca", x, 60) for x in range(60, 125, 16)],
    "rm_rua": [("obj_poste", x, 52) for x in (120, 300, 460, 620, 780)]
              + [("obj_barril", 60, 330), ("obj_barril", 72, 334), ("obj_caixote", 86, 328), ("obj_caixao", 540, 52),
                 ("obj_carroca", 740, 300), ("obj_barril", 900, 330)],
    "rm_mercado": [("obj_poste", 60, 52), ("obj_poste", 580, 52), ("obj_caixote", 100, 100), ("obj_caixote", 114, 104),
                   ("obj_barril", 128, 98), ("obj_carroca", 540, 160), ("obj_caixote", 520, 470), ("obj_barril", 536, 474),
                   ("obj_caixao", 60, 500)],
    "rm_portao": [("obj_poste", 196, 52), ("obj_poste", 284, 52)]
                 + [("obj_cerca", x, 50) for x in range(40, 170, 16)]
                 + [("obj_cerca", x, 50) for x in range(312, 450, 16)],
    "rm_arena_1": [("obj_poste", 60, 52), ("obj_poste", 420, 52), ("obj_caixao", 40, 340), ("obj_caixao", 440, 340)],
}

RIMS = {frozenset({"c", "e"}): "topo ↖", frozenset({"c"}): "topo ↑", frozenset({"c", "d"}): "topo ↗",
        frozenset({"e"}): "topo ←", frozenset(): "topo centro", frozenset({"d"}): "topo →",
        frozenset({"b", "e"}): "topo ↙", frozenset({"b"}): "topo ↓", frozenset({"b", "d"}): "topo ↘"}


def muros(nome):
    R = ROOMS[nome]
    w, h = R["w"] // T, R["h"] // T
    m = [[False] * w for _ in range(h)]
    for i in R["instances"]:
        if i["obj"] == "obj_parede":
            x0, y0 = int(i["x"]) // T, int(i["y"]) // T
            for yy in range(y0, y0 + int(round(i.get("sy", 1)))):
                for xx in range(x0, x0 + int(round(i.get("sx", 1)))):
                    if 0 <= xx < w and 0 <= yy < h:
                        m[yy][xx] = True
    return m


def pintar(nome, seed=None):
    muro = muros(nome)
    rnd = random.Random(seed if seed is not None else sum(map(ord, nome)))
    h, w = len(muro), len(muro[0])

    def M(x, y):
        return True if not (0 <= x < w and 0 <= y < h) else muro[y][x]

    chao = [[None] * w for _ in range(h)]
    det = [[None] * w for _ in range(h)]
    face = [[M(x, y) and 0 <= y + 1 < h and not M(x, y + 1) for x in range(w)] for y in range(h)]
    for y in range(h):
        for x in range(w):
            if M(x, y):
                if face[y][x]:
                    fe = not (x > 0 and M(x - 1, y) and face[y][x - 1])
                    fd = not (x < w - 1 and M(x + 1, y) and face[y][x + 1])
                    if fe and fd:
                        chao[y][x] = "face sozinha"
                    elif fe:
                        chao[y][x] = "face ponta esquerda"
                    elif fd:
                        chao[y][x] = "face ponta direita"
                    else:
                        chao[y][x] = rnd.choice(["face 1", "face 2", "face 1", "face 2", "face com janela", "face rachada"])
                else:
                    rims = set()
                    if not M(x, y - 1):
                        rims.add("c")
                    if not M(x - 1, y):
                        rims.add("e")
                    if not M(x + 1, y):
                        rims.add("d")
                    if not M(x, y + 1) and not face[y][x]:
                        rims.add("b")
                    nome_t = RIMS.get(frozenset(rims), "topo centro")
                    if not rims:
                        for (dx, dy, n) in ((1, -1, "canto interno ↗"), (-1, -1, "canto interno ↖"),
                                            (1, 1, "canto interno ↘"), (-1, 1, "canto interno ↙")):
                            if not M(x + dx, y + dy):
                                nome_t = n
                    chao[y][x] = nome_t
            else:
                acima = y <= 2 and any(y - k >= 0 and face[y - k][x] for k in (1, 2))
                if acima:
                    chao[y][x] = "meio-fio (rua embaixo)" if y == 2 else rnd.choice(["calçada 1", "calçada 2"])
                else:
                    chao[y][x] = (rnd.choice(["pedra 1", "pedra 2", "pedra 3", "pedra 4"]) if rnd.random() < 0.9
                                  else rnd.choice(["grama na pedra 1", "grama na pedra 2"]))
                if y > 0 and face[y - 1][x]:
                    det[y][x] = "sombra do muro"
                elif rnd.random() < 0.035:
                    det[y][x] = rnd.choice(["rachadura", "rachadura", "folhas", "folhas 2", "pedrinhas", "pedrinhas",
                                            "poça", "sangue no chão"] + (["bueiro"] if rnd.random() < 0.3 else []))
    # portas no muro de cima: escada; vão do atalho: passagem escura
    atalhos = [i for i in ROOMS[nome]["instances"] if i["obj"] == "obj_atalho"]
    for x in range(w):
        if not muro[0][x]:
            if any(abs(x * T + 8 - a["x"]) < 16 and a["y"] <= 32 for a in atalhos):
                chao[0][x], det[0][x] = "pedra 1", "passagem escura"
            else:
                esq = x == 0 or muro[0][x - 1]
                dir_ = x == w - 1 or muro[0][x + 1]
                chao[0][x] = "escada esquerda" if esq else ("escada direita" if dir_ else "escada meio")
                det[0][x] = None
    return chao, det


_folha = None


def _tile(nome):
    global _folha
    if _folha is None:
        _folha = tiles.montar()
    i = tiles.indice(nome)
    return _folha.crop(((i % 8) * T, (i // 8) * T, (i % 8) * T + T, (i // 8) * T + T))


def render(nome, com_objetos=True):
    chao, det = pintar(nome)
    h, w = len(chao), len(chao[0])
    out = Image.new("RGBA", (w * T, h * T), (20, 16, 18, 255))
    cache = {}
    for camada in (chao, det):
        for y in range(h):
            for x in range(w):
                n = camada[y][x]
                if n:
                    if n not in cache:
                        cache[n] = _tile(n)
                    out.alpha_composite(cache[n], (x * T, y * T))
    if com_objetos:
        lista = []
        desenhos = {"obj_poste": "spr_poste", "obj_caixote": "spr_caixote", "obj_barril": "spr_barril",
                    "obj_carroca": "spr_carroca", "obj_caixao": "spr_caixao", "obj_cerca": "spr_cerca",
                    "obj_lanterna": "spr_lanterna", "obj_pilar": "spr_pilar", "obj_boneco": "spr_boneco"}
        for i in ROOMS[nome]["instances"]:
            o = i["obj"]
            if o == "obj_atalho":
                img = props.quadros("spr_atalho")[0]
                out.alpha_composite(img, (int(i["x"]) - 16, int(i["y"]) - 16))
            elif o == "obj_nevoa":
                nv = props.quadros("spr_nevoa")[0]
                for a in range(int(round(i.get("sx", 1)))):
                    for b in range(int(round(i.get("sy", 1)))):
                        out.alpha_composite(nv, (int(i["x"]) + a * 16, int(i["y"]) + b * 16))
            elif o in desenhos:
                lista.append((o, int(i["x"]), int(i["y"])))
        lista += list(POSICOES.get(nome, []))
        for (o, x, y) in sorted(lista, key=lambda t: t[2]):
            if o in desenhos:
                spr = desenhos[o]
                img = props.quadros(spr)[0]
                ox, oy = props.PROPS[spr][1]
                out.alpha_composite(img, (x - ox, y - oy))
    return out


def guia(nome, k=2):
    img = render(nome)
    g = img.resize((img.width * k, img.height * k), Image.NEAREST)
    d = ImageDraw.Draw(g)
    for x in range(0, g.width, T * k):
        d.line([(x, 0), (x, g.height)], fill=(235, 225, 205, 150), width=1)
    for y in range(0, g.height, T * k):
        d.line([(0, y), (g.width, y)], fill=(235, 225, 205, 150), width=1)
    return g


def mapa_tileset(k=4):
    f = tiles.montar()
    from kit.previa import _fonte
    fonte = _fonte(10)
    cel = T * k
    W = 8 * (cel + 4) + 8
    H = 6 * (cel + 30) + 8
    t = Image.new("RGBA", (W, H), (30, 30, 34, 255))
    d = ImageDraw.Draw(t)
    for i, (n, _) in enumerate(tiles.TILES):
        cx, cy = (i % 8) * (cel + 4) + 4, (i // 8) * (cel + 30) + 4
        tile = f.crop(((i % 8) * T, (i // 8) * T, (i % 8) * T + T, (i // 8) * T + T))
        fundo = Image.new("RGBA", (T, T), (60, 56, 60, 255))
        fundo.alpha_composite(tile)
        t.alpha_composite(fundo.resize((cel, cel), Image.NEAREST), (cx, cy))
        d.text((cx, cy + cel + 2), f"{i} {n}", fill=(230, 225, 210, 255), font=fonte)
    return t


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "previa")
    for n in POSICOES:
        guia(n).save(os.path.join(out, f"guia_{n}.png"))
    mapa_tileset().save(os.path.join(out, "tileset_mapa.png"))
    print("ok")
