"""Grava e lê .aseprite (RGBA, uma camada, tags por animação, pivô na origem, paleta nas amostras).

Formato: https://github.com/aseprite/aseprite/blob/main/docs/ase-file-specs.md
Só o subconjunto que a skill usa. `confere()` faz a ida e volta pixel por pixel.
"""
import struct
import zlib

from PIL import Image


def _str(s):
    b = s.encode("utf-8")
    return struct.pack("<H", len(b)) + b


def _chunk(tipo, dados):
    return struct.pack("<IH", len(dados) + 6, tipo) + dados


def grava(caminho, quadros, duracoes, tags=(), paleta=(), pivo=None, camada="sprite"):
    """quadros: lista de PIL RGBA do mesmo tamanho; duracoes: ms por quadro;
    tags: lista de (nome, de, ate); paleta: lista de RGB; pivo: (x, y) da origem."""
    w, h = quadros[0].size
    frames = []
    for i, (q, dur) in enumerate(zip(quadros, duracoes)):
        chunks = []
        if i == 0:
            # paleta (amostras)
            if paleta:
                n = len(paleta)
                dados = struct.pack("<III", n, 0, n - 1) + b"\0" * 8
                for (r, g, b) in paleta:
                    dados += struct.pack("<HBBBB", 0, r, g, b, 255)
                chunks.append(_chunk(0x2019, dados))
            # camada
            dados = struct.pack("<HHHHHHB", 3, 0, 0, 0, 0, 0, 255) + b"\0" * 3 + _str(camada)
            chunks.append(_chunk(0x2004, dados))
            # tags
            if tags:
                dados = struct.pack("<H", len(tags)) + b"\0" * 8
                for nome, de, ate in tags:
                    dados += struct.pack("<HHBH", de, ate, 0, 0) + b"\0" * 6 + bytes((0, 0, 0)) + b"\0" + _str(nome)
                chunks.append(_chunk(0x2018, dados))
            # pivô (fatia do quadro inteiro com pivô na origem)
            if pivo is not None:
                dados = struct.pack("<III", 1, 2, 0) + _str("origem")
                dados += struct.pack("<IiiII", 0, 0, 0, w, h) + struct.pack("<ii", pivo[0], pivo[1])
                chunks.append(_chunk(0x2022, dados))
        # cel comprimido
        px = q.convert("RGBA").tobytes()
        dados = struct.pack("<HhhBHh", 0, 0, 0, 255, 2, 0) + b"\0" * 5 + struct.pack("<HH", w, h) + zlib.compress(px, 9)
        chunks.append(_chunk(0x2005, dados))
        corpo = b"".join(chunks)
        cab = struct.pack("<IHHHH", 16 + len(corpo), 0xF1FA, min(len(chunks), 0xFFFF), int(dur), 0) + struct.pack("<I", len(chunks))
        frames.append(cab + corpo)
    corpo = b"".join(frames)
    cab = struct.pack("<IHHHHHIH", 128 + len(corpo), 0xA5E0, len(quadros), w, h, 32, 1, 100)
    cab += struct.pack("<II", 0, 0) + bytes((0, 0, 0, 0)) + struct.pack("<H", 0) + bytes((1, 1))
    cab += struct.pack("<hhHH", 0, 0, 16, 16)
    cab += b"\0" * (128 - len(cab))
    with open(caminho, "wb") as f:
        f.write(cab + corpo)


def le(caminho):
    """Devolve (quadros PIL, duracoes, tags, pivo)."""
    d = open(caminho, "rb").read()
    tam, magia, n, w, h, prof = struct.unpack_from("<IHHHHH", d, 0)
    assert magia == 0xA5E0 and prof == 32, "não é .aseprite RGBA"
    pos = 128
    quadros, duracoes, tags, pivo = [], [], [], None
    for _ in range(n):
        ftam, fmag, _velho, dur = struct.unpack_from("<IHHH", d, pos)
        assert fmag == 0xF1FA
        nchunks = struct.unpack_from("<I", d, pos + 12)[0]
        p = pos + 16
        img = Image.new("RGBA", (w, h))
        for _c in range(nchunks):
            ctam, ctipo = struct.unpack_from("<IH", d, p)
            dados = d[p + 6:p + ctam]
            if ctipo == 0x2005:
                _lay, x, y, _op, tipo, _z = struct.unpack_from("<HhhBHh", dados, 0)
                cw, ch = struct.unpack_from("<HH", dados, 16)
                if tipo == 2:
                    px = zlib.decompress(dados[20:])
                    img.paste(Image.frombytes("RGBA", (cw, ch), px), (x, y))
            elif ctipo == 0x2018:
                nt = struct.unpack_from("<H", dados, 0)[0]
                q = 10
                for _t in range(nt):
                    de, ate = struct.unpack_from("<HH", dados, q)
                    q += 17
                    ln = struct.unpack_from("<H", dados, q)[0]
                    nome = dados[q + 2:q + 2 + ln].decode("utf-8")
                    q += 2 + ln
                    tags.append((nome, de, ate))
            elif ctipo == 0x2022:
                nk, flags = struct.unpack_from("<II", dados, 0)
                ln = struct.unpack_from("<H", dados, 12)[0]
                q = 14 + ln
                if flags & 2:
                    pivo = struct.unpack_from("<ii", dados, q + 20)
            p += ctam
        quadros.append(img)
        duracoes.append(dur)
        pos += ftam
    return quadros, duracoes, tags, pivo


def confere(caminho, quadros, tags=None, pivo=None):
    """Ida e volta pixel por pixel. Devolve lista de problemas (vazia = ok)."""
    q2, _d, t2, p2 = le(caminho)
    prob = []
    if len(q2) != len(quadros):
        prob.append(f"{len(q2)} quadros lidos, {len(quadros)} gravados")
    for i, (a, b) in enumerate(zip(quadros, q2)):
        if a.convert("RGBA").tobytes() != b.tobytes():
            prob.append(f"quadro {i} diferente")
    if tags is not None and list(map(tuple, tags)) != list(map(tuple, t2)):
        prob.append(f"tags diferentes: {t2}")
    if pivo is not None and tuple(pivo) != tuple(p2 or ()):
        prob.append(f"pivô diferente: {p2}")
    return prob
