# Dia 6 — As três armas, escala e hyper armor

**Quando:** sáb 10/10 · **Tempo:** ~3 h

**No fim do dia:** as 3 armas (Bengala, Machado, Cutelo) funcionam, trocadas pelas teclas 1, 2 e 3 no modo debug. O dano escala com Força e Destreza. O giro do machado tem hyper armor, e a esquiva corta o fim de qualquer golpe.

## O que você vai aprender

- Por que **dados separados do código** valem ouro: 3 armas sem nenhum `if` por arma.
- **Escala de atributo** (a fórmula do GDD).
- **Hyper armor**: tomar dano sem ser interrompido.
- **Cancelamento**: sair do recovery com uma esquiva.

---

## Passo 1 — Sprites provisórios das armas (15 min)

A arma vai ser desenhada separada do corpo, girando para a mira (amanhã). Crie estes sprites, todos **apontando para a direita**, com a **origem no cabo** (ponta esquerda, no meio da altura):

| Sprite | Tamanho | Cor | Origem |
|---|---|---|---|
| `spr_arma_bengala` | 20×2 | prata | x 0, y 1 |
| `spr_arma_machado` | 22×4 | cinza | x 0, y 2 |
| `spr_arma_cutelo` | 18×3 | prata escuro | x 0, y 1 |
| `spr_fx_corte` | 20×4 | branco | x 0, y 2 |

O `spr_fx_corte` é o "risco" do golpe (efeito visual). Quando a arte chegar, cada tipo de golpe ganha seu próprio efeito; por enquanto, todos usam este.

## Passo 2 — Dados das três armas (30 min)

**scr_dados** (substitua a função `dados_armas`)
<!-- src: scripts/scr_dados.gml #dados_armas -->
```gml
function dados_armas() {
    // Um golpe: windup, ativo e recovery em frames;
    // alcance e avanço em pixels; arco em graus.

    // --- Bengala-lâmina (Destreza): rápida, curta, combo longo ---
    var _bengala_leve = {
        windup: 5, ativo: 3, recovery: 8,
        dano: 9, stamina: 10,
        alcance: 22, arco: 90, avanco: 4,
        hyper: false, fx: spr_fx_corte
    };
    var _bengala_pesado = {
        windup: 14, ativo: 4, recovery: 14,
        dano: 22, stamina: 25,
        alcance: 34, arco: 30, avanco: 20,
        hyper: false, fx: spr_fx_corte
    };

    // --- Machado de caça (Força): lento, largo, dano alto ---
    var _machado_leve = {
        windup: 14, ativo: 5, recovery: 16,
        dano: 24, stamina: 22,
        alcance: 28, arco: 180, avanco: 6,
        hyper: false, fx: spr_fx_corte
    };
    var _machado_pesado = {
        windup: 22, ativo: 8, recovery: 22,
        dano: 38, stamina: 35,
        alcance: 30, arco: 360, avanco: 0,
        hyper: true, fx: spr_fx_corte
    };

    // --- Cutelo serrado (híbrida): médio, versátil ---
    var _cutelo_leve = {
        windup: 8, ativo: 4, recovery: 11,
        dano: 14, stamina: 15,
        alcance: 25, arco: 120, avanco: 5,
        hyper: false, fx: spr_fx_corte
    };
    var _cutelo_pesado = {
        windup: 16, ativo: 5, recovery: 16,
        dano: 28, stamina: 28,
        alcance: 32, arco: 60, avanco: 10,
        hyper: false, fx: spr_fx_corte
    };

    global.armas = {
        bengala: {
            nome: "Bengala-lâmina",
            esc_for: 0.1,
            esc_des: 1.0,
            sprite: spr_arma_bengala,
            leves: [_bengala_leve, _bengala_leve, _bengala_leve, _bengala_leve],
            pesado: _bengala_pesado
        },
        machado: {
            nome: "Machado de caça",
            esc_for: 1.0,
            esc_des: 0.1,
            sprite: spr_arma_machado,
            leves: [_machado_leve, _machado_leve],
            pesado: _machado_pesado
        },
        cutelo: {
            nome: "Cutelo serrado",
            esc_for: 0.6,
            esc_des: 0.6,
            sprite: spr_arma_cutelo,
            leves: [_cutelo_leve, _cutelo_leve, _cutelo_leve],
            pesado: _cutelo_pesado
        }
    };
}
```

Olhe o que **não** mudou: o estado de ataque. Ele lê `golpe.windup`, `golpe.arco`… de qualquer arma. A bengala tem combo de 4 porque a lista `leves` tem 4 itens. O giro do machado acerta em volta porque o arco é 360. **Nenhum `if (arma == machado)` em lugar nenhum.** É isso que "dados separados do código" quer dizer.

As letras de escala do GDD viraram números: **A = 1,0**, **C = 0,6**, **E = 0,1**.

## Passo 3 — Atributos e teclas de teste (20 min)

**obj_game → Create** (adicione antes de `room_goto`)
<!-- src: objects/obj_game/Create_0.gml @antes: room_goto -->
```gml
// --- Atributos (sobem com almas no dia 17) ---
atr_forca = 0;
atr_destreza = 0;
```

**obj_game → Begin Step** (adicione no fim)
<!-- src: objects/obj_game/Step_1.gml @fim -->
```gml
// Teclas de teste (só com o F3 ligado)
if (debug) {
    if (keyboard_check_pressed(ord("1"))) arma = global.armas.bengala;
    if (keyboard_check_pressed(ord("2"))) arma = global.armas.machado;
    if (keyboard_check_pressed(ord("3"))) arma = global.armas.cutelo;
    if (keyboard_check_pressed(ord("7"))) atr_forca += 1;
    if (keyboard_check_pressed(ord("8"))) atr_destreza += 1;
    if (keyboard_check_pressed(ord("0"))) {
        atr_forca = 0;
        atr_destreza = 0;
    }
}
```

