"""Pintura à mão do quadro-base do caçador (idle 0), pra ajustar antes de virar carimbos."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import paleta as P  # noqa: E402
from kit import previa as pv  # noqa: E402
from kit.tela import de_segmentos  # noqa: E402
from personagens.cacador_leg import LEG  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "previa")

BASE = """
3: 12 oo
4: 11 o43o.oooo
5: 10 o4321o2321ooo
6: 10 o321101211012o
7: 10 o1000000000013o
8: 10 ogGGgtpppppGgo
9: 13 ohhPQPtPo
10: 13 oHhPQQQPPo
11: 12 oRhhpPQPpo
12: 12 ohotpPPpo
13: 12 o232WVW1o
14: 11 o4332wWw110o
15: 10 o433221W01100o
16: 9 o33222110G010co
17: 9 o322111000100co
18: 9 o2111010r0000o
19: 10 oottt00rWwoo
20: 11 o21100BNno
21: 11 o22110bBo0o
22: 11 o321210tr00o
23: 10 o23212100r0co
24: 10 o23212100r10co
25: 10 o232112100r0co
26: 9 o2231102100r10co
27: 9 o1121001000r000o
28: 9 oobnBooobnnNBooo
29: 10 obBno.obBnnNo
30: 10 ooooo.ooooooo
"""


def extensoes(texto):
    for l in texto.strip().splitlines():
        y, r = l.split(":", 1)
        x0, st = r.strip().split(" ", 1)
        print(f"{int(y):2d}: x{int(x0)}..x{int(x0) + len(st) - 1}  ({len(st)})")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        extensoes(BASE)
    t = de_segmentos(BASE, LEG, P.RAMPAS, 32, 32)
    im = t.imagem()
    pv.grade(im, k=20).save(os.path.join(OUT, "cacador_pinta_grade.png"))
    pv.folha([("base", [im, pv.silhueta(im), pv.valores(im)])], k=8, larg_rotulo=60).save(os.path.join(OUT, "cacador_pinta.png"))
    print("ok")
