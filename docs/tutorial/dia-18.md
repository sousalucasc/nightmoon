# Dia 18 — O mapa

**Quando:** qui 22/10 · **Tempo:** ~3 h

**No fim do dia:** as 5 rooms do jogo existem e se ligam por portas: **praça** (lanterna) → **rua** → **mercado** → **portão** → **arena**. No mercado há um **portão-atalho** que só abre pelo lado de dentro e volta para a praça.

## O que você vai aprender

- **Portas** com destino configurado por instância (**Creation Code**).
- **Pontos de chegada** numerados.
- Um **atalho** que lembra que foi aberto.

---

## Passo 1 — Portas, chegadas e atalho (50 min)

| Sprite | Tamanho | Cor | Origem |
|---|---|---|---|
| `spr_porta` | 16×16 | verde | x 0, y 0 |
| `spr_chegada` | 8×8 | azul | x 4, y 4 |
| `spr_atalho` | 32×16 | marrom | x 16, y 16 |

**obj_porta** (sprite `spr_porta`, **Visible desmarcado**). Eventos: Create, Step.

**obj_porta → Create** (arquivo inteiro)
<!-- src: objects/obj_porta/Create_0.gml -->
```gml
// Mude estes valores no Creation Code de cada porta (duplo clique → Creation Code).
destino = rm_teste;   // room para onde leva
chegada = 1;          // número do obj_chegada na room de destino
```

**obj_porta → Step** (arquivo inteiro)
<!-- src: objects/obj_porta/Step_0.gml -->
```gml
if (jogo_congelado() || !instance_exists(obj_player)) exit;

if (place_meeting(x, y, obj_player)) {
    obj_game.chegada_id = chegada;
    trocar_room(destino);
}
```

**obj_chegada** (sprite `spr_chegada`, **Visible desmarcado**). Só o Create:

**obj_chegada → Create** (arquivo inteiro)
<!-- src: objects/obj_chegada/Create_0.gml -->
```gml
numero = 1;   // mude no Creation Code
```

**obj_atalho** (sprite `spr_atalho`, **Parent `obj_parede`**, Visible marcado). Eventos: Create, Step.

**obj_atalho → Create** (arquivo inteiro)
<!-- src: objects/obj_atalho/Create_0.gml -->
```gml
// Por qual lado o portão abre: "cima", "baixo", "esquerda", "direita" ou "nenhum".
// Mude no Creation Code.
abre_por = "nenhum";

// Já foi aberto nesta partida? Então não existe mais.
if (obj_game.atalho_aberto) {
    instance_destroy();
}
```

**obj_atalho → Step** (arquivo inteiro)
<!-- src: objects/obj_atalho/Step_0.gml -->
```gml
if (jogo_congelado() || !instance_exists(obj_player)) exit;

var _p = obj_player;
if (point_distance(x, y, _p.x, _p.y) < 32 && obj_game.aperta_interagir) {
    var _lado_certo = (abre_por == "cima" && _p.y < y)
        || (abre_por == "baixo" && _p.y > y)
        || (abre_por == "esquerda" && _p.x < x)
        || (abre_por == "direita" && _p.x > x);
    if (_lado_certo) {
        obj_game.atalho_aberto = true;
        mostrar_texto("O portão abriu.");
        instance_destroy();
    } else {
        mostrar_texto("Não abre por este lado.");
    }
}
```

Como o atalho é filho de `obj_parede`, ele **bloqueia a passagem** enquanto existir. Destruído, a passagem fica livre.

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
        atalho_aberto = false;
        chegada_id = -1;            // número da chegada ao passar por uma porta
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

**obj_game → Room Start** (adicione antes da linha `// A mancha de almas, se ela ficou nesta room.`)
<!-- src: objects/obj_game/Other_4.gml @antes: // A mancha de almas, se ela ficou nesta room. -->
```gml
// Chegando por uma porta: o player aparece no obj_chegada com o mesmo número.
if (chegada_id >= 0 && instance_exists(obj_player)) {
    with (obj_chegada) {
        if (numero == other.chegada_id) {
            obj_player.x = x;
            obj_player.y = y;
        }
    }
    chegada_id = -1;
}

```

Dentro do `with (obj_chegada)`, **`other`** é quem chamou o `with`: o `obj_game`. `other.chegada_id` é o número que a porta guardou.

## Passo 2 — Como configurar uma porta (leia antes de montar)

1. Coloque o `obj_porta` na passagem (estique com Scale para cobrir a abertura inteira).
2. Duplo clique nele → **Creation Code** → digite, por exemplo:

```gml
destino = rm_rua;
chegada = 1;
```

3. Na room de destino, coloque um `obj_chegada` perto da porta de volta, **longe o bastante dela** (uns 24 px) para o player não nascer em cima da porta e voltar na hora. Creation Code dele: `numero = 1;`

O **Creation Code** roda depois do Create, só naquela instância. É como cada porta tem um destino diferente usando o mesmo objeto.

## Passo 3 — Montar as rooms (90 min)

Crie as 5 rooms. Em todas: grid 16×16, um `obj_player` onde está indicado (é onde você nasce ao começar ali; portas e lanternas reposicionam ele).

Abaixo, **P** = `obj_parede` (x, y, Scale X, Scale Y). Portas e chegadas com o Creation Code entre aspas.

### rm_praca — 480×270

| O quê | x | y | Scale | Creation Code |
|---|---|---|---|---|
| P (cima, esquerda) | 0 | 0 | 14×1 | |
| P (cima, direita) | 256 | 0 | 14×1 | |
| P (baixo) | 0 | 254 | 30×1 | |
| P (esquerda) | 0 | 16 | 1×15 | |
| P (direita, cima) | 464 | 16 | 1×6 | |
| P (direita, baixo) | 464 | 160 | 1×6 | |
| `obj_porta` (leste) | 464 | 112 | 1×3 | `destino = rm_rua; chegada = 1;` |
| `obj_porta` (norte, atalho) | 224 | 0 | 2×1 | `destino = rm_mercado; chegada = 2;` |
| `obj_atalho` | 240 | 32 | 1×1 | `abre_por = "nenhum";` |
| `obj_chegada` | 432 | 136 | | `numero = 1;` |
| `obj_chegada` | 240 | 60 | | `numero = 2;` |
| `obj_lanterna` | 240 | 120 | | |
| `obj_player` | 240 | 150 | | |

### rm_rua — 960×360

| O quê | x | y | Scale | Creation Code |
|---|---|---|---|---|
| P (cima) | 0 | 0 | 60×1 | |
| P (baixo) | 0 | 344 | 60×1 | |
| P (esquerda, cima) | 0 | 16 | 1×9 | |
| P (esquerda, baixo) | 0 | 208 | 1×9 | |
| P (direita, cima) | 944 | 16 | 1×9 | |
| P (direita, baixo) | 944 | 208 | 1×9 | |
| P (bloco) | 304 | 96 | 6×2 | |
| P (bloco) | 608 | 240 | 6×2 | |
| `obj_pilar` | 448 | 184 | | |
| `obj_pilar` | 760 | 120 | | |
| `obj_porta` (oeste) | 0 | 160 | 1×3 | `destino = rm_praca; chegada = 1;` |
| `obj_porta` (leste) | 944 | 160 | 1×3 | `destino = rm_mercado; chegada = 1;` |
| `obj_chegada` | 40 | 184 | | `numero = 1;` |
| `obj_chegada` | 912 | 184 | | `numero = 2;` |
| `obj_aldeao` | 200 | 100 | | |
| `obj_aldeao` | 232 | 124 | | |
| `obj_aldeao` | 500 | 260 | | |
| `obj_aldeao` | 540 | 290 | | |
| `obj_aldeao` | 568 | 256 | | |
| `obj_brutamontes` | 820 | 190 | | |
| `obj_player` | 40 | 184 | | |

### rm_mercado — 640×540

| O quê | x | y | Scale | Creation Code |
|---|---|---|---|---|
| P (cima, esquerda) | 0 | 0 | 18×1 | |
| P (cima, direita) | 320 | 0 | 20×1 | |
| P (baixo, esquerda) | 0 | 524 | 18×1 | |
| P (baixo, direita) | 320 | 524 | 20×1 | |
| P (esquerda, cima) | 0 | 16 | 1×9 | |
| P (esquerda, baixo) | 0 | 208 | 1×20 | |
| P (direita) | 624 | 16 | 1×32 | |
| P (bloco) | 144 | 208 | 4×4 | |
| P (bloco) | 416 | 304 | 4×4 | |
| `obj_porta` (oeste) | 0 | 160 | 1×3 | `destino = rm_rua; chegada = 2;` |
| `obj_porta` (norte, atalho) | 288 | 0 | 2×1 | `destino = rm_praca; chegada = 2;` |
| `obj_atalho` | 304 | 32 | 1×1 | `abre_por = "baixo";` |
| `obj_porta` (sul) | 288 | 524 | 2×1 | `destino = rm_portao; chegada = 1;` |
| `obj_chegada` | 40 | 184 | | `numero = 1;` |
| `obj_chegada` | 304 | 60 | | `numero = 2;` |
| `obj_chegada` | 304 | 496 | | `numero = 3;` |
| `obj_aldeao` | 120 | 80 | | |
| `obj_aldeao` | 500 | 100 | | |
| `obj_aldeao` | 304 | 260 | | |
| `obj_aldeao` | 200 | 420 | | |
| `obj_aldeao` | 450 | 460 | | |
| `obj_brutamontes` | 304 | 150 | | |
| `obj_brutamontes` | 520 | 380 | | |
| `obj_player` | 40 | 184 | | |

