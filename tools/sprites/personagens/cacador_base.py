"""Bancada do quadro-base do caçador (idle 0): máscara de partes -> esboço -> ASCII pra pintar.

Só ferramenta de trabalho: o módulo final é personagens/cacador.py (carimbos pintados à mão).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import paleta as P  # noqa: E402
from kit import esboco as es  # noqa: E402
from kit import previa as pv  # noqa: E402
from kit.tela import Tela, para_segmentos  # noqa: E402
from personagens.conceito_esboco import mascara  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "previa")

MASC = """
4: 12 HH
5: 11 HHHH.HHHH
6: 11 HHHHHHHHHHHH
7: 10 HHHHHHHHHHHHHH
8: 12 GGGFFFFFFG
9: 13 hhFFFFFFF
10: 12 khhFFFFF
11: 12 kkhFFFF
12: 14 hFFF
13: 12 CCCWWWC
14: 10 CCCCCWWCCCC
15: 9 CCCCCCCWCCCCC
16: 9 CCCCCCCuLCCCCC
17: 9 CCCCCCCKLCCCCC
18: 10 CCCCCCKLCCCC
19: 12 KKKKKuLMM
20: 12 KKKKKKLMMM
21: 12 KKKKKKKLMM
22: 11 KKKKKKKKLKK
23: 11 KKKKKKKKLKKK
24: 10 KKKKKKKKKLKKK
25: 10 KKKKKKKKKLKKKK
26: 9 KKKKKKKKKKLKKKK
27: 9 KKKKKKKKKKLKKKKK
28: 11 BBB....BBBB
29: 11 BBB....BBBBB
"""
PARTES = {
    "H": es.Parte("casaco", base=1.6, ganho=1.4, altura=2, projeta=True, frente=4, sombra=2, recorte=1),
    "G": es.Parte("ouro", base=1.0, plano=True, frente=4),
    "h": es.Parte("cabelo", base=1.0, ganho=1.0, altura=1, frente=1),
    "k": es.Parte("forro", base=1.0, plano=True, frente=1),
    "F": es.Parte("pele", base=1.6, ganho=1.0, altura=2, frente=2),
    "W": es.Parte("marfim", base=1.4, ganho=1.0, altura=1, frente=3),
    "C": es.Parte("casaco", base=2.2, ganho=1.8, altura=3, projeta=True, frente=2, sombra=2, recorte=1),
    "K": es.Parte("casaco", base=1.4, ganho=1.5, altura=3, frente=1, recorte=1),
    "L": es.Parte("forro", base=0.6, plano=True, frente=1),
    "u": es.Parte("ouro", base=1.4, plano=True, frente=3),
    "M": es.Parte("couro", base=2.0, ganho=1.0, altura=1, frente=3),
    "B": es.Parte("couro", base=1.4, ganho=1.0, altura=1),
}


def render():
    linhas = mascara(MASC)
    tons, grade = es.sombreia(linhas, PARTES)
    q = es.limpa_orfaos(es.quantiza(tons, P.RAMPAS))
    t = Tela(32, 32, P.RAMPAS)
    for (x, y), (r, tom) in q.items():
        t.pinta(x, y, r, tom)
    t.contorno(("contorno", 0))
    return t


if __name__ == "__main__":
    t = render()
    im = t.imagem()
    pv.grade(im, k=20).save(os.path.join(OUT, "cacador_base_grade.png"))
    pv.folha([("base", [im, pv.silhueta(im), pv.valores(im)])], k=8, larg_rotulo=60).save(os.path.join(OUT, "cacador_base.png"))
    from personagens.cacador_leg import LEG
    print(para_segmentos(t, LEG))
