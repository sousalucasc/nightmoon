# Dia 8 — Pistolas

**Quando:** seg 12/10 (feriado: se sobrar tempo, adiante o dia 9) · **Tempo:** ~3 h

**No fim do dia:** Q dispara. A **pistola** sai rápido, com 1 bala reta de longo alcance. A **escopeta** sai devagar e solta 5 chumbos em leque, de perto. As balas acabam.

## O que você vai aprender

- **Projétil** como objeto que anda sozinho.
- **`collision_line`**: não deixar projétil rápido atravessar alvo fino.
- **Leque de tiros** (espalhar N projéteis num ângulo).
- **3/4**: o projétil anda no chão, mas é desenhado na altura da mão.

---

## Passo 1 — Sprites provisórios (10 min)

| Sprite | Tamanho | Cor | Origem |
|---|---|---|---|
| `spr_projetil` | 4×4 | amarelo | x 2, y 2 |
| `spr_arma_pistola` | 8×3 | cinza escuro | x 0, y 1 |
| `spr_arma_escopeta` | 12×3 | marrom | x 0, y 1 |
| `spr_fx_disparo` | 6×6 | amarelo claro | x 0, y 3 |

## Passo 2 — Dados das pistolas (15 min)

**scr_dados** (nova função, adicione no fim)
<!-- src: scripts/scr_dados.gml #dados_pistolas -->
```gml
function dados_pistolas() {
    // GDD seção 8. Tempos em frames, velocidade em px/frame, alcance em px.
    global.pistolas = {
        pistola: {
            nome: "Pistola",
            startup: 3, recovery: 14,
            projeteis: 1, leque: 0,
            vel: 8, alcance: 120,
            dano: 8, esc_for: 0, esc_des: 1.0,
            parry_bonus: 4,
            sprite: spr_arma_pistola
        },
        escopeta: {
            nome: "Escopeta de cano serrado",
            startup: 8, recovery: 22,
            projeteis: 5, leque: 40,
            vel: 6, alcance: 56,
            dano: 6, esc_for: 1.0, esc_des: 0,
            parry_bonus: 0,
            sprite: spr_arma_escopeta
        }
    };
}
```

- **`startup`**: frames entre apertar Q e a bala sair. Pistola 3, escopeta 8: a pistola é a de timing fácil.
- **`parry_bonus`**: frames extras de janela de parry (dia 11).
- **`leque: 40`** com 5 chumbos: eles saem em -20°, -10°, 0°, +10° e +20° da mira.

**obj_game → Create** (adicione antes de `room_goto`)
<!-- src: objects/obj_game/Create_0.gml @antes: room_goto -->
```gml
dados_pistolas();
pistola = global.pistolas.pistola;   // pistola equipada
contador_tiros = 0;                  // cada tiro ganha um número único
```

**obj_game → Begin Step** (dentro do `if (debug)`, adicione antes da linha da tecla 7)
<!-- src: objects/obj_game/Step_1.gml @antes: if (keyboard_check_pressed(ord("7"))) -->
```gml
    if (keyboard_check_pressed(ord("4"))) pistola = global.pistolas.pistola;
    if (keyboard_check_pressed(ord("5"))) pistola = global.pistolas.escopeta;
```

**obj_game → Draw GUI** (arquivo inteiro)
<!-- src: objects/obj_game/Draw_64.gml -->
```gml
// Draw GUI: desenhado por cima de tudo, em coordenadas de tela (320x180).
if (debug) {
    draw_text(4, 4, "Arma: " + arma.nome);
    draw_text(4, 18, "Pistola: " + pistola.nome);
    draw_text(4, 32, "FOR " + string(atr_forca) + "  DES " + string(atr_destreza));
    if (instance_exists(obj_player)) {
        draw_text(4, 46, "Balas: " + string(obj_player.balas));
    }
}
```

## Passo 3 — O projétil (40 min)

Crie o objeto **`obj_projetil`** com o sprite `spr_projetil`. Eventos: Create, Step, Draw.

