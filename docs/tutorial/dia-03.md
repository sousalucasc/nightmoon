# Dia 3 — Máquina de estados e esquivas

**Quando:** qua 07/10 · **Tempo:** ~3 h

**No fim do dia:** Espaço parado faz um **backstep** (pulo curto para trás). Espaço andando faz um **dash** na direção do movimento. Os dois têm **iframes** (frames de invulnerabilidade), visíveis com F3.

## O que você vai aprender

- **Máquina de estados**: o player está sempre em exatamente um estado, e cada estado decide o que pode fazer.
- **`enum`** e **`switch`**.
- **Struct** para guardar os dados de cada esquiva.
- Como fazer uma velocidade que desacelera até parar, percorrendo a distância certa.

---

## Por que uma máquina de estados?

Sem ela, você acabaria com variáveis como `esta_esquivando`, `esta_atacando`, `esta_curando`… e dezenas de `if` para impedir combinações impossíveis ("atacando **e** esquivando?"). Com estados:

- O player tem **uma** variável `estado`.
- O Step olha o estado e roda **só** o código daquele estado.
- Cada estado decide para quais outros pode ir. O estado `ESQUIVA` simplesmente não tem código de ataque, então é impossível atacar no meio da esquiva.

Os estados do player (do GDD):

| Estado | O que faz |
|---|---|
| `LIVRE` | parado ou andando; pode começar qualquer ação |
| `ESQUIVA` | backstep ou dash |
| `ATAQUE` | golpe leve ou pesado (dia 5) |
| `TIRO` | pistola (dia 8) |
| `CURA` | frasco (dia 15) |
| `HITSTUN` | tomou dano, perdeu o controle (dia 4) |
| `VISCERAL` | golpe crítico após parry (dia 11) |
| `MORTE` | morreu (dia 4) |

---

## Passo 1 — O enum (10 min)

**scr_config** (arquivo inteiro)
<!-- src: scripts/scr_config.gml -->
```gml
// Configurações usadas pelo jogo inteiro.
// Um #macro é um apelido: antes de compilar, o GameMaker troca o nome pelo valor.

#macro LARGURA_BASE 320
#macro ALTURA_BASE 180

// Estados do player. Cada nome vira um número: LIVRE = 0, ESQUIVA = 1...
// Alguns só serão usados nos próximos dias.
enum PL {
    LIVRE,
    ESQUIVA,
    ATAQUE,
    TIRO,
    CURA,
    HITSTUN,
    VISCERAL,
    MORTE
}
```

Um **enum** dá nomes para números. `PL.ESQUIVA` é só o número 1, mas lendo o código você entende. Se escrevesse `estado = 1`, daqui a uma semana não saberia o que é 1.

Para o debug mostrar o nome do estado na tela, o `obj_game` guarda os nomes numa lista, **na mesma ordem do enum**:

**obj_game → Create** (adicione antes de `room_goto`)
<!-- src: objects/obj_game/Create_0.gml @antes: room_goto -->
```gml
// Nomes dos estados, na mesma ordem do enum PL (para o debug)
nomes_pl = ["LIVRE", "ESQUIVA", "ATAQUE", "TIRO", "CURA", "HITSTUN", "VISCERAL", "MORTE"];
```

`nomes_pl[PL.ESQUIVA]` é `nomes_pl[1]`, que é `"ESQUIVA"`.

## Passo 2 — Variáveis novas do player (15 min)

**obj_player → Create** (adicione no fim)
<!-- src: objects/obj_player/Create_0.gml @fim -->
```gml
// --- Estado ---
estado = PL.LIVRE;
estado_timer = 0;   // frames desde que entrou no estado atual

// --- Esquiva ---
// Dados de cada esquiva (GDD seção 5). Um struct guarda vários valores com nome.
backstep = { duracao: 16, distancia: 36, iframe_ini: 2, iframe_fim: 7, custo: 15 };
dash     = { duracao: 22, distancia: 64, iframe_ini: 2, iframe_fim: 13, custo: 25 };
esq = backstep;     // qual das duas está acontecendo agora
esq_dir = 0;        // direção da esquiva
esq_vel = 0;        // velocidade atual
esq_desacel = 0;    // quanto a velocidade cai por frame
invulneravel = false;
```

- **`estado_timer`** conta os frames dentro do estado atual. Zera a cada troca. É com ele que sabemos "estou no frame 5 do dash".
- **`backstep` e `dash` são structs**: `backstep.duracao` é 16, `dash.distancia` é 64. Guardar os números num struct deixa o código do estado igual para os dois: ele só lê `esq.duracao`, seja qual for a esquiva.
- **`esq = backstep`** não copia o struct: faz `esq` **apontar** para ele. Depois, `esq == dash` pergunta "esq está apontando para o dash?".
- **`custo`** é a stamina, que entra amanhã.

## Passo 3 — O script do player (60 min)

Crie o script **`scr_player`**, apague o conteúdo e digite:

**scr_player** (arquivo inteiro)
<!-- src: scripts/scr_player.gml -->
```gml
// Funções do player.
// Quem chama é o obj_player, então x, y, estado etc. aqui dentro são os dele.

function player_trocar(_novo) {
    estado = _novo;
    estado_timer = 0;
}

/// Anda na direção do input. _mult: 1 = velocidade normal, 0.5 = metade.
function player_mover(_mult) {
    var _mx = obj_game.mover_x;
    var _my = obj_game.mover_y;
    var _comp = point_distance(0, 0, _mx, _my);
    if (_comp > 0) {
        move_and_collide(_mx / _comp * vel * _mult, _my / _comp * vel * _mult, obj_parede);
    }
}

function player_estado_livre() {
    player_mover(1);
    if (obj_game.aperta_esquiva) {
        player_comecar_esquiva();
    }
}

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
    player_trocar(PL.ESQUIVA);
}

function player_estado_esquiva() {
    move_and_collide(lengthdir_x(esq_vel, esq_dir), lengthdir_y(esq_vel, esq_dir), obj_parede);
    esq_vel = max(0, esq_vel - esq_desacel);

    // Invulnerável só dentro da janela de iframes.
    invulneravel = (estado_timer >= esq.iframe_ini && estado_timer <= esq.iframe_fim);

    if (estado_timer >= esq.duracao) {
        invulneravel = false;
        player_trocar(PL.LIVRE);
    }
}
```

Explicando cada função:

- **`player_trocar(novo)`**: troca o estado **e** zera o timer. Sempre troque de estado por ela. Se esquecer de zerar o timer, o estado novo começa "no meio" e termina na hora errada.
- **As funções usam `x`, `estado`, `vel`…** Isso funciona porque quem chama é o `obj_player`. Uma função chamada de dentro de uma instância enxerga as variáveis dela.
- **`player_mover(_mult)`**: o movimento de ontem virou função, porque vamos reusar (a cura anda a 50%).
- **`player_estado_livre`**: anda e, se apertou Espaço, começa a esquiva.
- **`player_comecar_esquiva`** decide qual esquiva e **guarda a direção no começo**. Durante o dash, mudar o WASD não muda a direção. Esquiva comprometida é parte do estilo souls.
- **`lengthdir_x(dist, dir)`** e **`lengthdir_y(dist, dir)`**: quanto de x e de y andar para percorrer `dist` na direção `dir`. É o jeito de transformar "ângulo + velocidade" em movimento.
- **A conta da velocidade**: se a velocidade começa em `v` e cai em linha reta até 0, a distância percorrida é a área de um triângulo, `v × duração ÷ 2`. Queremos 36 px em 16 frames: `v = 2 × 36 ÷ 16 = 4,5 px/frame`. O dash dá `2 × 64 ÷ 22 ≈ 5,8`.
- **`max(0, ...)`** impede a velocidade de ficar negativa.
- **`invulneravel = (condição)`**: a comparação já dá `true` ou `false`, que vai direto para a variável.

## Passo 4 — O Step vira um switch (15 min)

**obj_player → Step** (arquivo inteiro)
<!-- src: objects/obj_player/Step_0.gml -->
```gml
estado_timer += 1;

switch (estado) {
    case PL.LIVRE:
        player_estado_livre();
        break;
    case PL.ESQUIVA:
        player_estado_esquiva();
        break;
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

- **`switch (estado)`** pula direto para o `case` igual ao estado atual.
- **`break`** sai do switch. Sem ele, o código continua rodando o `case` de baixo. É o erro mais comum com switch.
- **O timer sobe no começo do Step.** Então, no primeiro frame de um estado, `estado_timer` vale 1. Um estado com `duracao: 16` roda os frames 1 a 16.

## Passo 5 — Debug do estado (15 min)

**obj_player → Draw** (arquivo inteiro)
<!-- src: objects/obj_player/Draw_0.gml -->
```gml
// Com o debug ligado, o player fica ciano enquanto está invulnerável.
var _cor = c_white;
if (obj_game.debug && invulneravel) {
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
    draw_set_colour(c_white);
}
```

- A **cor** passada ao `draw_sprite_ext` tinge o sprite. `c_aqua` deixa ciano.
- **`draw_set_halign(fa_center)`** centraliza o texto no x. Volte para `fa_left` depois, senão todo texto do jogo fica centralizado.

---

## Teste do dia

- [ ] Parado + Espaço: pulo curto para longe do mouse.
- [ ] Andando + Espaço: dash mais longo na direção do WASD.
- [ ] Durante a esquiva, WASD não muda a direção nem dá pra esquivar de novo.
- [ ] F3: o texto em cima muda de `LIVRE` para `ESQUIVA` e volta.
- [ ] F3: o player fica ciano por um pedaço curto do backstep e um pedaço maior do dash.
- [ ] Esquivar contra a parede não atravessa.

## Se deu errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| A esquiva nunca termina | `player_trocar` não zera o timer, ou o Step não tem `estado_timer += 1` | Passos 3 e 4. |
| Faz a esquiva e depois a ação do estado de baixo | Faltou `break` num `case` | Passo 4. |
| `variable not set: estado` | O bloco do Create não foi adicionado | Passo 2. |
| `unknown function player_estado_livre` | Nome da função diferente entre o script e o Step | Compare letra por letra. |
| Backstep vai para o lado errado | Faltou o `+ 180` | Passo 3. |
| Texto do estado errado (ex.: mostra ESQUIVA parado) | A lista `nomes_pl` fora da ordem do enum | Passo 1. |

## Commit

`dia 3: máquina de estados e esquivas`
