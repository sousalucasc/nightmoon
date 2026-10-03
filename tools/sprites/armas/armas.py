"""ARMAS — sprites separados que o código gira pra mira (apontando pra DIREITA, origem no cabo).

Mesmos tamanhos e origens do contrato (arte/origens.md), pra o tutorial não mudar:
bengala 26×5 (3,3) · machado 30×16 (4,8) · cutelo 26×8 (3,4) · pistola 12×7 (3,3) ·
escopeta 16×8 (3,3) · foice 22×9 (3,7) · dama_longa 27×5 (2,2) · dama_longa_sangue 27×5 (2,2).

Regras (conhecimento/13): lâmina de UM gume (largura de um lado do eixo, dorso continuando o
cabo), aço frio de contraste alto com o gume num fio claro de 1 px; madeira com veio no
comprimento; um brilho só. Desenhadas com 1 px de contorno (automático) dentro do tamanho.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import paleta as P  # noqa: E402
from kit.tela import Tela, de_segmentos  # noqa: E402

LEG = {
    "o": ("contorno", 0),
    "m": ("madeira", 1), "M": ("madeira", 2), "j": ("madeira", 3), "J": ("madeira", 4),
    "f": ("ferro", 1), "F": ("ferro", 2), "e": ("ferro", 3), "E": ("ferro", 4), "D": ("ferro", 5),
    "a": ("aco", 0), "A": ("aco", 1), "s": ("aco", 2), "S": ("aco", 3), "V": ("aco", 4),
    "g": ("ouro", 0), "G": ("ouro", 1), "Y": ("ouro", 2),
    "b": ("couro", 0), "B": ("couro", 1), "n": ("couro", 2), "N": ("couro", 3),
    "v": ("sangue", 0), "x": ("sangue", 1), "X": ("sangue", 2), "Z": ("sangue", 3),
    "r": ("forro", 1),
}

ARMAS = {
    # bengala-lâmina: cabo de couro com castão de ouro, lâmina fina e reta
    "spr_arma_bengala": ((26, 5), (3, 3), """
1: 1 GY
2: 1 gGBnBGSSSSSSSSSSSSSSSSSV
3: 2 bBnBgAssssssssssssssssA
"""),
    # machado de caça: cabo longo de madeira, cabeça larga de um gume virada pra cima
    "spr_arma_machado": ((30, 16), (4, 8), """
1: 22 eEEE
2: 21 eEEED
3: 20 eEEEED
4: 20 FeeeED
5: 20 FFeeeD
6: 19 fFFeeeD
7: 1 bnBbjJjJjJjJjJjjjjfFFFeD
8: 1 bnBbMjMjMjMjMjMMMMMfFFFeD
9: 1 bbbbmmmmmmmmmmmmmmmfFFFa
10: 19 ffFA
11: 20 fA
"""),
    # cutelo serrado: lâmina larga e retangular, dentes de serra no dorso (em cima), gume embaixo
    "spr_arma_cutelo": ((26, 8), (3, 4), """
1: 8 e.e.e.e.e.e.e.e.e
2: 7 eEeEeEeEeEeEeEeEeE
3: 1 bnBgFeeeeeeeeeeeeeeeeeE
4: 1 bnBgfFFFFFFFFFFFFFFFFFe
5: 1 bbbgffFFFFFFFFFFFFFFFFe
6: 6 SSSSSSSSSSSSSSSSSV
"""),
    # pistola de pederneira: coronha de madeira caída, cano curto
    "spr_arma_pistola": ((12, 7), (3, 3), """
1: 4 eEEEEEE
2: 1 jJMfFFFFFFe
3: 1 JjMgfffffo
4: 1 MjM
5: 1 mM
"""),
    # escopeta de cano serrado: cano grosso com boca larga
    "spr_arma_escopeta": ((16, 8), (3, 3), """
1: 4 eEEEEEEEEeE
2: 1 jJMfFFFFFFFFFeE
3: 1 JjMgfffffffffeA
4: 1 MjM.ffffffffffe
5: 1 mM
6: 1 m
"""),
    # foice do aldeão: cabo de madeira, lâmina curva e enferrujada pra cima
    "spr_arma_foice": ((22, 9), (3, 7), """
1: 13 SEEEEe
2: 12 S....eEEe
3: 18 eEE
4: 19 eE
5: 18 eEe
6: 16 FFe
7: 1 mMjMjMjMjMjMjJFFF
"""),
    # lâmina longa da Dama: fina, levemente curva, guarda de ouro
    "spr_arma_dama_longa": ((27, 5), (2, 2), """
1: 4 G.SSSSSSSSSSSSSSSSSSSSV
2: 1 BngGYAssssssssssssssssssS
3: 4 G
"""),
    "spr_arma_dama_longa_sangue": ((27, 5), (2, 2), """
1: 4 G.XxXXZXXxXXXZXXxXXXXZ
2: 1 BngGYxXXxXXXxXXXXxXXXxXX
3: 4 G...v.....v......v
"""),
}


def imagem(nome):
    (w, h), _orig, txt = ARMAS[nome]
    t = Tela(w, h, P.RAMPAS)
    de_segmentos(txt, LEG, P.RAMPAS, w, h, tela=t, grupo="arma")
    t.contorno(("contorno", 0))
    return t.imagem()


def origem(nome):
    return ARMAS[nome][1]


if __name__ == "__main__":
    from kit import previa as pv
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "previa")
    pv.folha([(n.replace("spr_arma_", ""), [imagem(n)]) for n in ARMAS], k=8, larg_rotulo=160,
             titulo="armas (origem = cabo)").save(os.path.join(out, "armas_folha.png"))
    print("ok")
