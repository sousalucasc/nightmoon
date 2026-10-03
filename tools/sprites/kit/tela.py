"""Tela: onde as peças (carimbos) são montadas, com o mapa de material por pixel.

O mapa de material diz de que rampa veio cada pixel; o contorno usa isso pra escolher a cor
(contorno colorido / seletivo) e a auditoria pra saber o que é corpo, arma ou FX.
"""
import numpy as np
from PIL import Image


class Tela:
    def __init__(self, w, h, paleta):
        """paleta: dict rampa -> lista de RGB (escuro -> claro)."""
        self.w, self.h = w, h
        self.paleta = paleta
        self.px = np.zeros((h, w, 4), np.uint8)
        self.mat = np.full((h, w), "", dtype=object)   # rampa de cada pixel ('' = vazio)
        self.tom = np.full((h, w), -1, dtype=np.int16)
        self.grupo = np.full((h, w), "", dtype=object)  # 'corpo', 'arma', 'fx'... (pra auditoria)

    # --- pintar --------------------------------------------------------------
    def pinta(self, x, y, rampa, tom, grupo="corpo"):
        if 0 <= x < self.w and 0 <= y < self.h:
            r, g, b = self.paleta[rampa][tom][:3]
            self.px[y, x] = (r, g, b, 255)
            self.mat[y, x] = rampa
            self.tom[y, x] = tom
            self.grupo[y, x] = grupo

    def apaga(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y, x] = 0
            self.mat[y, x] = ""
            self.tom[y, x] = -1
            self.grupo[y, x] = ""

    def carimba(self, carimbo, x, y, espelha=False, grupo="corpo", so_vazio=False):
        """Prende o carimbo com a âncora em (x, y)."""
        c = carimbo.espelhado() if espelha else carimbo
        for dx, dy, rampa, tom in c.pixels():
            px, py = x + dx, y + dy
            if so_vazio and 0 <= px < self.w and 0 <= py < self.h and self.mat[py, px]:
                continue
            if rampa is None:
                self.apaga(px, py)
            else:
                self.pinta(px, py, rampa, tom, grupo)

    def cheio(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h and self.px[y, x, 3] > 0

    # --- contorno ---------------------------------------------------------------
    def contorno(self, escuro, claro=None, rampa_do_contorno=None, diagonais=False, grupos=None):
        """Contorno de 1 px em volta da silhueta.

        escuro: cor (rampa, tom) do contorno do lado da sombra.
        claro: dict rampa -> (rampa, tom) pro lado da luz (cima/esquerda): contorno seletivo.
               None = contorno igual em volta toda.
        rampa_do_contorno: dict rampa -> (rampa, tom) pra contorno colorido (o lado da sombra
               também muda de cor conforme o material vizinho).
        grupos: só contorna pixels destes grupos (ex.: {'corpo'}).
        """
        cheio = self.px[:, :, 3] > 0
        if grupos is not None:
            sel = np.isin(self.grupo, list(grupos))
            cheio = cheio & sel
        alvo = []
        viz4 = [(0, -1, True), (-1, 0, True), (1, 0, False), (0, 1, False)]
        viz = viz4 + ([(-1, -1, True), (1, -1, True), (-1, 1, False), (1, 1, False)] if diagonais else [])
        for y in range(self.h):
            for x in range(self.w):
                if self.px[y, x, 3] > 0:
                    continue
                vizinhos = []
                for dx, dy, lado_luz in viz:
                    # o pixel do corpo está em (x - dx, y - dy) visto deste vazio
                    bx, by = x - dx, y - dy
                    if 0 <= bx < self.w and 0 <= by < self.h and cheio[by, bx]:
                        vizinhos.append((self.mat[by, bx], lado_luz))
                if vizinhos:
                    alvo.append((x, y, vizinhos))
        for x, y, vizinhos in alvo:
            # luz de cima-esquerda: o vazio está ACIMA ou À ESQUERDA do corpo quando dy=-1/dx=-1
            luz = all(l for _, l in vizinhos)
            mat = vizinhos[0][0]
            cor = escuro
            if rampa_do_contorno and mat in rampa_do_contorno:
                cor = rampa_do_contorno[mat]
            if luz and claro and mat in claro:
                cor = claro[mat]
            self.pinta(x, y, cor[0], cor[1], grupo="contorno")

    # --- utilidades -------------------------------------------------------------
    def imagem(self):
        return Image.fromarray(self.px.copy(), "RGBA")

    def bbox(self, grupos=None):
        m = self.px[:, :, 3] > 0
        if grupos is not None:
            m = m & np.isin(self.grupo, list(grupos))
        ys, xs = np.nonzero(m)
        if len(xs) == 0:
            return None
        return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())

    def copia(self):
        t = Tela(self.w, self.h, self.paleta)
        t.px, t.mat, t.tom, t.grupo = self.px.copy(), self.mat.copy(), self.tom.copy(), self.grupo.copy()
        return t

    def desloca(self, dx, dy):
        t = Tela(self.w, self.h, self.paleta)
        for arr_src, arr_dst, vazio in ((self.px, t.px, 0), (self.mat, t.mat, ""), (self.tom, t.tom, -1), (self.grupo, t.grupo, "")):
            arr_dst[...] = vazio
            ys0, ys1 = max(0, dy), min(self.h, self.h + dy)
            xs0, xs1 = max(0, dx), min(self.w, self.w + dx)
            arr_dst[ys0:ys1, xs0:xs1] = arr_src[ys0 - dy:ys1 - dy, xs0 - dx:xs1 - dx]
        return t


