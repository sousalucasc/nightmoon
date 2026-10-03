"""Amostra da paleta: uma linha por rampa, com L* e o ΔE entre vizinhos."""
from PIL import Image, ImageDraw

from . import paleta as pal
from .previa import _fonte


def amostra(rampas, caminho, cel=28):
    f = _fonte(10)
    W = 140 + max(len(r) for r in rampas.values()) * (cel + 4) + 10
    H = 8 + len(rampas) * (cel + 18)
    t = Image.new("RGBA", (W, H), (30, 30, 34, 255))
    d = ImageDraw.Draw(t)
    y = 6
    avisos = []
    for nome, r in rampas.items():
        d.text((6, y + 8), nome, fill=(220, 220, 220, 255), font=f)
        x = 140
        for i, c in enumerate(r):
            d.rectangle([x, y, x + cel, y + cel], fill=tuple(c) + (255,))
            d.text((x, y + cel + 2), f"{pal.L(c):.0f}", fill=(200, 200, 200, 255), font=f)
            if i > 0:
                de = pal.delta_e(r[i - 1], c)
                if de < 5:
                    avisos.append(f"{nome}: tons {i-1}-{i} ΔE {de:.1f}")
                d.text((x - 4, y - 1), f"{de:.0f}", fill=(255, 120, 120, 255) if de < 5 else (120, 200, 120, 255), font=_fonte(8))
            x += cel + 4
        y += cel + 18
    t.save(caminho)
    return avisos
