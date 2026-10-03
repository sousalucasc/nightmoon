"""Pano preso em (u, v): saia de casaco, capa e cauda cujas dobras andam junto com o pano.

As dobras são faixas pintadas em u (0 = borda esquerda, 1 = borda direita) que o módulo da
sprite escolhe à mão; o código só estica essas faixas entre a cintura e a barra de cada quadro.
Assim a dobra não treme quando a barra balança (ela está presa no pano, não na tela).
"""


def _lerp(a, b, t):
    return a + (b - a) * t


def saia(y0, y1, cintura, barra, faixas, curva=1.25, barra_tons=None, topo_tons=None, abertura=None,
         recorte=None, linha_barra=None):
    """Devolve lista de (x, y, rampa, tom).

    cintura: (x_esq, x_dir) na linha y0; barra: (x_esq, x_dir) na linha y1.
    faixas: lista de (u_ate, (rampa, tom)) em ordem crescente de u; o tom vale até u_ate.
    curva: >1 abre mais embaixo (sino); 1 = trapézio reto.
    barra_tons: dict {(rampa, tom): (rampa, tom)} que escurece a última linha (sujeira da barra).
    topo_tons: idem pras 1-2 primeiras linhas (sombra da capa por cima).
    abertura: (u0, u1, (rampa, tom)) a frente do casaco (forro aparecendo), pode variar com v:
              função v -> (u_centro) ou número fixo.
    recorte: (rampa, tom) do fio frio na borda direita (só onde a linha tem >= 6 px).
    linha_barra: lista de deslocamentos por coluna relativa (ondulação da barra), ex. [0, 0, 1, 0].
    """
    px = []
    n = y1 - y0
    for y in range(y0, y1 + 1):
        v = (y - y0) / n if n else 1.0
        tv = v ** curva
        xe = round(_lerp(cintura[0], barra[0], tv))
        xd = round(_lerp(cintura[1], barra[1], tv))
        larg = max(1, xd - xe)
        for x in range(xe, xd + 1):
            u = (x - xe) / larg
            cor = faixas[-1][1]
            for u_ate, c in faixas:
                if u <= u_ate:
                    cor = c
                    break
            if abertura is not None:
                uc = abertura[0](v) if callable(abertura[0]) else abertura[0]
                if abs(u - uc) <= abertura[1] / 2 + 1e-9:
                    cor = abertura[2]
            if recorte is not None and x == xd and (xd - xe) >= 6 and 0.45 <= v <= 0.65:
                cor = recorte
            if y <= y0 + 1 and topo_tons:
                cor = topo_tons.get(cor, cor)
            if y == y1 and barra_tons:
                cor = barra_tons.get(cor, cor)
            px.append((x, y, cor[0], cor[1]))
        if y == y1 and linha_barra:
            # barra ondulada: alguns pixels descem 1 linha
            for i, d in enumerate(linha_barra):
                x = xe + i * max(1, (xd - xe) // max(1, len(linha_barra) - 1))
                if d and xe <= x <= xd:
                    c = next(((r, t) for (xx, yy, r, t) in px if xx == x and yy == y), None)
                    if c:
                        px.append((x, y + d, c[0], c[1]))
    return px