**obj_projetil → Create** (arquivo inteiro)
<!-- src: objects/obj_projetil/Create_0.gml -->
```gml
// Valores padrão. Quem cria o projétil troca estes valores logo depois.
do_player = true;   // true: tiro do player; false: tiro de inimigo
dir = 0;
vel = 8;
alcance = 100;
dano = 5;
parry_bonus = 0;
tiro_id = -1;       // chumbos do mesmo tiro dividem este número
dist = 0;           // quanto já andou
altura = 10;        // desenhado 10 px acima do chão (na altura da mão)
image_speed = 0;
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

// Tiro do player: acertou algum alvo no caminho?
if (do_player) {
    var _alvo = projetil_achar_alvo(_x0, _y0, x, y, obj_boneco);
    if (_alvo != noone) {
        projetil_acertar_inimigo(_alvo);
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
draw_sprite_ext(sprite_index, 0, x, y - altura, 1, 1, dir, c_white, 1);
```

- **Paredes: `collision_line`.** A bala anda 8 pixels por frame e poderia "pular" uma parede fina. `collision_line` testa **a linha inteira** entre a posição antiga e a nova, e devolve quem encostou ou `noone` (ninguém).
- **Alvos: `projetil_achar_alvo` (abaixo)**, que usa o `raio` do corpo, igual aos golpes. A máscara dos inimigos é só a dos pés (6 px de altura), e uma bala mirada no inimigo passa exatamente na linha dos pés: pela máscara, ela passaria raspando por baixo e erraria.
- **`altura`**: tudo no jogo acontece no plano do chão (os pés). A bala voa no chão, mas é desenhada 10 px acima para parecer que sai da mão.
- **`exit`** depois do `instance_destroy`: a instância destruída ainda terminaria o evento; o `exit` evita rodar o resto à toa.

**scr_combate** (nova função, adicione no fim)
<!-- src: scripts/scr_combate.gml #projetil_achar_alvo -->
```gml
/// Procura um alvo do tipo _obj cujo corpo (raio) encoste no caminho que o projétil
/// fez neste frame (de _x0, _y0 até _x1, _y1). Devolve o id, ou noone.
function projetil_achar_alvo(_x0, _y0, _x1, _y1, _obj) {
    var _achou = noone;
    var _mx = (_x0 + _x1) / 2;   // meio do caminho
    var _my = (_y0 + _y1) / 2;
    with (_obj) {
        if (_achou == noone) {
            var _r = raio + 2;
            if (point_distance(_x1, _y1, x, y) <= _r || point_distance(_mx, _my, x, y) <= _r) {
                _achou = id;
            }
        }
    }
    return _achou;
}
```

Testando o ponto final **e** o meio do caminho, a bala nunca "pula" um alvo: ela anda no máximo 8 px por frame, e todo corpo tem pelo menos 8 px de raio (6 + 2).

**scr_combate** (nova função, adicione no fim)
<!-- src: scripts/scr_combate.gml #projetil_acertar_inimigo -->
```gml
/// Roda dentro do projétil, quando ele acerta um inimigo.
function projetil_acertar_inimigo(_alvo) {
    inimigo_dano(_alvo, dano);
    aplicar_hitstop(2);
}
```

## Passo 4 — O player atira (50 min)

**obj_player → Create** (adicione no fim)
<!-- src: objects/obj_player/Create_0.gml @fim -->
```gml
// --- Tiro ---
balas_max = 10;
balas = balas_max;
tiro_id = -1;       // número do último tiro
```

**scr_player** (substitua a função `player_estado_livre`)
<!-- src: scripts/scr_player.gml #player_estado_livre -->
```gml
function player_estado_livre() {
    player_mover(1);
    if (player_tentar_esquivar()) return;
    if (player_tentar_atacar()) return;
    if (player_tentar_atirar()) return;
}
```

