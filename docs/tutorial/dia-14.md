# Dia 14 — Chefe, fase 2 e arena

**Quando:** dom 18/10 · **Tempo:** ~3 h

**No fim do dia:** o chefe dorme até você atravessar a **névoa**, que fecha atrás de você. Aparece a barra de vida dele. Aos 50%, ele para, treme e vira **besta**: mais rápido, com garras em combo de 3, investida e salto rápido. Morto, aparece "CAÇA ENCERRADA" e a névoa some.

---

## Passo 1 — Sprites (5 min)

| Sprite | Tamanho | Cor | Origem |
|---|---|---|---|
| `spr_chefe_besta` | 28×28 | cinza-escuro | x 14, y 28 |
| `spr_nevoa` | 16×16 | branco | x 0, y 0 |

## Passo 2 — Mensagem na tela (15 min)

**obj_game → Create** (adicione antes de `room_goto`)
<!-- src: objects/obj_game/Create_0.gml @antes: room_goto -->
```gml
chefe_morto = false;
// --- Mensagem no meio da tela ---
texto = "";
texto_timer = 0;
```

**scr_util** (nova função, adicione no fim)
<!-- src: scripts/scr_util.gml #mostrar_texto -->
```gml
/// Mostra uma mensagem no meio da tela por 3 segundos.
function mostrar_texto(_texto) {
    obj_game.texto = _texto;
    obj_game.texto_timer = 180;
}
```

**obj_game → End Step** (adicione no fim)
<!-- src: objects/obj_game/Step_2.gml @fim -->
```gml
if (texto_timer > 0) {
    texto_timer -= 1;
}
```

**obj_game → Draw GUI** (adicione no fim)
<!-- src: objects/obj_game/Draw_64.gml @fim -->
```gml
// Mensagem no meio da tela
if (texto_timer > 0) {
    draw_set_halign(fa_center);
    draw_set_colour(c_yellow);
    draw_text(LARGURA_BASE / 2, 70, texto);
    draw_set_colour(c_white);
    draw_set_halign(fa_left);
}
```

## Passo 3 — Transformação (40 min)

**scr_combate** (substitua a função `inimigo_dano`)
<!-- src: scripts/scr_combate.gml #inimigo_dano -->
```gml
/// Aplica dano num inimigo.
function inimigo_dano(_inst, _dano) {
    with (_inst) {
        if (estado != INI.MORTE && estado != INI.TRANSFORMA && !no_ar) {
            hp -= _dano;
            flash = 6;
            ultimo_dano = _dano;
            fx_criar(x, y - 10, spr_fx_sangue, irandom(359), 1);
            if (tem_fase2 && fase == 1 && hp <= hp_max / 2) {
                // Chefe na metade da vida: transforma (e não morre neste golpe).
                hp = max(hp, 1);
                inimigo_trocar(INI.TRANSFORMA);
            } else if (hp <= 0) {
                hp = 0;
                inimigo_morrer();
            } else if (pode_hitstun && inimigo_pode_interromper()) {
                inimigo_trocar(INI.HITSTUN);
            }
        }
    }
}
```

**scr_inimigo** (nova função, adicione no fim)
<!-- src: scripts/scr_inimigo.gml #inimigo_estado_transforma -->
```gml
/// Chefe virando besta: 90 frames parado e invulnerável, depois troca tudo.
function inimigo_estado_transforma() {
    if (estado_timer == 1) {
        tremer_tela(4);
    }
    if (estado_timer >= 90) {
        fase = 2;
        ataques = ataques_fase2;
        vel = vel_fase2;
        spr = spr_fase2;
        tem_arma = false;      // a besta larga o machado
        inimigo_trocar(INI.PERSEGUIR);
    }
}
```

**scr_inimigo** (substitua a função `inimigo_morrer`)
<!-- src: scripts/scr_inimigo.gml #inimigo_morrer -->
```gml
function inimigo_morrer() {
    obj_game.almas += almas;
    fx_criar(x, y - 10, spr_fx_sangue, 0, 1);
    if (e_chefe) {
        obj_game.chefe_morto = true;
        mostrar_texto("CAÇA ENCERRADA");
    }
    inimigo_trocar(INI.MORTE);
}
```

**scr_inimigo**, na função `inimigo_animar` (adicione antes da linha `case INI.MORTE:`)
<!-- src: scripts/scr_inimigo.gml @antes: case INI.MORTE: -->
```gml
        case INI.TRANSFORMA:
            // Tremendo no lugar enquanto vira besta.
            sprite_index = spr.stagger;
            image_index = (anim_timer div 4) mod sprite_get_number(sprite_index);
            break;
```

