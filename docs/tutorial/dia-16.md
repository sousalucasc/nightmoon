# Dia 16 — Lanterna, morte e almas no chão

**Quando:** ter 20/10 · **Tempo:** ~3 h

**No fim do dia:** o loop souls existe. **F** perto da lanterna: descansa, enche vida, frascos e balas, e os inimigos renascem. **Morrer**: tela escurece, você volta na última lanterna, e suas almas ficam numa mancha de sangue onde você morreu. Pegar a mancha devolve as almas; morrer de novo antes disso apaga elas. Inimigo morto continua morto até você descansar ou morrer.

## O que você vai aprender

- Separar **o que é da partida** (almas, checkpoint) de **o que é do jogo** (câmera, input).
- **Fade** entre rooms.
- Guardar dados do player entre rooms (**Room End**).
- Lembrar quais inimigos morreram, usando uma **chave** por inimigo.

---

## Passo 1 — Funções da partida (30 min)

Crie o script **`scr_jogo`**:

**scr_jogo** (arquivo inteiro)
<!-- src: scripts/scr_jogo.gml -->
```gml
// Partida: começar, morrer, descansar, trocar de room.

/// Zera tudo que é da partida. Chamada ao abrir o jogo
/// (e no "Começar" do título, no dia 19).
function jogo_novo() {
    with (obj_game) {
        arma = global.armas.cutelo;
        pistola = global.pistolas.pistola;
        atr_forca = 0;
        atr_destreza = 0;
        almas = 0;
        chefe_morto = false;
        lanterna_sala = rm_teste;   // onde volta ao morrer antes de descansar
        lanterna_x = -1;            // -1: usa o lugar do player na room
        lanterna_y = -1;
        chegar_na_lanterna = false;
        mancha = { ativa: false, sala: -1, x: 0, y: 0, almas: 0 };
        mortos = [];                // inimigos mortos desde o último descanso
        mortes = 0;
        tempo = 0;                  // frames jogados
        player_hp = -1;             // -1 = cheio
        player_frascos = -1;
        player_balas = -1;
    }
}

/// Troca de room com fade (escurece, troca, clareia).
function trocar_room(_destino) {
    with (obj_game) {
        if (!fade_indo) {
            fade_indo = true;
            fade_destino = _destino;
        }
    }
}

/// Descansar numa lanterna: enche tudo, marca o checkpoint e renasce os inimigos.
function lanterna_descansar(_lanterna) {
    with (obj_player) {
        hp = hp_max;
        frascos = frascos_max;
        balas = balas_max;
    }
    with (obj_game) {
        lanterna_sala = room;
        lanterna_x = _lanterna.x;
        lanterna_y = _lanterna.y + 12;
        mortos = [];
        chegar_na_lanterna = true;
    }
    trocar_room(room);   // recarrega a room: os inimigos voltam
}

/// O player morreu: as almas ficam no chão e ele volta na lanterna.
function jogo_player_morreu(_x, _y) {
    with (obj_game) {
        mortes += 1;
        // A mancha nova substitui a antiga: quem morre duas vezes perde as almas.
        mancha = { ativa: almas > 0, sala: room, x: _x, y: _y, almas: almas };
        almas = 0;
        mortos = [];
        player_hp = -1;
        player_frascos = -1;
        player_balas = -1;
        chegar_na_lanterna = true;
    }
    trocar_room(obj_game.lanterna_sala);
}
```

- **`sala`** e não `room`: `room` é uma variável do próprio GameMaker (a room atual). Não dá para usar esse nome dentro do struct.
- **`mancha = { ... }`** cria um struct novo, jogando fora o anterior. É isso que faz a mancha antiga sumir.
- **Descansar recarrega a própria room** (`trocar_room(room)`). Rooms não são persistentes: recarregar recria todos os inimigos.

## Passo 2 — O obj_game reorganizado (30 min)

Hoje o Create do `obj_game` muda bastante: o que é da partida sai dele e vai para `jogo_novo()`. **Apague tudo e digite:**

