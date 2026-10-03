# Dia 7 — Sensação de impacto, arma na mão e animação

**Quando:** dom 11/10 · **Tempo:** ~2,5 h (o resto do dia é folga para recuperar atraso)

**No fim do dia:** acertar congela o jogo por um instante (hitstop), a tela treme, o boneco pisca branco, a arma aparece na mão girando no golpe, e o player troca de sprite conforme o estado. Mesmo com retângulos, bater tem que parecer pesado.

## O que você vai aprender

- **Hitstop**: congelar tudo por 3–10 frames no impacto.
- **Screenshake** (tremor de câmera).
- **Flash branco** com `gpu_set_fog`.
- **Objeto de efeito** que toca uma animação e some.
- **Animação controlada pelo código**, sincronizada com a frame data.

---

## Passo 1 — Funções de "juice" (20 min)

**obj_game → Create** (adicione antes de `room_goto`)
<!-- src: objects/obj_game/Create_0.gml @antes: room_goto -->
```gml
// --- Sensação de impacto ---
hitstop = 0;    // frames que o jogo fica congelado
tremor = 0;     // força do tremor da câmera
```

**obj_game → Begin Step** (adicione no começo, antes de tudo)
<!-- src: objects/obj_game/Step_1.gml @inicio -->
```gml
if (hitstop > 0) {
    hitstop -= 1;
}
```

**scr_util** (novas funções, adicione no fim)
<!-- src: scripts/scr_util.gml #jogo_congelado -->
```gml
/// true enquanto o jogo está parado (hitstop; depois, também menus e fade).
function jogo_congelado() {
    return obj_game.hitstop > 0;
}
```

<!-- src: scripts/scr_util.gml #aplicar_hitstop -->
```gml
/// Congela o jogo por alguns frames: dá peso ao impacto.
function aplicar_hitstop(_frames) {
    obj_game.hitstop = max(obj_game.hitstop, _frames);
}
```

<!-- src: scripts/scr_util.gml #tremer_tela -->
```gml
/// Treme a câmera. _forca: deslocamento máximo em pixels.
function tremer_tela(_forca) {
    obj_game.tremor = max(obj_game.tremor, _forca);
}
```

<!-- src: scripts/scr_util.gml #fx_criar -->
```gml
/// Cria um efeito visual que toca a animação uma vez e some.
/// _escala_y = -1 espelha o efeito (golpe no sentido contrário).
function fx_criar(_x, _y, _spr, _ang, _escala_y) {
    var _fx = instance_create_depth(_x, _y, -_y - 1, obj_fx);
    _fx.sprite_index = _spr;
    _fx.image_angle = _ang;
    _fx.escala_y = _escala_y;
    return _fx;
}
```

<!-- src: scripts/scr_util.gml #anim_quadro -->
```gml
/// Qual quadro mostrar de uma animação que deve durar _dur frames.
function anim_quadro(_t, _dur, _spr) {
    var _n = sprite_get_number(_spr);
    return min(_n - 1, floor(_t / _dur * _n));
}
```

- **`max(atual, novo)`** no hitstop e no tremor: se dois acertos acontecem juntos, vale o maior, e não a soma. Somar deixaria o jogo travado.
- **`instance_create_depth(x, y, depth, objeto)`** cria uma instância. Devolve o id dela, e com esse id mudamos as variáveis da nova instância (`_fx.sprite_index = ...`).
- **`anim_quadro`**: um sprite de 4 quadros numa esquiva de 16 frames mostra um quadro a cada 4 frames. A conta é `timer ÷ duração × quadros`.

## Passo 2 — Câmera que treme (10 min)

