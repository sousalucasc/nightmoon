"""Comandos da arte do Nightmoon.

    python tools/sprites/sprites.py audita      # auditoria de todas as sprites (texto em previa/)
    python tools/sprites/sprites.py exporta     # grava tudo em arte/ (tiras, prévias, origens.md) + .aseprite
    python tools/sprites/sprites.py previa      # folhas e GIFs em tools/sprites/previa/

Cada módulo (personagens/, inimigos/, chefes/, armas/, fx/, cenario/, hud/) é a fonte da
verdade da sua sprite. Não edite os PNG em arte/: eles são gerados daqui.
"""
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import paleta as P  # noqa: E402
from kit import auditoria as au  # noqa: E402
from kit import exporta as ex  # noqa: E402
from kit import previa as pv  # noqa: E402

PREVIA = os.path.join(AQUI, "previa")


def personagens():
    """(nome_base, pasta_arte, origem, módulo, {anim_do_modulo: nome_no_jogo}, pacote)"""
    from chefes import chefe_besta, chefe_humano, dama
    from inimigos import aldeao, brutamontes
    from personagens import cacador
    return [
        ("spr_player", "player", (16, 30), cacador,
         {a: a for a in ("idle", "walk", "backstep", "dash", "ataque", "tiro", "cura", "hit", "visceral", "morte")},
         "personagens/cacador"),
        ("spr_aldeao", "inimigos", (16, 30), aldeao,
         {a: a for a in ("idle", "walk", "ataque", "hit", "stagger", "caido", "morte")}, "inimigos/aldeao"),
        ("spr_brutamontes", "inimigos", (24, 45), brutamontes,
         {a: a for a in ("idle", "walk", "pancada", "agarrao", "stagger", "caido", "morte")}, "inimigos/brutamontes"),
        ("spr_chefe", "chefes", (24, 45), chefe_humano,
         {a: a for a in ("idle", "walk", "ataque", "tiro", "salto", "stagger", "caido")}, "chefes/chefe_humano"),
        ("spr_chefe_besta", "chefes", (32, 60), chefe_besta,
         {a: a for a in ("idle", "corrida", "garra", "investida", "salto", "stagger", "caido", "morte")},
         "chefes/chefe_besta"),
        ("spr_dama", "chefes", (16, 30), dama,
         {a: a for a in ("idle", "walk", "ataque", "estocada", "passo", "stagger", "caido", "transforma", "morte")},
         "chefes/dama"),
    ]