**obj_game → Create** (arquivo inteiro)
<!-- src: objects/obj_game/Create_0.gml -->
```gml
// obj_game: controla o jogo inteiro.
// Nasce na rm_init e é persistente: continua existindo quando a room muda.

// --- Resolução ---
// O jogo é desenhado numa tela pequena (320x180) e ampliado na janela.
surface_resize(application_surface, LARGURA_BASE, ALTURA_BASE);
display_set_gui_size(LARGURA_BASE, ALTURA_BASE);
camera = camera_create_view(0, 0, LARGURA_BASE, ALTURA_BASE);
cam_x = 0;
cam_y = 0;
depth = -10000;     // o Draw GUI do obj_game fica por cima de todos

// --- Input ---
// Preenchido no Begin Step. Nenhum outro objeto lê teclado ou mouse.
mover_x = 0;
mover_y = 0;
mira_dir = 0;
aperta_esquiva = false;
aperta_leve = false;
aperta_pesado = false;
aperta_tiro = false;
aperta_cura = false;
aperta_interagir = false;
// Buffer: por quantos frames ainda vale um botão apertado
buf_esquiva = 0;
buf_leve = 0;
buf_pesado = 0;
buf_tiro = 0;

// --- Debug ---
debug = false;
// Nomes dos estados, na mesma ordem dos enums (para o debug)
nomes_pl = ["LIVRE", "ESQUIVA", "ATAQUE", "TIRO", "CURA", "HITSTUN", "VISCERAL", "MORTE"];
nomes_ini = ["IDLE", "PERSEGUIR", "VOLTAR", "ATAQUE", "HITSTUN", "STAGGER", "VISCERAL", "CAIDO", "TRANSFORMA", "MORTE"];

// --- Sensação de impacto ---
hitstop = 0;
tremor = 0;

// --- Mensagem no meio da tela ---
texto = "";
texto_timer = 0;

// --- Fade entre rooms ---
fade = 0;             // 0 = transparente, 1 = tela preta
fade_indo = false;
fade_destino = -1;

// --- Dados ---
dados_armas();
dados_pistolas();
contador_tiros = 0;

// --- Partida ---
jogo_novo();

room_goto(rm_teste);
```

Adicione o evento **Step** (o normal) no `obj_game`:

**obj_game → Step** (arquivo inteiro)
<!-- src: objects/obj_game/Step_0.gml -->
```gml
// Fade: escurece, troca de room e clareia.
if (fade_indo) {
    fade = min(1, fade + 0.08);
    if (fade >= 1) {
        fade_indo = false;
        room_goto(fade_destino);
    }
} else if (fade > 0) {
    fade = max(0, fade - 0.08);
}

// Tempo de jogo (em frames), só enquanto joga.
if (instance_exists(obj_player) && !jogo_congelado()) {
    tempo += 1;
}
```

**obj_game → Room Start** (arquivo inteiro)
<!-- src: objects/obj_game/Other_4.gml -->
```gml
// Room Start: roda sempre que uma room começa.
// Toda room usa a mesma câmera de 320x180.
view_enabled = true;
view_visible[0] = true;
view_camera[0] = camera;
view_xport[0] = 0;
view_yport[0] = 0;
view_wport[0] = LARGURA_BASE;
view_hport[0] = ALTURA_BASE;

// Voltando de uma morte ou de um descanso: o player aparece na lanterna.
if (chegar_na_lanterna && instance_exists(obj_player)) {
    chegar_na_lanterna = false;
    if (lanterna_x >= 0) {
        obj_player.x = lanterna_x;
        obj_player.y = lanterna_y;
    }
}

// A mancha de almas, se ela ficou nesta room.
if (mancha.ativa && mancha.sala == room) {
    instance_create_depth(mancha.x, mancha.y, 0, obj_mancha);
}

// A câmera já começa em cima do player.
if (instance_exists(obj_player)) {
    cam_x = obj_player.x - LARGURA_BASE / 2;
    cam_y = obj_player.y - ALTURA_BASE / 2;
}
```

