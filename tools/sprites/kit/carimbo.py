"""Carimbo: peça pintada à mão em ASCII, um caractere por pixel, com âncora.

    LEG = {"1": ("casaco", 1), "o": ("contorno", 0), ...}   # caractere -> (rampa, tom)
    CABECA = Carimbo('''
        ..oo..
        .o12o.
    ''', LEG, ancora=(2, 1))

- '.' e ' ' são transparentes.
- A âncora é o ponto do esqueleto onde a peça se prende (pescoço, ombro, quadril...).
  Ela também pode vir marcada com '@' no desenho (o pixel do '@' vira transparente, ou
  `sob='x'` pra pintá-lo com a cor do caractere 'x').
- O texto é aparado das linhas vazias de cima e de baixo e da indentação comum.
"""
import textwrap


class Carimbo:
    def __init__(self, texto, legenda, ancora=(0, 0), sob=".", nome=""):
        linhas = textwrap.dedent(texto).split("\n")
        while linhas and not linhas[0].strip():
            linhas.pop(0)
        while linhas and not linhas[-1].strip():
            linhas.pop()
        w = max(len(l) for l in linhas) if linhas else 0
        self.linhas = [l.ljust(w, ".") for l in linhas]
        self.legenda = legenda
        self.nome = nome
        self.w, self.h = w, len(self.linhas)
        self.ancora = ancora
        for y, l in enumerate(self.linhas):
            x = l.find("@")
            if x >= 0:
                self.ancora = (x, y)
                self.linhas[y] = l[:x] + sob + l[x + 1:]
        for y, l in enumerate(self.linhas):
            for x, ch in enumerate(l):
                if ch not in ".  " and ch not in legenda:
                    raise ValueError(f"carimbo {nome!r}: caractere {ch!r} sem legenda na linha {y}, coluna {x}")

    def pixels(self):
        """(dx, dy, rampa, tom) relativos à âncora."""
        ax, ay = self.ancora
        for y, l in enumerate(self.linhas):
            for x, ch in enumerate(l):
                if ch in ". ":
                    continue
                rampa, tom = self.legenda[ch]
                yield x - ax, y - ay, rampa, tom

    def espelhado(self):
        """Cópia espelhada na horizontal (a âncora vai junto)."""
        c = Carimbo.__new__(Carimbo)
        c.linhas = [l[::-1] for l in self.linhas]
        c.legenda, c.nome, c.w, c.h = self.legenda, self.nome + "~", self.w, self.h
        c.ancora = (self.w - 1 - self.ancora[0], self.ancora[1])
        return c

    def troca(self, mapa):
        """Cópia com caracteres trocados (variante de cor), ex.: {'1': '2'}."""
        c = Carimbo.__new__(Carimbo)
        c.linhas = ["".join(mapa.get(ch, ch) for ch in l) for l in self.linhas]
        c.legenda, c.nome, c.w, c.h, c.ancora = self.legenda, self.nome, self.w, self.h, self.ancora
        return c
