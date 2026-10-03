"""EFEITOS — Nightmoon, direção sépia e ouro.

Efeito vive pouco: lê pela forma e pelo valor (conhecimento/13). Sem contorno, alfa binário,
núcleo quase branco (marfim-ouro) e borda mais escura e saturada. O código cria cada efeito
com fx_criar: 1 quadro a cada 3 frames, girado pra mira; `escala_y = -1` espelha o corte.

Tamanhos = contrato (o raio do corte casa com o alcance do golpe):
corte_90 47 (bengala, alcance 22) · corte_120 51 (cutelo 25) · corte_180 57 (machado 28) ·
giro_360 59 (machado pesado 30) · estocada 38×9 · disparo 11×7 · sangue 22×16 · parry 29 ·
impacto 17 · poeira 17×9 · corte (genérico) 51 · projétil 7×3.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import paleta as P  # noqa: E402
from kit.tela import Tela  # noqa: E402


def _tela(w, h):
    return Tela(w, h, P.RAMPAS)


def corte(tam, arco_graus, giro=False):
    """Meia-lua de golpe em 4 quadros: entra, cheia (o smear), sai, restos."""
    c = (tam - 1) / 2
    R = c - 1.5
    meio = arco_graus / 2
    quadros = []
    # (início, fim) do trecho visível em graus, espessura máxima, e se quebra em lascas
    fases = [(-meio, -meio + arco_graus * 0.45, 3.2, False),
             (-meio, meio, 5.5, False),
             (-meio + arco_graus * 0.35, meio, 3.0, True),
             (meio - arco_graus * 0.3, meio, 1.6, True)]
    if giro:
        fases = [(-180, -40, 3.5, False), (-180, 180, 5.0, False), (-60, 180, 3.0, True), (100, 180, 1.8, True)]
    rnd = random.Random(tam * 7 + arco_graus)
    for q, (a0, a1, esp, lascas) in enumerate(fases):
        t = _tela(tam, tam)
        for y in range(tam):
            for x in range(tam):
                dx, dy = x - c, y - c
                r = math.hypot(dx, dy)
                ang = math.degrees(math.atan2(dy, dx))
                if not (a0 <= ang <= a1):
                    continue
                # a espessura afina nas pontas do arco (meia-lua)
                u = (ang - a0) / max(1e-6, (a1 - a0))
                e = esp * math.sin(math.pi * min(1.0, max(0.0, u))) ** 0.6
                if giro and q == 1:
                    e = esp
                interno = R - e
                if not (interno <= r <= R):
                    continue
                k = (r - interno) / max(1e-6, e)      # 0 = dentro, 1 = fio de fora
                if lascas and rnd.random() < 0.18 + 0.2 * q / 3:
                    continue
                tom = 3 if k > 0.62 else (2 if k > 0.3 else (1 if k > 0.12 else 0))
                if q == 3:
                    tom = max(0, tom - 1)
                t.pinta(x, y, "luzfx", tom, grupo="fx")
        quadros.append(t.imagem())
    return quadros


def estocada():
    w, h = 38, 9
    out = []
    fases = [(0, 16, 1.5), (0, 37, 3.5), (8, 37, 2.0)]
    for q, (x0, x1, esp) in enumerate(fases):
        t = _tela(w, h)
        for x in range(x0, x1 + 1):
            u = (x - x0) / max(1, x1 - x0)
            e = esp * (0.35 + 0.65 * u) if q < 2 else esp * (1 - u * 0.6)
            for y in range(h):
                d = abs(y - 4)
                if d <= e / 2:
                    k = 1 - d / max(0.5, e / 2)
                    tom = 3 if k > 0.6 else (2 if k > 0.25 else 1)
                    if q == 2 and (x % 3 == 0):
                        continue
                    t.pinta(x, y, "luzfx", tom, grupo="fx")
        if q == 1:   # ponta mais clara e um brilho em cruz
            for (x, y) in ((36, 4), (35, 3), (35, 5), (37, 4)):
                t.pinta(x, y, "luzfx", 3, grupo="fx")
        out.append(t.imagem())
    return out


def disparo():
    w, h = 11, 7
    formas = [
        # estrela de pólvora
        {(0, 3): 3, (1, 3): 3, (2, 3): 3, (3, 3): 3, (4, 3): 2, (5, 3): 1, (2, 2): 2, (2, 4): 2,
         (3, 1): 1, (3, 5): 1, (1, 2): 3, (1, 4): 3, (2, 1): 1, (2, 5): 1},
        # cone de fogo
        {(0, 3): 3, (1, 3): 3, (2, 3): 3, (3, 3): 3, (4, 3): 3, (5, 3): 2, (6, 3): 2, (7, 3): 1,
         (1, 2): 3, (2, 2): 2, (3, 2): 2, (4, 2): 1, (1, 4): 3, (2, 4): 2, (3, 4): 2, (4, 4): 1,
         (3, 1): 1, (5, 2): 1, (3, 5): 1, (5, 4): 1, (8, 3): 0},
    ]
    out = []
    for f in formas:
        t = _tela(w, h)
        for (x, y), tom in f.items():
            t.pinta(x, y, "luzfx", tom, grupo="fx")
        out.append(t.imagem())
    # fumaça
    t = _tela(w, h)
    for (x, y, tom) in ((4, 3, 2), (5, 3, 2), (5, 2, 1), (6, 2, 1), (6, 3, 2), (7, 3, 1), (7, 4, 1),
                        (8, 2, 0), (9, 3, 0), (6, 4, 1), (8, 4, 0)):
        t.pinta(x, y, "poeira", tom, grupo="fx")
    out.append(t.imagem())
    return out


def sangue():
    """22×16, origem (4, 8): o jorro sai pra direita em arco e cai."""
    w, h = 22, 16
    rnd = random.Random(11)
    gotas = []
    for i in range(16):
        ang = math.radians(rnd.uniform(-40, 28))
        vel = rnd.uniform(2.4, 4.1)
        tam = rnd.choice((1, 1, 2, 2, 3))
        gotas.append((ang, vel, tam))
    out = []
    for q in range(5):
        t = _tela(w, h)
        tt = 0.8 + q * 0.85
        for ang, vel, tam in gotas:
            x = 4 + math.cos(ang) * vel * tt
            y = 8 + math.sin(ang) * vel * tt + 0.42 * tt * tt   # gravidade
            s = max(1, tam - (1 if q >= 3 else 0))
            for dx in range(s):
                for dy in range(s):
                    X, Y = int(round(x)) + dx, int(round(y)) + dy
                    if 0 <= X < w and 0 <= Y < h:
                        tom = 3 if (dx == 0 and dy == 0 and s > 1 and q < 2) else (2 if q < 3 else 1)
                        t.pinta(X, Y, "sangue", tom, grupo="fx")
        if q == 0:   # o núcleo do corte
            for (x, y) in ((4, 8), (5, 8), (5, 7), (6, 8), (4, 7), (5, 9)):
                t.pinta(x, y, "sangue", 3, grupo="fx")
        out.append(t.imagem())
    return out


def anel(tam, raios, espessuras, rampa="luzfx", faiscas=True):
    c = (tam - 1) / 2
    out = []
    rnd = random.Random(tam)
    for q, (R, e) in enumerate(zip(raios, espessuras)):
        t = _tela(tam, tam)
        for y in range(tam):
            for x in range(tam):
                r = math.hypot(x - c, y - c)
                if R - e <= r <= R:
                    k = (r - (R - e)) / max(1e-6, e)
                    tom = 3 if k > 0.5 else 2
                    if q >= 2:
                        tom -= 1
                    if q == 3 and (x + y) % 2:
                        continue
                    t.pinta(x, y, rampa, max(0, tom), grupo="fx")
        if faiscas:
            for i in range(8):
                ang = i * math.pi / 4 + 0.3
                d = R + 2 + q * 1.5
                x, y = int(round(c + math.cos(ang) * d)), int(round(c + math.sin(ang) * d))
                if 0 <= x < tam and 0 <= y < tam and q < 3:
                    t.pinta(x, y, rampa, 3 if q < 2 else 1, grupo="fx")
        if q == 0:
            for (x, y) in ((c, c), (c - 1, c), (c + 1, c), (c, c - 1), (c, c + 1)):
                t.pinta(int(x), int(y), rampa, 3, grupo="fx")
        out.append(t.imagem())
    return out


def impacto():
    tam = 17
    c = 8
    out = []
    # 0: estrela grande; 1: anel; 2: faíscas; 3: pontos
    t = _tela(tam, tam)
    for i in range(-6, 7):
        for (x, y) in ((c + i, c), (c, c + i)):
            k = abs(i)
            t.pinta(x, y, "luzfx", 3 if k < 3 else (2 if k < 5 else 1), grupo="fx")
    for i in range(-3, 4):
        t.pinta(c + i, c + i, "luzfx", 2 if abs(i) < 2 else 1, grupo="fx")
        t.pinta(c + i, c - i, "luzfx", 2 if abs(i) < 2 else 1, grupo="fx")
    out.append(t.imagem())
    out += anel(tam, [6, 7.5], [2.2, 1.2], faiscas=True)[:2]
    t = _tela(tam, tam)
    for ang in range(0, 360, 45):
        x = int(round(c + math.cos(math.radians(ang + 20)) * 7))
        y = int(round(c + math.sin(math.radians(ang + 20)) * 7))
        t.pinta(x, y, "luzfx", 1, grupo="fx")
    out.append(t.imagem())
    return out


def poeira():
    w, h = 17, 9
    out = []
    bolas = [(-4, 1.6), (0, 2.2), (4, 1.6), (-7, 1.0), (7, 1.0)]
    for q in range(4):
        t = _tela(w, h)
        for dx, r in bolas:
            R = r + q * 0.7
            cx, cy = 8 + dx * (1 + q * 0.25), 6 - q * 0.6
            for y in range(h):
                for x in range(w):
                    d = math.hypot(x - cx, (y - cy) * 1.4)
                    if d <= R:
                        k = d / R
                        tom = 2 if k < 0.5 else 1
                        if q >= 2:
                            tom -= 1
                        if q == 3 and (x * 7 + y * 3) % 5 < 2:
                            continue
                        t.pinta(x, y, "poeira", max(0, tom), grupo="fx")
        out.append(t.imagem())
    return out


def projetil():
    t = _tela(7, 3)
    for (x, y, r, tom) in ((0, 1, "luzfx", 0), (1, 1, "luzfx", 1), (2, 1, "luzfx", 1), (3, 1, "luzfx", 2),
                           (4, 1, "luzfx", 3), (5, 1, "luzfx", 3), (4, 0, "luzfx", 2), (4, 2, "luzfx", 2),
                           (5, 0, "luzfx", 1), (5, 2, "luzfx", 1), (6, 1, "luzfx", 2)):
        t.pinta(x, y, r, tom, grupo="fx")
    return [t.imagem()]


EFEITOS = {
    # nome: (função, origem, ms por quadro na prévia)
    "spr_fx_corte_90": (lambda: corte(47, 90), (23, 23)),
    "spr_fx_corte_120": (lambda: corte(51, 120), (25, 25)),
    "spr_fx_corte_180": (lambda: corte(57, 180), (28, 28)),
    "spr_fx_giro_360": (lambda: corte(59, 360, giro=True), (29, 29)),
    "spr_fx_estocada": (estocada, (0, 4)),
    "spr_fx_disparo": (disparo, (0, 3)),
    "spr_fx_sangue": (sangue, (4, 8)),
    "spr_fx_parry": (lambda: anel(29, [5, 9, 12, 13.5], [3, 2.5, 1.6, 1.2]), (14, 14)),
    "spr_fx_impacto": (impacto, (8, 8)),
    "spr_fx_poeira": (poeira, (8, 8)),
    "spr_fx_corte": (lambda: corte(51, 120), (25, 25)),
    "spr_projetil": (projetil, (4, 1)),
}


def quadros(nome):
    return EFEITOS[nome][0]()


if __name__ == "__main__":
    from kit import previa as pv
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "previa")
    pv.folha([(n.replace("spr_", ""), quadros(n)) for n in EFEITOS], k=3, larg_rotulo=130,
             titulo="efeitos", fundo_cel=(40, 34, 32, 255)).save(os.path.join(out, "efeitos_folha.png"))
    print("ok")