**obj_game → End Step** (arquivo inteiro)
<!-- src: objects/obj_game/Step_2.gml -->
```gml
// End Step: roda depois do Step de todo mundo.

// Câmera: segue o player devagar e não mostra fora da room.
if (instance_exists(obj_player)) {
    var _alvo_x = obj_player.x - LARGURA_BASE / 2;
    var _alvo_y = obj_player.y - ALTURA_BASE / 2;
    cam_x = lerp(cam_x, _alvo_x, 0.15);
    cam_y = lerp(cam_y, _alvo_y, 0.15);
}
cam_x = clamp(cam_x, 0, room_width - LARGURA_BASE);
cam_y = clamp(cam_y, 0, room_height - ALTURA_BASE);

// Tremor: desloca a câmera ao acaso, cada vez menos.
var _tx = 0;
var _ty = 0;
if (tremor > 0) {
    _tx = random_range(-tremor, tremor);
    _ty = random_range(-tremor, tremor);
    tremor = tremor * 0.85;
    if (tremor < 0.3) {
        tremor = 0;
    }
}

// Pixel art: a câmera só para em pixel inteiro.
camera_set_view_pos(camera, round(cam_x + _tx), round(cam_y + _ty));
```

O tremor diminui 15% por frame (`× 0,85`) até sumir. O `obj_game` não congela no hitstop, então a câmera treme **durante** o congelamento, que é exatamente o efeito de impacto.

## Passo 3 — Objeto de efeito (15 min)

Crie o objeto **`obj_fx`**, sem sprite. Eventos: Create, Step, Draw.

**obj_fx → Create** (arquivo inteiro)
<!-- src: objects/obj_fx/Create_0.gml -->
```gml
quadro = 0;
velocidade = 1 / 3;   // avança 1 quadro da animação a cada 3 frames
escala_y = 1;
image_speed = 0;
```

**obj_fx → Step** (arquivo inteiro)
<!-- src: objects/obj_fx/Step_0.gml -->
```gml
if (jogo_congelado()) exit;

quadro += velocidade;
if (quadro >= sprite_get_number(sprite_index)) {
    instance_destroy();
}
```

**obj_fx → Draw** (arquivo inteiro)
<!-- src: objects/obj_fx/Draw_0.gml -->
```gml
draw_sprite_ext(sprite_index, quadro, x, y, 1, escala_y, image_angle, c_white, 1);
```

`exit` sai do evento na hora. Com o jogo congelado, o efeito não anda.

## Passo 4 — Boneco piscando branco (10 min)

**obj_boneco → Step** (arquivo inteiro)
<!-- src: objects/obj_boneco/Step_0.gml -->
```gml
if (jogo_congelado()) exit;

if (flash > 0) {
    flash -= 1;
}
```

**obj_boneco → Draw** (arquivo inteiro)
<!-- src: objects/obj_boneco/Draw_0.gml -->
```gml
// Piscando: gpu_set_fog pinta o sprite inteiro de uma cor só.
if (flash > 0) gpu_set_fog(true, c_white, 1, 0);
draw_sprite_ext(sprite_index, 0, x, y, 1, 1, 0, c_white, 1);
if (flash > 0) gpu_set_fog(false, c_white, 0, 1);

if (ultimo_dano > 0) {
    draw_set_halign(fa_center);
    draw_text(x, y - 40, string(ultimo_dano));
    draw_set_halign(fa_left);
}
```

**`gpu_set_fog`** é um truque: a "névoa" pinta tudo que é desenhado com uma cor só. Ligou, desenhou, **desligou**. Se esquecer de desligar, tudo que vier depois sai branco.

## Passo 5 — Animação e arma do player (40 min)

**obj_player → Create** (adicione no fim)
<!-- src: objects/obj_player/Create_0.gml @fim -->
```gml
// --- Animação ---
image_speed = 0;    // quem escolhe o quadro é o código (player_animar)
anim_timer = 0;
sentido = 1;        // lado do giro da arma (alterna no combo)

// Sprite de cada estado. Quando a arte chegar, é só trocar aqui.
spr = {
    parado: spr_player,
    andando: spr_player,
    backstep: spr_player,
    dash: spr_player,
    ataque: spr_player,
    tiro: spr_player,
    cura: spr_player,
    hit: spr_player,
    visceral: spr_player,
    morte: spr_player
};
```

