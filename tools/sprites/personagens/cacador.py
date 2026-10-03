"""CAÇADOR (player) — Nightmoon, direção sépia e ouro.

BRIEF
- O que é: o personagem do jogador; está em toda tela, no meio de 2 a 6 inimigos. Lê a 1x
  como "caçador de tricórnio e sobretudo" e se separa do chão pela massa escura com rosto claro.
- Escala: quadro 32×32, origem (16, 30) na sola; figura de 28 px (tricórnio na linha 3, sola
  na 30); cabeça+chapéu 9 px (33%), ≈3,5 cabeças sem o chapéu. Mão da arma SEMPRE em (18, 20)
  quando há arma; mão da pistola no tiro em (19, 18).
- Gancho: tricórnio com galão dourado + capa curta de ombros (Inverness) sobre sobretudo até o
  tornozelo. Traços (3): gravata e punho marfim; rabo de cavalo com fita vinho; linha do forro
  vinho descendo pela frente do casaco.
- Materiais: casaco (lã escura quente; dobras em cano saindo da cintura, textura só na luz),
  couro (luva e bota, brilho de 1 px), marfim (gravata, punho), pele sépia, ouro (galão e um
  botão), forro vinho. Acento: OURO.
- Ponto de interesse: rosto pálido sob a aba + gravata marfim.
- Luz: morna, de cima-esquerda; fio frio de recorte (rampa `recorte`) na borda direita da capa
  e do casaco, pra separar do chão escuro.
- Animações (GDD seção 14): idle 4 (~6 fps), walk 6 (10 fps), backstep 4 (16 frames), dash 4
  (22), ataque 3 (windup/ativo/recovery, mão fixa), tiro 3, cura 4 (24; injeta o frasco na
  coxa, como em Bloodborne), hit 2 (18), visceral 4 (40), morte 6 (60).
- Referências: tools/sprites/referencias/cacador.md (VS Trevor/Alucard pra escala e preto que
  lê; trajes de Bloodborne; conceito C escolhido pelo dono com o tricórnio do caçador antigo).

Construção: carimbos pintados à mão (cabeça, capa, mão, botas) + saia de pano em (u, v)
(kit.tecido) + remendos por quadro. Contorno automático de 1 px no fim; o lado da luz recebe o
contorno normal (a aresta clara já está pintada no carimbo).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import paleta as P  # noqa: E402
from kit import tecido  # noqa: E402
from kit.tela import Tela, de_segmentos  # noqa: E402
from personagens.cacador_leg import LEG  # noqa: E402

W = H_ = 32
ORIGEM = (16, 30)

# ------------------------------------------------------------------ carimbos --
# Coordenadas absolutas do quadro-base; a pose desloca (dx, dy).
CAB = {
    "normal": """
4: 12 33
5: 11 3321.2331
6: 11 332211233112
7: 11 1100000000012
8: 11 GGGGtpppppGG
9: 14 hhPQPtP
10: 14 hhPQQQPP
11: 13 RhhpPQPp
12: 13 R.tpPPp
""",
    # olhando pra baixo (cura): a aba desce sobre o rosto, só o queixo e o nariz pegam luz
    "baixa": """
5: 12 33
6: 11 3321.2331
7: 11 332211233112
8: 11 1100000000012
9: 11 GGGGtppppGGG
10: 14 hhtpPPp
11: 13 RhhpPQQP
12: 13 R.tpPQp
""",
    # jogada pra trás (dano): a cabeça recua 1 px e sobe; olho fechado de dor, boca aberta
    "tras": """
3: 11 33
4: 10 3321.2331
5: 10 332211233112
6: 10 1100000000012
7: 10 GGGGtpppppGG
8: 13 hhPQPtP
9: 13 hhPQQQPP
10: 12 RhhpPQtP
11: 12 R.tpPPp
""",
}

TRONCO = {
    "normal": """
13: 13 232WVW1
14: 12 4332wWw110
15: 11 433221W01100
16: 10 33222110G010c
17: 10 322111000100c
18: 10 2111010r0000
""",
    # inclinado pra frente (ataque, dash): a capa avança 1 px em cima
    "frente": """
