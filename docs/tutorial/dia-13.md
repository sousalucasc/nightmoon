# Dia 13 — Chefe, fase 1

**Quando:** sáb 17/10 · **Tempo:** ~3 h

**No fim do dia:** o **Caçador Caído** luta numa room de teste. De perto, dá uma machadada dupla (aceita parry). De média distância, atira com escopeta (desvie). De longe, salta e cai onde você estava, com a área de impacto marcada no chão.

## O que você vai aprender

- **Tipos de ataque** diferentes no mesmo estado (golpe, tiro, salto).
- **Movimento de salto** com `lerp` e `sin`: ir de A até B subindo e descendo.
- **Parâmetro opcional** em função (`_tiro_id = -1`).
- Projéteis do inimigo usando o mesmo objeto dos seus.

---

## Passo 1 — Sprite e room de teste (15 min)

| Sprite | Tamanho | Cor | Origem |
|---|---|---|---|
| `spr_chefe` | 20×28 | azul-acinzentado | x 10, y 28 |

Crie a room **`rm_teste_chefe`**: **480×360**. Coloque paredes nas quatro bordas (como na `rm_teste`: Scale X 30 em cima e embaixo; Scale Y 21 nas laterais, em x 464). Coloque um `obj_player` em **(240, 300)**. O chefe vem no passo 5.

Para ir e voltar entre as rooms de teste, duas teclas de debug:

**obj_game → Begin Step** (dentro do `if (debug)`, adicione antes da linha da tecla 7)
<!-- src: objects/obj_game/Step_1.gml @antes: if (keyboard_check_pressed(ord("7"))) -->
```gml
    if (keyboard_check_pressed(ord("B"))) room_goto(rm_teste_chefe);
    if (keyboard_check_pressed(ord("T"))) room_goto(rm_teste);
```

## Passo 2 — Variáveis novas do pai (10 min)

**obj_inimigo_pai → Create** (adicione no fim)
<!-- src: objects/obj_inimigo_pai/Create_0.gml @fim -->
```gml
// --- Chefe e ataques especiais ---
nome = "";
e_chefe = false;
tem_fase2 = false;
fase = 1;
no_ar = false;      // no meio do salto: não apanha
altura = 0;         // quanto o corpo está acima do chão (só para desenhar)
salto_x0 = x;       // de onde saltou
salto_y0 = y;
salto_x1 = x;       // onde vai cair
salto_y1 = y;
boca_x = 12;        // onde fica a boca da arma de fogo no desenho (clarão e chumbos saem dali)
boca_y = 12;
```

## Passo 3 — Tiro e salto no estado de ataque (60 min)

**scr_inimigo** (substitua a função `inimigo_comecar_ataque`)
<!-- src: scripts/scr_inimigo.gml #inimigo_comecar_ataque -->
```gml
function inimigo_comecar_ataque(_a) {
    ataque = _a;
    acertados = [];
    if (instance_exists(obj_player)) {
        ataque_dir = point_direction(x, y, obj_player.x, obj_player.y);
        if (_a.tipo == "salto") {
            salto_x0 = x;
            salto_y0 = y;
            salto_x1 = obj_player.x;
            salto_y1 = obj_player.y;
        }
    }
    inimigo_trocar(INI.ATAQUE);
}
```

