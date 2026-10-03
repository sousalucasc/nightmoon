# Dia 10 — Aldeão completo e almas

**Quando:** qua 14/10 · **Tempo:** ~2,5 h

**No fim do dia:** o Aldeão tem combo de 2 golpes (o segundo vem em 50% das vezes), segura uma foice que gira no golpe, sangra ao apanhar e dá 20 almas ao morrer. Todo inimigo passa a ter animação por estado, e eles não se empilham.

## O que você vai aprender

- **Combo de inimigo** com `seguinte` e `chance`.
- **Animação do inimigo** pelo mesmo método do player.
- Reaproveitar o **desenho da arma** do player nos inimigos.

---

## Passo 1 — Sprites provisórios (5 min)

| Sprite | Tamanho | Cor | Origem |
|---|---|---|---|
| `spr_arma_foice` | 16×3 | cinza enferrujado | x 0, y 1 |
| `spr_fx_sangue` | 6×6 | vermelho escuro | x 3, y 3 |

## Passo 2 — Almas (10 min)

**obj_game → Create** (adicione antes de `room_goto`)
<!-- src: objects/obj_game/Create_0.gml @antes: room_goto -->
```gml
almas = 0;
```

**obj_game → Draw GUI** (arquivo inteiro)
<!-- src: objects/obj_game/Draw_64.gml -->
```gml
// Draw GUI: desenhado por cima de tudo, em coordenadas de tela (320x180).
if (debug) {
    draw_text(4, 4, "Arma: " + arma.nome);
    draw_text(4, 18, "Pistola: " + pistola.nome);
    draw_text(4, 32, "FOR " + string(atr_forca) + "  DES " + string(atr_destreza));
    draw_text(4, 46, "Almas: " + string(almas));
    if (instance_exists(obj_player)) {
        draw_text(4, 60, "Balas: " + string(obj_player.balas));
    }
}
```

**scr_inimigo** (substitua a função `inimigo_morrer`)
<!-- src: scripts/scr_inimigo.gml #inimigo_morrer -->
```gml
function inimigo_morrer() {
    obj_game.almas += almas;
    fx_criar(x, y - 10, spr_fx_sangue, 0, 1);
    inimigo_trocar(INI.MORTE);
}
```

**scr_combate**, na função `inimigo_dano` (logo depois da linha `ultimo_dano = _dano;`, adicione)
<!-- src: scripts/scr_combate.gml @depois: ultimo_dano = _dano; -->
```gml
            fx_criar(x, y - 10, spr_fx_sangue, irandom(359), 1);
```

Cada acerto espirra sangue num ângulo sorteado (`irandom(359)` = 0 a 359 graus).

## Passo 3 — Animação e arma de inimigo (40 min)

**scr_inimigo** (substitua a função `ataque_novo`)
<!-- src: scripts/scr_inimigo.gml #ataque_novo -->
```gml
/// Cria um ataque de inimigo com os valores mais comuns.
/// Depois de criar, dá pra mudar qualquer campo (ex.: _a.avanco = 24;).
function ataque_novo(_windup, _ativo, _recovery, _dano, _alcance, _arco, _parry) {
    return {
        windup: _windup, ativo: _ativo, recovery: _recovery,
        dano: _dano, alcance: _alcance, arco: _arco,
        parry: _parry,           // aceita parry?
        avanco: 0,               // pixels que anda durante o ativo
        dist_min: 0,             // só usa este ataque com o player
        dist_max: _alcance + 6,  //   entre dist_min e dist_max
        seguinte: undefined,     // ataque que pode emendar (combo)
        chance: 0,               // chance de emendar, de 0 a 1
        tipo: "golpe",           // "golpe", "tiro" ou "salto"
        spr: undefined           // sprite próprio deste ataque (opcional)
    };
}
```

O campo novo, `spr`, serve para inimigos com mais de uma animação de ataque (o Brutamontes tem pancada **e** agarrão).

**obj_inimigo_pai → Create** (adicione no fim)
<!-- src: objects/obj_inimigo_pai/Create_0.gml @fim -->
```gml
// --- Animação e arma ---
image_speed = 0;
anim_timer = 0;
// Sprite de cada estado. Os filhos trocam quando a arte chegar.
spr = {
    parado: sprite_index,
    andando: sprite_index,
    ataque: sprite_index,
    hit: sprite_index,
    stagger: sprite_index,
    caido: sprite_index,
    morte: sprite_index
};
tem_arma = false;    // desenha uma arma separada girando? (Aldeão: foice)
arma_sprite = -1;
// Onde fica a mão da arma no desenho: 3 px à frente do centro, 10 acima dos pés (Aldeão).
mao_x = 3;
mao_y = 10;
```