**`image_speed = 0`** desliga a animação automática do GameMaker. A animação do ataque precisa bater com a frame data: quadro 0 no windup, 1 no ativo, 2 no recovery. Se o GameMaker animasse sozinho, o corte apareceria na hora errada.

**scr_combate** (nova função, adicione no fim)
<!-- src: scripts/scr_combate.gml #angulo_golpe -->
```gml
/// Ângulo da arma durante um golpe: parada no começo do arco no windup,
/// varre o arco no ativo, parada no fim do arco no recovery.
function angulo_golpe(_timer, _windup, _ativo, _dir, _arco, _sentido) {
    var _ini = _dir + _arco / 2 * _sentido;
    var _fim = _dir - _arco / 2 * _sentido;
    if (_timer <= _windup) return _ini;
    if (_timer <= _windup + _ativo) return lerp(_ini, _fim, (_timer - _windup) / _ativo);
    return _fim;
}
```

**scr_player** (substitua a função `player_comecar_golpe`)
<!-- src: scripts/scr_player.gml #player_comecar_golpe -->
```gml
function player_comecar_golpe(_golpe, _pesado) {
    golpe = _golpe;
    golpe_pesado = _pesado;
    acertados = [];                 // golpe novo: ninguém acertado ainda
    ataque_dir = obj_game.mira_dir;
    // Golpes do combo alternam o lado do corte: ida e volta.
    if (_pesado || combo_i mod 2 == 0) {
        sentido = 1;
    } else {
        sentido = -1;
    }
    player_gastar_stamina(golpe.stamina);
    player_trocar(PL.ATAQUE);
}
```

**scr_player** (substitua a função `player_estado_ataque`)
<!-- src: scripts/scr_player.gml #player_estado_ataque -->
```gml
function player_estado_ataque() {
    var _arma = obj_game.arma;
    var _fim_windup = golpe.windup;
    var _fim_ativo  = golpe.windup + golpe.ativo;
    var _fim_total  = _fim_ativo + golpe.recovery;

    if (estado_timer <= _fim_windup) {
        // Windup: ainda gira para a mira.
        ataque_dir = obj_game.mira_dir;
    } else if (estado_timer <= _fim_ativo) {
        // Primeiro frame do ativo: efeito do corte.
        if (estado_timer == _fim_windup + 1) {
            fx_criar(x, y - 10, golpe.fx, ataque_dir, sentido * lado);
        }
        // Ativo: avança um pouco e acerta quem estiver no setor.
        var _passo = golpe.avanco / golpe.ativo;
        move_and_collide(lengthdir_x(_passo, ataque_dir), lengthdir_y(_passo, ataque_dir), obj_parede);

        var _dano = dano_escalado(golpe.dano, _arma.esc_for, _arma.esc_des);
        var _novos = golpe_setor(x, y, ataque_dir, golpe.alcance, golpe.arco, obj_boneco, acertados);
        for (var i = 0; i < array_length(_novos); i++) {
            array_push(acertados, _novos[i]);
            inimigo_dano(_novos[i], _dano);
        }
        if (array_length(_novos) > 0) {
            aplicar_hitstop(3);
            tremer_tela(1);
        }
    } else {
        // Recovery: um leve apertado aqui continua o combo.
        if (!golpe_pesado && player_tentar_atacar()) return;
        // Na segunda metade do recovery, a esquiva corta o golpe.
        if (estado_timer > _fim_ativo + golpe.recovery / 2) {
            if (player_tentar_esquivar()) return;
        }
    }

    if (estado_timer >= _fim_total) {
        player_trocar(PL.LIVRE);
    }
}
```

