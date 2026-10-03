# Apêndice A — Importar a arte

Toda a arte da V1 está pronta na pasta `arte/` do projeto (personagens, armas, efeitos, cenário, HUD, fonte, logo), e os sons em `audio/`.

Importe cada parte **no dia indicado**, depois de terminar o código daquele dia. É a mesma ordem da tabela "Quando cada arte entra" do [cronograma](../CRONOGRAMA.md). O código do tutorial já está preparado para essa arte: a mão da arma, a boca do bacamarte e o tempo da morte já usam as medidas dos desenhos. Aqui é só importar e trocar nomes nos structs.

---

## Regra geral

**Como importar uma animação:**

1. No Asset Browser, botão direito na pasta certa (ex.: **Sprites → Player**) → **Create → Sprite**.
2. Dê o nome exato da lista (ex.: `spr_player_idle`).
3. No editor do sprite, clique em **Import** e escolha o arquivo `spr_player_idle_strip4.png`. O `_strip4` no nome do arquivo faz o GameMaker cortar a tira em 4 quadros sozinho.
4. Em **Origin**, escolha **Custom** e digite a origem da lista (ex.: `16`, `30`).

**Como trocar a imagem de um sprite provisório** (armas, efeitos): abra o sprite que já existe, clique em **Import**, escolha o arquivo e acerte a **Origin**. O nome continua o mesmo, então o código não muda.

- A origem de **todos** os sprites está em [`arte/origens.md`](../../arte/origens.md). Personagens têm a origem nos pés; armas, no cabo.
- Todo personagem está desenhado **virado para a direita**; o código espelha com `lado`.
- **Não mexa na máscara** (Collision Mask) dos sprites da arte. A colisão usa `spr_mask_player` e `spr_mask_grande`, que continuam iguais.
- Arrastar o PNG do Windows Explorer direto para o Asset Browser também funciona. Depois confira se o nome ficou **sem** o `_stripN` (se ficou, renomeie com F2) e acerte a origem.

---

## Dia 2 — Pilar

| Sprite | Arquivo | Quadros | Origem |
|---|---|---|---|
| `spr_pilar` (por cima) | `arte/cenario/spr_pilar.png` | 1 | 8, 32 |

A máscara do provisório continua valendo: depois de importar, confira em **Collision Mask** se ainda está **Manual**, retângulo **0, 22 → 15, 31** (só a base do pilar bloqueia; a parte de cima o player passa por trás).

---

## Dia 5 — Boneco de treino

| Sprite | Arquivo | Quadros | Origem |
|---|---|---|---|
| `spr_boneco` (por cima) | `arte/cenario/spr_boneco.png` | 1 | 8, 24 |

---

## Dia 7 — Player, armas corpo a corpo e cortes

**Player** (pasta `arte/player/`). Todos 32×32, origem **16, 30**:

| Sprite | Arquivo | Quadros |
|---|---|---|
| `spr_player_idle` | `spr_player_idle_strip4.png` | 4 |
| `spr_player_walk` | `spr_player_walk_strip6.png` | 6 |
| `spr_player_backstep` | `spr_player_backstep_strip4.png` | 4 |
| `spr_player_dash` | `spr_player_dash_strip4.png` | 4 |
| `spr_player_ataque` | `spr_player_ataque_strip3.png` | 3 |
| `spr_player_tiro` | `spr_player_tiro_strip3.png` | 3 |
| `spr_player_cura` | `spr_player_cura_strip4.png` | 4 |
| `spr_player_hit` | `spr_player_hit_strip2.png` | 2 |
| `spr_player_visceral` | `spr_player_visceral_strip4.png` | 4 |
| `spr_player_morte` | `spr_player_morte_strip6.png` | 6 |

No **Create do `obj_player`**, troque o struct `spr` inteiro por:

```gml
spr = {
    parado: spr_player_idle,
    andando: spr_player_walk,
    backstep: spr_player_backstep,
    dash: spr_player_dash,
    ataque: spr_player_ataque,
    tiro: spr_player_tiro,
    cura: spr_player_cura,
    hit: spr_player_hit,
    visceral: spr_player_visceral,
    morte: spr_player_morte
};
```

No editor do `obj_player`, troque o **Sprite** de `spr_player` para `spr_player_idle`. Precisa: quando um menu abre logo ao entrar na room (a escolha de arma), o jogo congela antes do primeiro Step do player, e ele apareceria com o sprite do objeto, o retângulo provisório.

**Armas** (pasta `arte/armas/`). Importe **por cima** dos provisórios:

| Sprite | Arquivo | Origem |
|---|---|---|
| `spr_arma_bengala` | `spr_arma_bengala.png` | 3, 3 |
| `spr_arma_machado` | `spr_arma_machado.png` | 4, 8 |
| `spr_arma_cutelo` | `spr_arma_cutelo.png` | 3, 4 |