`sprite_index`, no Create do pai, já é o sprite do **filho** (o GameMaker coloca o sprite do objeto antes de rodar o Create). Por isso o struct começa com o sprite provisório de cada inimigo.

**scr_inimigo** (nova função, adicione no fim)
<!-- src: scripts/scr_inimigo.gml #inimigo_animar -->
```gml
/// Escolhe sprite e quadro conforme o estado.
function inimigo_animar() {
    anim_timer += 1;
    switch (estado) {
        case INI.IDLE:
            sprite_index = spr.parado;
            image_index = (anim_timer div 10) mod sprite_get_number(sprite_index);
            break;
        case INI.PERSEGUIR:
        case INI.VOLTAR:
            sprite_index = spr.andando;
            image_index = (anim_timer div 6) mod sprite_get_number(sprite_index);
            break;
        case INI.ATAQUE:
            // O ataque pode ter sprite próprio. 3 quadros: windup, ativo, recovery.
            if (ataque.spr != undefined) {
                sprite_index = ataque.spr;
            } else {
                sprite_index = spr.ataque;
            }
            if (estado_timer <= ataque.windup) {
                image_index = 0;
            } else if (estado_timer <= ataque.windup + ataque.ativo) {
                image_index = 1;
            } else {
                image_index = 2;
            }
            break;
        case INI.HITSTUN:
            sprite_index = spr.hit;
            image_index = 0;
            break;
        case INI.STAGGER:
            sprite_index = spr.stagger;
            image_index = (anim_timer div 8) mod sprite_get_number(sprite_index);
            break;
        case INI.VISCERAL:
        case INI.CAIDO:
            sprite_index = spr.caido;
            image_index = 0;
            break;
        case INI.MORTE:
            sprite_index = spr.morte;
            image_index = anim_quadro(estado_timer, 40, sprite_index);
            break;
    }
}
```

Dois `case` seguidos sem nada entre eles (`PERSEGUIR` e `VOLTAR`) dividem o mesmo código.

**scr_inimigo** (substitua a função `inimigo_estado_morte`)
<!-- src: scripts/scr_inimigo.gml #inimigo_estado_morte -->
```gml
/// Morto: a animação de morte leva 40 frames, o corpo fica no chão e some aos 100.
function inimigo_estado_morte() {
    if (estado_timer >= 100) {
        instance_destroy();
    }
}
```

Antes o inimigo sumia aos 30 frames. Com a arte, a morte termina com o corpo caído e uma poça de sangue: ele precisa ficar um tempo no chão. O Draw abaixo apaga o corpo devagar nos últimos 30 frames.

**obj_inimigo_pai → Step** (adicione antes da linha `depth = -y;`)
<!-- src: objects/obj_inimigo_pai/Step_0.gml @antes: depth = -y; -->
```gml
// Inimigos não se empilham: se estiver encostado em outro, se afasta devagar.
var _outro = instance_place(x, y, obj_inimigo_pai);
if (_outro != noone && _outro.estado != INI.MORTE && estado != INI.MORTE) {
    var _dir_fuga = point_direction(_outro.x, _outro.y, x, y);
    move_and_collide(lengthdir_x(0.5, _dir_fuga), lengthdir_y(0.5, _dir_fuga), obj_parede);
}

inimigo_animar();

```

**`instance_place(x, y, objeto)`** devolve uma instância daquele objeto que está encostando em mim (nunca eu mesmo), ou `noone`.

