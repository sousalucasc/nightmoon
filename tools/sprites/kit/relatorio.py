"""Relatório de um personagem: folha, GIFs, cebola, auditoria por quadro e de animação."""
import os

import numpy as np

from . import auditoria as au
from . import previa as pv

PREVIA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "previa")


def audita_anims(nome, anims, ctx_base, ctx_por_anim=None, laços=("idle", "walk"), dano=("hit", "idle")):
    """anims: dict anim -> lista de PIL. Devolve (texto, n_erros, n_avisos)."""
    ctx_por_anim = ctx_por_anim or {}
    linhas = [f"# Auditoria — {nome}"]
    erros = avisos = 0
    for anim, qs in anims.items():
        ctx = dict(ctx_base)
        ctx.update(ctx_por_anim.get(anim, {}))
        for i, q in enumerate(qs):
            c = dict(ctx)
            if callable(c.get("tier")):
                c["tier"] = c["tier"](anim, i)
            if "pula_origem" in c and (anim, i) in c["pula_origem"]:
                c.pop("origem", None)
            rel = au.audita_quadro(q, c)
            e = [r for r in rel if r.nivel == "ERRO"]
            v = [r for r in rel if r.nivel == "AVISO" and r.nome not in c.get("avisos_ok", ())]
            erros += len(e)
            avisos += len(v)
            if e or v:
                linhas.append(f"{anim}[{i}]: " + "; ".join(f"{r.nivel} {r.nome} {r.valor} {r.msg}".strip() for r in e + v))
        # animação: quadros iguais seguidos, emenda do laço
        for i in range(1, len(qs)):
            if np.array_equal(np.array(qs[i - 1]), np.array(qs[i])):
                linhas.append(f"{anim}: AVISO quadros_iguais {i - 1} e {i}")
                avisos += 1
        if anim in laços and len(qs) > 1 and np.array_equal(np.array(qs[-1]), np.array(qs[0])):
            linhas.append(f"{anim}: AVISO emenda_laco (último = primeiro)")
            avisos += 1
    if dano[0] in anims and dano[1] in anims:
        m1 = np.array(anims[dano[0]][0])[:, :, 3] > 0
        m2 = np.array(anims[dano[1]][0])[:, :, 3] > 0
        i = au.iou(m1, m2)
        nivel = "ok" if i < 0.8 else "AVISO"
        if nivel == "AVISO":
            avisos += 1
        linhas.append(f"silhueta_dano: IoU({dano[0]}[0], {dano[1]}[0]) = {i:.2f} ({nivel})")
    linhas.insert(1, f"{erros} erro · {avisos} avisos")
    return "\n".join(linhas), erros, avisos


def previas(nome, anims, duracoes, k=5):
    """Folha de todas as animações, GIF e cebola de cada uma, em tools/sprites/previa/."""
    os.makedirs(PREVIA, exist_ok=True)
    pv.folha([(a, qs) for a, qs in anims.items()], k=k, larg_rotulo=110, titulo=nome).save(
        os.path.join(PREVIA, f"{nome}_folha.png"))
    for a, qs in anims.items():
        if len(qs) > 1:
            pv.gif(qs, duracoes[a], os.path.join(PREVIA, f"{nome}_{a}.gif"), k=4)
            pv.cebola(qs, k=4).save(os.path.join(PREVIA, f"{nome}_{a}_cebola.png"))