**scr_player** (novas funções, adicione no fim)
<!-- src: scripts/scr_player.gml #player_animar -->
```gml
/// Escolhe sprite e quadro conforme o estado.
function player_animar() {
    anim_timer += 1;
    switch (estado) {
        case PL.LIVRE:
            if (obj_game.mover_x != 0 || obj_game.mover_y != 0) {
                sprite_index = spr.andando;
                image_index = (anim_timer div 6) mod sprite_get_number(sprite_index);
            } else {
                sprite_index = spr.parado;
                image_index = (anim_timer div 10) mod sprite_get_number(sprite_index);
            }
            break;
        case PL.ESQUIVA:
            sprite_index = (esq == dash) ? spr.dash : spr.backstep;
            image_index = anim_quadro(estado_timer, esq.duracao, sprite_index);
            break;
        case PL.ATAQUE:
            // 3 quadros: windup, ativo, recovery
            sprite_index = spr.ataque;
            if (estado_timer <= golpe.windup) {
                image_index = 0;
            } else if (estado_timer <= golpe.windup + golpe.ativo) {
                image_index = 1;
            } else {
                image_index = 2;
            }
            break;
        case PL.HITSTUN:
            sprite_index = spr.hit;
            image_index = anim_quadro(estado_timer, 18, sprite_index);
            break;
        case PL.MORTE:
            sprite_index = spr.morte;
            image_index = anim_quadro(estado_timer, 60, sprite_index);
            break;
    }
}
```

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
}
```

- A **mão** fica em `(x + 2 * lado, y - 10)`: é onde está a mão da frente no desenho do caçador (`arte/player`), 2 pixels à frente do centro e 10 acima dos pés. O `* lado` põe a mão do outro lado quando ele olha para a esquerda. Com o retângulo provisório, a arma sai do meio dele; com a arte, sai da luva.
- **`sentido * lado`**: olhando para a esquerda, o giro é espelhado, para o golpe continuar "de cima para baixo".

## Passo 6 — Step e Draw do player (30 min)

**obj_player → Step** (arquivo inteiro)
<!-- src: objects/obj_player/Step_0.gml -->
```gml
if (jogo_congelado()) exit;

estado_timer += 1;

switch (estado) {
    case PL.LIVRE:   player_estado_livre();   break;
    case PL.ESQUIVA: player_estado_esquiva(); break;
    case PL.ATAQUE:  player_estado_ataque();  break;
    case PL.HITSTUN: player_estado_hitstun(); break;
    case PL.MORTE:   player_estado_morte();   break;
}

// Stamina volta a encher depois de 30 frames sem gastar.
if (st_espera > 0) {
    st_espera -= 1;
} else {
    st = min(st_max, st + 1);
}

// Invulnerabilidade depois de apanhar.
if (invul_timer > 0) {
    invul_timer -= 1;
}

// O corpo vira para o lado do golpe (atacando) ou do mouse.
var _olhar = obj_game.mira_dir;
if (estado == PL.ATAQUE) {
    _olhar = ataque_dir;
}
if (_olhar > 90 && _olhar < 270) {
    lado = -1;
} else {
    lado = 1;
}

player_animar();

// Quem está mais embaixo na tela é desenhado por cima.
depth = -y;
```

**obj_player → Draw** (arquivo inteiro)
<!-- src: objects/obj_player/Draw_0.gml -->
```gml
// Com o debug ligado, o player fica ciano enquanto está invulnerável.
var _cor = c_white;
if (obj_game.debug && (invulneravel || invul_timer > 0)) {
    _cor = c_aqua;
}

// Arma apontando para cima fica atrás do corpo; para baixo, na frente.
var _dir_arma = obj_game.mira_dir;
if (estado == PL.ATAQUE) {
    _dir_arma = ataque_dir;
}
var _arma_atras = (_dir_arma > 20 && _dir_arma < 160);
// Morto, curando (o frasco está na mão) ou no visceral (golpe com a mão): sem arma.
var _com_arma = (estado != PL.MORTE && estado != PL.CURA && estado != PL.VISCERAL);

