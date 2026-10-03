"""Cor: conversões (sRGB, CIELAB, OKLab/OKLCh), ΔE, L*, contraste e rampas com matiz girando.

Tudo em tuplas RGB de 0 a 255. As rampas saem do escuro pro claro.
"""
import math


# --- sRGB <-> linear -------------------------------------------------------

def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _gam(c):
    c = max(0.0, min(1.0, c))
    v = 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
    return v * 255.0


# --- CIELAB (D65) ----------------------------------------------------------

def lab(rgb):
    r, g, b = (_lin(v) for v in rgb[:3])
    x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047
    y = (0.2126729 * r + 0.7151522 * g + 0.0721750 * b) / 1.0
    z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116

    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def L(rgb):
    """L* perceptual (0 = preto, 100 = branco)."""
    return lab(rgb)[0]


def delta_e(c1, c2):
    """CIEDE2000 entre duas cores RGB. Abaixo de ~5, o olho não separa no jogo (cor gêmea)."""
    return delta_e_lab(lab(c1), lab(c2))


def delta_e_lab(lab1, lab2):
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    C1 = math.hypot(a1, b1)
    C2 = math.hypot(a2, b2)
    Cm = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cm ** 7 / (Cm ** 7 + 25 ** 7))) if Cm > 0 else 0.5
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if C1p > 0 else 0.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if C2p > 0 else 0.0
    dLp = L2 - L1
    dCp = C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    else:
        dhp = h2p - h1p
        if dhp > 180:
            dhp -= 360
        elif dhp < -180:
            dhp += 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp / 2))
    Lpm = (L1 + L2) / 2
    Cpm = (C1p + C2p) / 2
    if C1p * C2p == 0:
        hpm = h1p + h2p
    else:
        hpm = (h1p + h2p) / 2
        if abs(h1p - h2p) > 180:
            hpm += 180 if (h1p + h2p) < 360 else -180
    T = (1 - 0.17 * math.cos(math.radians(hpm - 30)) + 0.24 * math.cos(math.radians(2 * hpm))
         + 0.32 * math.cos(math.radians(3 * hpm + 6)) - 0.20 * math.cos(math.radians(4 * hpm - 63)))
    dth = 30 * math.exp(-(((hpm - 275) / 25) ** 2))
    Rc = 2 * math.sqrt(Cpm ** 7 / (Cpm ** 7 + 25 ** 7)) if Cpm > 0 else 0
    Sl = 1 + (0.015 * (Lpm - 50) ** 2) / math.sqrt(20 + (Lpm - 50) ** 2)
    Sc = 1 + 0.045 * Cpm
    Sh = 1 + 0.015 * Cpm * T
    Rt = -math.sin(math.radians(2 * dth)) * Rc
    return math.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2 + Rt * (dCp / Sc) * (dHp / Sh))


def luminancia(rgb):
    r, g, b = (_lin(v) for v in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(c1, c2):
    """Razão de contraste (WCAG): 1 a 21."""
    l1, l2 = luminancia(c1), luminancia(c2)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


# --- OKLab / OKLCh ---------------------------------------------------------

def oklab(rgb):
    r, g, b = (_lin(v) for v in rgb[:3])
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)


def de_oklab(Lk, a, b):
    l_ = Lk + 0.3963377774 * a + 0.2158037573 * b
    m_ = Lk - 0.1055613458 * a - 0.0638541728 * b
    s_ = Lk - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return (r, g, bb)


def oklch(rgb):
    Lk, a, b = oklab(rgb)
    return (Lk, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360)


def _cabe(r, g, b):
    return all(-1e-6 <= v <= 1 + 1e-6 for v in (r, g, b))


def de_oklch(Lk, C, h):
    """OKLCh -> RGB 0-255; se sair do gamut, reduz o croma até caber (mantém L e h)."""
    lo, hi = 0.0, C
    a, b = C * math.cos(math.radians(h)), C * math.sin(math.radians(h))
    r, g, bb = de_oklab(Lk, a, b)
    if not _cabe(r, g, bb):
        for _ in range(30):
            mid = (lo + hi) / 2
            a, b = mid * math.cos(math.radians(h)), mid * math.sin(math.radians(h))
            r, g, bb = de_oklab(Lk, a, b)
            if _cabe(r, g, bb):
                lo = mid
            else:
                hi = mid
        a, b = lo * math.cos(math.radians(h)), lo * math.sin(math.radians(h))
        r, g, bb = de_oklab(Lk, a, b)
    return tuple(int(round(_gam(v))) for v in (r, g, bb))


def rampa(L0, L1, C, h_meio, n, giro=30.0, croma_pontas=0.45, quente=70.0):
    """Rampa de n tons, do escuro (L0) ao claro (L1), em OKLCh.

    - O matiz parte de h_meio e gira: a sombra vai pro frio (azul/roxo, ~280°) e a luz pro
      quente (amarelo, ~`quente`°), no total de `giro` graus de ponta a ponta.
    - O croma faz um arco: C no meio, C * croma_pontas nas duas pontas.
    Devolve lista de RGB.
    """
    out = []
    for i in range(n):
        t = i / (n - 1) if n > 1 else 0.5
        Lk = L0 + (L1 - L0) * t
        # matiz: puxa pro frio no escuro e pro quente no claro, pelo caminho mais curto
        alvo_frio, alvo_quente = 285.0, quente
        def puxa(h, alvo, k):
            d = ((alvo - h + 180) % 360) - 180
            return (h + max(-abs(d), min(abs(d), k)) * (1 if d >= 0 else -1)) % 360
        if t < 0.5:
            h = puxa(h_meio, alvo_frio, giro * (0.5 - t))
        else:
            h = puxa(h_meio, alvo_quente, giro * (t - 0.5))
        arco = 1 - (1 - croma_pontas) * (abs(t - 0.5) * 2) ** 1.5
        out.append(de_oklch(Lk, C * arco, h))
    return out


def hexa(rgb):
    return "#%02x%02x%02x" % tuple(rgb[:3])


def de_hexa(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def gemeas(cores, limite=5.0):
    """Pares de cores com ΔE2000 abaixo do limite."""
    cs = list(cores)
    pares = []
    for i in range(len(cs)):
        for j in range(i + 1, len(cs)):
            d = delta_e(cs[i], cs[j])
            if d < limite:
                pares.append((cs[i], cs[j], d))
    return pares