**Cortes** (pasta `arte/efeitos/`). Crie estes sprites novos (em **Sprites → Efeitos**) e importe `spr_fx_corte` por cima do provisório:

| Sprite | Arquivo | Origem |
|---|---|---|
| `spr_fx_corte_90` | `spr_fx_corte_90_strip4.png` | 23, 23 |
| `spr_fx_corte_120` | `spr_fx_corte_120_strip4.png` | 25, 25 |
| `spr_fx_corte_180` | `spr_fx_corte_180_strip4.png` | 28, 28 |
| `spr_fx_giro_360` | `spr_fx_giro_360_strip4.png` | 29, 29 |
| `spr_fx_estocada` | `spr_fx_estocada_strip3.png` | 0, 4 |
| `spr_fx_corte` (por cima) | `spr_fx_corte_strip4.png` | 25, 25 |

No **scr_dados**, em `dados_armas`, troque o `fx:` de cada golpe:

| Golpe | Variável | fx |
|---|---|---|
| Bengala leve | `_bengala_leve` | `spr_fx_corte_90` |
| Bengala pesado | `_bengala_pesado` | `spr_fx_estocada` |
| Machado leve | `_machado_leve` | `spr_fx_corte_180` |
| Machado pesado | `_machado_pesado` | `spr_fx_giro_360` |
| Cutelo leve | `_cutelo_leve` | `spr_fx_corte_120` |
| Cutelo pesado | `_cutelo_pesado` | `spr_fx_estocada` |

**Teste:** a arma sai da luva do caçador; no golpe, o corpo recua no windup e avança no ativo junto com o corte (a mão fica parada, a arma gira em volta dela); o corte tem o tamanho do alcance (ligue o F3 e compare com o setor vermelho).

---

## Dia 8 — Pistolas, projétil e clarão

Importe **por cima** dos provisórios:

| Sprite | Arquivo | Quadros | Origem |
|---|---|---|---|
| `spr_arma_pistola` | `arte/armas/spr_arma_pistola.png` | 1 | 3, 3 |
| `spr_arma_escopeta` | `arte/armas/spr_arma_escopeta.png` | 1 | 3, 3 |
| `spr_projetil` | `arte/efeitos/spr_projetil.png` | 1 | 4, 1 |
| `spr_fx_disparo` | `arte/efeitos/spr_fx_disparo_strip3.png` | 3 | 0, 3 |

Nenhum código muda. A pistola já é desenhada na mão do quadro de tiro (`x + 3 * lado, y - 12`), e o clarão sai na ponta do sprite de cada pistola.

---

## Dia 10 — Aldeão, foice e sangue

**Aldeão** (pasta `arte/inimigos/`). Todos 32×32, origem **16, 30**:

| Sprite | Arquivo | Quadros |
|---|---|---|
| `spr_aldeao_idle` | `spr_aldeao_idle_strip4.png` | 4 |
| `spr_aldeao_walk` | `spr_aldeao_walk_strip6.png` | 6 |
| `spr_aldeao_ataque` | `spr_aldeao_ataque_strip3.png` | 3 |
| `spr_aldeao_hit` | `spr_aldeao_hit_strip2.png` | 2 |
| `spr_aldeao_stagger` | `spr_aldeao_stagger_strip2.png` | 2 |
| `spr_aldeao_caido` | `spr_aldeao_caido_strip2.png` | 2 |
| `spr_aldeao_morte` | `spr_aldeao_morte_strip6.png` | 6 |

No editor do `obj_aldeao`, troque o **Sprite** para `spr_aldeao_idle` (pelo mesmo motivo do player). No **Create do `obj_aldeao`**, adicione no fim:

```gml
spr = {
    parado: spr_aldeao_idle,
    andando: spr_aldeao_walk,
    ataque: spr_aldeao_ataque,
    hit: spr_aldeao_hit,
    stagger: spr_aldeao_stagger,
    caido: spr_aldeao_caido,
    morte: spr_aldeao_morte
};
```

Importe **por cima** dos provisórios:

| Sprite | Arquivo | Quadros | Origem |
|---|---|---|---|
| `spr_arma_foice` | `arte/armas/spr_arma_foice.png` | 1 | 3, 7 |
| `spr_fx_sangue` | `arte/efeitos/spr_fx_sangue_strip5.png` | 5 | 4, 8 |

**Teste:** a foice sai da mão da frente do Aldeão (a tocha fica erguida na outra); morto, ele cai, a tocha apaga no chão, a poça aparece e o corpo some devagar.

---

## Dia 11 — Anel de parry

| Sprite | Arquivo | Quadros | Origem |
|---|---|---|---|
| `spr_fx_parry` (por cima) | `arte/efeitos/spr_fx_parry_strip4.png` | 4 | 14, 14 |

---

## Dia 12 — Brutamontes