**scr_inimigo** (substitua a função `inimigo_estado_ataque`)
<!-- src: scripts/scr_inimigo.gml #inimigo_estado_ataque -->
```gml
function inimigo_estado_ataque() {
    var _a = ataque;
    var _fim_windup = _a.windup;
    var _fim_ativo  = _a.windup + _a.ativo;
    var _fim_total  = _fim_ativo + _a.recovery;

    if (estado_timer <= _fim_windup) {
        // Segue o player, mas trava nos últimos 8 frames: senão seria impossível esquivar.
        if (estado_timer < _fim_windup - 8 && instance_exists(obj_player)) {
            ataque_dir = point_direction(x, y, obj_player.x, obj_player.y);
            if (_a.tipo == "salto") {
                salto_x1 = obj_player.x;
                salto_y1 = obj_player.y;
            }
        }
    } else if (estado_timer <= _fim_ativo) {
        var _t = estado_timer - _fim_windup;   // 1, 2, 3... dentro do ativo
        if (_a.tipo == "tiro") {
            if (_t == 1) {
                inimigo_atirar(_a);
            }
        } else if (_a.tipo == "salto") {
            if (_t <= _a.voo) {
                // No ar: vai do ponto de saída até o alvo, subindo e descendo.
                no_ar = true;
                var _k = _t / _a.voo;              // vai de 0 a 1
                x = lerp(salto_x0, salto_x1, _k);
                y = lerp(salto_y0, salto_y1, _k);
                altura = sin(_k * pi) * 24;        // 0 → 24 → 0
                if (_t == _a.voo) {
                    inimigo_pousar();
                }
            } else {
                inimigo_golpear(_a);               // impacto em volta
            }
        } else {
            if (_a.avanco > 0) {
                var _passo = _a.avanco / _a.ativo;
                move_and_collide(lengthdir_x(_passo, ataque_dir), lengthdir_y(_passo, ataque_dir), obj_parede);
            }
            inimigo_golpear(_a);
        }
        // Combo: no último frame do ativo, pode emendar o próximo golpe.
        if (estado_timer == _fim_ativo && _a.seguinte != undefined && random(1) < _a.chance) {
            inimigo_comecar_ataque(_a.seguinte);
            return;
        }
    }

    lado = (lengthdir_x(1, ataque_dir) < 0) ? -1 : 1;

    if (estado_timer >= _fim_total) {
        espera = espera_entre;
        inimigo_trocar(INI.PERSEGUIR);
    }
}
```

**scr_inimigo** (novas funções, adicione no fim)
<!-- src: scripts/scr_inimigo.gml #inimigo_pousar -->
```gml
/// Fim do salto: volta ao chão. Se caiu encostado numa parede, recua até ficar livre.
function inimigo_pousar() {
    no_ar = false;
    altura = 0;
    tremer_tela(3);
    var _volta = point_direction(x, y, salto_x0, salto_y0);
    var _n = 0;
    while (place_meeting(x, y, obj_parede) && _n < 40) {
        x += lengthdir_x(1, _volta);
        y += lengthdir_y(1, _volta);
        _n += 1;
    }
}
```

<!-- src: scripts/scr_inimigo.gml #inimigo_atirar -->
```gml
/// Tiro de escopeta do inimigo: 5 chumbos espalhados no arco do ataque.
function inimigo_atirar(_a) {
    obj_game.contador_tiros += 1;
    for (var i = 0; i < 5; i++) {
        var _ang = ataque_dir - _a.arco / 2 + _a.arco * i / 4;
        var _b = instance_create_depth(x, y, depth - 1, obj_projetil);
        _b.do_player = false;
        _b.dir = _ang;
        _b.vel = 5;
        _b.alcance = _a.alcance;
        _b.dano = _a.dano;
        _b.tiro_id = obj_game.contador_tiros;
        _b.cor = c_red;
        _b.altura = boca_y;     // os chumbos voam na altura da boca do cano
    }
    // Clarão na boca da arma desenhada no sprite (o chefe define boca_x e boca_y).
    fx_criar(x + boca_x * lado, y - boca_y, spr_fx_disparo, ataque_dir, 1);
    tremer_tela(1);
}
```

O salto em detalhe:

- **`_k`** vai de 0 (saída) a 1 (chegada) durante o voo.
- **`lerp(saída, chegada, _k)`**: com `_k = 0,5`, está na metade do caminho.
- **`sin(_k * pi)`**: a função seno vai de 0, sobe até 1 no meio e volta a 0. Multiplicando por 24, o corpo sobe até 24 px e desce. É a parábola do pulo.
- **A posição (`x, y`) continua no chão**, como uma sombra andando. Só o **desenho** sobe (`altura`). Por isso ele cai exatamente no ponto marcado.
- **`inimigo_pousar`**: o alvo era o seu pé. Se você estava colado numa parede, a máscara grande do chefe pode cair dentro dela. O `while` recua 1 px por vez em direção ao ponto de saída até sair da parede (no máximo 40 vezes, para nunca travar).
- **`while`** repete enquanto a condição for verdadeira. Sempre garanta que ela vai ficar falsa um dia (aqui, o `_n < 40`).

