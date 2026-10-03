"""Montador genérico de personagem: carimbos pintados à mão + pano em (u, v) + remendos.

    b = Boneco(w, h, paleta, legenda, pecas, ordem, saia=cfg)
    img = b.montar(pose).imagem()

pecas: {"cab": {"normal": SEG, ...}, "tronco": {...}, ...}  (texto 'y: x0 ...' em coordenadas do
       quadro-base; a pose desloca)
ordem: lista de camadas, de trás pra frente. Cada camada é:
       - nome de grupo de peças (a pose dá (variante, dx, dy); com `rel` o deslocamento soma o
         x/y do corpo) ;
       - "saia" (pano do kit.tecido) ;
       - "lista:<chave>" (lista absoluta de (texto, x, y) na pose, ex. botas) ;
       - "remendos" (textos absolutos pintados por cima).
Pose: {"x": dx do corpo, "y": dy do corpo, "<grupo>": (variante, dx, dy) ou None, "saia": {...},
       "<lista>": [...], "remendos": [...], "quadro": texto (quadro inteiro à mão)}.
"""
from . import tecido
from .tela import Tela, de_segmentos


class Boneco:
    def __init__(self, w, h, paleta, legenda, pecas, ordem, saia=None, rel=None, padrao=None,
                 contorno=("contorno", 0), grupos_arma=()):
        self.w, self.h = w, h
        self.paleta, self.leg = paleta, legenda
        self.pecas, self.ordem = pecas, ordem
        self.saia_cfg = saia or {}
        self.rel = set(rel if rel is not None else pecas.keys())
        self.padrao = padrao or {}
        self.contorno = contorno

    def _seg(self, t, texto, dx=0, dy=0, grupo="corpo"):
        de_segmentos(texto, self.leg, self.paleta, self.w, self.h, tela=t, dx=dx, dy=dy, grupo=grupo)

    def montar(self, pose):
        p = dict(self.padrao)
        p.update(pose)
        t = Tela(self.w, self.h, self.paleta)
        if "quadro" in p:
            self._seg(t, p["quadro"])
            if self.contorno:
                t.contorno(self.contorno)
            return t
        bx, by = p.get("x", 0), p.get("y", 0)
        for camada in self.ordem:
            if camada == "saia":
                s = dict(self.saia_cfg)
                s.update(p.get("saia", {}))
                if s.get("nenhuma"):
                    continue
                y0 = s["y0"] + by
                cint = s.get("cintura_abs") or (s["cintura"][0] + bx, s["cintura"][1] + bx)
                px = tecido.saia(y0, s["y1"], cint, s["barra"], s["faixas"], curva=s.get("curva", 1.25),
                                 topo_tons=s.get("topo"), barra_tons=s.get("barra_tons"),
                                 abertura=s.get("abertura"), recorte=s.get("recorte"))
                for x, y, r, tom in px:
                    t.pinta(x, y, r, tom)
                for (txt, x, y) in s.get("pontas", []):   # farrapos da barra
                    self._seg(t, txt, x, y)
            elif camada.startswith("lista:"):
                for (txt, x, y) in p.get(camada[6:], []):
                    self._seg(t, txt, x, y)
            elif camada == "remendos":
                for rem in p.get("remendos", []):
                    if isinstance(rem, tuple):
                        self._seg(t, rem[0], rem[1], rem[2])
                    else:
                        self._seg(t, rem)
            else:
                v = p.get(camada)
                if not v:
                    continue
                var, dx, dy = v
                if camada in self.rel:
                    dx, dy = dx + bx, dy + by
                self._seg(t, self.pecas[camada][var], dx, dy)
        if self.contorno:
            t.contorno(self.contorno)
        return t