Pasta `arte/inimigos/`. Todos 48×48, origem **24, 45**:

| Sprite | Arquivo | Quadros |
|---|---|---|
| `spr_brutamontes_idle` | `spr_brutamontes_idle_strip4.png` | 4 |
| `spr_brutamontes_walk` | `spr_brutamontes_walk_strip6.png` | 6 |
| `spr_brutamontes_pancada` | `spr_brutamontes_pancada_strip3.png` | 3 |
| `spr_brutamontes_agarrao` | `spr_brutamontes_agarrao_strip3.png` | 3 |
| `spr_brutamontes_stagger` | `spr_brutamontes_stagger_strip2.png` | 2 |
| `spr_brutamontes_caido` | `spr_brutamontes_caido_strip2.png` | 2 |
| `spr_brutamontes_morte` | `spr_brutamontes_morte_strip6.png` | 6 |

No editor do `obj_brutamontes`, troque o **Sprite** para `spr_brutamontes_idle`. No **Create do `obj_brutamontes`**, adicione no fim (depois da linha `ataques = [_pancada, _agarrao];`):

```gml
spr = {
    parado: spr_brutamontes_idle,
    andando: spr_brutamontes_walk,
    ataque: spr_brutamontes_pancada,
    hit: spr_brutamontes_stagger,     // ele não sofre hitstun; fica aqui só por garantia
    stagger: spr_brutamontes_stagger,
    caido: spr_brutamontes_caido,
    morte: spr_brutamontes_morte
};
// Cada ataque com a sua animação
_pancada.spr = spr_brutamontes_pancada;
_agarrao.spr = spr_brutamontes_agarrao;
```

`_pancada` e `_agarrao` são os mesmos structs que estão dentro de `ataques` (struct é passado por referência), então mudar `_pancada.spr` muda o ataque da lista.

**Teste:** no aviso da pancada (branco) ele ergue os dois punhos acima da gaiola e bate com eles no chão, dentro do setor vermelho (ligue o F3 para ver o setor); no aviso do agarrão (vermelho) abre os braços e avança com a garra.

---

## Dias 13 e 14 — Chefe

Faça **depois de terminar o dia 14**: o dia 14 reescreve o Create do chefe inteiro, e o que você colocasse antes se perderia.

**Humano** (pasta `arte/chefes/`). 48×48, origem **24, 45**:

| Sprite | Arquivo | Quadros |
|---|---|---|
| `spr_chefe_idle` | `spr_chefe_idle_strip4.png` | 4 |
| `spr_chefe_walk` | `spr_chefe_walk_strip6.png` | 6 |
| `spr_chefe_ataque` | `spr_chefe_ataque_strip3.png` | 3 |
| `spr_chefe_tiro` | `spr_chefe_tiro_strip3.png` | 3 |
| `spr_chefe_salto` | `spr_chefe_salto_strip3.png` | 3 |
| `spr_chefe_stagger` | `spr_chefe_stagger_strip2.png` | 2 |
| `spr_chefe_caido` | `spr_chefe_caido_strip2.png` | 2 |

**Transformação e besta** (pasta `arte/chefes/`). 64×64, origem **32, 60**:

| Sprite | Arquivo | Quadros |
|---|---|---|
| `spr_chefe_transforma` | `spr_chefe_transforma_strip8.png` | 8 |
| `spr_chefe_besta_idle` | `spr_chefe_besta_idle_strip4.png` | 4 |
| `spr_chefe_besta_corrida` | `spr_chefe_besta_corrida_strip6.png` | 6 |
| `spr_chefe_besta_garra` | `spr_chefe_besta_garra_strip3.png` | 3 |
| `spr_chefe_besta_investida` | `spr_chefe_besta_investida_strip3.png` | 3 |
| `spr_chefe_besta_salto` | `spr_chefe_besta_salto_strip3.png` | 3 |
| `spr_chefe_besta_stagger` | `spr_chefe_besta_stagger_strip2.png` | 2 |
| `spr_chefe_besta_caido` | `spr_chefe_besta_caido_strip2.png` | 2 |
| `spr_chefe_besta_morte` | `spr_chefe_besta_morte_strip8.png` | 8 |

O machado já foi importado no dia 7. O bacamarte do tiro está desenhado no próprio `spr_chefe_tiro` (o Draw esconde o machado durante o tiro).

No editor do `obj_chefe`, troque o **Sprite** para `spr_chefe_idle`.

**1. Create do `obj_chefe`.** Apague o bloco `spr_fase2 = { ... };` que o dia 14 criou (o dos sprites provisórios) e, no lugar dele, cole:

