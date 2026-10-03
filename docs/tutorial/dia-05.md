# Dia 5 — Frame data e ataque

**Quando:** sex 09/10 · **Tempo:** ~3 h

**No fim do dia:** o player ataca com o **Cutelo** (combo de 3 golpes leves + um pesado), cada golpe tem windup, ativo e recovery, e um boneco de treino mostra o dano recebido.

## O que você vai aprender

- **Frame data**: todo golpe tem três fases, contadas em frames.
- **Dados separados do código**: os números das armas moram num script só de dados.
- **Golpe em setor**: acertar quem está perto e dentro de um ângulo.
- **Combo** com buffer.

---

## Frame data em 1 minuto

| Fase | O que acontece | Por quê |
|---|---|---|
| **Windup** (preparação) | o personagem levanta a arma; ainda dá pra girar | dá tempo do outro lado reagir |
| **Ativo** | a arma está "cortando": quem estiver no setor toma dano | o momento do acerto |
| **Recovery** (recuperação) | a arma volta; o personagem está vulnerável | é aqui que o inimigo te pune, e você pune ele |

Um golpe leve do Cutelo é: windup **8**, ativo **4**, recovery **11**. Total: 23 frames.

**O golpe é um setor**, como uma fatia de pizza à frente do player: acerta quem estiver a até *alcance* pixels **e** dentro de *arco* graus da direção do golpe.

---

## Passo 1 — Os dados das armas (20 min)

Crie o script **`scr_dados`**:

**scr_dados** (arquivo inteiro)
<!-- src: scripts/scr_dados.gml -->
```gml
// Dados do jogo. Números do GDD, seção 7.
// Balancear = mudar número aqui, sem mexer no resto do código.

function dados_armas() {
    // Um golpe: windup, ativo e recovery em frames;
    // alcance e avanço em pixels; arco em graus.
    var _cutelo_leve = {
        windup: 8, ativo: 4, recovery: 11,
        dano: 14, stamina: 15,
        alcance: 25, arco: 120, avanco: 5,
        hyper: false
    };
    var _cutelo_pesado = {
        windup: 16, ativo: 5, recovery: 16,
        dano: 28, stamina: 28,
        alcance: 32, arco: 60, avanco: 10,
        hyper: false
    };

    global.armas = {
        cutelo: {
            nome: "Cutelo serrado",
            esc_for: 0.6,
            esc_des: 0.6,
            leves: [_cutelo_leve, _cutelo_leve, _cutelo_leve],
            pesado: _cutelo_pesado
        }
    };
}
```

- Cada golpe é um struct. A arma é um struct que tem uma **lista** (`leves`) de golpes do combo e um golpe `pesado`.
- **`leves: [_cutelo_leve, _cutelo_leve, _cutelo_leve]`**: o combo tem 3 golpes, e os três usam os mesmos números. A lista guarda 3 referências para o mesmo struct.
- **`avanco`**: quantos pixels o player anda para a frente durante o ativo (o "passo" do golpe).
- **`hyper`**: hyper armor, amanhã.
- **`esc_for` e `esc_des`**: escalas de Força e Destreza, amanhã.
- **`global.armas`** é uma variável global: existe uma vez para o jogo todo.

**obj_game → Create** (adicione antes de `room_goto`)
<!-- src: objects/obj_game/Create_0.gml @antes: room_goto -->
```gml
// --- Dados e equipamento ---
dados_armas();
arma = global.armas.cutelo;   // arma equipada
```

## Passo 2 — Funções de golpe (30 min)

Crie o script **`scr_util`** (funções pequenas usadas em vários lugares):

**scr_util** (arquivo inteiro)
<!-- src: scripts/scr_util.gml -->
```gml
// Funções pequenas usadas em vários lugares.

/// Desenha o contorno de um setor (fatia) — usado no debug dos golpes.
function desenhar_setor(_x, _y, _dir, _alcance, _arco) {
    var _passos = 12;
    var _ini = _dir - _arco / 2;
    var _px = _x + lengthdir_x(_alcance, _ini);
    var _py = _y + lengthdir_y(_alcance, _ini);
    if (_arco < 360) {
        draw_line(_x, _y, _px, _py);
    }
    for (var i = 1; i <= _passos; i++) {
        var _a = _ini + _arco * i / _passos;
        var _nx = _x + lengthdir_x(_alcance, _a);
        var _ny = _y + lengthdir_y(_alcance, _a);
        draw_line(_px, _py, _nx, _ny);
        _px = _nx;
        _py = _ny;
    }
    if (_arco < 360) {
        draw_line(_x, _y, _px, _py);
    }
}
```

O contorno do arco é desenhado com 12 pedacinhos de linha reta. O `for` repete o bloco com `i` valendo 1, 2… até 12.

