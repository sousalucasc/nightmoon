"""Prévias: ampliação, silhueta, valores, folhas com rótulo, cena no chão, GIF e papel de cebola."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from . import paleta as pal

FUNDO_FOLHA = (30, 30, 34, 255)
TEXTO = (225, 225, 225, 255)


def _fonte(tam=12):
    for nome in ("segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(nome, tam)
        except OSError:
            pass
    return ImageFont.load_default()


def amplia(img, k, fundo=None):
    img = img.convert("RGBA")
    if fundo is not None:
        b = Image.new("RGBA", img.size, fundo)
        b.alpha_composite(img)
        img = b
    return img.resize((img.width * k, img.height * k), Image.NEAREST)


def silhueta(img, cor=(12, 10, 16, 255)):
    a = np.array(img.convert("RGBA"))
    out = np.zeros_like(a)
    m = a[:, :, 3] > 0
    out[m] = cor
    return Image.fromarray(out, "RGBA")


def valores(img):
    """Cinza perceptual (L*)."""
    a = np.array(img.convert("RGBA"))
    out = a.copy()
    cache = {}
    for y in range(a.shape[0]):
        for x in range(a.shape[1]):
            if a[y, x, 3] == 0:
                continue
            c = tuple(int(v) for v in a[y, x, :3])
            if c not in cache:
                v = int(round(pal.L(c) / 100 * 255))
                cache[c] = (v, v, v)
            out[y, x, :3] = cache[c]
    return Image.fromarray(out, "RGBA")


def folha(linhas, k=4, fundo_cel=(52, 54, 62, 255), margem=8, titulo=None, larg_rotulo=110):
    """linhas: lista de (rótulo, [imagens]). Cada imagem ampliada k vezes, lado a lado."""
    f = _fonte(12)
    cels = []
    for rot, ims in linhas:
        cels.append((rot, [amplia(i, k, fundo_cel) for i in ims]))
    W = larg_rotulo + max(sum(i.width + margem for i in ims) for _, ims in cels) + margem
    H = (24 if titulo else 0) + sum(max(i.height for i in ims) + margem for _, ims in cels) + margem
    tela = Image.new("RGBA", (W, H), FUNDO_FOLHA)
    d = ImageDraw.Draw(tela)
    y = margem
    if titulo:
        d.text((margem, 4), titulo, fill=TEXTO, font=_fonte(14))
        y += 24
    for rot, ims in cels:
        d.text((margem, y + 2), rot, fill=TEXTO, font=f)
        x = larg_rotulo
        for im in ims:
            tela.alpha_composite(im, (x, y))
            x += im.width + margem
        y += max(i.height for i in ims) + margem
    return tela


def cena(chao, sprites, k=1):
    """chao: imagem do chão; sprites: lista de (img, x, y, origem_x, origem_y), desenhados por y."""
    tela = chao.convert("RGBA").copy()
    for img, x, y, ox, oy in sorted(sprites, key=lambda s: s[2]):
        tela.alpha_composite(img.convert("RGBA"), (int(x - ox), int(y - oy)))
    return tela.resize((tela.width * k, tela.height * k), Image.NEAREST) if k > 1 else tela


def brilho_aditivo(img, luz, x, y):
    """Soma uma imagem de luz (RGBA) centrada em (x, y), como o bm_add do GameMaker."""
    base = np.array(img.convert("RGBA")).astype(np.int32)
    l = np.array(luz.convert("RGBA")).astype(np.int32)
    h, w = l.shape[:2]
    x0, y0 = int(x - w // 2), int(y - h // 2)
    for j in range(h):
        for i in range(w):
            X, Y = x0 + i, y0 + j
            if 0 <= X < base.shape[1] and 0 <= Y < base.shape[0]:
                a = l[j, i, 3] / 255.0
                base[Y, X, :3] = np.minimum(255, base[Y, X, :3] + (l[j, i, :3] * a).astype(np.int32))
    return Image.fromarray(base.astype(np.uint8), "RGBA")


def gif(quadros, duracoes_ms, caminho, k=4, fundo=(52, 54, 62, 255)):
    ims = [amplia(q, k, fundo).convert("P", palette=Image.ADAPTIVE) for q in quadros]
    if isinstance(duracoes_ms, (int, float)):
        duracoes_ms = [duracoes_ms] * len(ims)
    ims[0].save(caminho, save_all=True, append_images=ims[1:], duration=list(duracoes_ms), loop=0, disposal=2)


def cebola(quadros, k=6, fundo=(52, 54, 62, 255)):
    """Todos os quadros sobrepostos com transparência (o último por cima, opaco)."""
    w, h = quadros[0].size
    base = Image.new("RGBA", (w, h), fundo)
    n = len(quadros)
    for i, q in enumerate(quadros):
        a = np.array(q.convert("RGBA")).copy()
        alfa = 0.25 + 0.75 * (i + 1) / n
        a[:, :, 3] = (a[:, :, 3] * alfa).astype(np.uint8)
        base.alpha_composite(Image.fromarray(a, "RGBA"))
    return amplia(base, k)


def rotular(img, texto, alto=18):
    f = _fonte(12)
    t = Image.new("RGBA", (img.width, img.height + alto), FUNDO_FOLHA)
    t.alpha_composite(img.convert("RGBA"), (0, alto))
    ImageDraw.Draw(t).text((4, 2), texto, fill=TEXTO, font=f)
    return t


def lado_a_lado(imagens, margem=10, fundo=FUNDO_FOLHA):
    W = sum(i.width for i in imagens) + margem * (len(imagens) + 1)
    H = max(i.height for i in imagens) + 2 * margem
    t = Image.new("RGBA", (W, H), fundo)
    x = margem
    for i in imagens:
        t.alpha_composite(i.convert("RGBA"), (x, margem))
        x += i.width + margem
    return t


def empilha(imagens, margem=10, fundo=FUNDO_FOLHA):
    W = max(i.width for i in imagens) + 2 * margem
    H = sum(i.height for i in imagens) + margem * (len(imagens) + 1)
    t = Image.new("RGBA", (W, H), fundo)
    y = margem
    for i in imagens:
        t.alpha_composite(i.convert("RGBA"), (margem, y))
        y += i.height + margem
    return t


def grade(img, k=16, fundo=(52, 54, 62, 255), cor_linha=(80, 82, 92, 255), numeros=True):
    """Ampliação com grade de pixel e números das colunas/linhas, pra editar o ASCII."""
    big = amplia(img, k, fundo)
    m = 18 if numeros else 0
    t = Image.new("RGBA", (big.width + m, big.height + m), FUNDO_FOLHA)
    t.alpha_composite(big, (m, m))
    d = ImageDraw.Draw(t)
    w, h = img.size
    for x in range(w + 1):
        d.line([(m + x * k, m), (m + x * k, m + h * k)], fill=cor_linha, width=1)
    for y in range(h + 1):
        d.line([(m, m + y * k), (m + w * k, m + y * k)], fill=cor_linha, width=1)
    if numeros:
        f = _fonte(10)
        for x in range(w):
            d.text((m + x * k + 2, 2), str(x % 10), fill=(200, 200, 120, 255) if x % 10 == 0 else TEXTO, font=f)
        for y in range(h):
            d.text((2, m + y * k + 2), str(y), fill=TEXTO, font=f)
    return t