```gml
spr = {
    parado: spr_chefe_idle, andando: spr_chefe_walk, ataque: spr_chefe_ataque,
    hit: spr_chefe_stagger, stagger: spr_chefe_stagger, caido: spr_chefe_caido,
    morte: spr_chefe_stagger, transforma: spr_chefe_transforma
};
spr_fase2 = {
    parado: spr_chefe_besta_idle, andando: spr_chefe_besta_corrida, ataque: spr_chefe_besta_garra,
    hit: spr_chefe_besta_stagger, stagger: spr_chefe_besta_stagger, caido: spr_chefe_besta_caido,
    morte: spr_chefe_besta_morte
};
// Ataques com animação própria
_tiro.spr = spr_chefe_tiro;
_salto.spr = spr_chefe_salto;
_investida.spr = spr_chefe_besta_investida;
_salto2.spr = spr_chefe_besta_salto;
```

- A machadada usa `spr.ataque` e as garras usam `spr_fase2.ataque`, então não precisam de linha própria.
- O humano nunca morre (vira besta na metade da vida); o `morte` dele só existe porque o struct precisa do campo.
- A máscara continua `spr_mask_grande` nas duas fases.

**2. Transformação.** `spr_chefe_transforma` começa no humano, termina exatamente na pose do `spr_chefe_besta_idle` (a troca de sprite no fim não pula) e o machado cai no próprio desenho.

No **scr_inimigo**, função `inimigo_animar`, troque o que está dentro do `case INI.TRANSFORMA` (o comentário e as duas linhas de sprite; o `break;` fica) por:

```gml
            // Animação da transformação: 8 quadros em 90 frames.
            sprite_index = spr.transforma;
            image_index = anim_quadro(estado_timer, 90, sprite_index);
```

No **scr_inimigo**, substitua a função `inimigo_estado_transforma` inteira. O `tem_arma = false` sobe para o primeiro frame (senão o jogo desenha o machado na mão por cima da animação) e entra um tremor no rugido, que começa no quadro 5 (frame 57):

```gml
/// Chefe virando besta: 90 frames parado e invulnerável, depois troca tudo.
function inimigo_estado_transforma() {
    if (estado_timer == 1) {
        tremer_tela(4);
        tem_arma = false;      // o machado cai no desenho da transformação
    }
    if (estado_timer == 57) {
        tremer_tela(6);        // rugido
    }
    if (estado_timer >= 90) {
        fase = 2;
        ataques = ataques_fase2;
        vel = vel_fase2;
        spr = spr_fase2;
        inimigo_trocar(INI.PERSEGUIR);
    }
}
```

**3. Névoa.** Importe **por cima** do `spr_nevoa`: `arte/cenario/spr_nevoa_strip4.png`, 4 quadros, origem **0, 0** (continua 16×16). A instância da névoa é esticada na room; com a arte, o sprite precisa se **repetir** em vez de esticar (esticado, a textura borra).

**obj_nevoa → Draw** (arquivo inteiro):

```gml
// A névoa é o sprite de 16x16 repetido pela área da instância (esticada na room),
// com a textura andando para o lado.
var _alpha = 0.4;
if (fechada) {
    _alpha = 0.8;
}
var _quadro = (current_time div 150) mod sprite_get_number(sprite_index);
for (var i = 0; i < image_xscale; i++) {
    for (var j = 0; j < image_yscale; j++) {
        draw_sprite_ext(sprite_index, _quadro, x + i * 16, y + j * 16, 1, 1, 0, c_white, _alpha);
    }
}
```

- **`current_time`** são os milissegundos desde que o jogo abriu. `div 150` troca de quadro a cada 150 ms, mesmo com o jogo pausado.
- O Step da névoa não muda: ele usa `sprite_width` e `sprite_height`, que já contam a escala.

**Teste** (rm_teste_chefe): o machado sai da mão; no tiro, o machado some e o clarão sai da boca do bacamarte; na metade da vida ele larga o machado, incha, ruge e vira a besta sem pulo; a besta morre, cai e some devagar.

---

## Dia 15 — HUD: ícones e barras

Importe **por cima** dos provisórios (origem **0, 0** em todos, mesmo tamanho):

| Sprite | Arquivo |
|---|---|
| `spr_icone_frasco` | `arte/ui/spr_icone_frasco.png` |
| `spr_icone_bala` | `arte/ui/spr_icone_bala.png` |
| `spr_icone_almas` | `arte/ui/spr_icone_almas.png` |

Crie estes sprites novos (em **Sprites → UI**, origem **0, 0**):

| Sprite | Arquivo | Detalhe |
|---|---|---|
| `spr_hud_moldura` | `arte/ui/spr_hud_moldura.png` | **Nine Slice**: marque *Enabled* e ponha **2** em Left, Top, Right e Bottom |
| `spr_hud_vida` | `arte/ui/spr_hud_vida.png` | preenchimento da vida (4×4) |
| `spr_hud_stamina` | `arte/ui/spr_hud_stamina.png` | preenchimento da stamina (4×2) |
| `spr_hud_chefe` | `arte/ui/spr_hud_chefe.png` | preenchimento da barra do chefe (4×4) |