**scr_combate** (novas funções, adicione no fim)
<!-- src: scripts/scr_combate.gml #golpe_setor -->
```gml
/// Procura alvos do tipo _obj dentro de um setor (fatia).
/// Devolve um array com os que estão dentro e ainda não estão em _acertados.
function golpe_setor(_x, _y, _dir, _alcance, _arco, _obj, _acertados) {
    var _novos = [];
    with (_obj) {
        if (!array_contains(_acertados, id)) {
            var _dist = point_distance(_x, _y, x, y);
            var _ang = point_direction(_x, _y, x, y);
            // angle_difference dá a diferença entre dois ângulos, de -180 a 180.
            var _no_arco = (_arco >= 360) || (abs(angle_difference(_dir, _ang)) <= _arco / 2);
            if (_dist <= _alcance + raio && _no_arco) {
                array_push(_novos, id);
            }
        }
    }
    return _novos;
}
```

<!-- src: scripts/scr_combate.gml #inimigo_dano -->
```gml
/// Aplica dano num inimigo (por enquanto, só o boneco).
function inimigo_dano(_inst, _dano) {
    with (_inst) {
        hp -= _dano;
        flash = 6;
        ultimo_dano = _dano;
    }
}
```

Como o `golpe_setor` funciona:

- **`with (_obj)`** roda o bloco uma vez para **cada** instância daquele objeto. Dentro dele, `x`, `y`, `id` e `raio` são do alvo da vez.
- **`id`** é o identificador único de cada instância.
- **`array_contains(lista, valor)`**: esse alvo já foi acertado por este golpe? Então pula. É o que impede um golpe de 4 frames ativos de acertar 4 vezes.
- **O ângulo**: `angle_difference(direção_do_golpe, ângulo_até_o_alvo)` diz quantos graus o alvo está fora do centro. Se for até metade do arco (60° num arco de 120°), está dentro.
- **`_alcance + raio`**: o alvo tem um corpo. Somando o raio dele, o golpe acerta quando encosta na borda, não só quando chega no centro.
- **`||`** (ou): arco de 360° acerta em volta, sem olhar ângulo.

## Passo 3 — Variáveis de ataque (5 min)

**obj_player → Create** (adicione no fim)
<!-- src: objects/obj_player/Create_0.gml @fim -->
```gml
// --- Ataque ---
golpe = undefined;      // struct do golpe atual (vem do scr_dados)
golpe_pesado = false;
combo_i = 0;            // posição no combo (0 = primeiro golpe)
ataque_dir = 0;         // direção do golpe (trava no ativo)
acertados = [];         // quem este golpe já acertou
raio = 6;               // tamanho do corpo, para os golpes inimigos
```

`undefined` quer dizer "ainda não tem valor".

## Passo 4 — O estado de ataque (60 min)

**scr_player** (substitua a função `player_estado_livre`)
<!-- src: scripts/scr_player.gml #player_estado_livre -->
```gml
function player_estado_livre() {
    player_mover(1);
    if (player_tentar_esquivar()) return;
    if (player_tentar_atacar()) return;
}
```

`return` sai da função na hora. "Se esquivou, não tenta atacar no mesmo frame."

**scr_player** (novas funções, adicione no fim)
<!-- src: scripts/scr_player.gml #player_tentar_atacar -->
```gml
/// Começa um golpe leve ou pesado se o botão está no buffer e tem stamina.
function player_tentar_atacar() {
    var _arma = obj_game.arma;
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

<!-- src: scripts/scr_player.gml #player_comecar_golpe -->
```gml
function player_comecar_golpe(_golpe, _pesado) {
    golpe = _golpe;
    golpe_pesado = _pesado;
    acertados = [];                 // golpe novo: ninguém acertado ainda
    ataque_dir = obj_game.mira_dir;
    player_gastar_stamina(golpe.stamina);
    player_trocar(PL.ATAQUE);
}
```

<!-- src: scripts/scr_player.gml #player_estado_ataque -->
```gml
function player_estado_ataque() {
    var _fim_windup = golpe.windup;
    var _fim_ativo  = golpe.windup + golpe.ativo;
    var _fim_total  = _fim_ativo + golpe.recovery;

    if (estado_timer <= _fim_windup) {
        // Windup: ainda gira para a mira.
        ataque_dir = obj_game.mira_dir;
    } else if (estado_timer <= _fim_ativo) {
        // Ativo: avança um pouco e acerta quem estiver no setor.
        var _passo = golpe.avanco / golpe.ativo;
        move_and_collide(lengthdir_x(_passo, ataque_dir), lengthdir_y(_passo, ataque_dir), obj_parede);

        var _novos = golpe_setor(x, y, ataque_dir, golpe.alcance, golpe.arco, obj_boneco, acertados);
        for (var i = 0; i < array_length(_novos); i++) {
            array_push(acertados, _novos[i]);
            inimigo_dano(_novos[i], golpe.dano);
        }
    } else {
        // Recovery: um leve apertado aqui continua o combo.
        if (!golpe_pesado && player_tentar_atacar()) return;
    }

    if (estado_timer >= _fim_total) {
        player_trocar(PL.LIVRE);
    }
}
```

Lendo o estado de ataque:

- **As três fases saem do timer.** Com windup 8 e ativo 4: frames 1–8 são windup, 9–12 ativo, 13–23 recovery.
- **No windup**, a direção segue o mouse. Do ativo em diante, trava: não dá pra girar o golpe no meio do corte.
- **No ativo**, o avanço é dividido pelos frames ativos (5 px em 4 frames = 1,25 px por frame). E a cada frame procura alvos novos.
- **O `for`** passa por cada alvo novo: marca como acertado e aplica o dano.
- **No recovery**, `player_tentar_atacar()` encadeia o próximo golpe. O combo usa o **buffer**: se você clicou durante o ativo, o clique ainda vale quando o recovery começa.
- **`combo_i = (combo_i + 1) mod 3`**: 0 → 1 → 2 → 0. Depois do último golpe, volta ao primeiro.
- **O pesado não encadeia**: o `!golpe_pesado` bloqueia. Ele sempre termina o combo.

## Passo 5 — Step e debug (15 min)

**obj_player → Step** (troque só a parte do `switch` por esta)
<!-- src: objects/obj_player/Step_0.gml @troca: case PL.ESQUIVA: player_estado_esquiva(); break; -->
```gml
    case PL.ESQUIVA: player_estado_esquiva(); break;
    case PL.ATAQUE:  player_estado_ataque();  break;
