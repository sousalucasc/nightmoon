"""Auditoria automática: mede a higiene da sprite. Não mede qualidade (isso é a rubrica visual).

    rel = audita_quadro(img, ctx)   # lista de Item(nivel, nome, valor, msg)
    imprime(rel)

ctx (dict) aceita:
    paleta: conjunto de RGB registrados (so_paleta)
    origem: (ox, oy) do quadro
    teto: teto de cores (padrão pelo tier)
    tier: altura alvo do corpo (px), ou (min, max)
    mascara_corpo: array bool (h, w) só do corpo (sem arma/fx); padrão = alfa > 0
    mascara_cabeca: array bool da cabeça (com chapéu/capuz)
    chaos: lista de RGB dos chãos do jogo (contraste)
    personagem_escuro: bool
    solto_ok: lista de (x, y) com pixel solto intencional
    acentos: conjunto de RGB de acento permitidos; acento_rampas: idem, só pra informar
    contorno: 'fechado' | 'seletivo' | 'nenhum'
    cores_contorno: conjunto de RGB que contam como contorno
    borda_ok: conjunto de lados que podem encostar ('cima','baixo','esq','dir')
    gemeas_ok: lista de pares (rgb, rgb) gêmeos de propósito
    fx: True pra efeito (não exige contorno, origem nem altura)
"""
from dataclasses import dataclass

import numpy as np

from . import paleta as pal

# faixa comercial (17 sprites de 25 a 59 px; ver conhecimento/10_auditoria.md)
LIMITES = {
    "peq": (42, 66),        # % de aglomerados de 1-2 px
    "dens": (10, 28),       # aglomerados por 100 px do miolo
    "orfaos": (0, 6.3),     # por 100 px
    "xadrez": (0, 3.8),     # por 100 px
    "alcance": 20,          # p95 - p5 de L* mínimo
}
CABECA_TIER = [(24, (33, 55)), (32, (22, 34)), (48, (16, 26)), (9999, (12, 21))]
TETO_TIER = [(16, 12), (32, 20), (64, 32), (128, 48), (99999, 256)]


@dataclass
class Item:
    nivel: str   # ERRO, AVISO, ok
    nome: str
    valor: str
    msg: str = ""


def _cores(a):
    m = a[:, :, 3] > 0
    return {tuple(int(v) for v in c) for c in a[m][:, :3]}


def _rotula(m):
    """Componentes 4-conexos de uma máscara bool. Devolve (rótulos, n)."""
    h, w = m.shape
    lab = np.zeros((h, w), np.int32)
    n = 0
    for y in range(h):
        for x in range(w):
            if m[y, x] and lab[y, x] == 0:
                n += 1
                pilha = [(x, y)]
                lab[y, x] = n
                while pilha:
                    cx, cy = pilha.pop()
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < w and 0 <= ny < h and m[ny, nx] and lab[ny, nx] == 0:
                            lab[ny, nx] = n
                            pilha.append((nx, ny))
    return lab, n