13: 14 232WVW1
14: 12 43332wWw110
15: 11 4433221W0110
16: 10 33322110G010c
17: 10 322211000100c
18: 10 2111010r0000
""",
    # recuado (dano, backstep): a capa abre pra frente embaixo
    "tras": """
13: 12 232WVW1
14: 11 4332wWw110
15: 10 433221W01100
16: 10 3222110G0100c
17: 10 22111000100 0c
18: 10 2111010r00000
""",
}

MAO = {
    # punho marfim + luva, mão (18, 20)
    "baixa": """
19: 18 Ww
20: 17 BNn
21: 17 bBt
""",
    # braço da pistola saindo da frente da capa, mão em (19, 18)
    "pistola": """
16: 19 21
17: 18 WBn
18: 18 wNnB
""",
    # cura: a mão no cinto pega o frasco
    "cinto": """
18: 16 J
19: 15 BX
20: 15 Nx
21: 15 bB
""",
    # cura: crava o frasco na coxa
    "coxa": """
21: 17 X
22: 16 BNn
23: 16 bBt
""",
    "coxa_vazio": """
21: 17 I
22: 16 BNn
23: 16 bBt
""",
    # visceral: puxa, estica, crava, arranca
    "puxa": """
20: 13 WB
21: 13 bn
""",
    "estica": """
16: 20 12
17: 21 122
18: 23 WBNnn
""",
    "crava": """
16: 20 12
17: 21 122Xx
18: 23 WBXZx
19: 25 xv
""",
    "arranca": """
