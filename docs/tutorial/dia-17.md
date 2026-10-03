# Dia 17 — Menus: escolha de armas, subir nível e pausa

**Quando:** qua 21/10 · **Tempo:** ~3 h

**No fim do dia:** ao começar, um menu pede para escolher a arma e depois a pistola. Descansar na lanterna abre o menu da lanterna, com **Subir nível** (Vida, Stamina, Força, Destreza, pagando almas). **Esc** pausa.

## O que você vai aprender

- **Um objeto de menu só**, que muda de comportamento pelo `tipo`.
- Congelar o jogo enquanto um menu está aberto.
- **Consumir input**: a tecla que confirmou o menu não pode disparar mais nada.

---

## Passo 1 — Input dos menus (15 min)

**obj_game → Create** (adicione antes da linha `// --- Debug ---`)
<!-- src: objects/obj_game/Create_0.gml @antes: // --- Debug --- -->
```gml
// Menus
menu_cima = false;
menu_baixo = false;
menu_ok = false;
menu_voltar = false;
abrir_menu_lanterna = false;

```

**obj_game → Begin Step** (adicione no fim)
<!-- src: objects/obj_game/Step_1.gml @fim -->
```gml
// Menus
menu_cima   = keyboard_check_pressed(ord("W")) || keyboard_check_pressed(vk_up);
menu_baixo  = keyboard_check_pressed(ord("S")) || keyboard_check_pressed(vk_down);
menu_ok     = keyboard_check_pressed(vk_enter) || keyboard_check_pressed(ord("F"));
menu_voltar = keyboard_check_pressed(vk_escape);

// Esc durante o jogo: pausa.
if (menu_voltar && !instance_exists(obj_menu) && instance_exists(obj_player) && !fade_indo) {
    menu_abrir("pausa");
}
```

**scr_util** (substitua a função `jogo_congelado`)
<!-- src: scripts/scr_util.gml #jogo_congelado -->
```gml
/// true enquanto o jogo está parado: hitstop, fade ou menu aberto.
function jogo_congelado() {
    return obj_game.hitstop > 0 || obj_game.fade_indo || instance_exists(obj_menu);
}
```

Com um menu aberto, player, inimigos e projéteis saem do Step na primeira linha. É a pausa inteira, de graça.

## Passo 2 — Atributos na partida (15 min)

**scr_jogo** (substitua a função `jogo_novo`)
<!-- src: scripts/scr_jogo.gml #jogo_novo -->
```gml
/// Zera tudo que é da partida. Chamada ao abrir o jogo
/// (e no "Começar" do título, no dia 19).
function jogo_novo() {
    with (obj_game) {
        arma = global.armas.cutelo;
        pistola = global.pistolas.pistola;
        escolheu = false;           // já escolheu arma e pistola?
        atr_vida = 0;
        atr_stamina = 0;
        atr_forca = 0;
        atr_destreza = 0;
        niveis = 0;                 // níveis comprados
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
```

**scr_player** (novas funções, adicione no fim)
<!-- src: scripts/scr_player.gml #player_hp_max -->
```gml
/// Vida e stamina máximas pelos atributos (GDD seção 9).
function player_hp_max() {
    return 100 + 15 * obj_game.atr_vida;
}
```

<!-- src: scripts/scr_player.gml #player_st_max -->
```gml
function player_st_max() {
    return 100 + 10 * obj_game.atr_stamina;
}
```

**obj_player → Create** (troque a linha `hp_max = 100;` por esta)
<!-- src: objects/obj_player/Create_0.gml @troca: hp_max = 100; -->
```gml
hp_max = player_hp_max();
```

**obj_player → Create** (troque a linha `st_max = 100;` por esta)
<!-- src: objects/obj_player/Create_0.gml @troca: st_max = 100; -->
```gml
st_max = player_st_max();
```

## Passo 3 — Funções dos menus (50 min)

Crie o script **`scr_menu`**:

**scr_menu** (arquivo inteiro)
<!-- src: scripts/scr_menu.gml -->
```gml
// Menus. Um objeto só (obj_menu); o "tipo" diz qual menu é.

/// Abre um menu. Tipos: "lanterna", "nivel", "arma", "pistola", "pausa", "titulo".
function menu_abrir(_tipo) {
    var _m = instance_create_depth(0, 0, -9000, obj_menu);
    _m.tipo = _tipo;
    switch (_tipo) {
        case "lanterna":
            _m.titulo = "Lanterna";
            _m.opcoes = ["Subir nível", "Continuar"];
            break;
        case "nivel":
            _m.titulo = "Subir nível";
            _m.opcoes = menu_textos_nivel();
            break;
        case "arma":
            _m.titulo = "Escolha sua arma";
            _m.opcoes = [global.armas.bengala.nome, global.armas.machado.nome, global.armas.cutelo.nome];
            break;
        case "pistola":
            _m.titulo = "Escolha sua pistola";
            _m.opcoes = [global.pistolas.pistola.nome, global.pistolas.escopeta.nome];
            break;
        case "pausa":
            _m.titulo = "Pausa";
            _m.opcoes = ["Continuar", "Sair do jogo"];
            break;
        case "titulo":
            _m.titulo = "NIGHTMOON";
            _m.opcoes = ["Começar", "Sair"];
            break;
    }
    return _m;
}

/// Os textos do menu de nível, com o valor atual de cada atributo.
function menu_textos_nivel() {
    return [
        "Vida " + string(obj_game.atr_vida),
        "Stamina " + string(obj_game.atr_stamina),
        "Força " + string(obj_game.atr_forca),
        "Destreza " + string(obj_game.atr_destreza),
        "Voltar"
    ];
}

/// Roda dentro do obj_menu quando o jogador confirma a opção "sel".
function menu_confirmar() {
    switch (tipo) {
        case "lanterna":
            if (sel == 0) {
                menu_abrir("nivel");
            }
            instance_destroy();
            break;
        case "nivel":
            if (sel == 4) {
                menu_abrir("lanterna");
                instance_destroy();
            } else {
                if (!nivel_comprar(sel)) {
                    mostrar_texto("Almas insuficientes");
                }
                opcoes = menu_textos_nivel();
            }
            break;
        case "arma":
            if (sel == 0) obj_game.arma = global.armas.bengala;
            if (sel == 1) obj_game.arma = global.armas.machado;
            if (sel == 2) obj_game.arma = global.armas.cutelo;
            menu_abrir("pistola");
            instance_destroy();
            break;
        case "pistola":
            if (sel == 0) obj_game.pistola = global.pistolas.pistola;
            if (sel == 1) obj_game.pistola = global.pistolas.escopeta;
            obj_game.escolheu = true;
            instance_destroy();
            break;
        case "pausa":
            if (sel == 0) {
                instance_destroy();
            } else {
                game_end();
            }
            break;
    }
}

/// Roda dentro do obj_menu quando o jogador aperta Esc.
/// (Não pode se chamar menu_voltar: esse já é o nome da variável do obj_game.)
function menu_cancelar() {
    switch (tipo) {
        case "nivel":
            menu_abrir("lanterna");
            instance_destroy();
            break;
        case "lanterna":
        case "pausa":
            instance_destroy();
            break;
    }
}

/// A tecla que mexeu no menu não pode disparar mais nada neste frame.
function menu_consumir_input() {
    with (obj_game) {
        aperta_interagir = false;
        aperta_cura = false;
        buf_leve = 0;
        buf_pesado = 0;
        buf_esquiva = 0;
        buf_tiro = 0;
    }
}

function nivel_custo() {
    return 100 + 50 * obj_game.niveis;
}

/// _atributo: 0 vida, 1 stamina, 2 força, 3 destreza. Devolve true se comprou.
function nivel_comprar(_atributo) {
    var _custo = nivel_custo();
    if (obj_game.almas < _custo) return false;
    obj_game.almas -= _custo;
    obj_game.niveis += 1;
    switch (_atributo) {
        case 0: obj_game.atr_vida += 1; break;
        case 1: obj_game.atr_stamina += 1; break;
        case 2: obj_game.atr_forca += 1; break;
        case 3: obj_game.atr_destreza += 1; break;
    }
    // Aplica na hora: o player já está descansado, então enche junto.
    with (obj_player) {
        hp_max = player_hp_max();
        st_max = player_st_max();
        hp = hp_max;
        st = st_max;
    }
    return true;
}
```

- **Um `switch` com texto** (`case "lanterna":`) funciona igual ao de números.
- **Menus abrem outros menus:** confirmar na lanterna → cria o menu de nível e destrói a si mesmo. Só existe um menu por vez.
- **`nivel_comprar`** devolve `false` sem almas suficientes, e o menu avisa.
- **Nunca dê a uma variável o mesmo nome de uma função.** O `obj_game` tem a variável `menu_voltar` (Esc apertado). Se a função também se chamasse `menu_voltar`, o GameMaker leria o nome como a função, que sempre conta como "verdadeiro": o jogo acharia que Esc está apertado o tempo todo e o pause abriria sozinho, sem sair. O compilador **não avisa** esse erro.
- **O custo sobe:** 100, 150, 200… (GDD seção 9).

## Passo 4 — O objeto de menu (40 min)

Crie o objeto **`obj_menu`**, sem sprite. Eventos: Create, Step, **Draw GUI**.