**obj_inimigo_pai → Step** (logo depois da linha do `case INI.CAIDO`, adicione)
<!-- src: objects/obj_inimigo_pai/Step_0.gml @depois: case INI.CAIDO:     inimigo_estado_caido();     break; -->
```gml
    case INI.TRANSFORMA: inimigo_estado_transforma(); break;
```

## Passo 4 — O chefe completo (30 min)

**obj_chefe → Create** (arquivo inteiro)
<!-- src: objects/obj_chefe/Create_0.gml -->
```gml
event_inherited();

nome = "Caçador Caído";
e_chefe = true;
hp_max = 900;
hp = hp_max;
vel = 1.3;
raio = 12;
almas = 800;
pode_hitstun = false;
aggro = 400;          // na arena, vê o player de qualquer lugar
desiste = 99999;      // nunca desiste
dist_parar = 24;
espera_entre = 15;
mask_index = spr_mask_grande;
acordado = false;     // a névoa acorda ele

// --- Fase 1 ---
// Machadada dupla: o segundo golpe sempre vem (chance 1).
var _machadada2 = ataque_novo(14, 5, 24, 25, 30, 140, true);
var _machadada1 = ataque_novo(20, 5, 0, 25, 30, 140, true);
_machadada1.seguinte = _machadada2;
_machadada1.chance = 1;
_machadada1.dist_max = 40;

// Tiro de escopeta: média distância, não aceita parry (desvie).
var _tiro = ataque_novo(30, 1, 30, 20, 80, 40, false);
_tiro.tipo = "tiro";
_tiro.dist_min = 40;
_tiro.dist_max = 100;

// Salto: de longe; cai onde o player estava.
var _salto = ataque_novo(30, 28, 30, 30, 28, 360, false);
_salto.tipo = "salto";
_salto.voo = 24;
_salto.dist_min = 100;
_salto.dist_max = 9999;

ataques = [_machadada1, _tiro, _salto];
tem_arma = true;
arma_sprite = spr_arma_machado;
// No desenho do chefe: a mão do machado e a boca do bacamarte (em px a partir dos pés).
mao_x = 4;
mao_y = 12;
boca_x = 20;
boca_y = 22;

// --- Fase 2 (besta, abaixo de 50%) ---
tem_fase2 = true;

// Garras: combo de 3, rápido, aceita parry.
var _garra3 = ataque_novo(8, 4, 20, 15, 26, 120, true);
var _garra2 = ataque_novo(8, 4, 0, 15, 26, 120, true);
var _garra1 = ataque_novo(10, 4, 0, 15, 26, 120, true);
_garra1.seguinte = _garra2;
_garra1.chance = 1;
_garra2.seguinte = _garra3;
_garra2.chance = 1;
_garra1.dist_max = 36;

// Investida: atravessa 120 px; acerta quem estiver em volta dele no caminho.
var _investida = ataque_novo(24, 20, 30, 30, 14, 360, false);
_investida.avanco = 120;
_investida.dist_min = 40;
_investida.dist_max = 110;

// Salto rápido
var _salto2 = ataque_novo(20, 24, 24, 30, 28, 360, false);
_salto2.tipo = "salto";
_salto2.voo = 20;
_salto2.dist_min = 110;
_salto2.dist_max = 9999;

ataques_fase2 = [_garra1, _investida, _salto2];
vel_fase2 = 2.0;
spr_fase2 = {
    parado: spr_chefe_besta,
    andando: spr_chefe_besta,
    ataque: spr_chefe_besta,
    hit: spr_chefe_besta,
    stagger: spr_chefe_besta,
    caido: spr_chefe_besta,
    morte: spr_chefe_besta
};
```

A **investida** não precisou de código novo: é um golpe com arco 360 (acerta em volta) e `avanco` 120. O estado de ataque já anda o avanço durante o ativo e procura o player todo frame.

Adicione o evento **Draw GUI** no `obj_chefe`:

**obj_chefe → Draw GUI** (arquivo inteiro)
<!-- src: objects/obj_chefe/Draw_64.gml -->
```gml
// Barra do chefe: só depois que ele acorda.
if (acordado && estado != INI.MORTE) {
    var _larg = 200;
    var _x1 = (LARGURA_BASE - _larg) / 2;
    var _y1 = ALTURA_BASE - 16;
    draw_set_colour(c_black);
    draw_rectangle(_x1 - 1, _y1 - 1, _x1 + _larg + 1, _y1 + 4, false);
    draw_set_colour(c_maroon);
    draw_rectangle(_x1, _y1, _x1 + _larg * hp / hp_max, _y1 + 3, false);
    draw_set_colour(c_white);
    draw_set_halign(fa_center);
    draw_text(LARGURA_BASE / 2, _y1 - 16, nome);
    draw_set_halign(fa_left);
}
```