**Nine slice** divide o sprite em 9 pedaços: os 4 cantos ficam do tamanho original e as bordas e o meio esticam. Assim a moldura estica para qualquer largura sem engrossar a borda.

**obj_game → Draw GUI**: troque o trecho das barras (de `// Vida:` até o `draw_set_colour(c_white);` logo antes de `// Frascos e balas`) por:

```gml
    // Vida: a barra cresce com o HP máximo (100 de vida = 50 px). A moldura é nine-slice.
    var _larg_hp = _p.hp_max / 2;
    draw_sprite_stretched(spr_hud_moldura, 0, 5, 5, _larg_hp + 4, 8);
    if (_p.hp > 0) {
        draw_sprite_stretched(spr_hud_vida, 0, 7, 7, _larg_hp * _p.hp / _p.hp_max, 4);
    }

    // Stamina
    var _larg_st = _p.st_max / 2;
    draw_sprite_stretched(spr_hud_moldura, 0, 5, 13, _larg_st + 4, 6);
    if (_p.st > 0) {
        draw_sprite_stretched(spr_hud_stamina, 0, 7, 15, _larg_st * _p.st / _p.st_max, 2);
    }
    draw_set_colour(c_white);
```

**obj_chefe → Draw GUI**: troque as 5 linhas dos retângulos (de `draw_set_colour(c_black);` até o `draw_set_colour(c_white);` depois do `c_maroon`) por:

```gml
    draw_sprite_stretched(spr_hud_moldura, 0, _x1 - 2, _y1 - 2, _larg + 4, 8);
    draw_sprite_stretched(spr_hud_chefe, 0, _x1, _y1, _larg * hp / hp_max, 4);
    draw_set_colour(c_white);
```

**`draw_sprite_stretched(sprite, quadro, x, y, largura, altura)`** desenha o sprite esticado para caber no retângulo. Com o preenchimento de 4 px de largura, esticar dá uma barra de qualquer tamanho com as mesmas faixas de cor.

---

## Dia 16 — Lanterna e mancha

| Sprite | Arquivo | Quadros | Origem |
|---|---|---|---|
| `spr_lanterna` (por cima) | `arte/cenario/spr_lanterna_strip4.png` | 4 | 8, 31 |
| `spr_mancha` (por cima) | `arte/cenario/spr_mancha_strip4.png` | 4 | 8, 8 |
| `spr_luz` (novo) | `arte/cenario/spr_luz.png` | 1 | 24, 24 |

- **Lanterna:** o `draw_self()` já anima sozinho, na velocidade do sprite. No editor do `spr_lanterna`, ponha a velocidade em **8** quadros por segundo (a chama tremula sem piscar demais).
- **Mancha:** o Draw dela usa o quadro 0. **obj_mancha → Draw** (arquivo inteiro):

```gml
// Pulsa e cintila: a transparência sobe e desce, e o brilho troca de quadro a cada 150 ms.
var _quadro = (current_time div 150) mod sprite_get_number(sprite_index);
draw_sprite_ext(sprite_index, _quadro, x, y, 1, 1, 0, c_white, 0.6 + 0.4 * sin(current_time / 200));
```

**Brilho da lanterna (opcional).** No **obj_lanterna → Draw**, adicione no começo (antes do `draw_self();`):

```gml
// Brilho da chama no chão: a luz é somada à cor do que está embaixo.
gpu_set_blendmode(bm_add);
draw_sprite_ext(spr_luz, 0, x, y - 22, 1, 1, 0, make_colour_rgb(255, 150, 60), 0.35);
gpu_set_blendmode(bm_normal);
```

**`bm_add`** soma as cores em vez de cobrir: o escuro fica igual e o claro fica mais claro, como luz de verdade. Sempre volte para `bm_normal` logo depois.

---

## Dia 18 — Cenário: tileset, objetos e portão

**1. Tileset.** Importe `arte/cenario/spr_tiles_rua.png` como o sprite `spr_tiles_rua` (origem 0, 0). Botão direito nele → **Create → Tile Set**, nome `ts_rua`, **Tile Width 16, Tile Height 16**, sem offset nem separação. O primeiro tile (canto de cima à esquerda) é vazio de propósito: o GameMaker usa o tile 0 como "sem tile".

O mapa de todos os tiles, com número e nome, está em `arte/cenario/previa/tileset_mapa.png`.

**2. Camadas.** Em cada room, no painel **Layers**, crie duas **Tile Layers** com o `ts_rua`:

- `Chao`: chão e muros.
- `Detalhes`: sombra, rachaduras, folhas, sangue, poça, bueiro, passagem (tiles com fundo transparente).

Arraste as duas para **baixo de Instances** e **acima de Background**, com `Detalhes` acima de `Chao`. Tudo que é alto (poste, lanterna, pilar, caixote, carroça, cerca) é objeto, não tile: objeto se ordena pelo `depth = -y` e o player passa na frente ou atrás do jeito certo.