**obj_menu → Create** (arquivo inteiro)
<!-- src: objects/obj_menu/Create_0.gml -->
```gml
tipo = "";
titulo = "";
opcoes = [];
sel = 0;        // opção selecionada
espera = 2;     // ignora o input dos primeiros frames (a tecla que abriu ainda está descendo)
```

**obj_menu → Step** (arquivo inteiro)
<!-- src: objects/obj_menu/Step_0.gml -->
```gml
if (espera > 0) {
    espera -= 1;
    exit;
}

var _n = array_length(opcoes);
if (obj_game.menu_cima) {
    sel = (sel - 1 + _n) mod _n;    // sobe; do primeiro vai para o último
}
if (obj_game.menu_baixo) {
    sel = (sel + 1) mod _n;         // desce; do último volta ao primeiro
}

if (obj_game.menu_ok) {
    menu_confirmar();
    menu_consumir_input();
} else if (obj_game.menu_voltar) {
    menu_cancelar();
    menu_consumir_input();
}
```

**obj_menu → Draw GUI** (arquivo inteiro)
<!-- src: objects/obj_menu/Draw_64.gml -->
```gml
draw_set_font(fnt_hud);

// Fundo escurecido
draw_set_alpha(0.75);
draw_set_colour(c_black);
draw_rectangle(0, 0, LARGURA_BASE, ALTURA_BASE, false);
draw_set_alpha(1);

draw_set_halign(fa_center);
draw_set_colour(c_white);
draw_text(LARGURA_BASE / 2, 30, titulo);

for (var i = 0; i < array_length(opcoes); i++) {
    if (i == sel) {
        draw_set_colour(c_yellow);
        draw_text(LARGURA_BASE / 2, 60 + i * 14, "> " + opcoes[i] + " <");
    } else {
        draw_set_colour(c_white);
        draw_text(LARGURA_BASE / 2, 60 + i * 14, opcoes[i]);
    }
}

draw_set_colour(c_white);
if (tipo == "nivel") {
    draw_text(LARGURA_BASE / 2, 140, "Almas: " + string(obj_game.almas) + "   Custo: " + string(nivel_custo()));
}
draw_set_halign(fa_left);
```

**`(sel - 1 + _n) mod _n`**: somar `_n` antes do `mod` evita número negativo. Com 5 opções e `sel = 0`, dá `(−1 + 5) mod 5 = 4`: vai para a última.

## Passo 5 — Quando os menus abrem (15 min)

**obj_game → Room Start** (adicione no fim)
<!-- src: objects/obj_game/Other_4.gml @fim -->
```gml
// Primeira vez com o player na tela: escolher arma e pistola.
// Depois de descansar: menu da lanterna.
if (!escolheu && instance_exists(obj_player)) {
    menu_abrir("arma");
} else if (abrir_menu_lanterna) {
    menu_abrir("lanterna");
}
abrir_menu_lanterna = false;
```

**scr_jogo** (substitua a função `lanterna_descansar`)
<!-- src: scripts/scr_jogo.gml #lanterna_descansar -->
```gml
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
        abrir_menu_lanterna = true;
    }
    trocar_room(room);   // recarrega a room: os inimigos voltam
}
```

As teclas de debug 1–5 continuam trocando arma e pistola com o F3 ligado, para testes.

---

## Teste do dia

- [ ] Ao abrir o jogo: "Escolha sua arma" (W/S e F ou Enter), depois "Escolha sua pistola". O jogo só anda depois.
- [ ] A arma escolhida é a que aparece na mão.
- [ ] F na lanterna: fade e menu "Lanterna". "Continuar" fecha; Esc também.
- [ ] "Subir nível" sem almas: "Almas insuficientes". Com almas (mate alguns Aldeões): Vida sobe, a barra de vida cresce, o custo sobe 50.
- [ ] Esc no meio do jogo: pausa (nada se mexe). Esc de novo: volta.
- [ ] Confirmar com F no menu da lanterna não faz descansar de novo.

## Se deu errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| Pause abre sozinho e não sai / não responde | Uma função com o mesmo nome de uma variável (ex.: `menu_voltar`) | A função é `menu_cancelar`. Passo 3. |
| O menu fecha na hora em que abre | Faltou a `espera` no Create do menu | Passo 4. |
| Confirmar com F descansa de novo | Faltou `menu_consumir_input()` | Passo 4. |
| O jogo não pausa com o menu | `jogo_congelado` sem `instance_exists(obj_menu)` | Passo 1. |
| `variable not set: escolheu` | `jogo_novo` antiga (sem as variáveis novas) | Passo 2. |
| Barra de vida não cresce ao subir Vida | `hp_max` ainda é `100` fixo no Create | Passo 2. |

## Commit

`dia 17: menus, nível e pausa`
