"""Esboço: sombreamento automático por partes (SÓ pra conceito e base de pintura).

Desenha-se a silhueta em ASCII com um caractere por PARTE (chapéu, rosto, capa...). O esboço
calcula um tom por pixel com luz de cima-esquerda (planos, não travesseiro): a borda virada pra
luz acende, a de costas escurece, o miolo fica no tom base; uma parte por cima de outra projeta
sombra dura logo abaixo dela. Depois o tom vira ASCII de dígitos pra ser repintado à mão.

    partes = {"C": Parte("capa", base=2, altura=3, projeta=True), ...}
    tons = sombreia(mascara_ascii, partes)          # dict (x, y) -> (rampa, tom)
"""
from dataclasses import dataclass

import numpy as np


@dataclass
class Parte:
    rampa: str
    base: float = 2.0       # tom do plano de frente (índice na rampa, pode ser fracionário)
    ganho: float = 1.6      # quanto a luz muda o tom (em tons)
    altura: int = 3         # "espessura" da forma: até quantos px da borda ainda curva
    projeta: bool = False   # projeta sombra dura nas partes de baixo
    sombra: int = 2         # alcance da sombra projetada (px)
    frente: int = 0         # ordem: quem está na frente projeta em quem está atrás
    plano: bool = False     # chapado (osso, metal pequeno): sem curva, só base
    recorte: int = 0        # +tons no fio da borda de baixo-direita (luz de trás)


def _distancia(m):
    """Distância (chessboard) de cada pixel da máscara até fora dela."""
    h, w = m.shape
    INF = 99
    d = np.where(m, INF, 0).astype(np.int32)
    # duas passadas (chamfer 8-viz)
    for y in range(h):
        for x in range(w):
            if d[y, x]:
                v = d[y, x]
                for dx, dy in ((-1, 0), (0, -1), (-1, -1), (1, -1)):
                    nx, ny = x + dx, y + dy
                    vv = d[ny, nx] + 1 if 0 <= nx < w and 0 <= ny < h else 1
                    v = min(v, vv)
                d[y, x] = v
    for y in range(h - 1, -1, -1):
        for x in range(w - 1, -1, -1):
            if d[y, x]:
                v = d[y, x]
                for dx, dy in ((1, 0), (0, 1), (1, 1), (-1, 1)):
                    nx, ny = x + dx, y + dy
                    vv = d[ny, nx] + 1 if 0 <= nx < w and 0 <= ny < h else 1
                    v = min(v, vv)
                d[y, x] = v
    return d


def sombreia(linhas, partes, luz=(-1.0, -1.25, 1.1), n_tons=None):
    """linhas: lista de strings (máscara de partes). Devolve dict (x, y) -> (rampa, tom int)."""
    h = len(linhas)
    w = max(len(l) for l in linhas)
    grade = np.full((h, w), ".", dtype="<U1")
    for y, l in enumerate(linhas):
        for x, ch in enumerate(l):
            grade[y, x] = ch
    L = np.array(luz, float)
    L /= np.linalg.norm(L)
    out = {}
    for ch, p in partes.items():
        m = grade == ch
        if not m.any():
            continue
        d = _distancia(m).astype(float)
        alt = np.minimum(d, p.altura)
        # perfil arredondado: sobe rápido na borda
        alt = np.where(m, np.sqrt(alt / p.altura) * p.altura, 0)
        gx = np.zeros_like(alt)
        gy = np.zeros_like(alt)
        gx[:, 1:-1] = (alt[:, 2:] - alt[:, :-2]) / 2
        gy[1:-1, :] = (alt[2:, :] - alt[:-2, :]) / 2
        gx[:, 0] = alt[:, 1] - alt[:, 0]
        gx[:, -1] = alt[:, -1] - alt[:, -2]
        gy[0, :] = alt[1, :] - alt[0, :]
        gy[-1, :] = alt[-1, :] - alt[-2, :]
        ys, xs = np.nonzero(m)
        for y, x in zip(ys, xs):
            if p.plano:
                t = p.base
            else:
                n = np.array([-gx[y, x], -gy[y, x], 1.0])
                n /= np.linalg.norm(n)
                s = float(n @ L) - float(np.array([0, 0, 1.0]) @ L)  # 0 no plano de frente
                t = p.base + p.ganho * s * 2.2
            # sombra projetada por partes da frente, logo acima
            for ch2, p2 in partes.items():
                if ch2 == ch or not p2.projeta or p2.frente <= p.frente:
                    continue
                for k in range(1, p2.sombra + 1):
                    if y - k >= 0 and grade[y - k, x] == ch2:
                        t -= 1.2 if k == 1 else 0.7
                        break
            # recorte na borda de baixo-direita
            if p.recorte and ((x + 1 >= w or grade[y, x + 1] == ".") or (y + 1 >= h or grade[y + 1, x] == ".")):
                if not (x - 1 < 0 or grade[y, x - 1] == ".") and not (y - 1 < 0 or grade[y - 1, x] == "."):
                    t += p.recorte
            out[(int(x), int(y))] = (p.rampa, t)
    return out, grade