def todas_as_sprites():
    """Lista de (nome, quadros, pasta, origem, ms, tipo) de TUDO, na ordem do origens.md."""
    from armas import armas
    from cenario import props, tiles
    from chefes import chefe_besta, dama
    from fx import efeitos
    from hud import fonte, hud, titulo
    lista = []
    pers = {p[0]: p for p in personagens()}

    def anims(base):
        nome, pasta, orig, mod, mapa, _pac = pers[base]
        for a_mod, a_jogo in mapa.items():
            lista.append((f"{nome}_{a_jogo}", mod.quadros(a_mod), pasta, orig, mod.ANIMS[a_mod][1], "personagem"))

    anims("spr_player")
    for n in ("spr_arma_bengala", "spr_arma_machado", "spr_arma_cutelo", "spr_arma_pistola", "spr_arma_escopeta",
              "spr_arma_foice"):
        lista.append((n, [armas.imagem(n)], "armas", armas.origem(n), 100, "arma"))
    for n in ("spr_fx_corte_90", "spr_fx_corte_120", "spr_fx_corte_180", "spr_fx_giro_360", "spr_fx_estocada",
              "spr_fx_disparo", "spr_fx_sangue", "spr_fx_parry", "spr_fx_impacto", "spr_fx_poeira", "spr_fx_corte",
              "spr_projetil"):
        lista.append((n, efeitos.quadros(n), "efeitos", efeitos.EFEITOS[n][1], 50, "fx"))
    anims("spr_aldeao")
    anims("spr_brutamontes")
    anims("spr_chefe")
    lista.append(("spr_chefe_transforma", chefe_besta.transforma(), "chefes", (32, 60), 190, "personagem"))
    anims("spr_chefe_besta")
    anims("spr_dama")
    for n in ("spr_arma_dama_longa", "spr_arma_dama_longa_sangue"):
        lista.append((n, [armas.imagem(n)], "armas", armas.origem(n), 100, "arma"))
    lista.append(("spr_fx_aura_sangue", dama.aura(), "efeitos", (16, 30), 120, "fx"))
    lista.append(("spr_tiles_rua", [tiles.montar()], "cenario", (0, 0), 100, "tileset"))
    for n in ("spr_lanterna", "spr_poste", "spr_pilar", "spr_caixote", "spr_barril", "spr_carroca", "spr_caixao",
              "spr_cerca", "spr_boneco", "spr_atalho", "spr_nevoa", "spr_mancha", "spr_luz"):
        lista.append((n, props.quadros(n), "cenario", props.PROPS[n][1], 125 if n == "spr_lanterna" else 150, "prop"))
    for n in ("spr_icone_frasco", "spr_icone_bala", "spr_icone_almas", "spr_icone_vida", "spr_icone_stamina",
              "spr_icone_forca", "spr_icone_destreza", "spr_icone_bengala", "spr_icone_machado", "spr_icone_cutelo",
              "spr_icone_pistola", "spr_icone_escopeta", "spr_mira", "spr_hud_moldura", "spr_hud_vida",
              "spr_hud_stamina", "spr_hud_chefe"):
        lista.append((n, [hud.imagem(n)], "ui", hud.ITENS[n][1], 100, "ui"))
    lista.append(("spr_fonte", fonte.quadros(), "ui", (0, 0), 100, "fonte"))
    lista.append(("spr_logo", [titulo.logo()], "ui", (57, 17), 100, "ui"))
    lista.append(("spr_fundo_titulo", [titulo.fundo_titulo()], "ui", (0, 0), 100, "ui"))
    return lista


# alfa parcial de propósito (o código desenha com alfa/aditivo, ou é sombra no chão)
ALFA_OK = {"spr_nevoa", "spr_luz", "spr_fonte", "spr_tiles_rua"}
TIER = {(32, 32): (24, 30), (48, 48): (30, 41), (64, 64): (38, 54)}
# quadros no ar ou em bote (a sola sai da linha de propósito)
ORIGEM_OK = {("spr_player_backstep", 1), ("spr_dama_passo", 1), ("spr_chefe_besta_garra", 1),
             ("spr_chefe_besta_investida", 1)}
ORIGEM_OK_TODAS = {"spr_chefe_besta_corrida"}          # galope: há quadros com as duas patas no ar
# branco puro que o código tinge (luz) e o pixel de alfa 1 do espaço da fonte
COR_OK = {"spr_luz", "spr_fonte"}


def audita():
    lista = todas_as_sprites()
    cores = P.todas()
    linhas, erros, avisos = [], 0, 0
    for nome, qs, pasta, orig, _ms, tipo in lista:
        ctx = {"paleta": cores, "fx": tipo in ("fx", "tileset", "fonte", "ui", "prop", "arma"),
               "contorno": "fechado" if tipo in ("personagem", "arma") else "nenhum"}
        if tipo == "personagem":
            ctx["origem"] = orig
        if tipo in ("fx", "tileset", "ui", "prop", "fonte", "arma"):
            ctx["borda_ok"] = {"cima", "baixo", "esq", "dir"}
        res = []
        for i, q in enumerate(qs):
            rel = au.audita_quadro(q, ctx)
            for r in rel:
                if r.nivel == "ERRO":
                    if r.nome == "alfa_binario" and nome in ALFA_OK:
                        continue
                    if r.nome == "origem" and (any(k in nome for k in ("morte", "caido", "salto", "transforma"))
                                               or (nome, i) in ORIGEM_OK or nome in ORIGEM_OK_TODAS):
                        continue
                    if r.nome == "so_paleta" and nome in COR_OK:
                        continue
                    res.append(f"  [{i}] ERRO {r.nome}: {r.valor}")
                    erros += 1
        if res:
            linhas.append(nome)
            linhas += res
    txt = f"{erros} erro(s) em {len(lista)} sprites\n" + "\n".join(linhas)
    os.makedirs(PREVIA, exist_ok=True)
    open(os.path.join(PREVIA, "auditoria_geral.txt"), "w", encoding="utf-8").write(txt)
    return txt, erros


