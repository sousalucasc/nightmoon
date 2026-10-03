# Dia 11 — Parry e visceral

**Quando:** qui 15/10 · **Tempo:** ~3 h

**No fim do dia:** atirar num inimigo no **fim do windup** dele (a janela de parry) deixa ele **atordoado** (stagger) por 1,5 s e devolve a bala. Chegando perto e apertando o ataque leve, sai o **visceral**: um golpe crítico com o player invulnerável.

Esse é o coração do combate estilo Bloodborne.

## O que você vai aprender

- **Janela de parry**: um intervalo de frames dentro do ataque inimigo.
- Por que a **bala chegando** é o que conta, não a bala saindo.
- Um estado que **controla outra instância** (o visceral move o inimigo de estado).

---

## Como funciona o parry

1. O inimigo começa o windup.
2. A janela de parry abre **10 frames antes do golpe sair** e fecha **2 frames depois** (12 frames = 0,2 s). A pistola ganha 4 frames a mais (16 frames).
3. Se um tiro seu **acerta o inimigo** com a janela aberta, e o ataque aceita parry (aviso **branco**), ele entra em `STAGGER`.
4. Com ele em `STAGGER`, chegue a até 28 px, mire nele e aperte o ataque leve: **visceral**.

Ataque com aviso **vermelho** não aceita parry. É a hora de esquivar.

---

## Passo 1 — Sprite (5 min)

| Sprite | Tamanho | Cor | Origem |
|---|---|---|---|
| `spr_fx_parry` | 12×12 | amarelo | x 6, y 6 |

## Passo 2 — A janela de parry (40 min)

**scr_combate** (nova função, adicione no fim)
<!-- src: scripts/scr_combate.gml #inimigo_janela_parry -->
```gml
/// true se o inimigo está na janela de parry: os últimos 10 frames do windup
/// e os 2 primeiros do ativo, mais _bonus frames para trás (pistola).
function inimigo_janela_parry(_inst, _bonus) {
    var _aberta = false;
    with (_inst) {
        if (estado == INI.ATAQUE && ataque.parry) {
            var _ini = ataque.windup - 10 - _bonus;
            var _fim = ataque.windup + 2;
            _aberta = (estado_timer > _ini && estado_timer <= _fim);
        }
    }
    return _aberta;
}
```

Com windup 24 e bônus 0: a janela vai do frame 15 ao 26 (os frames 15 a 24 são o fim do windup; 25 e 26 são o começo do ativo).

**scr_combate** (substitua a função `projetil_acertar_inimigo`)
<!-- src: scripts/scr_combate.gml #projetil_acertar_inimigo -->
```gml
/// Roda dentro do projétil, quando ele acerta um inimigo.
function projetil_acertar_inimigo(_alvo) {
    // Parry: chegou com a janela aberta, num ataque que aceita parry.
    if (inimigo_janela_parry(_alvo, parry_bonus) && _alvo.ultimo_tiro_parry != tiro_id) {
        _alvo.ultimo_tiro_parry = tiro_id;   // chumbos do mesmo tiro: um parry só
        with (_alvo) {
            inimigo_trocar(INI.STAGGER);
        }
        // Parry certo devolve a bala (no máximo uma por tiro).
        if (instance_exists(obj_player) && obj_player.ultimo_reembolso != tiro_id) {
            obj_player.ultimo_reembolso = tiro_id;
            obj_player.balas = min(obj_player.balas_max, obj_player.balas + 1);
        }
        fx_criar(_alvo.x, _alvo.y - 12, spr_fx_parry, 0, 1);
        aplicar_hitstop(6);
        tremer_tela(2);
    }
    inimigo_dano(_alvo, dano);
    aplicar_hitstop(2);
}
```

- **O stagger vem antes do dano.** O `inimigo_dano` coloca em hitstun quem pode ser interrompido; `STAGGER` não pode, então o atordoamento não é sobrescrito.
- **`tiro_id`**: os 5 chumbos da escopeta têm o mesmo número. Se três acertarem, o primeiro faz o parry; os outros dois só dão dano. Mas a escopeta pode dar parry em **dois inimigos diferentes** com o mesmo tiro, porque cada inimigo guarda o seu `ultimo_tiro_parry`.

**obj_inimigo_pai → Create** (adicione no fim)
<!-- src: objects/obj_inimigo_pai/Create_0.gml @fim -->
```gml
ultimo_tiro_parry = -1;   // último tiro que deu parry em mim
```

## Passo 3 — Estados de atordoado (20 min)

**scr_inimigo** (novas funções, adicione no fim)
<!-- src: scripts/scr_inimigo.gml #inimigo_estado_stagger -->
```gml
function inimigo_estado_stagger() {
    if (estado_timer >= 90) {
        inimigo_trocar(INI.PERSEGUIR);
    }
}
```

