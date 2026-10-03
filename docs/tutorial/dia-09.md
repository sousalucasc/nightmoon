# Dia 9 — O inimigo pai

**Quando:** ter 13/10 · **Tempo:** ~3 h

**No fim do dia:** existe um objeto `obj_inimigo_pai` com toda a inteligência de inimigo (perceber o player, perseguir, atacar com aviso, voltar para casa, apanhar, morrer). O primeiro filho dele, o **Aldeão**, já persegue e ataca. O boneco virou filho também.

## O que você vai aprender

- **Herança de verdade**: um pai com todo o comportamento, filhos que só mudam números.
- **`event_inherited()`**: rodar o evento do pai dentro do filho.
- **IA com estados**, igual à do player.
- Como fazer um ataque inimigo **justo** (aviso e mira que trava).

---

## Os estados do inimigo

| Estado | O que faz | Sai para |
|---|---|---|
| `IDLE` | parado no ponto inicial | `PERSEGUIR` quando o player chega perto |
| `PERSEGUIR` | anda até o player; escolhe um ataque | `ATAQUE`, ou `VOLTAR` se foi longe demais |
| `VOLTAR` | volta ao ponto inicial | `IDLE` |
| `ATAQUE` | windup → ativo → recovery | `PERSEGUIR` |
| `HITSTUN` | apanhou e parou | `PERSEGUIR` |
| `STAGGER`, `VISCERAL`, `CAIDO` | parry (dia 11) | — |
| `TRANSFORMA` | chefe (dia 14) | — |
| `MORTE` | some depois de 30 frames (no dia 10, o corpo passa a ficar no chão até o frame 100) | — |

---

## Passo 1 — Enum e nomes (10 min)

**scr_config** (adicione no fim)
<!-- src: scripts/scr_config.gml @fim -->
```gml
// Estados dos inimigos.
enum INI {
    IDLE,
    PERSEGUIR,
    VOLTAR,
    ATAQUE,
    HITSTUN,
    STAGGER,
    VISCERAL,
    CAIDO,
    TRANSFORMA,
    MORTE
}
```

**obj_game → Create** (adicione antes de `room_goto`)
<!-- src: objects/obj_game/Create_0.gml @antes: room_goto -->
```gml
nomes_ini = ["IDLE", "PERSEGUIR", "VOLTAR", "ATAQUE", "HITSTUN", "STAGGER", "VISCERAL", "CAIDO", "TRANSFORMA", "MORTE"];
```

## Passo 2 — Script do inimigo (60 min)

Crie o script **`scr_inimigo`**. É o maior do dia: digite com calma.