**obj_inimigo_pai → Draw** (arquivo inteiro)
<!-- src: objects/obj_inimigo_pai/Draw_0.gml -->
```gml
// Morto: o corpo some devagar nos últimos 30 frames (de 70 a 100).
var _alpha = 1;
if (estado == INI.MORTE) {
    _alpha = clamp((100 - estado_timer) / 30, 0, 1);
}

// Desenho normal, ou todo branco se acabou de apanhar.
if (flash > 0) gpu_set_fog(true, c_white, 1, 0);
draw_sprite_ext(sprite_index, image_index, x, y, lado, 1, 0, c_white, _alpha);
if (flash > 0) gpu_set_fog(false, c_white, 0, 1);

// Arma separada (Aldeão, chefe): gira no golpe igual à do player, a partir da mão.
if (tem_arma && estado != INI.MORTE) {
    var _ang = (lado == 1) ? -40 : 220;
    if (estado == INI.ATAQUE) {
        _ang = angulo_golpe(estado_timer, ataque.windup, ataque.ativo, ataque_dir, ataque.arco, lado);
    }
    draw_sprite_ext(arma_sprite, 0, x + mao_x * lado, y - mao_y, 1, 1, _ang, c_white, 1);
}

// Aviso no começo do windup: branco = aceita parry, vermelho = não aceita.
if (estado == INI.ATAQUE && estado_timer <= 8 && flash <= 0) {
    var _cor = c_red;
    if (ataque.parry) {
        _cor = c_white;
    }
    gpu_set_fog(true, _cor, 1, 0);
    draw_sprite_ext(sprite_index, image_index, x, y, lado, 1, 0, c_white, 0.6);
    gpu_set_fog(false, c_white, 0, 1);
}

if (obj_game.debug) {
    draw_set_halign(fa_center);
    draw_text(x, y - 44, obj_game.nomes_ini[estado] + " " + string(hp) + " (-" + string(ultimo_dano) + ")");
    draw_set_halign(fa_left);
    if (estado == INI.ATAQUE) {
        if (estado_timer > ataque.windup && estado_timer <= ataque.windup + ataque.ativo) {
            draw_set_colour(c_red);
        } else {
            draw_set_colour(c_gray);
        }
        desenhar_setor(x, y, ataque_dir, ataque.alcance, ataque.arco);
    }
    draw_set_colour(c_orange);
    draw_circle(inicio_x, inicio_y, 2, false);   // ponto inicial
    draw_set_colour(c_white);
}
```

A função `angulo_golpe` é a mesma do player (está no `scr_combate`). Escrever uma vez e usar nos dois é o motivo de ela ser uma função.

- **`clamp(valor, mínimo, máximo)`** prende o valor entre os dois limites. `(100 - estado_timer) / 30` dá 3 no começo da morte, 1 no frame 70 e 0 no frame 100; preso entre 0 e 1, o corpo fica inteiro até o 70 e some até o 100.
- **`mao_x * lado`**: a mão fica à frente do corpo, então olhando para a esquerda ela vai para o outro lado.

## Passo 4 — Aldeão completo (15 min)

**obj_aldeao → Create** (arquivo inteiro)
<!-- src: objects/obj_aldeao/Create_0.gml -->
```gml
event_inherited();

hp_max = 60;
hp = hp_max;
vel = 1.0;
raio = 7;
almas = 20;
mask_index = spr_mask_player;   // colisão só nos pés, como o player

// Golpe 2: mais rápido; só acontece emendado no golpe 1.
var _golpe2 = ataque_novo(12, 5, 26, 18, 22, 100, true);
// Golpe 1: 50% de chance de emendar o golpe 2.
var _golpe1 = ataque_novo(24, 5, 18, 18, 22, 100, true);
_golpe1.seguinte = _golpe2;
_golpe1.chance = 0.5;
ataques = [_golpe1];            // o golpe 2 não entra na lista: só vem pelo combo

tem_arma = true;
arma_sprite = spr_arma_foice;
```

**Por que o golpe 2 é criado primeiro?** O golpe 1 aponta para ele (`seguinte = _golpe2`). Precisa existir antes.

**Como o combo funciona:** no último frame do ativo do golpe 1, o estado de ataque sorteia (`random(1) < 0.5`). Se passou, começa o golpe 2 **pulando o recovery** do golpe 1. O windup do golpe 2 é curto (12): pega quem achou que o ataque tinha acabado.

Coloque mais 2 Aldeões na `rm_teste`: **(560, 300)** e **(520, 316)**.

---

## Arte do dia

Com a arte pronta, faça agora a parte **Dia 10** do [Apêndice A](apendice-a-arte.md).

## Teste do dia

- [ ] A foice gira no golpe do Aldeão.
- [ ] Às vezes ele emenda um segundo golpe rápido; às vezes não.
- [ ] Batendo, sangue espirra; morto, ele fica no chão, some devagar (em ~1,5 s) e o contador de almas (F3) sobe 20.
- [ ] Três Aldeões juntos não ficam um em cima do outro.
- [ ] Três Aldeões são perigosos, mas dá para vencer só com esquiva e golpes no recovery deles.

## Se deu errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| `variable not set: spr` no Step | Bloco novo do Create do pai não adicionado | Passo 3. |
| `variable not set: tem_arma` no boneco | Idem (o boneco herda do pai) | Passo 3. |
| Foice não aparece | `tem_arma = true` faltando, ou o sprite não existe | Passo 4. |
| Nunca faz o golpe 2 | `_golpe1.seguinte` escrito errado, ou `chance` 0 | Passo 4. |
| Inimigos tremem colados | Normal por um instante; se não parar, confira o `0.5` do afastamento | Passo 3. |

## Commit

`dia 10: Aldeão completo e almas`