<!-- src: scripts/scr_inimigo.gml #inimigo_estado_visceral -->
```gml
function inimigo_estado_visceral() {
    // Quem conduz o visceral é o player. Isto é só uma garantia se algo der errado.
    if (estado_timer >= 60) {
        inimigo_trocar(INI.CAIDO);
    }
}
```

<!-- src: scripts/scr_inimigo.gml #inimigo_estado_caido -->
```gml
function inimigo_estado_caido() {
    if (estado_timer >= 40) {
        inimigo_trocar(INI.PERSEGUIR);
    }
}
```

**obj_inimigo_pai → Step** (logo depois da linha do `case INI.HITSTUN`, adicione)
<!-- src: objects/obj_inimigo_pai/Step_0.gml @depois: case INI.HITSTUN:   inimigo_estado_hitstun();   break; -->
```gml
    case INI.STAGGER:   inimigo_estado_stagger();   break;
    case INI.VISCERAL:  inimigo_estado_visceral();  break;
    case INI.CAIDO:     inimigo_estado_caido();     break;
```

**obj_inimigo_pai → Draw** (adicione antes da linha `if (obj_game.debug) {`)
<!-- src: objects/obj_inimigo_pai/Draw_0.gml @antes: if (obj_game.debug) { -->
```gml
// Atordoado: sinal amarelo piscando em cima da cabeça (hora do visceral).
if (estado == INI.STAGGER && (estado_timer div 6) mod 2 == 0) {
    draw_set_colour(c_yellow);
    draw_circle(x, y - sprite_get_yoffset(sprite_index) + sprite_get_bbox_top(sprite_index) - 6, 3, false);
    draw_set_colour(c_white);
}

```

A conta acha o **topo do desenho**: `y - sprite_get_yoffset(...)` é a borda de cima do sprite, e `sprite_get_bbox_top(...)` é quantas linhas vazias o sprite tem antes do primeiro pixel. Assim o sinal fica logo acima da cabeça em qualquer tamanho de sprite, inclusive nos da arte, que têm espaço vazio em cima.

**obj_inimigo_pai → Draw** (dentro do `if (obj_game.debug)`, adicione antes da linha `draw_set_colour(c_orange);`)
<!-- src: objects/obj_inimigo_pai/Draw_0.gml @antes: draw_set_colour(c_orange); -->
```gml
    // Janela de parry aberta (contando o bônus da pistola): círculo amarelo
    if (inimigo_janela_parry(id, 4)) {
        draw_set_colour(c_yellow);
        draw_circle(x, y - 10, 12, true);
    }
```

**`id`** é o identificador da própria instância. A função pede "qual inimigo?", e a resposta é "eu".

## Passo 4 — O visceral (50 min)

**obj_player → Create** (adicione no fim)
<!-- src: objects/obj_player/Create_0.gml @fim -->
```gml
// --- Parry e visceral ---
visceral_alvo = noone;      // inimigo do visceral atual
ultimo_reembolso = -1;      // último tiro que devolveu bala
```

**scr_player** (substitua a função `player_tentar_atacar`)
<!-- src: scripts/scr_player.gml #player_tentar_atacar -->
```gml
/// Começa um golpe leve ou pesado se o botão está no buffer e tem stamina.
/// Se houver um inimigo atordoado na frente, o leve vira visceral.
function player_tentar_atacar() {
    var _arma = obj_game.arma;
    if (obj_game.buf_leve > 0) {
        var _alvo = player_procurar_visceral();
        if (_alvo != noone) {
            obj_game.buf_leve = 0;
            player_comecar_visceral(_alvo);   // visceral não gasta stamina
            return true;
        }
    }
    if (obj_game.buf_leve > 0 && st > 0) {
        obj_game.buf_leve = 0;
        // Vindo de um golpe leve, segue o combo. Senão, começa do primeiro.
        if (estado == PL.ATAQUE && !golpe_pesado) {
            combo_i = (combo_i + 1) mod array_length(_arma.leves);
        } else {
            combo_i = 0;
        }
        player_comecar_golpe(_arma.leves[combo_i], false);
        return true;
    }
    if (obj_game.buf_pesado > 0 && st > 0) {
        obj_game.buf_pesado = 0;
        player_comecar_golpe(_arma.pesado, true);
        return true;
    }
    return false;
}
```

**scr_player** (novas funções, adicione no fim)
<!-- src: scripts/scr_player.gml #player_procurar_visceral -->
```gml
/// Procura um inimigo em stagger perto e na direção da mira. Devolve o id, ou noone.
function player_procurar_visceral() {
    var _achou = noone;
    var _px = x;
    var _py = y;
    var _mira = obj_game.mira_dir;
    with (obj_inimigo_pai) {
        if (estado == INI.STAGGER) {
            var _dist = point_distance(_px, _py, x, y);
            var _ang = point_direction(_px, _py, x, y);
            if (_dist <= 28 + raio && abs(angle_difference(_mira, _ang)) <= 60) {
                _achou = id;
            }
        }
    }
    return _achou;
}
```

<!-- src: scripts/scr_player.gml #player_comecar_visceral -->
```gml
function player_comecar_visceral(_alvo) {
    visceral_alvo = _alvo;
    ataque_dir = point_direction(x, y, _alvo.x, _alvo.y);
    with (_alvo) {
        inimigo_trocar(INI.VISCERAL);
    }
    player_trocar(PL.VISCERAL);
}
```

<!-- src: scripts/scr_player.gml #player_estado_visceral -->
```gml
function player_estado_visceral() {
    invulneravel = true;
    // Frame 20: o golpe entra. Dano escala com Destreza, em qualquer arma.
    if (estado_timer == 20 && instance_exists(visceral_alvo)) {
        var _dano = round(60 * (1 + 0.08 * obj_game.atr_destreza));
        inimigo_dano(visceral_alvo, _dano);
        fx_criar(visceral_alvo.x, visceral_alvo.y - 10, spr_fx_sangue, ataque_dir, 1);
        aplicar_hitstop(10);
        tremer_tela(3);
    }
    if (estado_timer >= 40) {
        invulneravel = false;
        // Se ele sobreviveu, fica caído um tempo.
        if (instance_exists(visceral_alvo) && visceral_alvo.estado == INI.VISCERAL) {
            with (visceral_alvo) {
                inimigo_trocar(INI.CAIDO);
            }
        }
        player_trocar(PL.LIVRE);
    }
}
```

- **Por que guardar `_px` e `_py` antes do `with`?** Dentro do `with (obj_inimigo_pai)`, `x` e `y` são do inimigo. As variáveis `var` guardam a posição do player para usar lá dentro.
- **O player manda no inimigo:** `with (_alvo) inimigo_trocar(...)` roda a troca de estado **como se fosse o inimigo**.
- **`instance_exists(visceral_alvo)`**: se o inimigo morreu (ou sumiu) no meio, não tenta mexer nele.

**scr_player**, na função `player_animar` (adicione antes da linha `case PL.HITSTUN:`)
<!-- src: scripts/scr_player.gml @antes: case PL.HITSTUN: -->
```gml
        case PL.VISCERAL:
            sprite_index = spr.visceral;
            image_index = anim_quadro(estado_timer, 40, sprite_index);
            break;
```

**obj_player → Step** (logo depois da linha do `case PL.TIRO`, adicione)
<!-- src: objects/obj_player/Step_0.gml @depois: case PL.TIRO:    player_estado_tiro();    break; -->
```gml
    case PL.VISCERAL: player_estado_visceral(); break;
```

**obj_player → Step** (troque a linha `if (estado == PL.ATAQUE || estado == PL.TIRO) {` por esta)
<!-- src: objects/obj_player/Step_0.gml @troca: if (estado == PL.ATAQUE || estado == PL.TIRO) { -->
```gml
if (estado == PL.ATAQUE || estado == PL.TIRO || estado == PL.VISCERAL) {
```

---

## Arte do dia

Com a arte pronta, faça agora a parte **Dia 11** do [Apêndice A](apendice-a-arte.md).

## Teste do dia

Ligue o F3 e use o Aldeão.

- [ ] Durante o ataque do Aldeão aparece o círculo amarelo (janela aberta).
- [ ] Pistola (tecla 4) com o círculo amarelo na tela: ele fica atordoado, com o sinal amarelo piscando em cima da cabeça, e a bala volta.
- [ ] Tiro cedo demais (no começo do windup): só dano, sem stagger.
- [ ] Escopeta (tecla 5), de perto, no tempo certo: stagger. É mais difícil de acertar o tempo.
- [ ] Com ele atordoado, chegue perto, mire nele e clique: visceral (dano 60, congela mais tempo, player ciano o tempo todo).
- [ ] Um Aldeão (60 de vida) morre com um visceral.
- [ ] Tecla 8 (Destreza) aumenta o dano do visceral.

## Se deu errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| Parry nunca entra | O tiro sai na janela, mas **chega** depois. Com a pistola, atire um pouco antes do círculo amarelo | Treino; o círculo mostra a janela na hora da chegada. |
| Atordoa mas volta na hora | O dano veio antes do stagger e sobrescreveu com hitstun | Passo 2: stagger primeiro. |
| Visceral não sai | Longe demais (28 px + corpo) ou mirando para o lado | Chegue colado e mire nele. |
| Inimigo fica caído para sempre | Faltou `case INI.CAIDO` no Step do pai | Passo 3. |
| `variable not set: ultimo_tiro_parry` | Bloco do Create do pai não adicionado | Passo 2. |

## Commit

`dia 11: parry e visceral`