def de_texto(texto, legenda, paleta, w=None, h=None, ox=0, oy=0, grupo="corpo", tela=None):
    """Pinta um quadro inteiro escrito em ASCII (cada caractere -> (rampa, tom))."""
    import textwrap
    linhas = textwrap.dedent(texto).split("\n")
    while linhas and not linhas[0].strip():
        linhas.pop(0)
    while linhas and not linhas[-1].strip():
        linhas.pop()
    W = w or max(len(l) for l in linhas)
    H = h or len(linhas)
    t = tela or Tela(W, H, paleta)
    for y, l in enumerate(linhas):
        for x, ch in enumerate(l):
            if ch in ". ":
                continue
            if ch not in legenda:
                raise ValueError(f"caractere {ch!r} sem legenda (linha {y}, coluna {x})")
            r, tom = legenda[ch]
            t.pinta(ox + x, oy + y, r, tom, grupo)
    return t


def de_segmentos(texto, legenda, paleta, w, h, grupo="corpo", tela=None, dx=0, dy=0):
    """Quadro escrito por linha: 'y: x0 texto' (o texto começa na coluna x0; '.' é vazio).

        3: 14 hhhh
        4: 13 hhhhhh
    Várias linhas com o mesmo y somam segmentos. Linhas vazias e comentários (#) são ignorados.
    """
    t = tela or Tela(w, h, paleta)
    for n, linha in enumerate(texto.strip("\n").split("\n")):
        linha = linha.split("#")[0].rstrip()
        if not linha.strip():
            continue
        try:
            ys, resto = linha.split(":", 1)
            y = int(ys)
            partes = resto.strip().split(" ", 1)
            x0 = int(partes[0])
            s = partes[1] if len(partes) > 1 else ""
        except ValueError:
            raise ValueError(f"linha {n} mal formada: {linha!r}")
        for i, ch in enumerate(s):
            if ch in ". ":
                continue
            if ch not in legenda:
                raise ValueError(f"caractere {ch!r} sem legenda (y={y}, x={x0 + i})")
            r, tom = legenda[ch]
            if r is None:
                t.apaga(x0 + i + dx, y + dy)
            else:
                t.pinta(x0 + i + dx, y + dy, r, tom, grupo)
    return t


def para_segmentos(tela, legenda):
    """Escreve a tela no formato 'y: x0 texto' usando a legenda (caractere -> (rampa, tom))."""
    inv = {v: k for k, v in legenda.items()}
    linhas = []
    for y in range(tela.h):
        xs = [x for x in range(tela.w) if tela.mat[y, x]]
        if not xs:
            continue
        x0, x1 = min(xs), max(xs)
        s = []
        for x in range(x0, x1 + 1):
            r = tela.mat[y, x]
            s.append(inv.get((r, int(tela.tom[y, x])), "?") if r else ".")
        linhas.append(f"{y}: {x0} {''.join(s)}")
    return "\n".join(linhas)