def _limpa_previa(pasta):
    d = os.path.join(ex.ARTE, pasta, "previa")
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d, exist_ok=True)
    return d


def exporta():
    txt, erros = audita()
    if erros:
        print(txt)
        raise SystemExit("exportação recusada: há ERRO na auditoria")
    lista = todas_as_sprites()
    for pasta in ("player", "inimigos", "chefes", "armas", "efeitos", "cenario", "ui"):
        _limpa_previa(pasta)
    # sobra da arte antiga que não é sprite
    velho = os.path.join(ex.ARTE, "player", "spr_player_folha.png")
    if os.path.exists(velho):
        os.remove(velho)
    registro = []
    for nome, qs, pasta, orig, ms, tipo in lista:
        fundo = (52, 54, 62, 255) if tipo != "fx" else (40, 34, 32, 255)
        r = ex.salva_sprite(nome, qs, pasta, orig, duracao_ms=ms, gif=(len(qs) > 1 and tipo not in ("fonte",)),
                            fundo_gif=fundo, k_gif=3 if qs[0].width >= 48 else 4)
        if nome == "spr_tiles_rua":
            r["nota"] = " (tileset 16×16)"
        registro.append(r)
    ex.registro_md(registro)
    # .aseprite + spritesheet por personagem
    paleta = []
    for rr in P.RAMPAS.values():
        for c in rr:
            if c not in paleta:
                paleta.append(c)
    problemas = []
    for nome, pasta, orig, mod, mapa, pac in personagens():
        anims = [(a_jogo, mod.quadros(a_mod), mod.ANIMS[a_mod][1]) for a_mod, a_jogo in mapa.items()]
        if nome == "spr_chefe_besta":
            from chefes import chefe_besta
            anims.insert(0, ("transforma", chefe_besta.transforma(), 190))
        problemas += [f"{pac}: {p}" for p in ex.salva_aseprite(os.path.join(AQUI, pac + ".aseprite"), anims, paleta, orig)]
    P.gpl(os.path.join(AQUI, "nightmoon.gpl"))
    previas_jogo()
    print(f"exportado: {len(lista)} sprites; .aseprite: {'ok' if not problemas else problemas}")


