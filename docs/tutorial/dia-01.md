# Dia 1 — Projeto, resolução e input

**Quando:** seg 05/10 · **Tempo:** ~3 h

**No fim do dia:** o jogo abre numa janela 1280×720 mostrando uma tela de 320×180 ampliada, e um retângulo (o player) anda em 8 direções.

## O que você vai aprender

- Por que o jogo tem uma **room de inicialização** (`rm_init`) e um objeto que nunca morre (`obj_game`).
- Como desenhar em 320×180 e ampliar sem borrar (pixel art).
- Por que **só um objeto lê o teclado** e os outros perguntam para ele.
- Como andar na diagonal sem ficar mais rápido.

---

## Passo 1 — Opções do jogo (5 min)

1. Clique no ícone de engrenagem **Game Options** (barra de cima).
2. **Main → General**: confira que **Game frames per second** está em **60**.
3. **Windows → Graphics**:
   - **Interpolate colours between pixels**: desmarcado (senão a pixel art fica borrada).
   - **Scaling**: **Keep aspect ratio**.
4. **Apply** e feche.

## Passo 2 — As duas rooms (10 min)

1. No Asset Browser, abra a pasta **Rooms → Sistema**. Já existe uma `Room1`.
2. Renomeie para **`rm_init`** (clique nela e aperte F2).
3. Abra a `rm_init`. No painel **Room Settings** (esquerda): **Width 1280**, **Height 720**.
4. Botão direito na `rm_init` no Asset Browser → **Set As Home Room** (aparece uma casinha). É a primeira room que roda.
5. Crie outra room: botão direito na pasta **Rooms → Teste** → **Create → Room**. Nome **`rm_teste`**, **Width 640**, **Height 360**.

**Por que duas rooms?** A janela do jogo nasce com o tamanho da primeira room. A `rm_init` tem 1280×720, então a janela abre em 1280×720. Ela também é o lugar onde o `obj_game` nasce, uma vez só. Logo em seguida ele manda o jogo para a `rm_teste`.

## Passo 3 — Script de configuração (5 min)

Crie o script **`scr_config`**, apague o conteúdo e digite:

**scr_config** (arquivo inteiro)
<!-- src: scripts/scr_config.gml -->
```gml
// Configurações usadas pelo jogo inteiro.
// Um #macro é um apelido: antes de compilar, o GameMaker troca o nome pelo valor.

#macro LARGURA_BASE 320
#macro ALTURA_BASE 180
```

Em vez de espalhar `320` pelo código, você escreve `LARGURA_BASE`. Se um dia mudar a resolução, muda num lugar só.

## Passo 4 — O obj_game (40 min)

1. Crie o objeto **`obj_game`**. Não tem sprite.
2. Marque a caixa **Persistent**. Instância persistente não some quando a room muda.
3. Adicione os eventos **Create**, **Begin Step** e **Room Start** (Other → Room Start).

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

// --- Debug ---
debug = false;

room_goto(rm_teste);
```

O que cada parte faz:

- **`application_surface`** é a "tela" onde o GameMaker desenha tudo antes de mostrar na janela. `surface_resize` deixa essa tela com 320×180. O GameMaker amplia ela para caber na janela de 1280×720 (4×). Como a interpolação está desligada, cada pixel vira um quadrado 4×4 nítido.
- **`display_set_gui_size`** faz o **Draw GUI** (usado para HUD e menus) também trabalhar em 320×180.
- **`camera_create_view`** cria uma câmera que enxerga 320×180 pixels da room. Guardamos ela na variável `camera` para usar no Room Start.
- **Input:** as variáveis começam zeradas aqui e são preenchidas todo frame no Begin Step.
- **`room_goto(rm_teste)`** manda o jogo para a room de teste. A troca acontece no fim do frame.

**obj_game → Begin Step** (arquivo inteiro)
<!-- src: objects/obj_game/Step_1.gml -->
```gml
// Begin Step: roda antes do Step de todo mundo.
// Lê o input uma vez por frame.

// keyboard_check devolve 1 (apertada) ou 0 (solta).
// "Direita menos esquerda" dá -1, 0 ou 1.
mover_x = keyboard_check(ord("D")) - keyboard_check(ord("A"));
mover_y = keyboard_check(ord("S")) - keyboard_check(ord("W"));

// A mira é o ângulo do peito do player (10 px acima dos pés) até o mouse.
if (instance_exists(obj_player)) {
    mira_dir = point_direction(obj_player.x, obj_player.y - 10, mouse_x, mouse_y);
}

// _pressed: verdadeiro só no frame em que a tecla desceu.
aperta_esquiva   = keyboard_check_pressed(vk_space);
aperta_leve      = mouse_check_button_pressed(mb_left);
aperta_pesado    = mouse_check_button_pressed(mb_right);
aperta_tiro      = keyboard_check_pressed(ord("Q"));
aperta_cura      = keyboard_check_pressed(ord("E"));
aperta_interagir = keyboard_check_pressed(ord("F"));