**3. Pintar.** Siga o guia de cada room em `arte/cenario/previa/guia_rm_*.png` (tem grade de 16 px). As regras dos muros, que valem para qualquer room:

| Onde | Tile |
|---|---|
| Muro de cima (a face aparece) | `face 1`, `face 2`, `face com janela`, `face rachada`; nas pontas, `face ponta esquerda` / `face ponta direita` |
| Muro da esquerda | `topo →` (a borda clara fica virada para dentro da room) |
| Muro da direita | `topo ←` |
| Muro de baixo | `topo ↑` |
| Cantos de cima | `topo →` (esquerdo) e `topo ←` (direito) |
| Cantos de baixo | `canto interno ↗` (esquerdo) e `canto interno ↖` (direito) |
| Bloco no meio da room | linha de cima `topo ↖ ↑ ↗`, linhas do meio `topo ← centro →`, última linha de face |
| Abertura no muro do lado (porta) | o tile do muro logo acima da abertura vira `face sozinha`; o de baixo, `topo ↗` (muro da esquerda) ou `topo ↖` (muro da direita) |
| Porta no muro de cima | `escada esquerda`, `escada meio`, `escada direita` |
| Vão do portão do atalho | `pedra` no `Chao` e `passagem escura` no `Detalhes` |
| Chão | `pedra 1` a `4` misturadas; nas 2 linhas abaixo do muro de cima, `calçada`, com `meio-fio (rua embaixo)` na segunda |
| Detalhes | `sombra do muro` na linha logo abaixo de toda face; o resto espalhado, pouco |

Com o cenário pintado, **desmarque Visible no `obj_parede`**: as paredes continuam lá, invisíveis, em cima dos muros desenhados. (O `obj_pilar` e o `obj_atalho` são filhos dele, mas o Visible não é herdado: continuam aparecendo.)

**4. Portão do atalho.** Importe **por cima** do `spr_atalho`: `arte/cenario/spr_atalho.png`, origem **16, 16**. Tem o mesmo tamanho do provisório (32×16), então a colisão não muda.

**5. Objetos do cenário.** Importe os sprites (pasta `arte/cenario/`) e, em cada um, **Collision Mask → Mode: Manual, Type: Rectangle** com os valores da tabela (só a base bloqueia):

| Sprite | Origem | Máscara (Left, Top, Right, Bottom) |
|---|---|---|
| `spr_poste` | 8, 47 | 5, 43, 10, 47 |
| `spr_caixote` | 8, 19 | 1, 10, 14, 19 |
| `spr_barril` | 8, 19 | 2, 12, 13, 19 |
| `spr_carroca` | 24, 31 | 4, 16, 43, 31 |
| `spr_caixao` | 8, 27 | 2, 20, 13, 27 |
| `spr_cerca` | 8, 23 | 0, 20, 15, 23 |

Para cada um, crie um objeto (`obj_poste`, `obj_caixote`, `obj_barril`, `obj_carroca`, `obj_caixao`, `obj_cerca`) com o sprite e **Parent `obj_pilar`**. Não precisa de código: o pai já calcula o `depth`, e como o `obj_pilar` é filho do `obj_parede`, eles bloqueiam o player. A cerca encaixa lado a lado: ponha uma a cada 16 px. Não bloqueie as passagens entre as portas.

Para ficar igual à prévia, ponha nestas posições (x, y é a base do objeto; os guias de cada room já mostram tudo no lugar). Várias não caem na grade de 16: coloque o objeto, dê duplo clique nele e digite o **X** e o **Y**.

| Room | Objeto | Posições (x, y) |
|---|---|---|
| `rm_praca` | `obj_poste` | (190, 90) · (300, 90) |
| `rm_praca` | `obj_barril` | (330, 150) · (342, 154) |
| `rm_praca` | `obj_caixote` | (356, 148) |
| `rm_praca` | `obj_carroca` | (150, 200) |
| `rm_praca` | `obj_caixao` | (290, 60) |
| `rm_praca` | `obj_cerca` | x de 60 a 124, de 16 em 16, y 60 |
| `rm_rua` | `obj_poste` | (120, 52) · (300, 52) · (460, 52) · (620, 52) · (780, 52) |
| `rm_rua` | `obj_barril` | (60, 330) · (72, 334) · (900, 330) |
| `rm_rua` | `obj_caixote` | (86, 328) |
| `rm_rua` | `obj_caixao` | (540, 52) |
| `rm_rua` | `obj_carroca` | (740, 300) |
| `rm_mercado` | `obj_poste` | (60, 52) · (580, 52) |
| `rm_mercado` | `obj_caixote` | (100, 100) · (114, 104) · (520, 470) |
| `rm_mercado` | `obj_barril` | (128, 98) · (536, 474) |
| `rm_mercado` | `obj_carroca` | (540, 160) |
| `rm_mercado` | `obj_caixao` | (60, 500) |
| `rm_portao` | `obj_poste` | (196, 52) · (284, 52) |
| `rm_portao` | `obj_cerca` | x de 40 a 168, de 16 em 16, y 50; x de 312 a 440, de 16 em 16, y 50 |
| `rm_arena_1` | `obj_poste` | (60, 52) · (420, 52) |
| `rm_arena_1` | `obj_caixao` | (40, 340) · (440, 340) |


