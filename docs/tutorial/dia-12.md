# Dia 12 — Brutamontes

**Quando:** sex 16/10 · **Tempo:** ~2,5 h (dia leve: use o tempo que sobrar para treinar o parry e ajustar números)

**No fim do dia:** o Brutamontes existe. É lento, tem muita vida e **não é interrompido por golpes**. A pancada dele (aviso branco) é o alvo perfeito de parry. O agarrão (aviso vermelho) avança e não aceita parry: pune quem tenta atirar em tudo.

## O que você vai aprender

- Como um inimigo novo inteiro cabe em **um evento Create**, só com dados.
- **Hyper armor de inimigo** (`pode_hitstun = false`).
- Escolha de ataque **por distância**.

---

## Passo 1 — Sprites (5 min)

| Sprite | Tamanho | Cor | Origem |
|---|---|---|---|
| `spr_brutamontes` | 24×32 | vinho escuro | x 12, y 32 |
| `spr_mask_grande` | 18×8 | verde | x 9, y 8 |

`spr_mask_grande` é a máscara de colisão dos inimigos grandes: pés largos.

## Passo 2 — O objeto (20 min)

Crie o objeto **`obj_brutamontes`** com o sprite `spr_brutamontes` e **Parent `obj_inimigo_pai`**. Só o Create:

**obj_brutamontes → Create** (arquivo inteiro)
<!-- src: objects/obj_brutamontes/Create_0.gml -->
```gml
event_inherited();

hp_max = 180;
hp = hp_max;
vel = 0.7;
raio = 12;
almas = 60;
pode_hitstun = false;   // golpes não interrompem: só o parry para ele
dist_parar = 24;
espera_entre = 40;
mask_index = spr_mask_grande;

// Pancada: windup longo, aceita parry. É ela que ensina o parry.
var _pancada = ataque_novo(40, 6, 30, 40, 30, 120, true);
_pancada.dist_max = 34;

// Agarrão: aviso vermelho, avança 24 px, NÃO aceita parry.
var _agarrao = ataque_novo(30, 8, 36, 50, 18, 60, false);
_agarrao.avanco = 24;
_agarrao.dist_min = 20;
_agarrao.dist_max = 48;

ataques = [_pancada, _agarrao];
```

É só isso. Todo o resto (perseguir, avisar, atacar, parry, visceral, morrer) já está no pai.

**Como ele escolhe:**

| Distância até o player | Ataques possíveis |
|---|---|
| menos de 20 px | só a pancada |
| 20 a 34 px | pancada ou agarrão (sorteio) |
| 34 a 48 px | só o agarrão (ele avança 24 px para alcançar) |
| mais de 48 px | nenhum: ele anda |

**Por que o agarrão existe?** Se todo ataque aceitasse parry, bastaria atirar sempre. O agarrão tem aviso vermelho: quem atira no reflexo leva 50 de dano. Ler o aviso é o jogo.

Coloque um `obj_brutamontes` na `rm_teste` em **x 560, y 64**.

## Passo 3 — Ajuste fino (o resto do tempo)

Brinque com ele e anote o que parece errado. Os números ficam todos no Create acima:

| Se… | Mude |
|---|---|
| a pancada é fácil demais de ler | diminua o windup (40 → 34) |
| o agarrão pega mesmo esquivando | aumente o windup (30 → 34) |
| ele é lento demais para ameaçar | `vel` 0.7 → 0.85 |
| visceral nele é forte demais | aumente `hp_max` |

---

## Arte do dia

Com a arte pronta, faça agora a parte **Dia 12** do [Apêndice A](apendice-a-arte.md).

## Teste do dia

Ligue o F3.

- [ ] Batendo nele, ele não é interrompido (não entra em `HITSTUN`).
- [ ] A pancada tem aviso branco e janela de parry; parry nela atordoa.
- [ ] O agarrão tem aviso vermelho e avança; tiro nele não atordoa.
- [ ] Três viscerais matam (180 de vida, 60 por visceral com Destreza 0).
- [ ] Dá para matar sem parry, na paciência: bater no recovery e sair.

## Se deu errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| Ele é interrompido pelos golpes | `pode_hitstun = false` faltando | Passo 2. |
| Ele nunca usa o agarrão | O player fica perto demais (menos de 20 px) | Normal; afaste um pouco. |
| Ele fica preso nas paredes | Sem `mask_index`, a colisão é o sprite inteiro (24×32) | Passo 2. |

## Commit

`dia 12: Brutamontes`