**scr_player** (novas funções, adicione no fim)
<!-- src: scripts/scr_player.gml #player_tentar_atirar -->
```gml
/// Começa um tiro se Q está no buffer e tem bala.
function player_tentar_atirar() {
    if (obj_game.buf_tiro > 0 && balas > 0) {
        obj_game.buf_tiro = 0;
        balas -= 1;
        obj_game.contador_tiros += 1;
        tiro_id = obj_game.contador_tiros;
        ataque_dir = obj_game.mira_dir;
        player_trocar(PL.TIRO);
        return true;
    }
    return false;
}
```

<!-- src: scripts/scr_player.gml #player_estado_tiro -->
```gml
function player_estado_tiro() {
    var _p = obj_game.pistola;
    // Até o tiro sair, ainda dá pra mirar.
    if (estado_timer <= _p.startup) {
        ataque_dir = obj_game.mira_dir;
    }
    if (estado_timer == _p.startup) {
        player_disparar(_p);
    }
    // Segunda metade do recovery: dá pra esquivar.
    if (estado_timer > _p.startup + _p.recovery / 2) {
        if (player_tentar_esquivar()) return;
    }
    if (estado_timer >= _p.startup + _p.recovery) {
        player_trocar(PL.LIVRE);
    }
}
```

<!-- src: scripts/scr_player.gml #player_disparar -->
```gml
/// Cria os projéteis da pistola _p.
function player_disparar(_p) {
    for (var i = 0; i < _p.projeteis; i++) {
        var _ang = ataque_dir;
        if (_p.projeteis > 1) {
            // Espalha igualmente dentro do leque: de -leque/2 até +leque/2.
            _ang = ataque_dir - _p.leque / 2 + _p.leque * i / (_p.projeteis - 1);
        }
        var _b = instance_create_depth(x, y, depth - 1, obj_projetil);
        _b.do_player = true;
        _b.dir = _ang;
        _b.vel = _p.vel;
        _b.alcance = _p.alcance;
        _b.dano = dano_escalado(_p.dano, _p.esc_for, _p.esc_des);
        _b.parry_bonus = _p.parry_bonus;
        _b.tiro_id = tiro_id;
    }
    // Clarão na boca do cano: da mão da pistola até a ponta do sprite dela.
    var _cano = sprite_get_width(_p.sprite) - sprite_get_xoffset(_p.sprite);
    fx_criar(x + 3 * lado + lengthdir_x(_cano, ataque_dir), y - 12 + lengthdir_y(_cano, ataque_dir), spr_fx_disparo, ataque_dir, 1);
    tremer_tela(1);
}
```

- **`_cano`**: largura do sprite menos a origem (que fica no cabo) = do cabo até a boca. Com a escopeta, que é mais comprida, o clarão sai mais longe sozinho.

A conta do leque, com 5 chumbos e leque 40: `i` vai de 0 a 4, e `40 × i ÷ 4` dá 0, 10, 20, 30, 40. Subtraindo 20: -20, -10, 0, 10, 20.