def quantiza(tons, paleta):
    q = {}
    for (x, y), (r, t) in tons.items():
        n = len(paleta[r])
        q[(x, y)] = (r, int(max(0, min(n - 1, round(t)))))
    return q


def para_ascii(q, grade, codigos, w=None, h=None):
    """Converte (rampa, tom) em caracteres da legenda (codigos: (rampa, tom) -> char)."""
    h = h or grade.shape[0]
    w = w or grade.shape[1]
    linhas = []
    for y in range(h):
        s = []
        for x in range(w):
            v = q.get((x, y))
            s.append(codigos.get(v, "?") if v else ".")
        linhas.append("".join(s))
    return linhas


def limpa_orfaos(q, passes=2):
    """Esboço: troca o tom de pixel sem vizinho igual (8-viz) pelo tom mais comum dos vizinhos da
    mesma rampa. Só pra conceito; no refino o conserto é no carimbo."""
    for _ in range(passes):
        novo = dict(q)
        for (x, y), (r, t) in q.items():
            viz = [q.get((x + dx, y + dy)) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0)]
            viz = [v for v in viz if v]
            if any(v == (r, t) for v in viz):
                continue
            mesmos = [v[1] for v in viz if v[0] == r]
            if len(mesmos) >= 3:
                novo[(x, y)] = (r, max(set(mesmos), key=mesmos.count))
        q = novo
    return q


def limpa_xadrez(q, passes=2):
    """Esboço: desfaz xadrez 2×2 (a b / b a) puxando o pixel de cima-direita pro tom de cima-esquerda."""
    for _ in range(passes):
        mudou = False
        for (x, y), a in list(q.items()):
            b = q.get((x + 1, y))
            c = q.get((x, y + 1))
            d = q.get((x + 1, y + 1))
            if b and c and d and a == d and b == c and a != b and a[0] == b[0]:
                q[(x + 1, y)] = a
                mudou = True
        if not mudou:
            break
    return q


def pecas_de_mascara(linhas, partes, paleta, codigos, agrupa=None):
    """Sombreia a máscara inteira (com sombra projetada entre partes) e devolve um dict
    grupo -> texto de segmentos ('y: x0 ...'), pra virar carimbo e ser retocado à mão.

    codigos: (rampa, tom) -> caractere da legenda. agrupa: parte -> grupo (padrão: a própria parte).
    """
    tons, grade = sombreia(linhas, partes)
    q = limpa_xadrez(limpa_orfaos(quantiza(tons, paleta)))
    agrupa = agrupa or {}
    por_grupo = {}
    for (x, y), v in q.items():
        g = agrupa.get(grade[y, x], grade[y, x])
        por_grupo.setdefault(g, {})[(x, y)] = codigos[v]
    out = {}
    for g, px in por_grupo.items():
        ys = sorted({y for _, y in px})
        txt = []
        for y in ys:
            xs = sorted(x for x, yy in px if yy == y)
            x0, x1 = xs[0], xs[-1]
            s = "".join(px.get((x, y), ".") for x in range(x0, x1 + 1))
            txt.append(f"{y}: {x0} {s}")
        out[g] = "\n".join(txt)
    return out


def mascara_seg(texto, w, h):
    """Máscara em segmentos 'y: x0 texto' -> lista de linhas de largura w."""
    g = [["."] * w for _ in range(h)]
    for linha in texto.strip("\n").split("\n"):
        linha = linha.split("#")[0].rstrip()
        if not linha.strip():
            continue
        ys, resto = linha.split(":", 1)
        x0, s = resto.strip().split(" ", 1)
        for i, ch in enumerate(s):
            if ch != ".":
                g[int(ys)][int(x0) + i] = ch
    return ["".join(r) for r in g]