## Passo 4 — Dano: no ar e chumbos (20 min)

**scr_combate**, na função `inimigo_dano` (troque a linha `if (estado != INI.MORTE) {` por esta)
<!-- src: scripts/scr_combate.gml @troca: if (estado != INI.MORTE) { -->
```gml
        if (estado != INI.MORTE && !no_ar) {
```

No ar, o chefe não apanha.

**obj_player → Create** (adicione no fim)
<!-- src: objects/obj_player/Create_0.gml @fim -->
```gml
ultimo_tiro_levado = -1;    // chumbos do mesmo tiro só acertam uma vez
```

**scr_combate** (substitua a função `player_dano`)
<!-- src: scripts/scr_combate.gml #player_dano -->
```gml
/// Aplica dano no player. _de_x, _de_y: de onde veio o golpe (para o empurrão).
/// _tiro_id: número do tiro, para os chumbos de um mesmo tiro acertarem uma vez só.
/// Golpes não passam _tiro_id (fica -1). Devolve true se o dano entrou.
function player_dano(_dano, _de_x, _de_y, _tiro_id = -1) {
    var _entrou = false;
    with (obj_player) {
        var _mesmo_tiro = (_tiro_id != -1 && _tiro_id == ultimo_tiro_levado);
        if (!invulneravel && invul_timer <= 0 && estado != PL.MORTE && !_mesmo_tiro) {
            _entrou = true;
            aplicar_hitstop(4);
            tremer_tela(2);
            if (_tiro_id != -1) {
                ultimo_tiro_levado = _tiro_id;
            }
            hp -= _dano;
            // Hyper armor: golpe com a flag não é interrompido no windup nem no ativo.
            var _hyper = (estado == PL.ATAQUE && golpe.hyper && estado_timer <= golpe.windup + golpe.ativo);
            if (hp <= 0) {
                hp = 0;
                player_trocar(PL.MORTE);
            } else if (_hyper) {
                invul_timer = 10;   // o dano entra, mas o golpe continua
            } else {
                kb_dir = point_direction(_de_x, _de_y, x, y);
                kb_vel = 2 * 10 / 18;
                kb_desacel = kb_vel / 18;
                player_trocar(PL.HITSTUN);
            }
        }
    }
    return _entrou;
}
```

**`_tiro_id = -1`** no cabeçalho é um **parâmetro opcional**: quem não passar esse valor recebe -1. Os golpes chamam `player_dano(dano, x, y)` como sempre; os chumbos chamam com o quarto valor.

**Por que precisa?** Os 5 chumbos chegam juntos. O primeiro põe você em hitstun, mas hitstun não é invulnerável, então os outros quatro também entrariam: 100 de dano de uma vez. Com o `tiro_id`, o tiro inteiro conta como um acerto.

## Passo 5 — Projétil dos dois lados (20 min)

**obj_projetil → Create** (adicione no fim)
<!-- src: objects/obj_projetil/Create_0.gml @fim -->
```gml
cor = c_white;      // tiros inimigos ficam vermelhos
```

**obj_projetil → Step** (arquivo inteiro)
<!-- src: objects/obj_projetil/Step_0.gml -->
```gml
if (jogo_congelado()) exit;

var _x0 = x;
var _y0 = y;
x += lengthdir_x(vel, dir);
y += lengthdir_y(vel, dir);
dist += vel;

// Bateu numa parede no caminho?
if (collision_line(_x0, _y0, x, y, obj_parede, false, true) != noone) {
    instance_destroy();
    exit;
}

if (do_player) {
    // Tiro do player: acertou algum inimigo no caminho?
    var _alvo = projetil_achar_alvo(_x0, _y0, x, y, obj_inimigo_pai);
    if (_alvo != noone) {
        projetil_acertar_inimigo(_alvo);
        instance_destroy();
        exit;
    }
} else {
    // Tiro de inimigo: acertou o player?
    if (projetil_achar_alvo(_x0, _y0, x, y, obj_player) != noone) {
        player_dano(dano, _x0, _y0, tiro_id);
        instance_destroy();
        exit;
    }
}

// Passou do alcance: some.
if (dist >= alcance) {
    instance_destroy();
    exit;
}

depth = -y;
```

**obj_projetil → Draw** (arquivo inteiro)
<!-- src: objects/obj_projetil/Draw_0.gml -->
```gml
// A posição é no chão; o desenho fica na altura da mão.
draw_sprite_ext(sprite_index, 0, x, y - altura, 1, 1, dir, cor, 1);
```

## Passo 6 — Desenho com salto e marca no chão (20 min)

**obj_inimigo_pai → Draw** (arquivo inteiro)
<!-- src: objects/obj_inimigo_pai/Draw_0.gml -->
```gml
// Salto: sombra no chão durante o voo; no windup, a área do impacto em vermelho.
if (estado == INI.ATAQUE && ataque.tipo == "salto") {
    draw_set_alpha(0.4);
    if (no_ar) {
        draw_set_colour(c_black);
        draw_ellipse(x - 10, y - 4, x + 10, y + 2, false);
    } else if (estado_timer <= ataque.windup) {
        draw_set_colour(c_red);
        draw_ellipse(salto_x1 - ataque.alcance, salto_y1 - ataque.alcance / 2, salto_x1 + ataque.alcance, salto_y1 + ataque.alcance / 2, true);
    }
    draw_set_alpha(1);
    draw_set_colour(c_white);
}

var _dy = y - altura;   // no salto, o corpo sobe

// Morto: o corpo some devagar nos últimos 30 frames (de 70 a 100).
var _alpha = 1;
if (estado == INI.MORTE) {
    _alpha = clamp((100 - estado_timer) / 30, 0, 1);
}

// Desenho normal, ou todo branco se acabou de apanhar.
if (flash > 0) gpu_set_fog(true, c_white, 1, 0);
draw_sprite_ext(sprite_index, image_index, x, _dy, lado, 1, 0, c_white, _alpha);
if (flash > 0) gpu_set_fog(false, c_white, 0, 1);

// Arma separada (Aldeão, chefe): gira no golpe igual à do player, a partir da mão.
// No tiro, a arma de fogo já está desenhada nas mãos: a arma separada não aparece.
var _atirando = (estado == INI.ATAQUE && ataque.tipo == "tiro");
if (tem_arma && estado != INI.MORTE && !_atirando) {
    var _ang = (lado == 1) ? -40 : 220;
    if (estado == INI.ATAQUE) {
        _ang = angulo_golpe(estado_timer, ataque.windup, ataque.ativo, ataque_dir, ataque.arco, lado);
    }
    draw_sprite_ext(arma_sprite, 0, x + mao_x * lado, _dy - mao_y, 1, 1, _ang, c_white, 1);
}

// Aviso no começo do windup: branco = aceita parry, vermelho = não aceita.
if (estado == INI.ATAQUE && estado_timer <= 8 && flash <= 0) {
    var _cor = c_red;
    if (ataque.parry) {
        _cor = c_white;
    }
    gpu_set_fog(true, _cor, 1, 0);
    draw_sprite_ext(sprite_index, image_index, x, _dy, lado, 1, 0, c_white, 0.6);
    gpu_set_fog(false, c_white, 0, 1);
}

// Atordoado: sinal amarelo piscando em cima da cabeça (hora do visceral).
if (estado == INI.STAGGER && (estado_timer div 6) mod 2 == 0) {
    draw_set_colour(c_yellow);
    draw_circle(x, _dy - sprite_get_yoffset(sprite_index) + sprite_get_bbox_top(sprite_index) - 6, 3, false);
    draw_set_colour(c_white);
}

if (obj_game.debug) {
    draw_set_halign(fa_center);
    draw_text(x, _dy - 44, obj_game.nomes_ini[estado] + " " + string(hp) + " (-" + string(ultimo_dano) + ")");
    draw_set_halign(fa_left);
    if (estado == INI.ATAQUE) {
        if (estado_timer > ataque.windup && estado_timer <= ataque.windup + ataque.ativo) {
            draw_set_colour(c_red);
        } else {
            draw_set_colour(c_gray);
        }
        desenhar_setor(x, y, ataque_dir, ataque.alcance, ataque.arco);
    }
    // Janela de parry aberta (contando o bônus da pistola): círculo amarelo
    if (inimigo_janela_parry(id, 4)) {
        draw_set_colour(c_yellow);
        draw_circle(x, y - 10, 12, true);
    }
    draw_set_colour(c_orange);
    draw_circle(inicio_x, inicio_y, 2, false);   // ponto inicial
    draw_set_colour(c_white);
}
```

É o mesmo Draw de antes, com três mudanças: a sombra/área do salto no começo, tudo que é do corpo usando `_dy` (sobe junto no salto), e a arma separada escondida durante o tiro.

## Passo 7 — O chefe (20 min)

Crie o objeto **`obj_chefe`** com o sprite `spr_chefe` e **Parent `obj_inimigo_pai`**. Só o Create:

**obj_chefe → Create** (arquivo inteiro)
<!-- src: objects/obj_chefe/Create_0.gml -->
```gml
event_inherited();

nome = "Caçador Caído";
e_chefe = true;
hp_max = 900;
hp = hp_max;
vel = 1.3;
raio = 12;
almas = 800;
pode_hitstun = false;
aggro = 400;          // na arena, vê o player de qualquer lugar
desiste = 99999;      // nunca desiste
dist_parar = 24;
espera_entre = 15;
mask_index = spr_mask_grande;

// --- Fase 1 ---
// Machadada dupla: o segundo golpe sempre vem (chance 1).
var _machadada2 = ataque_novo(14, 5, 24, 25, 30, 140, true);
var _machadada1 = ataque_novo(20, 5, 0, 25, 30, 140, true);
_machadada1.seguinte = _machadada2;
_machadada1.chance = 1;
_machadada1.dist_max = 40;

// Tiro de escopeta: média distância, não aceita parry (desvie).
var _tiro = ataque_novo(30, 1, 30, 20, 80, 40, false);
_tiro.tipo = "tiro";
_tiro.dist_min = 40;
_tiro.dist_max = 100;

// Salto: de longe; cai onde o player estava.
var _salto = ataque_novo(30, 28, 30, 30, 28, 360, false);
_salto.tipo = "salto";
_salto.voo = 24;      // frames no ar; os 4 últimos do ativo são o impacto
_salto.dist_min = 100;
_salto.dist_max = 9999;

ataques = [_machadada1, _tiro, _salto];

tem_arma = true;
arma_sprite = spr_arma_machado;
// No desenho do chefe: a mão do machado e a boca do bacamarte (em px a partir dos pés).
mao_x = 4;
mao_y = 12;
boca_x = 20;
boca_y = 22;
```

`_salto.voo = 24` cria um campo novo no struct: dá para adicionar campos a qualquer momento.

Coloque um `obj_chefe` na `rm_teste_chefe` em **(240, 120)**.

---

## Teste do dia

F3 ligado, tecla **B** para ir à sala do chefe.

- [ ] Longe dele: ele salta; aparece uma elipse vermelha onde você está; ele sobe, cai ali e a tela treme.
- [ ] Saindo da elipse a tempo, o salto erra.
- [ ] Média distância: ele atira 5 chumbos vermelhos em leque. Levar o tiro tira 20 de uma vez, não 100.
- [ ] Perto: machadada dupla (sempre dois golpes), com aviso branco e janela de parry.
- [ ] Parry + visceral funcionam nele.
- [ ] Batendo nele no ar, nada acontece.
- [ ] Dá para vencer (900 de vida). Anote o que ficou fácil ou difícil demais.

## Se deu errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| `unknown function inimigo_atirar` | Função não adicionada ou nome diferente | Passo 3. |
| O chefe some no salto | Desenho usando `y` em vez de `_dy`… ou `altura` gigante | Passo 6. |
| O chefe cai dentro da parede e trava | Faltou `inimigo_pousar` | Passo 3. |
| Chumbos matam na hora | `player_dano` sem o `_tiro_id` | Passo 4. |
| Seus tiros acertam você | `_b.do_player = false` faltando no tiro do chefe | Passo 3. |
| Erro ao compilar no `_tiro_id = -1` | Versão muito antiga do GameMaker (parâmetro opcional é do 2.3+) | Atualize o GameMaker. |

## Commit

`dia 13: chefe fase 1`