def audita_quadro(img, ctx=None):
    ctx = ctx or {}
    a = np.array(img.convert("RGBA"))
    h, w = a.shape[:2]
    alfa = a[:, :, 3]
    cheio = alfa > 0
    rel = []
    fx = ctx.get("fx", False)

    if not cheio.any():
        return [Item("ERRO", "quadro_vazio", "0 px")]

    # ---- regra -------------------------------------------------------------
    parcial = int(((alfa > 0) & (alfa < 255)).sum())
    rel.append(Item("ERRO" if parcial else "ok", "alfa_binario", f"{parcial} px com alfa parcial"))

    cores = _cores(a)
    if "paleta" in ctx:
        fora = [c for c in cores if c not in ctx["paleta"]]
        rel.append(Item("ERRO" if fora else "ok", "so_paleta", f"{len(fora)} cores fora",
                        ", ".join(pal.hexa(c) for c in fora[:6])))

    ys, xs = np.nonzero(cheio)
    lados = {"cima": ys.min() == 0, "baixo": ys.max() == h - 1, "esq": xs.min() == 0, "dir": xs.max() == w - 1}
    toca = [k for k, v in lados.items() if v and k not in ctx.get("borda_ok", set())]
    rel.append(Item("ERRO" if toca else "ok", "borda_da_tela", ", ".join(toca) or "não encosta"))

    corpo = ctx.get("mascara_corpo")
    if corpo is None:
        corpo = cheio
    cys, cxs = np.nonzero(corpo)
    if not fx and "origem" in ctx:
        ox, oy = ctx["origem"]
        sola = int(cys.max())
        dx = abs((cxs.min() + cxs.max()) / 2 - ox)
        ok = abs(sola - oy) <= 1 and dx <= 6
        rel.append(Item("ok" if ok else "ERRO", "origem", f"sola na linha {sola} (origem {oy}), centro a {dx:.1f} px do x da origem"))

    # contorno fechado: pixels da borda da silhueta que são contorno
    borda = cheio & ~(np.pad(cheio, 1)[2:, 1:-1] & np.pad(cheio, 1)[:-2, 1:-1] & np.pad(cheio, 1)[1:-1, 2:] & np.pad(cheio, 1)[1:-1, :-2])
    estilo = ctx.get("contorno", "fechado")
    if not fx and estilo != "nenhum":
        cc = ctx.get("cores_contorno")
        if cc:
            eh = np.array([[tuple(int(v) for v in a[y, x, :3]) in cc for x in range(w)] for y in range(h)])
        else:
            lum = np.array([[pal.L(tuple(int(v) for v in a[y, x, :3])) if cheio[y, x] else 100 for x in range(w)] for y in range(h)])
            eh = lum < 18
        frac = (borda & eh).sum() / max(1, borda.sum())
        if estilo == "fechado":
            rel.append(Item("ok" if frac >= 0.97 else "ERRO", "contorno_fechado", f"{frac:.0%} da borda é contorno"))
        else:
            rel.append(Item("ok" if frac >= 0.6 else "AVISO", "contorno_seletivo", f"{frac:.0%} da borda é contorno"))

    # ---- cor ---------------------------------------------------------------
    alt_corpo = int(cys.max() - cys.min() + 1)
    teto = ctx.get("teto") or next(t for lim, t in TETO_TIER if alt_corpo <= lim)
    rel.append(Item("ok" if len(cores) <= teto else "AVISO", "teto_cores", f"{len(cores)} cores (teto {teto})"))

    ok_pares = {frozenset(p) for p in ctx.get("gemeas_ok", [])}
    gem = [g for g in pal.gemeas(cores) if frozenset((g[0], g[1])) not in ok_pares]
    rel.append(Item("AVISO" if gem else "ok", "cores_gemeas", f"{len(gem)} pares ΔE<5",
                    "; ".join(f"{pal.hexa(x)}~{pal.hexa(y)} ({d:.1f})" for x, y, d in gem[:5])))

    if ctx.get("acentos") is not None and ctx.get("acentos_proibidos"):
        ruins = [c for c in cores if c in ctx["acentos_proibidos"]]
        rel.append(Item("AVISO" if ruins else "ok", "acento", f"{len(ruins)} cores de acento fora do lugar"))

    if ctx.get("chaos") and not fx:
        # cor média da borda da silhueta contra cada chão
        bc = [tuple(int(v) for v in a[y, x, :3]) for y, x in zip(*np.nonzero(borda))]
        lum_b = np.median([pal.luminancia(c) for c in bc])
        piores = []
        for ch in ctx["chaos"]:
            lc = pal.luminancia(ch)
            r = (max(lum_b, lc) + 0.05) / (min(lum_b, lc) + 0.05)
            piores.append(r)
        pior = min(piores)
        rel.append(Item("ok" if pior >= 2 else "AVISO", "contraste_chao", f"pior razão {pior:.2f}:1 (borda contra chão)"))

    # ---- limpeza -------------------------------------------------------------
    solto_ok = set(map(tuple, ctx.get("solto_ok", [])))
    orf = []
    for y in range(h):
        for x in range(w):
            if not cheio[y, x] or borda[y, x]:
                continue
            c = tuple(a[y, x, :3])
            igual = False
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and cheio[ny, nx] and tuple(a[ny, nx, :3]) == c:
                        igual = True
            if not igual and (x, y) not in solto_ok:
                orf.append((x, y))
    rel.append(Item("AVISO" if orf else "ok", "pixel_solto", f"{len(orf)} órfãos no miolo", str(orf[:8]) if orf else ""))

    # nós: pixel da silhueta com só 1 vizinho cheio (4-viz) = ponta de 1 px
    nos = []
    furos = []
    for y in range(h):
        for x in range(w):
            n4 = sum(1 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                     if 0 <= x + dx < w and 0 <= y + dy < h and cheio[y + dy, x + dx])
            if cheio[y, x] and n4 == 1:
                nos.append((x, y))
            if not cheio[y, x] and n4 >= 3 and 0 < x < w - 1 and 0 < y < h - 1:
                furos.append((x, y))
    if not fx:
        rel.append(Item("AVISO" if nos else "ok", "nos_1px", f"{len(nos)} pontas de 1 px", str(nos[:8]) if nos else ""))
        rel.append(Item("AVISO" if furos else "ok", "furos_1px", f"{len(furos)} furos de 1 px", str(furos[:8]) if furos else ""))

    # xadrez 2x2 de duas cores
    xad = 0
    for y in range(h - 1):
        for x in range(w - 1):
            if cheio[y:y + 2, x:x + 2].all():
                p = a[y:y + 2, x:x + 2, :3]
                c00, c01, c10, c11 = map(tuple, (p[0, 0], p[0, 1], p[1, 0], p[1, 1]))
                if c00 == c11 and c01 == c10 and c00 != c01:
                    xad += 1
    rel.append(Item("AVISO" if xad > 2 else "ok", "pontilhado", f"{xad} xadrez 2x2"))

    # aglomerados no miolo (sem a borda)
    miolo = cheio & ~borda
    area = max(1, int(miolo.sum()))
    tamanhos = []
    for c in cores:
        m = miolo & np.all(a[:, :, :3] == np.array(c, np.uint8), axis=2)
        if not m.any():
            continue
        lab, n = _rotula(m)
        for i in range(1, n + 1):
            tamanhos.append(int((lab == i).sum()))
    if tamanhos:
        peq = 100 * sum(1 for t in tamanhos if t <= 2) / len(tamanhos)
        dens = 100 * len(tamanhos) / area
        orf100 = 100 * len(orf) / area
        xad100 = 100 * xad / area
        fora = []
        if not LIMITES["peq"][0] <= peq <= LIMITES["peq"][1]:
            fora.append("pequenos")
        if not LIMITES["dens"][0] <= dens <= LIMITES["dens"][1]:
            fora.append("densidade")
        if orf100 > LIMITES["orfaos"][1]:
            fora.append("órfãos")
        if xad100 > LIMITES["xadrez"][1]:
            fora.append("xadrez")
        rel.append(Item("AVISO" if fora else "ok", "aglomerados",
                        f"pequenos {peq:.0f}% · densidade {dens:.1f}/100px · órfãos {orf100:.1f} · xadrez {xad100:.1f}",
                        ("fora da faixa: " + ", ".join(fora)) if fora else ""))

    # ---- luz -----------------------------------------------------------------
    if not fx:
        Lm = np.zeros((h, w))
        for y, x in zip(*np.nonzero(cheio)):
            Lm[y, x] = pal.L(tuple(int(v) for v in a[y, x, :3]))
        vals = Lm[miolo] if miolo.any() else Lm[cheio]
        alc = float(np.percentile(vals, 95) - np.percentile(vals, 5))
        rel.append(Item("ok" if alc >= LIMITES["alcance"] else "AVISO", "alcance_valor", f"L* p95-p5 = {alc:.0f}"))
        # direção: média de L* na metade de cima-esquerda x baixo-direita do miolo
        cy, cx = np.nonzero(miolo) if miolo.any() else np.nonzero(cheio)
        mx, my = cx.mean(), cy.mean()
        d = (cx - mx) + (cy - my)  # > 0 = baixo-direita
        ce = Lm[cy[d < 0], cx[d < 0]].mean() if (d < 0).any() else 0
        bd = Lm[cy[d > 0], cx[d > 0]].mean() if (d > 0).any() else 0
        rel.append(Item("ok" if ce >= bd else "AVISO", "direcao", f"L* cima-esq {ce:.0f} x baixo-dir {bd:.0f}"))
        # travesseiro: a coroa interna (vizinha da borda) mais escura que o centro em TODOS os lados
        anel = miolo & ~(np.pad(miolo, 1)[2:, 1:-1] & np.pad(miolo, 1)[:-2, 1:-1] & np.pad(miolo, 1)[1:-1, 2:] & np.pad(miolo, 1)[1:-1, :-2])
        centro = miolo & ~anel
        if centro.any() and anel.any():
            ay, ax = np.nonzero(anel)
            lados_L = []
            for sel in (ax < mx, ax > mx, ay < my, ay > my):
                if sel.any():
                    lados_L.append(Lm[ay[sel], ax[sel]].mean())
            Lc = Lm[centro].mean()
            trav = all(l < Lc - 6 for l in lados_L)
            rel.append(Item("AVISO" if trav else "ok", "travesseiro", f"centro L* {Lc:.0f}, lados {', '.join(f'{l:.0f}' for l in lados_L)}"))
        mx_L = float(Lm[cheio].max())
        rel.append(Item("ok" if mx_L >= 55 else "AVISO", "acende_no_escuro", f"L* máx {mx_L:.0f}"))

    # ---- leitura -------------------------------------------------------------
    if not fx:
        alvo = ctx.get("tier")
        if alvo:
            lo, hi = alvo if isinstance(alvo, tuple) else (alvo - 2, alvo + 2)
            rel.append(Item("ok" if lo <= alt_corpo <= hi else "AVISO", "altura", f"corpo {alt_corpo} px (alvo {lo}-{hi})"))
        else:
            rel.append(Item("ok", "altura", f"corpo {alt_corpo} px"))
        bx = cxs.min(), cys.min(), cxs.max(), cys.max()
        rel.append(Item("ok", "caixa", f"x {bx[0]}-{bx[2]}, y {bx[1]}-{bx[3]} ({bx[2]-bx[0]+1}×{alt_corpo})"))
        cab = ctx.get("mascara_cabeca")
        if cab is not None and cab.any():
            hy = np.nonzero(cab)[0]
            alt_cab = hy.max() - hy.min() + 1
            pct = 100 * alt_cab / alt_corpo
            faixa = next(f for lim, f in CABECA_TIER if alt_corpo <= lim)
            rel.append(Item("ok" if faixa[0] <= pct <= faixa[1] else "AVISO", "proporcao_cabeca",
                            f"cabeça {alt_cab} px = {pct:.0f}% da altura (faixa {faixa[0]}-{faixa[1]}%) · {alt_corpo/alt_cab:.1f} cabeças"))
    return rel


def resumo(rel):
    e = sum(1 for i in rel if i.nivel == "ERRO")
    v = sum(1 for i in rel if i.nivel == "AVISO")
    return f"{e} erro · {v} avisos"


def imprime(rel, titulo=""):
    linhas = [f"== {titulo} ==  {resumo(rel)}"] if titulo else [resumo(rel)]
    for i in rel:
        marca = {"ERRO": "ERRO ", "AVISO": "aviso", "ok": "  ok "}[i.nivel]
        linhas.append(f"  {marca} {i.nome:18s} {i.valor}" + (f"  — {i.msg}" if i.msg else ""))
    return "\n".join(linhas)


def iou(m1, m2):
    i = (m1 & m2).sum()
    u = (m1 | m2).sum()
    return i / u if u else 0.0