**obj_game → Draw GUI** (adicione no fim)
<!-- src: objects/obj_game/Draw_64.gml @fim -->
```gml
// Fade: tela preta por cima de tudo.
if (fade > 0) {
    draw_set_alpha(fade);
    draw_set_colour(c_black);
    draw_rectangle(0, 0, LARGURA_BASE, ALTURA_BASE, false);
    draw_set_alpha(1);
    draw_set_colour(c_white);
}
```

**scr_util** (substitua a função `jogo_congelado`)
<!-- src: scripts/scr_util.gml #jogo_congelado -->
```gml
/// true enquanto o jogo está parado (hitstop, fade; depois, também menus).
function jogo_congelado() {
    return obj_game.hitstop > 0 || obj_game.fade_indo;
}
```

**Por que `room_goto` no fim do fade, e não na hora?** O fade leva ~13 frames para escurecer. Durante esse tempo o jogo fica congelado (ninguém se mexe), e a troca acontece com a tela preta.

## Passo 3 — O player entre rooms (20 min)

**obj_player → Create** (adicione no fim)
<!-- src: objects/obj_player/Create_0.gml @fim -->
```gml
// --- O que o obj_game guardou entre rooms (-1 = cheio) ---
if (obj_game.player_hp >= 0) hp = min(obj_game.player_hp, hp_max);
if (obj_game.player_frascos >= 0) frascos = obj_game.player_frascos;
if (obj_game.player_balas >= 0) balas = obj_game.player_balas;
```

Adicione o evento **Room End** (Other → Room End) no `obj_player`:

**obj_player → Room End** (arquivo inteiro)
<!-- src: objects/obj_player/Other_5.gml -->
```gml
// Saindo da room: guarda vida, frascos e balas para a próxima.
// Morto não guarda: quem morreu volta cheio.
if (estado != PL.MORTE) {
    obj_game.player_hp = hp;
    obj_game.player_frascos = frascos;
    obj_game.player_balas = balas;
}
```

**scr_player** (substitua a função `player_estado_morte`)
<!-- src: scripts/scr_player.gml #player_estado_morte -->
```gml
function player_estado_morte() {
    if (estado_timer == 60) {
        jogo_player_morreu(x, y);
    }
}
```

**Por que o player não é persistente?** Porque cada room tem o seu player colocado no editor, e ele é recriado ao entrar. O que precisa atravessar rooms (vida, frascos, balas) fica guardado no `obj_game`: o Room End salva, o Create carrega.

## Passo 4 — Inimigos que continuam mortos (15 min)

**obj_inimigo_pai → Create** (adicione no fim)
<!-- src: objects/obj_inimigo_pai/Create_0.gml @fim -->
```gml
// Já morto desde o último descanso? Então não aparece.
// A chave é única por inimigo: room + posição onde foi colocado.
chave = room_get_name(room) + "_" + string(x) + "_" + string(y);
if (array_contains(obj_game.mortos, chave)) {
    instance_destroy();
}
```

**scr_inimigo** (substitua a função `inimigo_morrer`)
<!-- src: scripts/scr_inimigo.gml #inimigo_morrer -->
```gml
function inimigo_morrer() {
    obj_game.almas += almas;
    array_push(obj_game.mortos, chave);   // não renasce até descansar
    fx_criar(x, y - 10, spr_fx_sangue, 0, 1);
    if (e_chefe) {
        obj_game.chefe_morto = true;
        mostrar_texto("CAÇA ENCERRADA");
    }
    inimigo_trocar(INI.MORTE);
}
```

**obj_chefe → Create** (adicione no fim)
<!-- src: objects/obj_chefe/Create_0.gml @fim -->
```gml
// O chefe nunca renasce, nem depois de descansar.
if (obj_game.chefe_morto) {
    instance_destroy();
}
```

**Por que `x` e `y` servem de chave?** No Create, o inimigo ainda está exatamente onde você colocou no editor. Dois inimigos nunca estão no mesmo lugar, então `"rm_rua_200_100"` identifica um inimigo só.

## Passo 5 — Lanterna e mancha (40 min)