**scr_inimigo** (arquivo inteiro)
<!-- src: scripts/scr_inimigo.gml -->
```gml
// Funções dos inimigos. Quem chama é o próprio inimigo,
// então x, y, estado etc. aqui dentro são dele.

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
        tipo: "golpe"            // "golpe", "tiro" ou "salto"
    };
}

function inimigo_trocar(_novo) {
    estado = _novo;
    estado_timer = 0;
}

function inimigo_dist_player() {
    if (!instance_exists(obj_player)) return 99999;
    return point_distance(x, y, obj_player.x, obj_player.y);
}

function inimigo_player_vivo() {
    return instance_exists(obj_player) && obj_player.estado != PL.MORTE;
}

function inimigo_estado_idle() {
    if (acordado && inimigo_player_vivo() && inimigo_dist_player() <= aggro) {
        inimigo_trocar(INI.PERSEGUIR);
    }
}

function inimigo_estado_perseguir() {
    // Player morreu, ou eu fui longe demais do meu ponto: volto.
    if (!inimigo_player_vivo() || point_distance(x, y, inicio_x, inicio_y) > desiste) {
        inimigo_trocar(INI.VOLTAR);
        return;
    }

    var _dist = inimigo_dist_player();
    var _dir = point_direction(x, y, obj_player.x, obj_player.y);
    lado = (obj_player.x < x) ? -1 : 1;

    // Entre um ataque e outro, espera um pouco.
    if (espera > 0) {
        espera -= 1;
    } else {
        var _a = inimigo_escolher_ataque(_dist);
        if (_a != undefined) {
            inimigo_comecar_ataque(_a);
            return;
        }
    }

    if (_dist > dist_parar) {
        move_and_collide(lengthdir_x(vel, _dir), lengthdir_y(vel, _dir), obj_parede);
    }
}

function inimigo_estado_voltar() {
    var _dist = point_distance(x, y, inicio_x, inicio_y);
    // Chegou (ou ficou preso tentando): volta a esperar.
    if (_dist < 4 || estado_timer > 300) {
        inimigo_trocar(INI.IDLE);
        return;
    }
    var _dir = point_direction(x, y, inicio_x, inicio_y);
    move_and_collide(lengthdir_x(vel, _dir), lengthdir_y(vel, _dir), obj_parede);
    lado = (lengthdir_x(1, _dir) < 0) ? -1 : 1;
}

/// Sorteia um ataque entre os que servem para a distância atual.
function inimigo_escolher_ataque(_dist) {
    var _validos = [];
    for (var i = 0; i < array_length(ataques); i++) {
        var _a = ataques[i];
        if (_dist >= _a.dist_min && _dist <= _a.dist_max) {
            array_push(_validos, _a);
        }
    }
    if (array_length(_validos) == 0) return undefined;
    return _validos[irandom(array_length(_validos) - 1)];
}

function inimigo_comecar_ataque(_a) {
    ataque = _a;
    acertados = [];
    if (instance_exists(obj_player)) {
        ataque_dir = point_direction(x, y, obj_player.x, obj_player.y);
    }
    inimigo_trocar(INI.ATAQUE);
}

function inimigo_estado_ataque() {
    var _a = ataque;
    var _fim_windup = _a.windup;
    var _fim_ativo  = _a.windup + _a.ativo;
    var _fim_total  = _fim_ativo + _a.recovery;

    if (estado_timer <= _fim_windup) {
        // Segue o player, mas trava nos últimos 8 frames: senão seria impossível esquivar.
        if (estado_timer < _fim_windup - 8 && instance_exists(obj_player)) {
            ataque_dir = point_direction(x, y, obj_player.x, obj_player.y);
        }
    } else if (estado_timer <= _fim_ativo) {
        if (_a.avanco > 0) {
            var _passo = _a.avanco / _a.ativo;
            move_and_collide(lengthdir_x(_passo, ataque_dir), lengthdir_y(_passo, ataque_dir), obj_parede);
        }
        inimigo_golpear(_a);
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

/// Acerta o player se ele estiver no setor do ataque.
function inimigo_golpear(_a) {
    var _alvos = golpe_setor(x, y, ataque_dir, _a.alcance, _a.arco, obj_player, acertados);
    if (array_length(_alvos) > 0 && player_dano(_a.dano, x, y)) {
        array_push(acertados, _alvos[0]);
    }
}

function inimigo_estado_hitstun() {
    if (estado_timer >= 12) {
        inimigo_trocar(INI.PERSEGUIR);
    }
}

function inimigo_estado_morte() {
    if (estado_timer >= 30) {
        instance_destroy();
    }
}

/// Golpes só interrompem quem está parado, andando, ou no windup/recovery de um ataque.
function inimigo_pode_interromper() {
    if (estado == INI.ATAQUE) {
        var _no_ativo = (estado_timer > ataque.windup && estado_timer <= ataque.windup + ataque.ativo);
        return !_no_ativo;
    }
    return (estado == INI.IDLE || estado == INI.PERSEGUIR || estado == INI.VOLTAR || estado == INI.HITSTUN);
}

function inimigo_morrer() {
    inimigo_trocar(INI.MORTE);
}
```

As partes importantes:

- **`ataque_novo`** devolve um struct já preenchido com o que quase todo ataque tem. Para um ataque diferente, você cria e depois muda só o campo: `_agarrao.avanco = 24;`.
- **`dist_min` e `dist_max`**: cada ataque serve para uma distância. O inimigo só escolhe entre os que servem **agora**. Longe demais de todos? Ele anda.
- **`irandom(n)`** sorteia um inteiro de 0 a n. Com 2 ataques válidos, sorteia 0 ou 1.
- **A mira trava nos últimos 8 frames do windup.** Se ele mirasse até o último frame, o dash nunca tiraria você do golpe. Com a trava, desviar no tempo certo funciona. Isso é o "morte justa" do GDD.
- **`inimigo_golpear`** só marca o player como acertado **se o dano entrou**. Se você estava nos iframes, o golpe continua "procurando" até o ativo acabar. Esquivar cedo demais não salva.
- **`espera_entre`**: pausa depois de cada ataque, para não virar metralhadora.
- **`inimigo_pode_interromper`**: acertar um inimigo no meio do ativo não cancela o golpe dele. Trocação tem risco.

## Passo 3 — O dano no inimigo (10 min)

**scr_combate** (substitua a função `inimigo_dano`)
<!-- src: scripts/scr_combate.gml #inimigo_dano -->
```gml
/// Aplica dano num inimigo.
function inimigo_dano(_inst, _dano) {
    with (_inst) {
        if (estado != INI.MORTE) {
            hp -= _dano;
            flash = 6;
            ultimo_dano = _dano;
            if (hp <= 0) {
                hp = 0;
                inimigo_morrer();
            } else if (pode_hitstun && inimigo_pode_interromper()) {
                inimigo_trocar(INI.HITSTUN);
            }
        }
    }
}
```

## Passo 4 — O objeto pai (30 min)

Crie o objeto **`obj_inimigo_pai`**, **sem sprite** (ele nunca é colocado na room; só os filhos). Eventos: Create, Step, Draw.

**obj_inimigo_pai → Create** (arquivo inteiro)
<!-- src: objects/obj_inimigo_pai/Create_0.gml -->
```gml
// Valores padrão de todo inimigo.
// Cada filho chama event_inherited() e depois muda o que precisar.
hp_max = 50;
hp = hp_max;
vel = 1;
raio = 8;            // tamanho do corpo para golpes
almas = 10;          // quanto dá ao morrer
aggro = 100;         // distância em que percebe o player
desiste = 250;       // distância do ponto inicial em que desiste e volta
dist_parar = 18;     // para de andar a esta distância do player
espera_entre = 30;   // frames de pausa entre ataques
pode_hitstun = true; // golpes interrompem?
acordado = true;     // o chefe começa dormindo (dia 14)
ataques = [];        // lista de ataques (ataque_novo)

// Estado
estado = INI.IDLE;
estado_timer = 0;
ataque = undefined;
ataque_dir = 0;
acertados = [];
espera = 0;
flash = 0;
ultimo_dano = 0;
lado = 1;
inicio_x = x;
inicio_y = y;
depth = -y;
```

**obj_inimigo_pai → Step** (arquivo inteiro)
<!-- src: objects/obj_inimigo_pai/Step_0.gml -->
```gml
if (jogo_congelado()) exit;

estado_timer += 1;
if (flash > 0) {
    flash -= 1;
}

switch (estado) {
    case INI.IDLE:      inimigo_estado_idle();      break;
    case INI.PERSEGUIR: inimigo_estado_perseguir(); break;
    case INI.VOLTAR:    inimigo_estado_voltar();    break;
    case INI.ATAQUE:    inimigo_estado_ataque();    break;
    case INI.HITSTUN:   inimigo_estado_hitstun();   break;
    case INI.MORTE:     inimigo_estado_morte();     break;
}

depth = -y;
```

**obj_inimigo_pai → Draw** (arquivo inteiro)
<!-- src: objects/obj_inimigo_pai/Draw_0.gml -->
```gml
// Desenho normal, ou todo branco se acabou de apanhar.
if (flash > 0) gpu_set_fog(true, c_white, 1, 0);
draw_sprite_ext(sprite_index, image_index, x, y, lado, 1, 0, c_white, 1);
if (flash > 0) gpu_set_fog(false, c_white, 0, 1);

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

O aviso desenha o sprite **de novo, por cima**, colorido e meio transparente (alpha 0,6), nos 8 primeiros frames do windup.

## Passo 5 — O boneco vira filho (10 min)

1. Abra o `obj_boneco`, clique em **Parent** e escolha **`obj_inimigo_pai`**.
2. **Apague os eventos Step e Draw do boneco** (botão direito no evento → Delete Event). Agora ele usa os do pai.
3. Troque o Create:

**obj_boneco → Create** (arquivo inteiro)
<!-- src: objects/obj_boneco/Create_0.gml -->
```gml
event_inherited();   // roda o Create do pai primeiro

