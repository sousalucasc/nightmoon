"""Bancada do aldeão novo (2ª rodada): quadro-base pintado à mão, antes de virar carimbos.

Volta 2: planos grandes (luz de cima-esquerda), um tom de sombra e um de luz por material,
tons cortados (sem linho0/madeira1, gêmeos do doente0/couro1)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LEG = {
    "o": ("contorno", 0),
    "b": ("ardosia", 1), "B": ("ardosia", 2), "n": ("ardosia", 3), 
    "k": ("doente", 0), "K": ("doente", 1), "L": ("doente", 2), "l": ("doente", 3),
    "E": ("olho", 0), "e": ("olho", 1),
    "r": ("forro", 0), "R": ("forro", 1), 
    "v": ("couro", 1), "V": ("couro", 2), "u": ("couro", 3),
    "2": ("linho", 1), "3": ("linho", 2), "4": ("linho", 3), 
    "C": ("chama", 1), "a": ("chama", 2), "A": ("chama", 3),
}

#          0         1         2         3
#          01234567890123456789012345678901
BASE = """
2: 0  ........a.......................
3: 0  .......aA.......................
4: 0  .......aAa......................
5: 0  ......CaAaC.....................
6: 0  ......CaAAC.....................
7: 0  .......CVC......................
8: 0  ........uV......................
9: 0  ........uV......................
10: 0 .......KLL........nnnBB.........
11: 0 .......kKKk..uV..nnBBBBBb.......
12: 0 .........KK.uuV..bBBBBbbbbb......
13: 0 ..........33uVVV.bKKkEkK........
14: 0 ...........2uVVVVbkLlLLLK.......
15: 0 ............vVVVVVkKLKoK........
16: 0 ............vVVrRRrkKKk.........
17: 0 ............vVrRRR43............
18: 0 ............vV44Rr43............
19: 0 ............vV43322LK...........
20: 0 ............vv33222KL...........
21: 0 .............v2222.kk...........
22: 0 .............bBBBnBBb...........
23: 0 .............bBBbBBnBb..........
24: 0 .............bBb.bBnBb..........
25: 0 ............bBb...BnB...........
26: 0 ............bB....bBb...........
27: 0 ............kK.....KK..........
28: 0 ..........23kK....34KK..........
29: 0 ..........2233....3344..........
"""


TOPO = "\n".join(l for l in BASE.strip().splitlines() if int(l.split(":")[0]) < 22)

PERNAS = {
    "base": """
22: 13 bBBBnBBb
23: 13 bBBbBBnBb
24: 13 bBb.bBnBb
25: 12 bBb...BnB
26: 12 bB....bBb
27: 12 kK.....KK
28: 12 k23....K34
29: 12 2233...3344
""",
    "passo_a": """
22: 13 bBBBnBBb
23: 12 bBBb.BBnBb
24: 11 bBb....bBnBb
25: 10 bBb......BnBb
26: 9 bB.........bBb
27: 8 kK...........KK
28: 8 k23..........K34
29: 8 2233.........3344
""",
    "passo_b": """
22: 13 bBBBnBBb
23: 13 BnBBbbBb
24: 12 BnBb...bBb
25: 11 BnB......bBb
26: 10 bBb.......bB
27: 10 KK........kK
28: 10 K34.......k23
29: 10 3344......2233
""",
    "meio_a": """
22: 13 bBBBnBBb
23: 13 bBBbBnBb
24: 13 bBBbBnB
25: 14 bBbBnB
26: 13 kKb.bBb
27: 12 k23..KK
28: 12 2233.K34
29: 17 3344
""",
    "meio_b": """
22: 13 bBBBnBBb
23: 13 bBBbBBnBb
24: 13 bBb.bBnBb
25: 14 bBbBnBb
26: 14 bBBnB
27: 14 kKK34
28: 14 k23344
29: 14 2233
""",
}
for _n, _t in PERNAS.items():
    globals()["P_" + _n] = TOPO + "\n" + _t


if __name__ == "__main__":
    print("use a bancada")