**scr_player**, na função `player_estado_ataque` (logo depois da linha `if (estado_timer > _fim_ativo + golpe.recovery / 2) {`, adicione)
<!-- src: scripts/scr_player.gml @depois: if (estado_timer > _fim_ativo + golpe.recovery / 2) { -->
```gml
            if (player_tentar_atirar()) return;
```

Agora a segunda metade do recovery de um golpe aceita **tiro** e esquiva. É o "atacar e atirar" do Bloodborne.

**scr_player**, na função `player_animar` (adicione antes da linha `case PL.HITSTUN:`)
<!-- src: scripts/scr_player.gml @antes: case PL.HITSTUN: -->
```gml
        case PL.TIRO:
            // 3 quadros: preparando, disparo, recovery
            sprite_index = spr.tiro;
            if (estado_timer < obj_game.pistola.startup) {
                image_index = 0;
            } else if (estado_timer <= obj_game.pistola.startup + 4) {
                image_index = 1;
            } else {
                image_index = 2;
            }
            break;
```

**scr_player** (substitua a função `player_desenhar_arma`)
<!-- src: scripts/scr_player.gml #player_desenhar_arma -->
```gml
/// Desenha a arma na mão, girando conforme o golpe.
function player_desenhar_arma() {
    var _ang;
    if (estado == PL.ATAQUE) {
        _ang = angulo_golpe(estado_timer, golpe.windup, golpe.ativo, ataque_dir, golpe.arco, sentido * lado);
    } else {
        // Parada: apontando para a mira, um pouco para baixo.
        _ang = obj_game.mira_dir - 30 * lado;
    }
    draw_sprite_ext(obj_game.arma.sprite, 0, x + 2 * lado, y - 10, 1, 1, _ang, c_white, 1);

    // No tiro, a pistola aparece apontando para o alvo.
    if (estado == PL.TIRO) {
        // Apontando para a esquerda, espelha na vertical para não ficar de cabeça para baixo.
        var _esc_y = 1;
        if (ataque_dir > 90 && ataque_dir < 270) {
            _esc_y = -1;
        }
        // A mão da pistola, no desenho do tiro, fica 3 px à frente e 12 acima dos pés.
        draw_sprite_ext(obj_game.pistola.sprite, 0, x + 3 * lado, y - 12, 1, _esc_y, ataque_dir, c_white, 1);
    }
}
```

## Passo 5 — Step e Draw (10 min)

**obj_player → Step** (logo depois da linha do `case PL.ATAQUE`, adicione)
<!-- src: objects/obj_player/Step_0.gml @depois: case PL.ATAQUE:  player_estado_ataque();  break; -->
```gml
    case PL.TIRO:    player_estado_tiro();    break;
```

**obj_player → Step** (troque a linha `if (estado == PL.ATAQUE) {` do bloco `_olhar` por esta)
<!-- src: objects/obj_player/Step_0.gml @troca: if (estado == PL.ATAQUE) { -->
```gml
if (estado == PL.ATAQUE || estado == PL.TIRO) {
```

**obj_player → Draw** (na parte do `_dir_arma`, troque a linha `if (estado == PL.ATAQUE) {` — a primeira do evento — por esta)
<!-- src: objects/obj_player/Draw_0.gml @troca: if (estado == PL.ATAQUE) { -->
```gml
if (estado == PL.ATAQUE || estado == PL.TIRO) {
```

Assim, atirando, o corpo e a arma viram para o lado do tiro.

---

## Arte do dia

Com a arte pronta, faça agora a parte **Dia 8** do [Apêndice A](apendice-a-arte.md).

## Teste do dia

Ligue o F3.

- [ ] Q: um projétil sai na direção do mouse e some depois de ~120 px.
- [ ] Tecla 5 (escopeta) + Q: 5 chumbos em leque, somem rápido (~56 px), e o tiro demora mais para sair.
- [ ] Acertar o boneco de longe com a pistola: dano 8. Com a escopeta colado nele: vários chumbos acertam.
- [ ] O contador de balas desce; com 0, Q não faz nada.
- [ ] Projétil some ao bater numa parede.
- [ ] Clique esquerdo e logo depois Q: o tiro corta o fim do golpe.

## Se deu errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| Projétil não aparece | `obj_projetil` sem sprite, ou `instance_create_depth` com objeto errado | Passo 3. |
| Projétil fica parado | O Create sobrescreve `vel` depois? Não: quem cria muda os valores **depois** do Create. Confira se `_b.vel = _p.vel` está lá | Passo 4. |
| Todos os chumbos saem no mesmo ângulo | Faltou o `if (_p.projeteis > 1)` ou a conta do leque | Passo 4. |
| Divisão por zero | A pistola (1 projétil) entrou na conta do leque | O `if` impede; confira. |
| `variable not set: balas` no Draw GUI | Bloco do Create do player não adicionado | Passo 4. |

## Commit

`dia 8: pistolas`