### rm_portao — 480×270

| O quê | x | y | Scale | Creation Code |
|---|---|---|---|---|
| P (cima, esquerda) | 0 | 0 | 14×1 | |
| P (cima, direita) | 256 | 0 | 14×1 | |
| P (baixo, esquerda) | 0 | 254 | 14×1 | |
| P (baixo, direita) | 256 | 254 | 14×1 | |
| P (esquerda) | 0 | 16 | 1×15 | |
| P (direita) | 464 | 16 | 1×15 | |
| `obj_porta` (norte) | 224 | 0 | 2×1 | `destino = rm_mercado; chegada = 3;` |
| `obj_porta` (sul) | 224 | 254 | 2×1 | `destino = rm_arena_1; chegada = 1;` |
| `obj_chegada` | 240 | 40 | | `numero = 1;` |
| `obj_chegada` | 240 | 228 | | `numero = 2;` |
| `obj_aldeao` | 180 | 140 | | |
| `obj_aldeao` | 300 | 140 | | |
| `obj_player` | 240 | 40 | | |

### rm_arena_1 — 480×360

| O quê | x | y | Scale | Creation Code |
|---|---|---|---|---|
| P (cima, esquerda) | 0 | 0 | 14×1 | |
| P (cima, direita) | 256 | 0 | 14×1 | |
| P (baixo) | 0 | 344 | 30×1 | |
| P (esquerda) | 0 | 16 | 1×21 | |
| P (direita) | 464 | 16 | 1×21 | |
| `obj_porta` (norte) | 224 | 0 | 2×1 | `destino = rm_portao; chegada = 2;` |
| `obj_chegada` | 240 | 40 | | `numero = 1;` |
| `obj_nevoa` | 16 | 72 | 28×1 | |
| `obj_chefe` | 240 | 240 | | |
| `obj_player` | 240 | 40 | | |

**Como o atalho funciona:** no mercado, o portão fica entre você e a porta norte. Estando **abaixo** dele (dentro do mercado), F abre. Na praça, o mesmo portão tem `abre_por = "nenhum"`: pelo lado de fora ele nunca abre. Mas quando abre no mercado, `atalho_aberto` vira `true` e **os dois** somem (o da praça se destrói no Create).

## Passo 4 — Para testar (10 min)

Para começar direto na praça enquanto testa, troque temporariamente a última linha do `obj_game → Create` para `room_goto(rm_praca);`. Amanhã ela vira a tela de título.

## Arte do dia

Com a arte pronta, faça agora a parte **Dia 18** do [Apêndice A](apendice-a-arte.md): tileset, guias de pintura de cada room, objetos do cenário e portão. Depois de pintar os tiles, desmarque **Visible** no `obj_parede`: as paredes continuam lá, invisíveis, em cima dos muros desenhados.

---

## Teste do dia

- [ ] Da praça para a rua, da rua para o mercado, do mercado para o portão e para a arena: cada porta leva para o lugar certo, com fade.
- [ ] Voltando por uma porta, você aparece perto da porta certa, não em cima dela.
- [ ] Na praça, F no portão: "Não abre por este lado."
- [ ] No mercado, por baixo, F no portão: abre. Passando pela porta norte, você chega na praça.
- [ ] Morrendo depois de abrir, o atalho continua aberto.
- [ ] Descansando na lanterna da praça e morrendo na rua, você volta na praça.

## Se deu errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| Porta leva para `rm_teste` | Creation Code não digitado (ficou o padrão) | Passo 2. |
| Chega e volta na hora | `obj_chegada` em cima da porta | Afaste uns 24 px. |
| Nasce dentro da parede | `obj_chegada` colado numa parede | Afaste. |
| Player nasce no lugar errado ao chegar | Número da chegada diferente do `chegada` da porta | Confira os pares. |
| `variable not set: chegada_id` | `jogo_novo` antiga | Passo 1. |

## Commit

`dia 18: mapa`
