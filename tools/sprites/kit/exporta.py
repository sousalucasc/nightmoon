"""Exportação pra engine (GameMaker): tiras _stripN.png em arte/<pasta>/, prévias e .aseprite.

Registro: cada exportação devolve uma linha pra `arte/origens.md` (nome, quadro, quadros, origem).
"""
import json
import os

from PIL import Image

from . import aseprite
from . import previa as pv

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ARTE = os.path.join(RAIZ, "arte")


def tira(quadros):
    w, h = quadros[0].size
    t = Image.new("RGBA", (w * len(quadros), h))
    for i, q in enumerate(quadros):
        t.alpha_composite(q.convert("RGBA"), (i * w, 0))
    return t


def arquivo(nome, n):
    return f"{nome}_strip{n}.png" if n > 1 else f"{nome}.png"


def salva_sprite(nome, quadros, pasta, origem, duracao_ms=100, gif=True, fundo_gif=(52, 54, 62, 255), k_gif=4):
    """Grava a tira em arte/<pasta>/ e o GIF em arte/<pasta>/previa/. Devolve a linha do registro."""
    dest = os.path.join(ARTE, pasta)
    os.makedirs(dest, exist_ok=True)
    # apaga versões antigas com outro número de quadros
    for f in os.listdir(dest):
        if f == f"{nome}.png" or (f.startswith(nome + "_strip") and f.endswith(".png")):
            os.remove(os.path.join(dest, f))
    tira(quadros).save(os.path.join(dest, arquivo(nome, len(quadros))))
    if gif and len(quadros) > 1:
        os.makedirs(os.path.join(dest, "previa"), exist_ok=True)
        pv.gif(quadros, duracao_ms, os.path.join(dest, "previa", f"{nome}.gif"), k=k_gif, fundo=fundo_gif)
    w, h = quadros[0].size
    return {"nome": nome, "w": w, "h": h, "n": len(quadros), "origem": origem, "pasta": pasta}


def salva_aseprite(caminho, anims, paleta, pivo):
    """anims: lista de (nome, quadros, duracao_ms). Uma tag por animação. Confere a ida e volta."""
    todos, dur, tags = [], [], []
    for nome, qs, d in anims:
        ini = len(todos)
        todos += qs
        dur += [d] * len(qs) if isinstance(d, (int, float)) else list(d)
        tags.append((nome, ini, len(todos) - 1))
    aseprite.grava(caminho, todos, dur, tags, paleta, pivo)
    prob = aseprite.confere(caminho, todos, tags, pivo)
    # spritesheet + json
    w, h = todos[0].size
    cols = min(8, len(todos))
    linhas = (len(todos) + cols - 1) // cols
    folha = Image.new("RGBA", (cols * w, linhas * h))
    meta = {"frames": [], "meta": {"size": {"w": cols * w, "h": linhas * h}, "frameTags": [],
                                    "pivot": {"x": pivo[0], "y": pivo[1]}}}
    for i, q in enumerate(todos):
        x, y = (i % cols) * w, (i // cols) * h
        folha.alpha_composite(q.convert("RGBA"), (x, y))
        meta["frames"].append({"frame": {"x": x, "y": y, "w": w, "h": h}, "duration": int(dur[i])})
    for nome, de, ate in tags:
        meta["meta"]["frameTags"].append({"name": nome, "from": de, "to": ate, "direction": "forward"})
    base = os.path.splitext(caminho)[0]
    folha.save(base + "_sheet.png")
    json.dump(meta, open(base + "_sheet.json", "w", encoding="utf-8"), indent=1)
    return prob


def registro_md(linhas, caminho=None):
    """Reescreve arte/origens.md a partir das linhas (na ordem dada)."""
    caminho = caminho or os.path.join(ARTE, "origens.md")
    out = ["# Origem de cada sprite", "",
           "Ao importar no GameMaker: **Origin → Custom** com estes valores. As tiras `_stripN` são cortadas sozinhas em N quadros.",
           "", "| Sprite | Tamanho do quadro | Quadros | Origem (x, y) |", "|---|---|---|---|"]
    for r in linhas:
        extra = r.get("nota", "")
        out.append(f"| {r['nome']} | {r['w']}×{r['h']} | {r['n']} | {r['origem'][0]}, {r['origem'][1]}{extra} |")
    open(caminho, "w", encoding="utf-8").write("\n".join(out) + "\n")