if (_arma_atras && _com_arma) player_desenhar_arma();
draw_sprite_ext(sprite_index, image_index, x, y, lado, 1, 0, _cor, 1);
if (!_arma_atras && _com_arma) player_desenhar_arma();

if (obj_game.debug) {
    draw_set_colour(c_lime);
    draw_rectangle(bbox_left, bbox_top, bbox_right, bbox_bottom, true);
    draw_line(x, y, mouse_x, mouse_y);
    // Nome do estado em cima da cabeça
    draw_set_halign(fa_center);
    draw_text(x, y - 36, obj_game.nomes_pl[estado]);
    draw_set_halign(fa_left);
    // Setor do golpe: cinza no windup/recovery, vermelho no ativo
    if (estado == PL.ATAQUE) {
        if (estado_timer > golpe.windup && estado_timer <= golpe.windup + golpe.ativo) {
            draw_set_colour(c_red);
        } else {
            draw_set_colour(c_gray);
        }
        desenhar_setor(x, y, ataque_dir, golpe.alcance, golpe.arco);
    }
    // Barras: vida (vermelho) e stamina (amarelo)
    draw_healthbar(x - 10, y - 28, x + 10, y - 27, hp / hp_max * 100, c_black, c_red, c_red, 0, true, false);
    draw_healthbar(x - 10, y - 25, x + 10, y - 24, st / st_max * 100, c_black, c_yellow, c_yellow, 0, true, false);
    draw_set_colour(c_white);
}
```

## Passo 7 — Dano no player também tem impacto (5 min)

**scr_combate**, na função `player_dano` (adicione logo depois da linha `_entrou = true;`)
<!-- src: scripts/scr_combate.gml @depois: _entrou = true; -->
```gml
            aplicar_hitstop(4);
            tremer_tela(2);
```

---

## Arte do dia

Com a arte pronta, faça agora a parte **Dia 7** do [Apêndice A](apendice-a-arte.md): importar os sprites do player, das armas e dos cortes, trocar os valores do `spr = { ... }` no Create do player e os `fx:` do `scr_dados`. Nenhum código de estado muda.

## Teste do dia

- [ ] Acertar o boneco: tudo congela por um instante, a tela treme, o boneco fica branco.
- [ ] Tomar dano da armadilha: congela e treme mais forte.
- [ ] A arma aparece na mão apontando para o mouse.
- [ ] No golpe, a arma varre o arco: fica parada no windup, gira no ativo, parada no recovery.
- [ ] Golpes do combo alternam o lado do corte.
- [ ] Mirando para cima, a arma fica atrás do corpo.
- [ ] Um risco branco (efeito) aparece no começo de cada ativo.

## Se deu errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| O jogo trava para sempre ao acertar | `hitstop -= 1` não está no Begin Step do obj_game | Passo 1. |
| Tudo fica branco depois de acertar | Faltou `gpu_set_fog(false, ...)` | Passo 4. |
| `variable not set: sentido` | Bloco do Create não adicionado | Passo 5. |
| Arma gira no sentido errado olhando para a esquerda | Faltou o `* lado` | Passo 5. |
| `sprite_get_number` dá erro no obj_fx | Um golpe no `scr_dados` está sem o campo `fx` | Dia 6, passo 2. |

## Checkpoint da semana 1

Tudo abaixo tem que funcionar antes de seguir:

| Tem que funcionar | Se não |
|---|---|
| Andar, colidir, câmera | termine no dia 8, antes das pistolas |
| Backstep e dash com iframes, stamina, tomar dano | idem |
| 3 armas com combo e pesado contra o boneco | idem, e aplique já os cortes 1 e 2 do [cronograma](../CRONOGRAMA.md#ordem-de-corte) |

## Commit

`dia 7: game feel, arma na mão, animação` — e um commit extra: `semana 1`.
