"""Paleta do Nightmoon — direção SÉPIA E OURO (escolhida em 2026-10-02).

Paleta-guia: rampa nova entra aqui, com nome. Cada rampa vai do escuro pro claro. A luz
principal é morna (lampião / lua velha) e vem de cima-esquerda; a sombra gira pro violeta; o
recorte (fio de luz do lado de trás) é frio. Acentos: OURO (detalhe precioso, interativo) e
SANGUE (vida, dano, frasco). Inimigos ficam em famílias de cor diferentes do caçador
(oliva-doente, carne, ardósia).
"""
from kit.paleta import de_hexa as H

RAMPAS = {
    # ---- universais
    "contorno": [H("#120a0e")],
    "tinta": [H("#120a0e"), H("#22161d"), H("#33262b")],         # linhas internas e oclusão
    "recorte": [H("#5c6478"), H("#8e98ae")],                       # fio frio de luz de trás

    # ---- caçador
    "casaco": [H("#120a0e"), H("#271a1f"), H("#382829"), H("#4d3c38"), H("#67564c")],
    "forro": [H("#4a1820"), H("#7a2330"), H("#a8403e")],
    "pele": [H("#6e4a46"), H("#a8806e"), H("#d9b89c"), H("#f0d8c0")],
    "marfim": [H("#8f8172"), H("#c9b9a2"), H("#efe4cf")],
    "couro": [H("#240c0d"), H("#331b16"), H("#482f25"), H("#76573c")],
    "ouro": [H("#7a4e1e"), H("#c08a36"), H("#ecc870")],
    "cabelo": [H("#170e14"), H("#281d1f"), H("#392e2b")],

    # ---- sangue, vidro
    "sangue": [H("#3a0c14"), H("#6e1420"), H("#a8202c"), H("#e0483e")],
    "vidro": [H("#2c2830"), H("#6a6670"), H("#c8c4cc")],

    # ---- aldeão (oliva doente)
    "trapo": [H("#1e1c14"), H("#2e2b1c"), H("#45402a"), H("#605a3a"), H("#7e7650")],
    "doente": [H("#3a3a32"), H("#5a5c4c"), H("#84866c"), H("#aaab8e")],
    "olho": [H("#c0283a"), H("#ff7a5a")],

    # ---- brutamontes (carne, saco, avental)
    "carne": [H("#382727"), H("#56403c"), H("#775f54"), H("#9a826c"), H("#bba68e")],
    "saco": [H("#2e2216"), H("#4a3824"), H("#735c2c"), H("#8e7448")],

    # ---- chefe (ardósia, bandagem marfim) e besta (pelagem cinza-cinza)
    "ardosia": [H("#070d18"), H("#151e2c"), H("#242f3d"), H("#384554"), H("#526371")],
    "pelagem": [H("#120a0e"), H("#312521"), H("#4a3a33"), H("#66574c"), H("#877a6e"), H("#aea599")],
    "pelebesta": [H("#2a1a1c"), H("#45292a"), H("#683c38")],

    # ---- Dama (vinho, prata)
    "vinho": [H("#26090f"), H("#41101a"), H("#661a28"), H("#8e2c38"), H("#b44a4e")],
    "prata": [H("#545866"), H("#868c9a"), H("#bcc2cc"), H("#e8ecf0")],

    # ---- inimigos refeitos (2026-10-02, 2ª rodada)
    "linho": [H("#3d332b"), H("#5c4e3e"), H("#7a6b54"), H("#988d75"), H("#b3ae9a")],      # camisa suja do aldeão
    "pelecinza": [H("#2a2631"), H("#47404d"), H("#665b68"), H("#877c85"), H("#a99da4")],  # pele de defunto do gigante
    "ferrugem": [H("#331e1a"), H("#562f23"), H("#78452c"), H("#946546")],                 # gaiola e grilhões
    "alvo": [H("#4d4540"), H("#6e675e"), H("#8f887d"), H("#b1aa9f"), H("#d6d1c6")],      # casaco branco do chefe
    "pelosangue": [H("#200e12"), H("#3b161d"), H("#5b1d26"), H("#7b2c31"), H("#9b423e"), H("#b56255")],  # pelo da besta

    # ---- metal e madeira (armas, objetos)
    "ferro": [H("#1a171b"), H("#2c282e"), H("#47424a"), H("#6c6870"), H("#a09ca4"), H("#dcd8dc")],
    "aco": [H("#2a2c34"), H("#4e5260"), H("#8a90a0"), H("#c4c8d4"), H("#f2f2f6")],
    "madeira": [H("#22140e"), H("#3a2416"), H("#563620"), H("#76502e"), H("#9a7040")],

    # ---- efeitos
    "luzfx": [H("#a86a24"), H("#e0a848"), H("#f6dc90"), H("#fff6dc")],
    "poeira": [H("#4e443c"), H("#6e6256"), H("#948676")],
    "nevoa": [H("#8a8070"), H("#b0a690"), H("#d6ccb4")],
    "chama": [H("#7a2810"), H("#c85a1c"), H("#f0a040"), H("#fde090")],

    # ---- cenário (chão, muro, mato)
    "pedra": [H("#281d1c"), H("#352a27"), H("#423732"), H("#50443e"), H("#5c534b"), H("#6c645c")],
    "laje": [H("#342d2a"), H("#443c38"), H("#544d47"), H("#645e57"), H("#76726a")],
    "muro": [H("#170f0e"), H("#251c1a"), H("#352a26"), H("#443934"), H("#564c45"), H("#6a625a")],
    "mato": [H("#32260b"), H("#42381d"), H("#554d31"), H("#6b6648")],
    "terra": [H("#2f211c"), H("#3f2f28"), H("#4e4035"), H("#5f5347")],
    "agua": [H("#141418"), H("#22232c"), H("#3a3c4a"), H("#7a7262")],

    # ---- fundo do título (céu em faixas, lua, cidade, neblina): cores próprias, registradas
    "titulo": [H("#100a0b"), H("#120b0e"), H("#180f10"), H("#191012"), H("#1e1412"), H("#221617"), H("#231716"), H("#281c18"), H("#2c1d1b"), H("#2e1f1d"), H("#2f201c"), H("#30221c"), H("#342420"), H("#382621"), H("#3c2a24"), H("#422e27"), H("#442f27"), H("#463128"), H("#4c362d"), H("#4c372c"), H("#523a2e"), H("#543c31"), H("#563e30"), H("#624736"), H("#b06222"), H("#be6c29"), H("#96826e"), H("#c87028"), H("#c8742f"), H("#e89a38"), H("#c6b08c"), H("#f6a43f"), H("#f0aa46"), H("#ffac45"), H("#d6c4a2"), H("#dccdb4"), H("#e8dabe"), H("#f4ecd6")],

    # ---- interface
    "ui": [H("#11080e"), H("#22161a"), H("#322525"), H("#483b38")],
    "texto": [H("#140b0e"), H("#c9b9a2"), H("#f6eedd")],
}


def todas():
    return {c for r in RAMPAS.values() for c in r}


def gpl(caminho):
    """Grava a paleta em formato GIMP (.gpl), que o Aseprite abre."""
    linhas = ["GIMP Palette", "Name: Nightmoon sepia e ouro", "Columns: 8", "#"]
    for nome, r in RAMPAS.items():
        for i, (cr, cg, cb) in enumerate(r):
            linhas.append(f"{cr:3d} {cg:3d} {cb:3d}\t{nome} {i}")
    open(caminho, "w", encoding="utf-8").write("\n".join(linhas) + "\n")
