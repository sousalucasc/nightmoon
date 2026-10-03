# Dia 4 — Buffer, stamina e tomar dano

**Quando:** qui 08/10 · **Tempo:** ~3 h

**No fim do dia:** a esquiva gasta stamina, dá para encadear esquivas apertando um pouco antes da anterior acabar, e uma armadilha causa dano, empurra e pode matar. Morrer reinicia a room.

## O que você vai aprender

- **Buffer de input**: o jogo "lembra" de um botão apertado cedo demais.
- **Stamina** com atraso para regenerar.
- **`with`**: rodar código "dentro" de outra instância.
- **Hitstun** e **knockback** (empurrão).

---

## Passo 1 — Buffer de input (30 min)

**O problema:** o dash dura 22 frames. Se você aperta Espaço no frame 20, o `aperta_esquiva` é verdadeiro só naquele frame, e o player ainda está no dash, então nada acontece. Parece que o jogo "comeu" o botão.

**A solução:** quando o botão desce, guardamos o número 8. A cada frame ele diminui 1. Qualquer estado que queira a esquiva pergunta "o buffer está acima de 0?". Assim, um aperto vale por 8 frames.

**scr_config** (adicione depois da linha `#macro ALTURA_BASE 180`)
<!-- src: scripts/scr_config.gml @depois: #macro ALTURA_BASE 180 -->
```gml
#macro BUFFER_FRAMES 8
```

**obj_game → Create** (adicione antes de `room_goto`)
<!-- src: objects/obj_game/Create_0.gml @antes: room_goto -->
```gml
// Buffer: por quantos frames ainda vale um botão apertado
buf_esquiva = 0;
buf_leve = 0;
buf_pesado = 0;
buf_tiro = 0;
```

**obj_game → Begin Step** (adicione no fim)
<!-- src: objects/obj_game/Step_1.gml @fim -->
```gml
// Buffer: lembra por alguns frames que o botão foi apertado.
// Forma: (condição) ? valor_se_sim : valor_se_não
buf_esquiva = aperta_esquiva ? BUFFER_FRAMES : max(0, buf_esquiva - 1);
buf_leve    = aperta_leve    ? BUFFER_FRAMES : max(0, buf_leve - 1);
buf_pesado  = aperta_pesado  ? BUFFER_FRAMES : max(0, buf_pesado - 1);
buf_tiro    = aperta_tiro    ? BUFFER_FRAMES : max(0, buf_tiro - 1);
```

O `? :` é um **if curto**. Leia a primeira linha assim: "se apertou a esquiva, o buffer vira 8; senão, diminui 1 (sem passar de 0)".

## Passo 2 — Variáveis de vida e stamina (10 min)

**obj_player → Create** (adicione no fim)
<!-- src: objects/obj_player/Create_0.gml @fim -->
```gml
// --- Vida e stamina ---
hp_max = 100;
hp = hp_max;
st_max = 100;
st = st_max;
st_espera = 0;      // frames até a stamina voltar a encher
invul_timer = 0;    // invulnerabilidade depois de tomar dano
kb_dir = 0;         // empurrão (knockback): direção
kb_vel = 0;         //   velocidade atual
kb_desacel = 0;     //   quanto cai por frame
```

## Passo 3 — Esquiva com buffer e stamina (30 min)

No `scr_player`, **substitua a função `player_estado_livre`**:

**scr_player** (substitua a função `player_estado_livre`)
<!-- src: scripts/scr_player.gml #player_estado_livre -->
```gml
function player_estado_livre() {
    player_mover(1);
    player_tentar_esquivar();
}
```

**scr_player** (nova função, adicione no fim)
<!-- src: scripts/scr_player.gml #player_tentar_esquivar -->
```gml
/// Começa uma esquiva se o botão foi apertado há pouco e ainda tem stamina.
/// Devolve true se começou.
function player_tentar_esquivar() {
    if (obj_game.buf_esquiva > 0 && st > 0) {
        obj_game.buf_esquiva = 0;   // gasta o buffer: um aperto = uma esquiva
        player_comecar_esquiva();
        return true;
    }
    return false;
}
```

