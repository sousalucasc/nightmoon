# Dia 15 — HUD e frascos de cura

**Quando:** seg 19/10 · **Tempo:** ~3 h

**No fim do dia:** o HUD mostra vida, stamina, frascos, balas e almas. **E** usa um frasco: cura 40% da vida, dá para andar devagar enquanto cura, e apanhar antes da hora cancela sem gastar o frasco.

---

## Passo 1 — Fonte e ícones (20 min)

**Fonte:** botão direito → **Create → Font**. Nome **`fnt_hud`**.
- Fonte: **m5x7** se estiver instalada (o Gralloch usa); senão **Consolas**.
- Tamanho: **12** (se as letras ficarem grandes demais na tela, tente 10).
- **Anti-aliasing: Off** (senão fica borrado em pixel art).

**Ícones** (origem **x 0, y 0** em todos):

| Sprite | Tamanho | Cor |
|---|---|---|
| `spr_icone_frasco` | 7×9 | vermelho |
| `spr_icone_bala` | 5×7 | amarelo |
| `spr_icone_almas` | 7×7 | branco |

## Passo 2 — O HUD (40 min)

**obj_game → Draw GUI** (arquivo inteiro)
<!-- src: objects/obj_game/Draw_64.gml -->
```gml
// Draw GUI: desenhado por cima de tudo, em coordenadas de tela (320x180).
draw_set_font(fnt_hud);

// --- HUD ---
if (instance_exists(obj_player)) {
    var _p = obj_player;

    // Vida: a barra cresce com o HP máximo (100 de vida = 50 px).
    var _larg_hp = _p.hp_max / 2;
    draw_set_colour(c_black);
    draw_rectangle(6, 6, 8 + _larg_hp, 11, false);
    draw_set_colour(c_red);
    if (_p.hp > 0) {
        draw_rectangle(7, 7, 7 + _larg_hp * _p.hp / _p.hp_max, 10, false);
    }

    // Stamina
    var _larg_st = _p.st_max / 2;
    draw_set_colour(c_black);
    draw_rectangle(6, 13, 8 + _larg_st, 16, false);
    draw_set_colour(c_yellow);
    if (_p.st > 0) {
        draw_rectangle(7, 14, 7 + _larg_st * _p.st / _p.st_max, 15, false);
    }
    draw_set_colour(c_white);

    // Frascos e balas (canto de baixo, à esquerda)
    draw_sprite(spr_icone_frasco, 0, 6, ALTURA_BASE - 14);
    draw_text(16, ALTURA_BASE - 16, string(_p.frascos));
    draw_sprite(spr_icone_bala, 0, 32, ALTURA_BASE - 13);
    draw_text(40, ALTURA_BASE - 16, string(_p.balas));

    // Almas (canto de baixo, à direita)
    draw_set_halign(fa_right);
    draw_text(LARGURA_BASE - 6, ALTURA_BASE - 16, string(almas));
    draw_set_halign(fa_left);
    draw_sprite(spr_icone_almas, 0, LARGURA_BASE - 16 - string_width(string(almas)), ALTURA_BASE - 13);
}

// --- Debug ---
if (debug) {
    draw_text(4, 22, "Arma: " + arma.nome);
    draw_text(4, 34, "Pistola: " + pistola.nome);
    draw_text(4, 46, "FOR " + string(atr_forca) + "  DES " + string(atr_destreza));
}

// Mensagem no meio da tela
if (texto_timer > 0) {
    draw_set_halign(fa_center);
    draw_set_colour(c_yellow);
    draw_text(LARGURA_BASE / 2, 70, texto);
    draw_set_colour(c_white);
    draw_set_halign(fa_left);
}
```

- **Barra = retângulo preto de fundo + retângulo colorido por cima**, com a largura proporcional: `largura_total × hp ÷ hp_max`.
- **A barra cresce com o HP máximo** (como no souls): subindo Vida no dia 17, ela fica mais comprida.
- **`string_width(texto)`** mede a largura do texto na fonte atual. Serve para colocar o ícone das almas logo à esquerda do número, qualquer que seja o tamanho dele.
- O debug desceu um pouco para não ficar em cima das barras.

## Passo 3 — Frascos (50 min)

**obj_player → Create** (adicione no fim)
<!-- src: objects/obj_player/Create_0.gml @fim -->
```gml
// --- Cura ---
frascos_max = 5;
frascos = frascos_max;
```

**scr_player** (substitua a função `player_estado_livre`)
<!-- src: scripts/scr_player.gml #player_estado_livre -->
```gml
function player_estado_livre() {
    player_mover(1);
    if (player_tentar_esquivar()) return;
    if (player_tentar_atacar()) return;
    if (player_tentar_atirar()) return;
    if (player_tentar_curar()) return;
}
```

**scr_player** (novas funções, adicione no fim)
<!-- src: scripts/scr_player.gml #player_tentar_curar -->
```gml
function player_tentar_curar() {
    if (obj_game.aperta_cura && frascos > 0 && hp < hp_max) {
        player_trocar(PL.CURA);
        return true;
    }
    return false;
}
```

<!-- src: scripts/scr_player.gml #player_estado_cura -->
```gml
function player_estado_cura() {
    player_mover(0.5);          // anda devagar enquanto cura
    // Frame 12: o frasco é usado. Apanhar antes disso cancela sem gastar.
    if (estado_timer == 12) {
        frascos -= 1;
        hp = min(hp_max, hp + round(hp_max * 0.4));
    }
    if (estado_timer >= 24) {
        player_trocar(PL.LIVRE);
    }
}
```

**Como o cancelamento funciona sem código extra:** tomar dano chama `player_trocar(PL.HITSTUN)`. O estado sai de `CURA` antes do frame 12, e o frame 12 nunca acontece. O frasco não é gasto.

**scr_player**, na função `player_animar` (adicione antes da linha `case PL.HITSTUN:`)
<!-- src: scripts/scr_player.gml @antes: case PL.HITSTUN: -->
```gml
        case PL.CURA:
            sprite_index = spr.cura;
            image_index = anim_quadro(estado_timer, 24, sprite_index);
            break;
```

**obj_player → Step** (logo depois da linha do `case PL.VISCERAL`, adicione)
<!-- src: objects/obj_player/Step_0.gml @depois: case PL.VISCERAL: player_estado_visceral(); break; -->
```gml
    case PL.CURA:    player_estado_cura();    break;
```

---

## Arte do dia

Com a arte pronta, faça agora a parte **Dia 15** do [Apêndice A](apendice-a-arte.md).

## Teste do dia

- [ ] HUD: barras no canto de cima; frascos e balas embaixo à esquerda; almas embaixo à direita.
- [ ] Tome dano e aperte E: a vida sobe 40 no frame 12 e o frasco cai para 4.
- [ ] Com a vida cheia, E não faz nada.
- [ ] Curando na frente do Brutamontes, se ele acertar antes do frame 12: sem cura e o frasco continua 5.
- [ ] Com 0 frascos, E não faz nada.

## Se deu errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| `fnt_hud` desconhecido | Fonte não criada ou nome diferente | Passo 1. |
| Texto borrado | Anti-aliasing ligado na fonte | Passo 1. |
| E não faz nada | Falta `case PL.CURA` no Step, ou a vida está cheia | Passo 3. |
| Cura acontece duas vezes | `estado_timer >= 12` em vez de `== 12` | Passo 3. |

## Commit

`dia 15: HUD e frascos`