def previas_jogo():
    """Prévias que o tutorial cita (arte/*/previa) + folhas de cada personagem."""
    from cenario import guias
    from hud import fonte, hud, titulo
    import random
    from PIL import Image
    # folhas por personagem
    for nome, pasta, orig, mod, mapa, pac in personagens():
        linhas = [(a_jogo, mod.quadros(a_mod)) for a_mod, a_jogo in mapa.items()]
        k = 4 if mod.quadros(list(mapa)[0])[0].width <= 32 else (3 if mod.quadros(list(mapa)[0])[0].width <= 48 else 2)
        pv.folha(linhas, k=k, larg_rotulo=100, titulo=nome).save(os.path.join(ex.ARTE, pasta, "previa", f"{nome}_folha.png"))
    # armas (uma por linha, origem marcada) e escala do elenco lado a lado
    from armas import armas
    pv.folha([(n.replace("spr_arma_", ""), [armas.imagem(n)]) for n in armas.ARMAS], k=6, larg_rotulo=150,
             titulo="armas (apontando pra direita; origem = cabo)").save(os.path.join(ex.ARTE, "armas", "previa", "armas.png"))
    elenco = elenco_escala()
    elenco.save(os.path.join(ex.ARTE, "chefes", "previa", "escala_elenco.png"))
    elenco.save(os.path.join(ex.ARTE, "inimigos", "previa", "escala_elenco.png"))
    # cenário: guias, mapa do tileset, cena
    d = os.path.join(ex.ARTE, "cenario", "previa")
    for n in guias.POSICOES:
        guias.guia(n).save(os.path.join(d, f"guia_{n}.png"))
    guias.mapa_tileset().save(os.path.join(d, "tileset_mapa.png"))
    cena_rua().save(os.path.join(d, "cena_rua.png"))
    # ui
    d = os.path.join(ex.ARTE, "ui", "previa")
    lg, f = titulo.logo(), titulo.fundo_titulo()
    tela = f.copy()
    tela.alpha_composite(Image.new("RGBA", f.size, (0, 0, 0, int(255 * 0.3))))
    tela.alpha_composite(lg, (160 - 57, 30 - 17))
    for i, (txt, cor) in enumerate((("> Começar <", (255, 255, 0)), ("Sair", None))):
        im = fonte.escrever(txt, cor=cor)
        tela.alpha_composite(im, (160 - im.width // 2, 60 + i * 14))
    pv.amplia(tela, 3).save(os.path.join(d, "titulo.png"))
    pv.folha([(n.replace("spr_", ""), [hud.imagem(n)]) for n in hud.ITENS], k=6, larg_rotulo=130).save(
        os.path.join(d, "icones.png"))
    hud_cena().save(os.path.join(d, "hud.png"))
    amostra = ["NIGHTMOON  Começar  Sair", "Almas insuficientes  CAÇA ENCERRADA", "VOCÊ MORREU  Tempo: 12 min 05 s",
               "abcdefghijklmnopqrstuvwxyz 0123456789", ".,:;!?-+()<>/'\"%_*= ÁÀÂÃÉÊÍÓÔÕÚ áàâãéêíóôõú Çç"]
    ims = [fonte.escrever(l) for l in amostra]
    t = Image.new("RGBA", (max(i.width for i in ims) + 8, len(ims) * 14 + 8), (30, 22, 24, 255))
    for k2, im in enumerate(ims):
        t.alpha_composite(im, (4, 4 + k2 * 14))
    pv.amplia(t, 3).save(os.path.join(d, "fonte.png"))


def elenco_escala():
    """Todos os personagens no mesmo chão, na escala do jogo (×3), pela origem nos pés."""
    from PIL import Image
    from chefes import chefe_besta, chefe_humano, dama
    from inimigos import aldeao, brutamontes
    from personagens import cacador
    figs = [(cacador.quadros("idle")[0], 16, 30), (aldeao.quadros("idle")[0], 16, 30),
            (brutamontes.quadros("idle")[0], 24, 45), (chefe_humano.quadros("idle")[0], 24, 45),
            (chefe_besta.quadros("idle")[0], 32, 60), (dama.quadros("idle")[0], 16, 30)]
    W = sum(f.width for f, _, _ in figs) + 8 * (len(figs) + 1)
    chao_y = 64
    t = Image.new("RGBA", (W, 72), (46, 40, 38, 255))
    x = 8
    for f, ox, oy in figs:
        t.alpha_composite(f, (x, chao_y - oy))
        x += f.width + 8
    return t.resize((t.width * 3, t.height * 3), Image.NEAREST)


def cena_rua():
    """A praça a 1x×2 com o caçador, aldeões e um brutamontes no chão do jogo, e o brilho dos postes."""
    from PIL import Image
    from cenario import guias, props
    from inimigos import aldeao, brutamontes
    from personagens import cacador
    img = guias.render("rm_praca")
    luz = props.luz()
    tint = Image.new("RGBA", luz.size, (255, 150, 60, 255))
    import numpy as np
    from PIL import Image as I
    a = np.array(luz).astype(float)
    t = np.array(tint).astype(float)
    t[:, :, 3] = a[:, :, 3] * 0.32
    luz_tingida = I.fromarray(t.astype("uint8"), "RGBA")
    for (x, y) in ((190, 50), (300, 50)):
        img = pv.brilho_aditivo(img, luz_tingida, x, y)
    cena = pv.cena(img, [(cacador.quadros("idle")[0], 240, 140, 16, 30),
                         (aldeao.quadros("walk")[1], 120, 120, 16, 30),
                         (aldeao.quadros("ataque")[0], 300, 210, 16, 30),
                         (brutamontes.quadros("idle")[0], 390, 220, 24, 45)])
    return cena.resize((cena.width * 2, cena.height * 2), I.NEAREST)


def hud_cena():
    """O HUD por cima do jogo na resolução base, ampliado 3x (como no dia 15)."""
    from PIL import Image
    from hud import fonte, hud
    from cenario import guias
    base = guias.render("rm_rua").crop((0, 80, 320, 260))
    mold, vida, st, chefe = (hud.imagem(n) for n in ("spr_hud_moldura", "spr_hud_vida", "spr_hud_stamina", "spr_hud_chefe"))

    def nine(img, w, h):
        out = Image.new("RGBA", (w, h))
        b = 2
        out.paste(img.crop((0, 0, b, b)), (0, 0))
        out.paste(img.crop((8 - b, 0, 8, b)), (w - b, 0))
        out.paste(img.crop((0, 8 - b, b, 8)), (0, h - b))
        out.paste(img.crop((8 - b, 8 - b, 8, 8)), (w - b, h - b))
        out.paste(img.crop((b, 0, 8 - b, b)).resize((w - 2 * b, b)), (b, 0))
        out.paste(img.crop((b, 8 - b, 8 - b, 8)).resize((w - 2 * b, b)), (b, h - b))
        out.paste(img.crop((0, b, b, 8 - b)).resize((b, h - 2 * b)), (0, b))
        out.paste(img.crop((8 - b, b, 8, 8 - b)).resize((b, h - 2 * b)), (w - b, b))
        out.paste(img.crop((b, b, 8 - b, 8 - b)).resize((w - 2 * b, h - 2 * b)), (b, b))
        return out
    tela = base.copy()
    tela.alpha_composite(nine(mold, 54, 8), (5, 5))
    tela.alpha_composite(vida.resize((38, 4), Image.NEAREST), (7, 7))
    tela.alpha_composite(nine(mold, 54, 6), (5, 13))
    tela.alpha_composite(st.resize((44, 2), Image.NEAREST), (7, 15))
    tela.alpha_composite(hud.imagem("spr_icone_frasco"), (6, 166))
    tela.alpha_composite(fonte.escrever("5"), (15, 165))
    tela.alpha_composite(hud.imagem("spr_icone_bala"), (30, 167))
    tela.alpha_composite(fonte.escrever("10"), (37, 165))
    tela.alpha_composite(hud.imagem("spr_icone_almas"), (282, 167))
    tela.alpha_composite(fonte.escrever("1200"), (291, 165))
    nm = fonte.escrever("Caçador Caído")
    tela.alpha_composite(nm, (160 - nm.width // 2, 150))
    tela.alpha_composite(nine(mold, 204, 8), (58, 163))
    tela.alpha_composite(chefe.resize((140, 4), Image.NEAREST), (60, 165))
    tela.alpha_composite(hud.imagem("spr_mira"), (200, 90))
    return tela.resize((960, 540), Image.NEAREST)


def previa():
    from kit import relatorio
    for nome, pasta, orig, mod, mapa, pac in personagens():
        anims = {a: mod.quadros(a) for a in mapa}
        relatorio.previas(nome, anims, {a: mod.ANIMS[a][1] for a in mapa})
    print("prévias em", PREVIA)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "audita"
    if cmd == "audita":
        print(audita()[0])
    elif cmd == "exporta":
        exporta()
    elif cmd == "previa":
        previa()