**scr_player** (substitua a função `player_comecar_esquiva`)
<!-- src: scripts/scr_player.gml #player_comecar_esquiva -->
```gml
function player_comecar_esquiva() {
    if (obj_game.mover_x != 0 || obj_game.mover_y != 0) {
        // Andando: dash na direção do movimento.
        esq = dash;
        esq_dir = point_direction(0, 0, obj_game.mover_x, obj_game.mover_y);
    } else {
        // Parado: backstep, para longe da mira.
        esq = backstep;
        esq_dir = obj_game.mira_dir + 180;
    }
    // Uma velocidade que cai até zero percorre: velocidade inicial x duração / 2.
    // Então, para percorrer a distância certa: inicial = 2 x distância / duração.
    esq_vel = 2 * esq.distancia / esq.duracao;
    esq_desacel = esq_vel / esq.duracao;
    player_gastar_stamina(esq.custo);
    player_trocar(PL.ESQUIVA);
}
```

**scr_player** (novas funções, adicione no fim)
<!-- src: scripts/scr_player.gml #player_gastar_stamina -->
```gml
function player_gastar_stamina(_custo) {
    st = max(0, st - _custo);
    st_espera = 30;   // meio segundo sem regenerar
}
```

<!-- src: scripts/scr_player.gml #player_estado_hitstun -->
```gml
function player_estado_hitstun() {
    // Empurrão que desacelera, igual à esquiva.
    move_and_collide(lengthdir_x(kb_vel, kb_dir), lengthdir_y(kb_vel, kb_dir), obj_parede);
    kb_vel = max(0, kb_vel - kb_desacel);
    if (estado_timer >= 18) {
        invul_timer = 10;
        player_trocar(PL.LIVRE);
    }
}
```

<!-- src: scripts/scr_player.gml #player_estado_morte -->
```gml
function player_estado_morte() {
    if (estado_timer >= 60) {
        room_restart();
    }
}
```

- **`player_tentar_esquivar` devolve `true` ou `false`.** Amanhã o ataque vai usar isso: "se esquivou, não faz mais nada neste frame".
- **`obj_game.buf_esquiva = 0`** "gasta" o aperto. Sem isso, um só aperto faria duas esquivas seguidas.
- **`st > 0`**: dá para esquivar com 1 de stamina, e ela vai a 0 (nunca negativa). Com 0, não esquiva.
- **Hitstun** = o momento em que você apanhou e não controla o personagem. Depois dele vêm 10 frames invulneráveis, para dois golpes no mesmo instante não te matarem.
- **`room_restart()`** recomeça a room do zero. É temporário: no dia 16, morrer vai te levar para a lanterna.

## Passo 4 — Função de dano (20 min)

Crie o script **`scr_combate`**:

**scr_combate** (arquivo inteiro)
<!-- src: scripts/scr_combate.gml -->
```gml
// Funções de combate: quem acerta quem, e quanto.

/// Aplica dano no player. _de_x, _de_y: de onde veio o golpe (para o empurrão).
/// Devolve true se o dano entrou.
function player_dano(_dano, _de_x, _de_y) {
    var _entrou = false;
    with (obj_player) {
        if (!invulneravel && invul_timer <= 0 && estado != PL.MORTE) {
            _entrou = true;
            hp -= _dano;
            kb_dir = point_direction(_de_x, _de_y, x, y);  // para longe da fonte
            kb_vel = 2 * 10 / 18;                          // 10 px em 18 frames
            kb_desacel = kb_vel / 18;
            if (hp <= 0) {
                hp = 0;
                player_trocar(PL.MORTE);
            } else {
                player_trocar(PL.HITSTUN);
            }
        }
    }
    return _entrou;
}
```

**`with (obj_player) { ... }`** roda o bloco **como se fosse o player**: dentro dele, `hp`, `x`, `estado` são as variáveis do player, mesmo que quem chamou a função seja a armadilha. Variáveis `var` (como `_entrou` e `_dano`) continuam visíveis dentro do `with`.

## Passo 5 — Armadilha de teste (30 min)

Crie o objeto **`obj_armadilha`**, **sem sprite**. Eventos: Create, Step, Draw.

**obj_armadilha → Create** (arquivo inteiro)
<!-- src: objects/obj_armadilha/Create_0.gml -->
```gml
ciclo = 0;      // conta de 0 a 95 e recomeça
raio = 20;
dano = 20;
ativa = false;
```

**obj_armadilha → Step** (arquivo inteiro)
<!-- src: objects/obj_armadilha/Step_0.gml -->
```gml
// 30 frames de aviso, 6 ativa, 60 desligada (96 no total).
ciclo = (ciclo + 1) mod 96;
ativa = (ciclo >= 30 && ciclo < 36);

if (ativa && instance_exists(obj_player)) {
    if (point_distance(x, y, obj_player.x, obj_player.y) <= raio) {
        player_dano(dano, x, y);
    }
}
```