**Brilho do poste (opcional).** **obj_poste → Draw**:

```gml
draw_self();
gpu_set_blendmode(bm_add);
draw_sprite_ext(spr_luz, 0, x, y - 40, 1, 1, 0, make_colour_rgb(255, 150, 60), 0.3);
gpu_set_blendmode(bm_normal);
```

---

## Dia 19 — Título, fonte, mira, ícones do menu e sons

**1. Sprites** (pasta `arte/ui/`, em **Sprites → UI**):

| Sprite | Arquivo | Quadros | Origem |
|---|---|---|---|
| `spr_logo` | `spr_logo.png` | 1 | 57, 17 (o centro) |
| `spr_fundo_titulo` | `spr_fundo_titulo.png` | 1 | 0, 0 |
| `spr_fonte` | `spr_fonte_strip106.png` | 106 | 0, 0 |
| `spr_mira` | `spr_mira.png` | 1 | 4, 4 |
| `spr_icone_vida`, `spr_icone_stamina`, `spr_icone_forca`, `spr_icone_destreza` | mesmo nome, `.png` | 1 | 0, 0 |
| `spr_icone_bengala`, `spr_icone_machado`, `spr_icone_cutelo` | mesmo nome, `.png` | 1 | 0, 0 |
| `spr_icone_pistola`, `spr_icone_escopeta` | mesmo nome, `.png` | 1 | 0, 0 |

**2. Fundo do título.** Abra a `rm_titulo`, selecione a camada **Background**, em **Sprite** escolha `spr_fundo_titulo` e deixe a **Colour** da camada em **branco** (FFFFFF). A cor da camada tinge o sprite: com cinza ou preto, o fundo fica escuro.

**3. Fonte e mira.** No **Create do `obj_game`**, adicione logo depois da linha `display_set_gui_size(LARGURA_BASE, ALTURA_BASE);`:

```gml
// Fonte bitmap: cada quadro do spr_fonte é um caractere, na mesma ordem desta string.
fnt_pixel = font_add_sprite_ext(spr_fonte, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,:;!?-+()<>/'\"%_*=ÁÀÂÃÉÊÍÓÔÕÚáàâãéêíóôõúÇç ", true, 1);
// A mira substitui a seta do Windows.
window_set_cursor(cr_none);
```

- **`font_add_sprite_ext(sprite, letras, proporcional, espaço)`**: `true` faz cada letra ocupar só a largura dela (o "i" é fino, o "m" é largo); `1` é o espaço entre letras.
- O **`\"`** no meio da string é a aspa dupla: sem a barra, a aspa fecharia a string.
- A string termina com um **espaço**: é o último quadro da fonte. Não apague.

Troque `draw_set_font(fnt_hud);` por `draw_set_font(obj_game.fnt_pixel);` em dois lugares: no começo do **Draw GUI do `obj_game`** e no começo do **Draw GUI do `obj_menu`**.

No **Draw GUI do `obj_game`**, adicione antes da linha `// Fade: tela preta por cima de tudo.`:

```gml
// Mira no lugar do cursor
draw_sprite(spr_mira, 0, device_mouse_x_to_gui(0), device_mouse_y_to_gui(0));
```

**`device_mouse_x_to_gui(0)`** converte a posição do mouse para as coordenadas do Draw GUI (320×180).

**4. Logo.** No **Draw GUI do `obj_menu`**:

- Troque `draw_set_alpha(0.75);` por `draw_set_alpha(tipo == "titulo" ? 0.3 : 0.75);`. No título o escurecimento é leve, para o fundo aparecer.
- Troque a linha `draw_text(LARGURA_BASE / 2, 30, titulo);` por:

```gml
if (tipo == "titulo") {
    draw_sprite(spr_logo, 0, LARGURA_BASE / 2, 30);
} else {
    draw_text(LARGURA_BASE / 2, 30, titulo);
}
```

**`a ? b : c`** é um `if` numa linha: vale `b` se `a` for verdade, senão `c`.

**5. Ícones nos menus.** No **Create do `obj_menu`**, adicione `icones = [];`. No **scr_menu**, função `menu_abrir`, adicione uma linha logo depois de cada um destes `_m.opcoes = ...`:

- no `case "nivel":` → `_m.icones = [spr_icone_vida, spr_icone_stamina, spr_icone_forca, spr_icone_destreza, -1];`
- no `case "arma":` → `_m.icones = [spr_icone_bengala, spr_icone_machado, spr_icone_cutelo];`
- no `case "pistola":` → `_m.icones = [spr_icone_pistola, spr_icone_escopeta];`

O `-1` é "sem ícone" (a opção Voltar). No **Draw GUI do `obj_menu`**, troque o `for` das opções inteiro por:

```gml
for (var i = 0; i < array_length(opcoes); i++) {
    var _texto = opcoes[i];
    if (i == sel) {
        draw_set_colour(c_yellow);
        _texto = "> " + opcoes[i] + " <";
    } else {
        draw_set_colour(c_white);
    }
    draw_text(LARGURA_BASE / 2, 60 + i * 14, _texto);
    // Ícone à esquerda do texto (menus de arma, pistola e nível)
    if (i < array_length(icones) && icones[i] != -1) {
        draw_sprite(icones[i], 0, LARGURA_BASE / 2 - string_width(_texto) / 2 - 14, 60 + i * 14);
    }
}
```

**6. Sons.** Os 9 sons do Passo 2 do dia 19 já estão prontos em `audio/`, com os mesmos nomes (`snd_golpe.wav`, `snd_acerto.wav`...). Para cada um: botão direito em **Sounds** → **Create → Sound**, dê o nome da tabela do dia 19 e importe o `.wav`. Não precisa gerar no jsfxr.

---

## Extras (opcional)

Dois efeitos prontos que o código não usa. Uma linha cada:

- **Poeira na esquiva** (`spr_fx_poeira`, `arte/efeitos/spr_fx_poeira_strip4.png`, 4 quadros, origem 8, 8). No **scr_player**, função `player_tentar_esquivar`, logo depois da linha `player_comecar_esquiva();`:

```gml
        fx_criar(x, y, spr_fx_poeira, 0, 1);
```

- **Impacto no pouso do salto** (`spr_fx_impacto`, `arte/efeitos/spr_fx_impacto_strip4.png`, 4 quadros, origem 8, 8). No **scr_inimigo**, função `inimigo_pousar`, logo depois da linha `tremer_tela(3);`:

```gml
    fx_criar(x, y - 4, spr_fx_impacto, 0, 1);
```

---

## V1.1 — Dama do Relógio (chefe 2)

A arte já existe, para quando você fizer o chefe 2 (não está no tutorial da V1):

- Animações em `arte/chefes/spr_dama_*` (idle, walk, ataque, estocada, passo, stagger, caido, transforma, morte). 32×32, origem **16, 30**: o mesmo tamanho do caçador, então use `mask_index = spr_mask_player`.
- Lâmina: `spr_arma_dama_longa` e, na fase 2, `spr_arma_dama_longa_sangue` (27×5, origem 2, 2). Ela é a `arma_sprite`, com `mao_x = 2` e `mao_y = 10`.
- A adaga da outra mão está desenhada no corpo.
- Fase 2: `spr_fx_aura_sangue` (32×32, origem 16, 30, 4 quadros), desenhada **antes** do corpo no Draw, em `x, _dy`.

---

## Se deu errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| Personagem flutua, afunda no chão ou "pula" ao trocar de animação | Origem errada | Confira em `arte/origens.md`. Todas as animações do mesmo personagem têm a mesma origem. |
| A animação mostra a tira inteira espremida, ou um quadro só | A tira não foi cortada | O arquivo precisa ter `_stripN` no nome **na hora de importar**. Apague o sprite e importe de novo. |
| `spr_player_idle` não existe (erro ao compilar) | O sprite ficou com `_strip4` no nome | Renomeie para o nome da tabela. |
| A arma gira em volta do lugar errado | Origem da arma errada | A origem da arma é no cabo (tabela do dia 7). |
| A arte ficou borrada | Interpolação ligada | Dia 1, passo 1: **Interpolate colours between pixels** desmarcado. |
| `variable not set: transforma` | O `case INI.TRANSFORMA` usa `spr.transforma`, mas o struct do chefe não tem | Parte "Dias 13 e 14", passo 1. |
| A névoa aparece borrada, esticada | O Draw ainda estica o sprite | Parte "Dias 13 e 14", passo 3. |
| A moldura da barra fica com a borda grossa | Nine Slice desligado no `spr_hud_moldura` | Parte "Dia 15". |
| Letras erradas (um "B" onde devia ser "A") | A string da fonte não bate com a ordem da imagem | Copie a string do Dia 19 de novo, inteira, com o espaço no fim. |
| O player atravessa o caixote, ou trava longe dele | Máscara do sprite errada | Parte "Dia 18", tabela das máscaras. |
| O player aparece por cima da cerca quando está atrás dela | A cerca foi pintada como tile | Cerca, poste, caixote etc. são objetos filhos do `obj_pilar`. |