if (keyboard_check_pressed(vk_f3)) {
    debug = !debug;
}
```

- **`ord("D")`** transforma a letra no código da tecla. A letra tem que ser **maiúscula**.
- **`mover_x`**: segurando D dá `1 - 0 = 1`; segurando A dá `0 - 1 = -1`; os dois ou nenhum dá `0`.
- **Lembre que `y` cresce para baixo**: W (cima) dá `mover_y = -1`.
- **`point_direction(x1, y1, x2, y2)`** devolve o ângulo de um ponto até o outro (0° = direita, 90° = cima).
- **Por que do peito (`y - 10`) e não dos pés?** Você vai mirar com o mouse no **corpo** dos inimigos, que é desenhado acima dos pés deles. Do peito do player até o peito do inimigo dá o mesmo ângulo que dos pés até os pés, e é nos pés que o jogo mede tudo. Mirando dos pés, os tiros passariam por cima dos inimigos.
- **`instance_exists(obj_player)`** evita erro na `rm_init`, onde ainda não tem player.
- **`keyboard_check`** = a tecla está segurada. **`keyboard_check_pressed`** = a tecla desceu **neste** frame (dispara uma vez por aperto).
- **`debug = !debug`** inverte: `true` vira `false` e vice-versa. O F3 liga e desliga os desenhos de teste que vamos usar o projeto inteiro.

**Por que só o obj_game lê o teclado?** Se amanhã você quiser trocar a tecla de esquiva, ou adicionar controle (gamepad), muda num lugar só. O player nunca chama `keyboard_check`: ele pergunta `obj_game.aperta_esquiva`.

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
```

Uma **view** é "a câmera ligada à tela". Este código liga a view 0 e diz que ela usa a nossa câmera, desenhando em 320×180. Como roda em todo Room Start, **nenhuma room precisa configurar câmera no editor**.

4. Abra a `rm_init`, selecione a camada **Instances** e arraste o `obj_game` para dentro dela (em qualquer lugar).

## Passo 5 — Sprite provisório do player (5 min)

Crie o sprite **`spr_player`**: **12×20**, cor clara, origem **Custom x 6, y 20**.

A origem (6, 20) fica no meio da base do sprite: **nos pés**. Num jogo 3/4, a posição do personagem é onde os pés tocam o chão. Tudo (distância, colisão, quem desenha na frente) vai usar os pés.

## Passo 6 — O obj_player (40 min)

1. Crie o objeto **`obj_player`** com o sprite `spr_player`.
2. Eventos: **Create**, **Step**, **Draw**.

**obj_player → Create** (arquivo inteiro)
<!-- src: objects/obj_player/Create_0.gml -->
```gml
vel = 1.5; // pixels por frame
```

**obj_player → Step** (arquivo inteiro)
<!-- src: objects/obj_player/Step_0.gml -->
```gml
var _mx = obj_game.mover_x;
var _my = obj_game.mover_y;

// Na diagonal, (1, 1) tem comprimento 1,41.
// Dividir pelo comprimento deixa qualquer direção com comprimento 1.
var _comp = point_distance(0, 0, _mx, _my);
if (_comp > 0) {
    x += _mx / _comp * vel;
    y += _my / _comp * vel;
}
```

**Por que dividir pelo comprimento?** Segurando D e S ao mesmo tempo, `mover_x = 1` e `mover_y = 1`. Se você somasse direto `1 × vel` nos dois, andaria `vel` para a direita **e** `vel` para baixo, ou seja, 1,41 × `vel` na diagonal. Isso é 41% mais rápido que em linha reta. Dividindo pelo comprimento (`point_distance(0, 0, 1, 1)` = 1,41), a diagonal vira (0,71, 0,71): comprimento 1.

**`var`** cria uma variável local: ela só existe até o fim deste evento. Use `var` para contas de passagem. O `_` no começo é convenção para você bater o olho e saber que é local.

**obj_player → Draw** (arquivo inteiro)
<!-- src: objects/obj_player/Draw_0.gml -->
```gml
draw_self();

if (obj_game.debug) {
    draw_line(x, y, mouse_x, mouse_y);
}
```

Quando um objeto tem evento **Draw**, o GameMaker para de desenhar ele sozinho. Por isso o `draw_self()`: "desenhe meu sprite como sempre". Com o debug ligado (F3), desenha uma linha dos pés até o mouse.

3. Abra a `rm_teste`, camada **Instances**, e coloque um `obj_player` no meio.

## Passo 7 — Rodar (F5)

Aperte **F5**. Deve abrir uma janela 1280×720 com fundo preto e um retângulo claro grande (ele tem 12×20 pixels, ampliado 4×).

---

## Teste do dia

- [ ] A janela abre em 1280×720, sem erro.
- [ ] O retângulo anda com WASD nas 8 direções.
- [ ] Na diagonal ele não fica mais rápido (compare no olho com a reta).
- [ ] F3 mostra uma linha do player até o mouse; F3 de novo esconde.
- [ ] O pixel está nítido, sem borrão.

## Se deu errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| Erro `unknown function or script` ou `rm_teste` desconhecido | Nome digitado diferente do recurso | Confira o nome exato no Asset Browser. |
| Janela abre pequena ou com outro tamanho | `rm_init` não é a Home Room, ou não tem 1280×720 | Passo 2. |
| Tela preta, nada aparece | O `obj_player` não foi colocado na `rm_teste`, ou foi colocado numa camada que não é Instances | Passo 6, item 3. |
| `unable to find instance for object index obj_game` | O `obj_game` não está na `rm_init`, ou não está marcado como Persistent | Passo 4. |
| O player não anda | `ord("d")` minúsculo | Letras do `ord` sempre maiúsculas. |
| Imagem borrada | Interpolação ligada | Passo 1. |
| Player anda devagar ou rápido demais | Game frames per second diferente de 60 | Passo 1. |

## Commit

GitHub Desktop → `dia 1: projeto, resolução e input` → **Commit to main**.