17: 20 12
18: 21 WX
19: 21 xXx
20: 22 v
""",
}

BOTA_TRAS = """
0: 0 bnB
1: 0 bBn
"""
BOTA_FRENTE = """
0: 0 bnnNB
1: 0 bBnnN
"""
# na caminhada: a perna de perto (mais clara) e a de longe (mais escura)
BOTA_PERTO = """
0: 0 bnnNB
1: 0 bBnnN
"""
BOTA_LONGE = """
0: 0 bBnB
1: 0 bbBn
"""
BOTA_ERGUIDA = """
0: 0 bBn
"""
BOTA_ERGUIDA_LONGE = """
0: 0 bbB
"""

# dobras do sobretudo em u (0 = esquerda, 1 = direita), luz de cima-esquerda
FAIXAS = [
    (0.20, ("casaco", 2)), (0.42, ("casaco", 3)), (0.64, ("casaco", 1)), (1.00, ("casaco", 0)),
]
TOPO = {("casaco", 2): ("casaco", 1), ("casaco", 3): ("casaco", 1), ("casaco", 1): ("casaco", 0)}
BARRA = {("casaco", 3): ("casaco", 2), ("casaco", 2): ("casaco", 1), ("casaco", 1): ("casaco", 0)}


def _seg(t, texto, dx=0, dy=0):
    de_segmentos(texto, LEG, P.RAMPAS, W, H_, tela=t, dx=dx, dy=dy)


def montar(p):
    """p: dict da pose. Ordem: bota de trás, saia, bota da frente, capa, cabeça, mão, remendos.
    Pose com "quadro" é um quadro inteiro pintado à mão (morte no chão)."""
    t = Tela(W, H_, P.RAMPAS)
    if "quadro" in p:
        _seg(t, p["quadro"])
        t.contorno(("contorno", 0))
        return t
    by = p.get("y", 0)              # sobe/desce o corpo todo (menos as botas)
    bx = p.get("x", 0)
    # botas
    for (stamp, x, y) in p.get("botas", [(BOTA_TRAS, 11, 28), (BOTA_FRENTE, 17, 28)]):
        _seg(t, stamp, x, y)
    # saia (sobretudo da cintura à barra)
    s = p.get("saia", {})
    y0 = 19 + by
    px = tecido.saia(y0, s.get("y1", 27), s.get("cintura", (12 + bx, 19 + bx)), s.get("barra", (10, 23)),
                     s.get("faixas", FAIXAS), curva=s.get("curva", 1.25), topo_tons=TOPO, barra_tons=BARRA,
                     abertura=(s.get("abre", 0.72), 0.07, ("forro", 0)), recorte=("recorte", 0))
    for x, y, r, tom in px:
        t.pinta(x, y, r, tom)
    # capa e cabeça
    tv, tdx, tdy = p.get("tronco", ("normal", 0, 0))
    _seg(t, TRONCO[tv], bx + tdx, by + tdy)
    cv, cdx, cdy = p.get("cab", ("normal", 0, 0))
    _seg(t, CAB[cv], bx + cdx, by + cdy)
    # mão (fica parada no ponto da arma, a não ser que a pose diga)
    mv = p.get("mao", ("baixa", 0, 0))
    if mv:
        _seg(t, MAO[mv[0]], mv[1], mv[2])
    m2 = p.get("mao2")
    if m2:
        _seg(t, MAO[m2[0]], m2[1], m2[2])
    for rem in p.get("remendos", []):
        _seg(t, rem)
    t.contorno(("contorno", 0))
    return t


# ------------------------------------------------------------------- poses ---
# Semântica: "x"/"y" movem o corpo inteiro (saia, capa, cabeça; as botas não). "tronco" e "cab"
# levam (variante, dx, dy) RELATIVOS a esse corpo. "mao"/"mao2" e "botas" são absolutos.

# respiração: a capa desce 1 px, a cabeça vai junto um quadro depois (nunca abaixo da capa);
# a barra do casaco balança 1 px atrasada
IDLE = [
    {},
    {"tronco": ("normal", 0, 1), "saia": {"barra": (10, 23)}},
    {"tronco": ("normal", 0, 1), "cab": ("normal", 0, 1), "saia": {"barra": (10, 24)}},
    {"saia": {"barra": (10, 24)}},
]

WALK = [
    # contato: perna de perto na frente
    {"botas": [(BOTA_LONGE, 9, 28), (BOTA_PERTO, 19, 28)], "saia": {"barra": (9, 24)}},
    # desce: o corpo baixa 1 px, a cabeça fica (olhar firme); a de longe sai do chão
    {"y": 1, "cab": ("normal", 0, -1), "botas": [(BOTA_ERGUIDA_LONGE, 11, 28), (BOTA_PERTO, 18, 28)],
     "saia": {"barra": (10, 23)}},
    # passagem: a de longe cruza por trás
    {"botas": [(BOTA_ERGUIDA_LONGE, 13, 28), (BOTA_PERTO, 16, 28)], "saia": {"barra": (11, 22)}},
    # contato: perna de longe na frente
    {"botas": [(BOTA_PERTO, 9, 28), (BOTA_LONGE, 19, 28)], "saia": {"barra": (9, 24)}},
    {"y": 1, "cab": ("normal", 0, -1), "botas": [(BOTA_ERGUIDA, 11, 28), (BOTA_LONGE, 18, 28)],
     "saia": {"barra": (10, 23)}},
    {"botas": [(BOTA_ERGUIDA, 13, 28), (BOTA_LONGE, 16, 28)], "saia": {"barra": (11, 22)}},
]

BOTAS_BASE = [(BOTA_TRAS, 11, 28), (BOTA_FRENTE, 17, 28)]

# backstep: agacha, salta pra trás (o casaco vai pra frente), pousa, volta
BACKSTEP = [
    {"y": 1, "saia": {"barra": (10, 24)}, "botas": [(BOTA_TRAS, 10, 28), (BOTA_FRENTE, 17, 28)]},
    {"y": -1, "x": -1, "tronco": ("tras", 0, 0), "cab": ("normal", -1, 0), "saia": {"barra": (11, 26), "y1": 26},
     "botas": [(BOTA_ERGUIDA_LONGE, 12, 27), (BOTA_ERGUIDA, 16, 27)]},
    {"y": 1, "cab": ("normal", -1, 0), "saia": {"barra": (10, 25)},
     "botas": [(BOTA_TRAS, 9, 28), (BOTA_FRENTE, 16, 28)]},
    {"saia": {"barra": (10, 24)}},
]

# dash: inclina, dispara (o casaco escorre pra trás), freia
DASH = [
    {"y": 1, "x": 1, "tronco": ("frente", 0, 0), "cab": ("normal", 1, 0), "saia": {"barra": (8, 23)},
     "botas": [(BOTA_LONGE, 9, 28), (BOTA_PERTO, 19, 28)]},
    {"y": 2, "x": 2, "tronco": ("frente", 0, 0), "cab": ("normal", 1, 0), "saia": {"barra": (6, 22), "y1": 27},
     "botas": [(BOTA_LONGE, 7, 28), (BOTA_PERTO, 20, 28)]},
    {"y": 2, "x": 2, "tronco": ("frente", 0, 0), "cab": ("normal", 1, 0), "saia": {"barra": (5, 23), "y1": 26},
     "botas": [(BOTA_ERGUIDA_LONGE, 9, 28), (BOTA_PERTO, 20, 28)]},
    {"tronco": ("tras", 0, 0), "cab": ("normal", -1, 0), "saia": {"barra": (10, 25)},
     "botas": [(BOTA_LONGE, 11, 28), (BOTA_PERTO, 19, 28)]},
]

# ataque (mão parada em 18,20; o corpo gira em volta dela)
ATAQUE = [
    {"y": 1, "x": -1, "tronco": ("tras", 0, 0), "saia": {"barra": (9, 23)},
     "botas": [(BOTA_TRAS, 10, 28), (BOTA_FRENTE, 18, 28)]},
    {"y": 1, "x": 1, "tronco": ("frente", 0, 0), "cab": ("normal", 1, 0), "saia": {"barra": (8, 24)},
     "botas": [(BOTA_LONGE, 9, 28), (BOTA_PERTO, 20, 28)]},
    {"tronco": ("frente", 0, 0), "cab": ("normal", 1, 0), "saia": {"barra": (9, 24)},
     "botas": [(BOTA_TRAS, 10, 28), (BOTA_FRENTE, 19, 28)]},
]

# tiro: o braço sai da capa com a mão em (19,18); o tiro dá um tranco pra trás
TIRO = [
    {"mao2": ("pistola", 0, 0)},
    {"x": -1, "tronco": ("tras", 0, 0), "saia": {"barra": (10, 24)}, "mao2": ("pistola", 0, 0),
     "botas": [(BOTA_TRAS, 10, 28), (BOTA_FRENTE, 17, 28)]},
    {"mao2": ("pistola", 0, 0), "saia": {"barra": (10, 24)}},
]

# cura: pega o frasco, crava na coxa, estremece, endireita (sem arma)
CURA = [
    {"mao": ("cinto", 0, 0), "cab": ("baixa", 0, 0)},
    {"y": 1, "tronco": ("frente", 0, 0), "cab": ("baixa", 0, 0), "mao": ("coxa", 0, 0), "saia": {"barra": (10, 24)}},
    {"tronco": ("tras", 0, 0), "cab": ("tras", 0, 0), "mao": ("coxa_vazio", 0, 0)},
    {"saia": {"barra": (10, 24)}},
]

# dano: tranco pra trás (silhueta diferente do parado), depois volta
HIT = [
    {"x": -2, "tronco": ("tras", 0, 0), "cab": ("tras", -1, 0), "saia": {"barra": (10, 25), "cintura": (10, 17)},
     "botas": [(BOTA_TRAS, 9, 28), (BOTA_FRENTE, 17, 28)]},
    {"x": -1, "y": 1, "saia": {"barra": (10, 24), "cintura": (11, 18)},
     "botas": [(BOTA_TRAS, 10, 28), (BOTA_FRENTE, 17, 28)]},
]

# visceral: puxa a mão, crava, torce, arranca (sem arma)
VISCERAL = [
    {"x": -1, "y": 1, "tronco": ("tras", 0, 0), "mao": ("puxa", 0, 0),
     "saia": {"barra": (9, 23)}, "botas": [(BOTA_TRAS, 10, 28), (BOTA_FRENTE, 17, 28)]},
    {"x": 2, "y": 1, "tronco": ("frente", 0, 0), "cab": ("normal", 1, 0), "mao": ("estica", 0, 0),
     "saia": {"barra": (8, 24)}, "botas": [(BOTA_LONGE, 9, 28), (BOTA_PERTO, 20, 28)]},
    {"x": 2, "y": 1, "tronco": ("frente", 0, 0), "cab": ("normal", 1, 0), "mao": ("crava", 0, 0),
     "saia": {"barra": (8, 24)}, "botas": [(BOTA_LONGE, 9, 28), (BOTA_PERTO, 20, 28)]},
    {"tronco": ("tras", 0, 0), "mao": ("arranca", 0, 0),
     "saia": {"barra": (10, 25)}, "botas": [(BOTA_TRAS, 10, 28), (BOTA_FRENTE, 18, 28)]},
]

# morte: cambaleia, os joelhos cedem, ajoelha, tomba pra frente, fica no chão (o tricórnio cai)
MORTE_CAINDO = """
13: 21 33
14: 20 3321
15: 19 3210
16: 15 23
16: 18 111
17: 13 3433210000
18: 12 433322110013
19: 11 33322211GGGG
20: 11 3222110tpppp
21: 11 2221100hPQPt
22: 11 2211110hPQQQ
23: 10 22111100RhpPQ
24: 9 2232110000hpP
25: 8 22321100000tt
26: 7 b223211100110
27: 6 bnB12211001100
28: 6 bBn01110000BNn
29: 7 bb0000000bBt
"""
MORTE_CHAO = """
24: 14 233332
25: 8 1222332333221hh
26: 5 bB12212212211110Rhhh
27: 4 bnB0110110110100Wwhhpp.33
28: 4 bBn00000000000000tppP3321
29: 6 0000000000000.BNn.11000
"""
MORTE_FIM = """
25: 13 22333221
26: 5 b1222122122211hh
27: 4 bnB1101101101000Rhhhp
28: 4 bBn000000000000Wwhhpp
29: 5 00000000000000tpBNn.3321
"""
MORTE = [
    {"x": -2, "tronco": ("tras", 0, 0), "cab": ("tras", -1, 0), "mao": None,
     "saia": {"barra": (10, 25), "cintura": (10, 17)}, "botas": [(BOTA_TRAS, 9, 28), (BOTA_FRENTE, 17, 28)]},
    {"x": -1, "y": 3, "cab": ("baixa", 0, 0), "mao": None,
     "saia": {"barra": (8, 25), "y1": 28}, "botas": [(BOTA_TRAS, 10, 28), (BOTA_FRENTE, 17, 28)]},
    {"y": 6, "cab": ("baixa", 1, 0), "mao": ("coxa", 1, 4),
     "saia": {"barra": (7, 26), "y1": 28, "curva": 0.8}, "botas": [(BOTA_ERGUIDA_LONGE, 6, 28)]},
    {"quadro": MORTE_CAINDO},
    {"quadro": MORTE_CHAO},
    {"quadro": MORTE_FIM},
]

ANIMS = {
    "idle": (IDLE, 160),
    "walk": (WALK, 100),
    "backstep": (BACKSTEP, 67),
    "dash": (DASH, 92),
    "ataque": (ATAQUE, 150),
    "tiro": (TIRO, 120),
    "cura": (CURA, 100),
    "hit": (HIT, 150),
    "visceral": (VISCERAL, 167),
    "morte": (MORTE, 167),
}


def quadros(nome):
    poses, _ = ANIMS[nome]
    return [montar(p).imagem() for p in poses]



# Exceções de auditoria (AVISO justificado; a próxima rodada não precisa perguntar de novo)
AUDITORIA = {
    "pixel_solto": "olho (1 px sob a aba), botão de ouro, punho e luva: detalhe de 1 px de propósito num corpo de 28 px",
    "nos_1px": "ponta do tricórnio e bico da bota: forma, não sujeira",
    "furos_1px": "vão entre a asa e a copa do tricórnio, entre a trança e o queixo, entre as botas",
    "cores_gemeas": "forro vinho × sangue (cura e visceral): mesma família de propósito, não se encostam",
    "teto_cores": "cura e visceral somam vidro e sangue (22 cores)",
    "direcao": "quadros deitados da morte: luz de cima vira lateral",
    "aglomerados": "densidade de aglomerados pequenos no limite: rosto, galão e gravata são o ponto de interesse",
}

if __name__ == "__main__":
    from kit import previa as pv
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "previa")
    nome = sys.argv[1] if len(sys.argv) > 1 else "idle"
    qs = quadros(nome)
    pv.folha([(nome, qs)], k=8, larg_rotulo=80).save(os.path.join(out, f"cacador_{nome}.png"))
    pv.gif(qs, ANIMS[nome][1], os.path.join(out, f"cacador_{nome}.gif"), k=6)
    pv.grade(qs[0], k=20).save(os.path.join(out, f"cacador_{nome}_0_grade.png"))
    print("ok", len(qs))
