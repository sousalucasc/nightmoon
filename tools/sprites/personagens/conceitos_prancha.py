"""Pranchas da PARADA 1: os três conceitos (cor, silhueta, valores) e no chão de cada direção."""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit import auditoria as au  # noqa: E402
from kit import paleta as pal  # noqa: E402
from kit import previa as pv  # noqa: E402
from cenario import conceito_chao as cch  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "previa")
NOMES = {"A": "A · Capuz de peregrino (verdete)", "B": "B · Corvo (lua de sangue)", "C": "C · Cartola (sépia e ouro)"}
LUZES = {"A": (224, 154, 56), "B": (216, 200, 160), "C": (240, 184, 96)}


def antigo():
    im = Image.open(os.path.join(RAIZ, "arte", "player", "spr_player_idle_strip4.png")).convert("RGBA")
    return im.crop((0, 0, 32, 32))


def prancha(quadros, sufixo=""):
    """quadros: dict 'A'/'B'/'C' -> imagem 32x32."""
    linhas = [(NOMES[k], [im, pv.silhueta(im), pv.valores(im)]) for k, im in quadros.items()]
    pv.folha(linhas, k=8, larg_rotulo=230, titulo="Caçador — conceitos (idle, 32×32, mão da arma em 18,20)").save(
        os.path.join(OUT, f"cacador_conceitos{sufixo}.png"))

    cenas = []
    for k, im in quadros.items():
        c = cch.cena2(k)
        c = pv.cena(c, [(im, 48, 62, 16, 30)])
        # poste de luz à esquerda: só o brilho aditivo, como o spr_luz do jogo
        c = pv.brilho_aditivo(c, cch.luz(LUZES[k]), 14, 30)
        x1 = c
        x2 = c.resize((c.width * 2, c.height * 2), Image.NEAREST)
        x3 = c.resize((c.width * 3, c.height * 3), Image.NEAREST)
        cenas.append(pv.rotular(pv.lado_a_lado([x1, x2, x3], margem=6), NOMES[k] + "  —  1x · 2x · 3x"))
    # antes: o caçador antigo no mesmo tamanho
    old = antigo()
    cenas.append(pv.rotular(pv.lado_a_lado([old, old.resize((64, 64), Image.NEAREST), old.resize((96, 96), Image.NEAREST)], margem=6), "antigo (recusado) — 1x · 2x · 3x"))
    pv.empilha(cenas).save(os.path.join(OUT, f"cacador_conceitos_chao{sufixo}.png"))


def audita(quadros, paletas, sufixo=""):
    import numpy as np
    linhas = []
    mascaras = {}
    for k, im in quadros.items():
        cores = {c for r in paletas[k].values() for c in r}
        d = cch.DIRECOES[k]
        chaos = d["pedra"] + [d["junta"], d["luz"]]
        rel = au.audita_quadro(im, {"paleta": cores, "origem": (16, 30), "tier": (27, 30), "chaos": chaos,
                                     "contorno": "seletivo"})
        linhas.append(au.imprime(rel, NOMES[k]))
        mascaras[k] = np.array(im)[:, :, 3] > 0
    ks = list(quadros)
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            linhas.append(f"IoU {ks[i]}x{ks[j]} = {au.iou(mascaras[ks[i]], mascaras[ks[j]]):.2f}")
    txt = "\n".join(linhas)
    open(os.path.join(OUT, f"cacador_conceitos_auditoria{sufixo}.txt"), "w", encoding="utf-8").write(txt)
    return txt


if __name__ == "__main__":
    from personagens import conceito_esboco as ce
    from personagens import cacador_conceitos as cc
    ts = ce.todos()
    quadros = {k: t.imagem() for k, t in ts.items()}
    prancha(quadros)
    print(audita(quadros, {"A": cc.PAL_A, "B": cc.PAL_B, "C": cc.PAL_C}))
