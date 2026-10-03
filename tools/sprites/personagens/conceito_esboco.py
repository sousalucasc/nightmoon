"""Conceitos do caçador em esboço (máscara de partes + sombreamento automático do kit).

Só pra decidir silhueta e direção de arte na PARADA 1. O escolhido é repintado à mão.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kit import esboco as es  # noqa: E402
from kit import previa as pv  # noqa: E402
from kit.tela import Tela  # noqa: E402
from personagens import cacador_conceitos as cc  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "previa")


def mascara(texto, w=32, h=32):
    g = [["."] * w for _ in range(h)]
    for linha in texto.strip("\n").split("\n"):
        linha = linha.split("#")[0].rstrip()
        if not linha.strip():
            continue
        ys, resto = linha.split(":", 1)
        y = int(ys)
        x0, s = resto.strip().split(" ", 1)
        for i, ch in enumerate(s):
            if ch != ".":
                g[y][int(x0) + i] = ch
    return ["".join(r) for r in g]


C_MASC = """
2: 14 HHHHH
3: 14 HHHHH
4: 14 HHHHH
5: 14 HHHHH
6: 14 bbbbb
7: 12 hhhhhhhhh
8: 14 RFFFF
9: 14 RFFFFF
10: 14 RFFFF
11: 15 FFF
12: 14 KWWWK
13: 12 CCCCWWCCC
14: 11 CCCCCKkCCCC
15: 11 CCCCCKkCCCC
16: 11 CCCCCKkCCCCC
17: 12 CCCCKkCCCC
18: 13 KKKKKKK
19: 13 KKKKGGG
20: 13 KKKKKGGG
21: 12 KKKKKKKK
22: 12 KKKKKKKKK
23: 11 KKKKKKKKKKK
24: 11 KKKKKKKKKKKK
25: 10 KKKKKKKKKKKKK
26: 9 KKKKKKKKKKKKKKK
27: 8 KKKKKKKKKKKKKKKKK
28: 11 BBB...BBBB
29: 11 BBB...BBBBB
"""
A_MASC = """
2: 10 UU
3: 11 UUUU
4: 11 UUUUUU
5: 12 UUUUUZ
6: 12 UUUUSSZ
7: 12 UUUSSSSZ
8: 12 UUUSMMMMM
9: 13 UUUSMMMZ
10: 13 UUUUUUU
11: 11 CCCCCCCCCC
12: 10 CCCCCCCCCCCC
13: 10 CCCCCCCCCCCC
14: 9 CCCCCCCCCCCCC
15: 9 CCCCCCCCCCCCCC
16: 10 CC.CCCCCC.CC
17: 12 KKKKKKKK
18: 11 TTTTATTTT
19: 8 N..KKKKKKGGG
20: 7 NNNKKKKKKKGGG
21: 7 NYN.KKKKLLKKK
22: 7 NYN.KKKK.LLKKKK
23: 7 NNN.KKK..LL.KKK
24: 11 LL....LLL
25: 11 BBB...BBBB
26: 11 BBB...BBBB
27: 11 BBB...BBBB
28: 11 BBB...BBBBB
29: 10 BBBB..BBBBBB
"""
A_PARTES = {
    "U": es.Parte("manto", base=1.6, ganho=1.6, altura=3, projeta=True, frente=3, sombra=1, recorte=1),
    "S": es.Parte("manto", base=0.0, plano=True, frente=2),
    "Z": es.Parte("manto", base=3.0, plano=True, frente=3),
    "M": es.Parte("osso", base=1.4, ganho=0.9, altura=1, frente=2),
    "C": es.Parte("manto", base=1.8, ganho=1.6, altura=3, projeta=True, frente=2, sombra=2, recorte=1),
    "K": es.Parte("casaco", base=2.0, ganho=1.6, altura=3, frente=1, recorte=1),
    "T": es.Parte("couro", base=1.0, ganho=0.8, altura=1, frente=2),
    "A": es.Parte("ambar", base=1.4, plano=True, frente=2),
    "Y": es.Parte("ambar", base=1.6, ganho=0.8, altura=1, frente=3),
    "N": es.Parte("couro", base=0.6, plano=True, frente=3),
    "G": es.Parte("couro", base=1.4, ganho=1.0, altura=1, frente=3),
    "L": es.Parte("manto", base=0.8, ganho=1.0, altura=1, frente=0),
    "B": es.Parte("couro", base=1.0, ganho=1.0, altura=1),
}

B_MASC = """
6: 14 UUU
7: 13 UUUUU
8: 12 UUUUUUQ
9: 12 UUUUEQQQQ
10: 12 UUUUQQQQQQ
11: 7 P..PUUUqqqqqQQ
12: 6 PPPPPPPPP.....qQ
13: 5 PPPPPPPPPPPP
14: 4 PPPPPKKKKKKKK
15: 6 PPKKKKKKKKKK
16: 7 PKKKKKKKKKKK
17: 7 KKKKKKKKKKKGG
18: 7 KKKKKKKKKKKGG
19: 7 KKKKKKKKKKGGG
20: 7 KKKKKKKKKKGGG
21: 7 KKKKKKKKKK
22: 6 KKKK.LLLKKKK
23: 6 KKK..LLL.KKK
24: 6 KK...LLL..LLL
25: 6 K....LLL...LLL
26: 10 LLL....LLL
27: 10 LL......LLL
28: 9 BBB......BBBB
29: 9 BBB......BBBBB
"""
B_PARTES = {
    "U": es.Parte("penas", base=1.8, ganho=1.8, altura=2, projeta=True, frente=3, sombra=1, recorte=1),
    "Q": es.Parte("osso", base=1.5, ganho=1.0, altura=1, frente=4),
    "q": es.Parte("osso", base=0.3, plano=True, frente=4),
    "E": es.Parte("sangue", base=2.0, plano=True, frente=4),
    "P": es.Parte("penas", base=2.2, ganho=1.8, altura=2, projeta=True, frente=2, sombra=2, recorte=1),
    "K": es.Parte("penas", base=1.6, ganho=1.7, altura=3, frente=1, recorte=1),
    "G": es.Parte("penas", base=2.0, ganho=1.0, altura=1, frente=3),
    "L": es.Parte("penas", base=1.0, ganho=1.2, altura=1, frente=0),
    "B": es.Parte("penas", base=0.6, ganho=1.0, altura=1),
}

C_PARTES = {
    "H": es.Parte("casaco", base=1.0, ganho=1.4, altura=2, recorte=1),
    "b": es.Parte("forro", base=1.0, plano=True),
    "h": es.Parte("casaco", base=1.6, ganho=1.2, altura=1, projeta=True, frente=3, sombra=1),
    "R": es.Parte("casaco", base=0.6, plano=True),
    "F": es.Parte("pele", base=1.3, ganho=0.9, altura=2),
    "W": es.Parte("marfim", base=1.4, ganho=1.0, altura=1, frente=2),
    "C": es.Parte("casaco", base=2.0, ganho=1.8, altura=3, projeta=True, frente=2, sombra=2, recorte=1),
    "K": es.Parte("casaco", base=1.3, ganho=1.5, altura=3, frente=1, recorte=1),
    "k": es.Parte("forro", base=1.0, plano=True, frente=1),
    "G": es.Parte("couro", base=1.3, ganho=1.0, altura=1, frente=3),
    "B": es.Parte("couro", base=1.0, ganho=1.0, altura=1),
}


def render(masc, partes, paleta, contorno=("contorno", 0), retoques=None):
    linhas = mascara(masc)
    tons, grade = es.sombreia(linhas, partes)
    q = es.limpa_orfaos(es.quantiza(tons, paleta))
    t = Tela(32, 32, paleta)
    for (x, y), (r, tom) in q.items():
        t.pinta(x, y, r, tom)
    t.contorno(contorno)
    # retoques à mão (olho, acento, brilho): (x, y, rampa, tom)
    for x, y, r, tom in (retoques or []):
        if r is None:
            t.apaga(x, y)
        else:
            t.pinta(x, y, r, tom)
    return t


def todos():
    return {
        "A": render(A_MASC, A_PARTES, cc.PAL_A, retoques=[(17, 7, "osso", 2)]),
        "B": render(B_MASC, B_PARTES, cc.PAL_B),
        "C": render(C_MASC, C_PARTES, cc.PAL_C, retoques=[(17, 9, "contorno", 0)]),
    }


if __name__ == "__main__":
    ts = todos()
    linhas = []
    for k, t in ts.items():
        im = t.imagem()
        linhas.append((k, [im, pv.silhueta(im), pv.valores(im)]))
        pv.grade(im, k=20).save(os.path.join(OUT, f"esboco_{k}_grade.png"))
    pv.folha(linhas, k=8, larg_rotulo=40).save(os.path.join(OUT, "esboco_todos.png"))
    print("ok")