**obj_armadilha → Draw** (arquivo inteiro)
<!-- src: objects/obj_armadilha/Draw_0.gml -->
```gml
if (ativa) {
    draw_set_colour(c_red);
    draw_circle(x, y, raio, false);          // cheio: machuca
} else if (ciclo < 30 && (ciclo div 4) mod 2 == 0) {
    draw_set_colour(c_yellow);
    draw_circle(x, y, raio, true);           // contorno piscando: aviso
} else {
    draw_set_colour(c_dkgray);
    draw_circle(x, y, raio, true);
}
draw_set_colour(c_white);
```

- **`mod`** é o resto da divisão. `(ciclo + 1) mod 96` conta 0, 1, 2… 95, 0, 1… para sempre.
- **`div`** é a divisão inteira: `ciclo div 4` sobe 1 a cada 4 frames. `mod 2` alterna entre 0 e 1. Juntos, fazem piscar a cada 4 frames.
- **`draw_circle(x, y, raio, contorno)`**: `true` desenha só a borda, `false` pinta cheio.

Coloque uma `obj_armadilha` na `rm_teste` em **x 496, y 112** (área livre à direita).

## Passo 6 — Step e Draw do player (30 min)

**obj_player → Step** (arquivo inteiro)
<!-- src: objects/obj_player/Step_0.gml -->
```gml
estado_timer += 1;

switch (estado) {
    case PL.LIVRE:   player_estado_livre();   break;
    case PL.ESQUIVA: player_estado_esquiva(); break;
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

// O corpo vira para o lado do mouse.
if (obj_game.mira_dir > 90 && obj_game.mira_dir < 270) {
    lado = -1;
} else {
    lado = 1;
}

// Quem está mais embaixo na tela é desenhado por cima.
depth = -y;
```

O `switch` agora está compacto (`case X: função(); break;` numa linha): é a mesma coisa de antes, só mais curto.

**obj_player → Draw** (arquivo inteiro)
<!-- src: objects/obj_player/Draw_0.gml -->
```gml
// Com o debug ligado, o player fica ciano enquanto está invulnerável.
var _cor = c_white;
if (obj_game.debug && (invulneravel || invul_timer > 0)) {
    _cor = c_aqua;
}
// lado = -1 espelha o desenho na horizontal.
draw_sprite_ext(sprite_index, image_index, x, y, lado, 1, 0, _cor, 1);

if (obj_game.debug) {
    draw_set_colour(c_lime);
    draw_rectangle(bbox_left, bbox_top, bbox_right, bbox_bottom, true);
    draw_line(x, y, mouse_x, mouse_y);
    // Nome do estado em cima da cabeça
    draw_set_halign(fa_center);
    draw_text(x, y - 36, obj_game.nomes_pl[estado]);
    draw_set_halign(fa_left);
    // Barras: vida (vermelho) e stamina (amarelo)
    draw_healthbar(x - 10, y - 28, x + 10, y - 27, hp / hp_max * 100, c_black, c_red, c_red, 0, true, false);
    draw_healthbar(x - 10, y - 25, x + 10, y - 24, st / st_max * 100, c_black, c_yellow, c_yellow, 0, true, false);
    draw_set_colour(c_white);
}
```

**`draw_healthbar`** desenha uma barra pronta. O quinto valor é de 0 a 100, por isso `hp / hp_max * 100`.

---

## Teste do dia

- [ ] Esquivar gasta stamina (F3 mostra a barra amarela caindo) e ela volta a encher meio segundo depois.
- [ ] Sem stamina, Espaço não faz nada.
- [ ] Apertar Espaço um pouco antes do dash acabar faz outro dash em seguida.
- [ ] Parado dentro da armadilha quando ela fica vermelha: toma dano, é empurrado, fica em `HITSTUN`.
- [ ] Dando dash através da armadilha vermelha (no tempo certo): nenhum dano.
- [ ] Tomando dano 5 vezes: `MORTE`, e a room recomeça depois de 1 segundo.

## Se deu errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| Um Espaço faz duas esquivas | Faltou `obj_game.buf_esquiva = 0` | Passo 3. |
| Armadilha mata na hora | Faltou o `invul_timer` (o dano entra todo frame) | Passos 3 e 6. |
| `unknown function player_dano` | Script `scr_combate` não criado ou nome diferente | Passo 4. |
| Dano entra mesmo no dash | O dash passou pela armadilha fora dos iframes (frames 2–13) | Treine o tempo; com F3, o player fica ciano nos iframes. |
| Player some ao morrer e nada acontece | Faltou `case PL.MORTE` no Step | Passo 6. |

## Commit

`dia 4: buffer, stamina, dano`