Um `if` sem chaves vale só para a linha de baixo (ou a mesma linha). Use assim só em coisas curtas como essas.

Adicione o evento **Draw GUI** no `obj_game`:

**obj_game → Draw GUI** (arquivo inteiro)
<!-- src: objects/obj_game/Draw_64.gml -->
```gml
// Draw GUI: desenhado por cima de tudo, em coordenadas de tela (320x180).
if (debug) {
    draw_text(4, 4, "Arma: " + arma.nome);
    draw_text(4, 18, "FOR " + string(atr_forca) + "  DES " + string(atr_destreza));
}
```

O **Draw GUI** não segue a câmera: (4, 4) é sempre o canto da tela. É onde vão HUD e menus.

## Passo 4 — Dano com escala e hyper armor (30 min)

**scr_combate** (nova função, adicione no fim)
<!-- src: scripts/scr_combate.gml #dano_escalado -->
```gml
/// Dano de arma com a escala de Força e Destreza (GDD seção 9).
function dano_escalado(_base, _esc_for, _esc_des) {
    var _bonus = _esc_for * 0.08 * obj_game.atr_forca + _esc_des * 0.08 * obj_game.atr_destreza;
    return round(_base * (1 + _bonus));
}
```

Exemplo: Machado leve (24) com Força 5: `24 × (1 + 1,0 × 0,08 × 5) = 24 × 1,4 = 33,6 → 34`. A mesma Força 5 na Bengala (escala 0,1) quase não muda nada.

**scr_combate** (substitua a função `player_dano`)
<!-- src: scripts/scr_combate.gml #player_dano -->
```gml
/// Aplica dano no player. _de_x, _de_y: de onde veio o golpe (para o empurrão).
/// Devolve true se o dano entrou.
function player_dano(_dano, _de_x, _de_y) {
    var _entrou = false;
    with (obj_player) {
        if (!invulneravel && invul_timer <= 0 && estado != PL.MORTE) {
            _entrou = true;
            hp -= _dano;
            // Hyper armor: golpe com a flag não é interrompido no windup nem no ativo.
            var _hyper = (estado == PL.ATAQUE && golpe.hyper && estado_timer <= golpe.windup + golpe.ativo);
            if (hp <= 0) {
                hp = 0;
                player_trocar(PL.MORTE);
            } else if (_hyper) {
                invul_timer = 10;   // o dano entra, mas o golpe continua
            } else {
                kb_dir = point_direction(_de_x, _de_y, x, y);
                kb_vel = 2 * 10 / 18;
                kb_desacel = kb_vel / 18;
                player_trocar(PL.HITSTUN);
            }
        }
    }
    return _entrou;
}
```

Com hyper armor você **toma o dano**, mas o golpe não para. É a troca do giro do machado: aguenta porrada para terminar o golpe.

## Passo 5 — Escala no golpe e cancelamento (30 min)

**scr_player** (substitua a função `player_estado_ataque`)
<!-- src: scripts/scr_player.gml #player_estado_ataque -->
```gml
function player_estado_ataque() {
    var _arma = obj_game.arma;
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

        var _dano = dano_escalado(golpe.dano, _arma.esc_for, _arma.esc_des);
        var _novos = golpe_setor(x, y, ataque_dir, golpe.alcance, golpe.arco, obj_boneco, acertados);
        for (var i = 0; i < array_length(_novos); i++) {
            array_push(acertados, _novos[i]);
            inimigo_dano(_novos[i], _dano);
        }
    } else {
        // Recovery: um leve apertado aqui continua o combo.
        if (!golpe_pesado && player_tentar_atacar()) return;
        // Na segunda metade do recovery, a esquiva corta o golpe.
        if (estado_timer > _fim_ativo + golpe.recovery / 2) {
            if (player_tentar_esquivar()) return;
        }
    }

    if (estado_timer >= _fim_total) {
        player_trocar(PL.LIVRE);
    }
}
```

**Por que só a segunda metade?** Se a esquiva cortasse o recovery inteiro, atacar nunca teria risco. Na primeira metade você está preso: é a janela em que o inimigo te pune.

---

## Teste do dia

Ligue o F3.

- [ ] 1, 2, 3 trocam a arma; o nome aparece no canto.
- [ ] Bengala: combo de 4, rápido, curto. Pesado: estocada que avança bastante.
- [ ] Machado: combo de 2, lento, setor de meia-volta. Pesado: giro que acerta atrás.
- [ ] Cutelo: igual ao dia 5.
- [ ] Tecla 7 (Força) aumenta muito o dano do machado e quase nada da bengala. Tecla 8 (Destreza): o contrário. Tecla 0 zera.
- [ ] Giro do machado dentro da armadilha vermelha: toma o dano, mas o giro não para.
- [ ] Espaço no fim de um golpe corta o recovery e esquiva; no começo do recovery, não.

## Se deu errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| `variable not set: spr_fx_corte` (ou de uma arma) | Sprite não criado, ou nome diferente | Passo 1. |
| Tecla 2 não troca a arma | F3 desligado (as teclas só valem com o debug) | Ligue o F3. |
| Machado pesado não acerta atrás | `arco: 360` digitado errado | Passo 2. |
| Dano não muda com a Força | O golpe ainda usa `golpe.dano` em vez de `_dano` | Passo 5. |
| Texto do debug sobreposto/ilegível | Normal com a fonte padrão; no dia 15 entra a fonte do HUD | — |

## Commit

`dia 6: três armas, escala, hyper armor`