| Sprite | Tamanho | Cor | Origem |
|---|---|---|---|
| `spr_lanterna` | 8×24 | amarelo | x 4, y 24 |
| `spr_mancha` | 12×6 | vermelho escuro | x 6, y 3 |

Crie o objeto **`obj_lanterna`** (sprite `spr_lanterna`). Eventos: Create, Step, Draw.

**obj_lanterna → Create** (arquivo inteiro)
<!-- src: objects/obj_lanterna/Create_0.gml -->
```gml
depth = -y;
perto = false;
```

**obj_lanterna → Step** (arquivo inteiro)
<!-- src: objects/obj_lanterna/Step_0.gml -->
```gml
if (jogo_congelado() || !instance_exists(obj_player)) exit;

perto = point_distance(x, y, obj_player.x, obj_player.y) < 24;
if (perto && obj_game.aperta_interagir && obj_player.estado == PL.LIVRE) {
    lanterna_descansar(id);
}
```

**obj_lanterna → Draw** (arquivo inteiro)
<!-- src: objects/obj_lanterna/Draw_0.gml -->
```gml
draw_self();
if (perto) {
    draw_set_halign(fa_center);
    draw_text(x, y - 40, "F: descansar");
    draw_set_halign(fa_left);
}
```

Crie o objeto **`obj_mancha`** (sprite `spr_mancha`). Eventos: Step, Draw.

**obj_mancha → Step** (arquivo inteiro)
<!-- src: objects/obj_mancha/Step_0.gml -->
```gml
if (jogo_congelado() || !instance_exists(obj_player)) exit;

// Encostou: as almas voltam.
if (point_distance(x, y, obj_player.x, obj_player.y) < 12) {
    obj_game.almas += obj_game.mancha.almas;
    obj_game.mancha.ativa = false;
    mostrar_texto("Almas recuperadas");
    instance_destroy();
}
```

**obj_mancha → Draw** (arquivo inteiro)
<!-- src: objects/obj_mancha/Draw_0.gml -->
```gml
// Pulsa: a transparência sobe e desce com o tempo.
draw_sprite_ext(sprite_index, 0, x, y, 1, 1, 0, c_white, 0.6 + 0.4 * sin(current_time / 200));
```

**`current_time`** são os milissegundos desde que o jogo abriu. `sin` dele sobe e desce de -1 a 1 para sempre: a mancha "respira".

Coloque um `obj_lanterna` na `rm_teste` em **(80, 64)**.

---

## Arte do dia

Com a arte pronta, faça agora a parte **Dia 16** do [Apêndice A](apendice-a-arte.md).

## Teste do dia

- [ ] F perto da lanterna: fade, você aparece embaixo dela com tudo cheio, e os inimigos mortos voltam.
- [ ] Mate um Aldeão, saia e volte pela tecla T (debug): ele continua morto.
- [ ] Junte almas e morra: fade, você volta na lanterna com 0 almas; no lugar da morte há uma mancha pulsando.
- [ ] Encoste na mancha: "Almas recuperadas" e o valor volta.
- [ ] Junte almas, morra, e morra de novo antes de pegar a mancha: a primeira mancha some e as almas dela se perdem.
- [ ] Vida, frascos e balas continuam os mesmos ao trocar de room pela tecla B/T.

## Se deu errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| `variable not set: fade_indo` | O Create novo do `obj_game` não foi digitado inteiro | Passo 2. |
| Ao morrer, volta com a vida zerada | O Room End salvou a vida de morto | Confira o `if (estado != PL.MORTE)` | 
| A lanterna descansa sem parar | F ainda apertado; normal só uma vez. Se repetir, confira `obj_game.aperta_interagir` (é `_pressed`) | Dia 1. |
| Inimigos mortos voltam ao trocar de room | Falta o `array_push` no `inimigo_morrer`, ou o bloco da chave no Create do pai | Passo 4. |
| Duas manchas aparecem | O `obj_mancha` foi colocado na room à mão | Ela é criada pelo código; não coloque no editor. |

## Commit

`dia 16: lanterna, morte e almas`