hp_max = 99999;
hp = hp_max;
raio = 8;
vel = 0;             // não anda
aggro = 0;           // não persegue
ataques = [];        // não ataca
```

**`event_inherited()`** roda o Create do pai. Sem essa linha, as variáveis do pai (`estado`, `flash`, `inicio_x`…) nunca seriam criadas, e o Step herdado quebraria. **Todo filho começa o Create com `event_inherited()`.**

Repare no `hp = hp_max` repetido: o pai fez `hp = 50` (o `hp_max` dele). Mudando `hp_max` no filho, tem que ajustar `hp` de novo.

4. Os golpes e tiros do player agora miram em **qualquer inimigo**, não só no boneco:

**scr_player**, na função `player_estado_ataque` (troque a linha do `golpe_setor` por esta)
<!-- src: scripts/scr_player.gml @troca: var _novos = golpe_setor(x, y, ataque_dir, golpe.alcance, golpe.arco, obj_boneco, acertados); -->
```gml
        var _novos = golpe_setor(x, y, ataque_dir, golpe.alcance, golpe.arco, obj_inimigo_pai, acertados);
```

**obj_projetil → Step** (troque a linha do `projetil_achar_alvo` com `obj_boneco` por esta)
<!-- src: objects/obj_projetil/Step_0.gml @troca: var _alvo = projetil_achar_alvo(_x0, _y0, x, y, obj_boneco); -->
```gml
    var _alvo = projetil_achar_alvo(_x0, _y0, x, y, obj_inimigo_pai);
```

Como o boneco é filho de `obj_inimigo_pai`, ele continua sendo acertado.

## Passo 6 — O primeiro Aldeão (20 min)

Crie o sprite **`spr_aldeao`**: **12×20**, cor marrom, origem **x 6, y 20**.

Crie o objeto **`obj_aldeao`** com esse sprite e **Parent `obj_inimigo_pai`**. Só o evento Create:

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

// Golpe: windup 24, ativo 5, recovery 18, dano 18, alcance 22, arco 100°, aceita parry
var _golpe = ataque_novo(24, 5, 18, 18, 22, 100, true);
ataques = [_golpe];
```

Coloque um `obj_aldeao` na `rm_teste` em **x 544, y 272**.

---

## Teste do dia

Ligue o F3.

- [ ] Longe do Aldeão, ele fica em `IDLE`. A menos de 100 px, vira `PERSEGUIR` e vem.
- [ ] Perto, ele para, pisca branco (aviso) e ataca. O setor aparece cinza e depois vermelho.
- [ ] Dá para esquivar do golpe dando dash **depois** do aviso, mais para o fim do windup.
- [ ] Você apanha dele (hitstun, empurrão).
- [ ] Batendo nele: ele pisca, perde vida, é interrompido (`HITSTUN`) e morre com 60 de dano total.
- [ ] Fugindo para longe, ele volta ao ponto laranja.
- [ ] O boneco continua apanhando normalmente.

## Se deu errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| `variable not set: estado` num filho | Faltou `event_inherited()` no Create do filho | Passos 5 e 6. |
| Boneco some ou dá erro no Step | Os eventos Step/Draw antigos do boneco ainda existem | Passo 5, item 2. |
| Aldeão não se mexe | `vel` 0, ou `aggro` pequeno, ou a room não tem ele na camada Instances | Passo 6. |
| Aldeão ataca de longe | `dist_max` grande demais | Ele usa `alcance + 6` por padrão. |
| Aldeão treme parado ao lado do player | `dist_parar` maior que o alcance do ataque | Deixe `dist_parar` menor que o alcance. |
| Impossível esquivar | Esquivou cedo demais (antes do fim do windup) | Espere o aviso passar e esquive perto do fim. |

## Commit

`dia 9: inimigo pai e primeiro Aldeão`
