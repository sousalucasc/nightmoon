"""HUD, ÍCONES E MIRA — Nightmoon, direção sépia e ouro.

Contrato (tamanhos e origens do Apêndice A, dias 15 e 19):
moldura 8×8 nine-slice (borda 2) · vida 4×4 · stamina 4×2 · chefe 4×4 · frasco 7×9 · bala 5×7 ·
almas 7×7 · ícones de menu 11×11 (vida, stamina, força, destreza, bengala, machado, cutelo,
pistola, escopeta) · mira 9×9 (origem 4,4).

Moldura escura com fio de ouro (a moldura de um relicário); vida em sangue, stamina em ouro
velho, chefe em vinho. Ícones (conhecimento/13): silhueta pura, contorno escuro completo, um
material, uma luz (cima-esquerda), um brilho.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import paleta as P  # noqa: E402
from kit.tela import Tela, de_segmentos  # noqa: E402

LEG = {
    "o": ("contorno", 0),
    "u": ("ui", 1), "U": ("ui", 2), "i": ("ui", 3),
    "g": ("ouro", 0), "G": ("ouro", 1), "Y": ("ouro", 2),
    "v": ("sangue", 0), "x": ("sangue", 1), "X": ("sangue", 2), "Z": ("sangue", 3),
    "w": ("marfim", 0), "W": ("marfim", 1), "V": ("marfim", 2),
    "a": ("aco", 1), "A": ("aco", 2), "s": ("aco", 3), "S": ("aco", 4),
    "f": ("ferro", 1), "F": ("ferro", 2), "e": ("ferro", 3), "E": ("ferro", 4),
    "m": ("madeira", 1), "M": ("madeira", 2), "j": ("madeira", 3),
    "p": ("pele", 0), "P": ("pele", 1), "Q": ("pele", 2),
    "b": ("couro", 1), "B": ("couro", 2), "n": ("couro", 3),
    "k": ("vidro", 1), "K": ("vidro", 2),
    "q": ("vinho", 1), "Q2": ("vinho", 2),
    "1": ("vinho", 1), "2": ("vinho", 2), "3": ("vinho", 3), "4": ("vinho", 4),
}


def _img(w, h, texto, contorno=True):
    t = Tela(w, h, P.RAMPAS)
    de_segmentos(texto, LEG, P.RAMPAS, w, h, tela=t)
    if contorno:
        t.contorno(("contorno", 0))
    return t.imagem()


MOLDURA = """
0: 0 oooooooo
1: 0 oGGGGGgo
2: 0 oGuuuugo
3: 0 oGuuuugo
4: 0 oGuuuugo
5: 0 oGuuuugo
6: 0 oggggggo
7: 0 oooooooo
"""
VIDA = """
0: 0 ZZZZ
1: 0 XXXX
2: 0 XXXX
3: 0 xxxx
"""
STAMINA = """
0: 0 YYYY
1: 0 GGGG
"""
CHEFE = """
0: 0 4444
1: 0 3333
2: 0 3333
3: 0 2222
"""

# ícones do HUD (com contorno automático: desenho interno 1 px menor de cada lado)
FRASCO = """
1: 2 mj
2: 2 kK
3: 1 kKKk
4: 1 XZXx
5: 1 XXXx
6: 1 XXxx
7: 2 xx
"""
BALA = """
1: 2 S
2: 1 sSa
3: 1 sAa
4: 1 sAa
5: 1 GGg
"""
ALMAS = """
1: 3 Y
2: 2 YG
3: 2 GYG
4: 1 GYYGg
5: 2 Ggg
"""

# ícones de menu, 11×11
I_VIDA = """
1: 5 Z
2: 4 ZX
3: 4 XXx
4: 3 XZXXx
5: 2 XZXXXxx
6: 2 XXXXXxx
7: 2 xXXXxxv
8: 3 xxxxv
"""
I_STAMINA = """
1: 2 GGGGGGG
2: 3 VWWWw
3: 4 WWw
4: 5 Y
5: 4 wGw
6: 3 wGYGw
7: 2 wGYYYGw
8: 2 ggggggg
"""
# força: bigorna de ferro
I_FORCA = """
3: 1 EEEEEEEEe
4: 2 eEEEEEEf
5: 4 fEEEf
6: 5 fEf
7: 4 FFFFF
8: 3 fffffff
"""
# destreza: duas adagas cruzadas
I_DESTREZA = """
1: 1 S.......S
2: 2 s.....s
3: 3 s...s
4: 4 s.s
5: 5 G
6: 4 G.G
7: 3 b...b
8: 2 b.....b
"""
I_BENGALA = """
1: 8 GY
2: 7 SG
3: 6 Ss
4: 5 Ss
5: 4 Ss
6: 3 Ss
7: 2 Ss
8: 2 b
9: 1 bn
"""
I_MACHADO = """
1: 5 EEe
2: 4 EEEEe
3: 4 eEEEf
4: 5 Fmf
5: 4 mM
6: 3 mM
7: 2 mM
8: 1 mM
9: 1 m
"""
I_CUTELO = """
1: 6 e.e.
2: 5 eEEEe
3: 4 eEEEf
4: 3 eEEEf
5: 3 EEEf
6: 3 Fff
7: 2 bG
8: 1 bn
9: 1 b
"""
I_PISTOLA = """
3: 2 eEEEEEe
4: 2 mGffff
5: 2 jM
6: 2 Mm
7: 2 m
"""
I_ESCOPETA = """
2: 2 eEEEEEEe
3: 2 mGfffffE
4: 2 jMff
5: 2 Mm
6: 2 m
"""

MIRA = """
0: 4 W
1: 4 w
3: 0 Ww.V.wW
5: 4 w
6: 4 W
"""


def mira():
    t = Tela(9, 9, P.RAMPAS)
    de_segmentos(MIRA, LEG, P.RAMPAS, 9, 9, tela=t)
    t.contorno(("contorno", 0))
    # o contorno não pode encostar na borda: a mira inteira cabe em 9×9
    return t.imagem()


ITENS = {
    "spr_hud_moldura": (lambda: _img(8, 8, MOLDURA, contorno=False), (0, 0)),
    "spr_hud_vida": (lambda: _img(4, 4, VIDA, contorno=False), (0, 0)),
    "spr_hud_stamina": (lambda: _img(4, 2, STAMINA, contorno=False), (0, 0)),
    "spr_hud_chefe": (lambda: _img(4, 4, CHEFE, contorno=False), (0, 0)),
    "spr_icone_frasco": (lambda: _img(7, 9, FRASCO), (0, 0)),
    "spr_icone_bala": (lambda: _img(5, 7, BALA), (0, 0)),
    "spr_icone_almas": (lambda: _img(7, 7, ALMAS), (0, 0)),
    "spr_icone_vida": (lambda: _img(11, 11, I_VIDA), (0, 0)),
    "spr_icone_stamina": (lambda: _img(11, 11, I_STAMINA), (0, 0)),
    "spr_icone_forca": (lambda: _img(11, 11, I_FORCA), (0, 0)),
    "spr_icone_destreza": (lambda: _img(11, 11, I_DESTREZA), (0, 0)),
    "spr_icone_bengala": (lambda: _img(11, 11, I_BENGALA), (0, 0)),
    "spr_icone_machado": (lambda: _img(11, 11, I_MACHADO), (0, 0)),
    "spr_icone_cutelo": (lambda: _img(11, 11, I_CUTELO), (0, 0)),
    "spr_icone_pistola": (lambda: _img(11, 11, I_PISTOLA), (0, 0)),
    "spr_icone_escopeta": (lambda: _img(11, 11, I_ESCOPETA), (0, 0)),
    "spr_mira": (mira, (4, 4)),
}


def imagem(nome):
    return ITENS[nome][0]()


if __name__ == "__main__":
    from kit import previa as pv
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "previa")
    pv.folha([(n.replace("spr_", ""), [imagem(n)]) for n in ITENS], k=8, larg_rotulo=130,
             titulo="HUD e ícones").save(os.path.join(out, "hud_folha.png"))
    print("ok")