O chefe **não** tem evento Draw próprio, então continua usando o Draw do pai. O Draw GUI é só dele.

## Passo 5 — A névoa (40 min)

Crie o objeto **`obj_nevoa`** com o sprite `spr_nevoa`. Eventos: Create, Step, Draw.

**obj_nevoa → Create** (arquivo inteiro)
<!-- src: objects/obj_nevoa/Create_0.gml -->
```gml
fechada = false;
parede = noone;     // a parede invisível que ela cria ao fechar

// Chefe já morto: a névoa nem aparece.
if (obj_game.chefe_morto) {
    instance_destroy();
}
```

**obj_nevoa → Step** (arquivo inteiro)
<!-- src: objects/obj_nevoa/Step_0.gml -->
```gml
if (jogo_congelado()) exit;

if (!fechada && instance_exists(obj_player) && instance_exists(obj_chefe)) {
    // O player está do mesmo lado da névoa que o chefe? Então já atravessou.
    var _cx = x + sprite_width / 2;
    var _cy = y + sprite_height / 2;
    var _lado_player;
    var _lado_chefe;
    if (sprite_width >= sprite_height) {
        // Névoa deitada: compara em cima/embaixo.
        _lado_player = sign(obj_player.y - _cy);
        _lado_chefe = sign(obj_chefe.y - _cy);
    } else {
        // Névoa em pé: compara esquerda/direita.
        _lado_player = sign(obj_player.x - _cx);
        _lado_chefe = sign(obj_chefe.x - _cx);
    }
    if (_lado_player == _lado_chefe && !place_meeting(x, y, obj_player)) {
        fechada = true;
        parede = instance_create_depth(x, y, 0, obj_parede);
        parede.image_xscale = image_xscale;
        parede.image_yscale = image_yscale;
        parede.visible = false;
        obj_chefe.acordado = true;
    }
}

// Chefe morreu (e sumiu): a névoa abre.
if (fechada && !instance_exists(obj_chefe)) {
    if (instance_exists(parede)) {
        instance_destroy(parede);
    }
    instance_destroy();
}
```

**obj_nevoa → Draw** (arquivo inteiro)
<!-- src: objects/obj_nevoa/Draw_0.gml -->
```gml
var _alpha = 0.4;
if (fechada) {
    _alpha = 0.8;
}
draw_sprite_ext(sprite_index, 0, x, y, image_xscale, image_yscale, 0, c_white, _alpha);
```

- **`sign(n)`** devolve -1, 0 ou 1 (o sinal do número). Se o player e o chefe dão o mesmo sinal, estão do mesmo lado da névoa.
- **Fechar** = criar um `obj_parede` invisível do mesmo tamanho. `sprite_width` e `image_xscale` já levam a escala em conta; como `spr_nevoa` e `spr_parede` têm 16×16 com origem no canto, a parede nova cobre exatamente a névoa.
- **`instance_destroy(parede)`** destrói outra instância pelo id.

Na `rm_teste_chefe`, coloque a névoa atravessando a sala: `obj_nevoa` em **(16, 240)**, **Scale X 28**, **Scale Y 1**. O player (em y 300) começa do lado de fora; o chefe (y 120), do lado de dentro.

---

## Arte do dia

Com a arte pronta, faça agora a parte **Dias 13 e 14** do [Apêndice A](apendice-a-arte.md).

## Teste do dia

- [ ] O chefe fica parado até você cruzar a névoa. Ela fica mais opaca e vira parede; a barra aparece.
- [ ] Aos 450 de vida ele para, treme 1,5 s (não apanha) e volta como besta: mais rápido, sem machado.
- [ ] Besta: garras em 3 golpes (parry funciona), investida atravessando a sala, salto.
- [ ] Um golpe grande perto dos 50% não mata: ele transforma primeiro.
- [ ] Morto: "CAÇA ENCERRADA", almas +800, a névoa some.

## Se deu errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| O chefe já vem atrás de você | `acordado = false` faltando | Passo 4. |
| A névoa fecha com você em cima e prende | Faltou o `!place_meeting(x, y, obj_player)` | Passo 5. |
| Transformou e parou de atacar | `ataques_fase2` com nome diferente, ou faltou `case INI.TRANSFORMA` no Step | Passos 3 e 4. |
| Barra do chefe não aparece | Draw GUI não é do `obj_chefe`, ou ele ainda não acordou | Passo 4. |

## Checkpoint da semana 2

| Tem que funcionar | Se não |
|---|---|
| Pistolas, parry, visceral | termine no dia 15; aplique os cortes 1 e 2 |
| Aldeão e Brutamontes | idem |
| Chefe jogável do começo ao fim | aplique os cortes 1, 2 e 3 |

## Commit

`dia 14: chefe fase 2 e arena` — e `semana 2`.