```

Ou seja: logo embaixo da linha do `case PL.ESQUIVA`, adicione a linha do `case PL.ATAQUE`.

**obj_player → Draw** (adicione dentro do `if (obj_game.debug)`, logo antes da linha `draw_healthbar(x - 10, y - 28, ...`)
<!-- src: objects/obj_player/Draw_0.gml @antes: draw_healthbar(x - 10, y - 28 -->
```gml
    // Setor do golpe: cinza no windup/recovery, vermelho no ativo
    if (estado == PL.ATAQUE) {
        if (estado_timer > golpe.windup && estado_timer <= golpe.windup + golpe.ativo) {
            draw_set_colour(c_red);
        } else {
            draw_set_colour(c_gray);
        }
        desenhar_setor(x, y, ataque_dir, golpe.alcance, golpe.arco);
        draw_set_colour(c_lime);
    }
```

## Passo 6 — Boneco de treino (30 min)

Crie o sprite **`spr_boneco`**: **16×24**, cor bege, origem **x 8, y 24**.

Crie o objeto **`obj_boneco`** com esse sprite. Eventos: Create, Step, Draw.

**obj_boneco → Create** (arquivo inteiro)
<!-- src: objects/obj_boneco/Create_0.gml -->
```gml
hp = 9999;
raio = 8;           // tamanho do corpo para os golpes
flash = 0;          // frames piscando depois de apanhar
ultimo_dano = 0;
depth = -y;
```

**obj_boneco → Step** (arquivo inteiro)
<!-- src: objects/obj_boneco/Step_0.gml -->
```gml
if (flash > 0) {
    flash -= 1;
}
```

**obj_boneco → Draw** (arquivo inteiro)
<!-- src: objects/obj_boneco/Draw_0.gml -->
```gml
var _cor = (flash > 0) ? c_red : c_white;
draw_sprite_ext(sprite_index, 0, x, y, 1, 1, 0, _cor, 1);

if (ultimo_dano > 0) {
    draw_set_halign(fa_center);
    draw_text(x, y - 40, string(ultimo_dano));
    draw_set_halign(fa_left);
}
```

**`string(numero)`** transforma número em texto. O `draw_text` só aceita texto.

Coloque um `obj_boneco` na `rm_teste` em **x 304, y 224**.

---

## Arte do dia

Com a arte pronta, faça agora a parte **Dia 5** do [Apêndice A](apendice-a-arte.md).

## Teste do dia

- [ ] Clique esquerdo: golpe; F3 mostra o setor cinza (windup) → vermelho (ativo) → cinza (recovery).
- [ ] Três cliques no ritmo: combo de 3 golpes; o player dá um passinho em cada.
- [ ] Clique direito: golpe pesado, mais lento e com setor mais estreito e longo.
- [ ] O boneco pisca vermelho e mostra 14 (leve) ou 28 (pesado).
- [ ] Cada golpe acerta uma vez só.
- [ ] Boneco fora do setor não toma dano.
- [ ] Atacar gasta stamina; sem stamina, não ataca.
- [ ] Dá para esquivar no fim de um ataque apertando Espaço durante ele (o buffer guarda).

## Se deu errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| Um golpe acerta várias vezes | `acertados = []` não está no `player_comecar_golpe`, ou falta o `array_push` | Passo 4. |
| Nunca acerta | Boneco sem `raio`, ou o alcance está sendo comparado errado | Passos 2 e 6. |
| Acerta atrás do player | Faltou o `abs(...)` no `angle_difference` | Passo 2. |
| `variable not set: golpe` no Draw | O setor é desenhado fora do `if (estado == PL.ATAQUE)` | Passo 5. |
| `unknown function dados_armas` | Nome da função diferente no `scr_dados` | Passo 1. |
| Combo não passa do primeiro golpe | Faltou o `mod`, ou o `if (estado == PL.ATAQUE && !golpe_pesado)` | Passo 4. |

## Commit

`dia 5: ataque e frame data`
