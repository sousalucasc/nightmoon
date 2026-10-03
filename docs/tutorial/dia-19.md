# Dia 19 — Título, fim e sons

**Quando:** sex 23/10 · **Tempo:** ~3 h

**No fim do dia:** o jogo abre numa tela de título (Começar / Sair). Derrotar o chefe leva, depois de 4 segundos, à tela de fim com tempo de jogo e número de mortes. Golpes, acertos, tiros, parry, dano, morte, lanterna e névoa têm som.

---

## Passo 1 — Título e fim (40 min)

Crie as rooms **`rm_titulo`** e **`rm_fim`**, as duas **320×180**, vazias.

**obj_game → Create** (troque a última linha, `room_goto(...)`, por esta)
<!-- src: objects/obj_game/Create_0.gml @troca: room_goto( -->
```gml
room_goto(rm_titulo);
```

**obj_game → Create** (adicione antes da linha `room_goto(rm_titulo);`)
<!-- src: objects/obj_game/Create_0.gml @antes: room_goto(rm_titulo); -->
```gml
fim_timer = 0;      // contagem até a tela de fim depois do chefe
```

**scr_jogo**, na função `jogo_novo` (troque a linha `lanterna_sala = rm_teste;` por esta)
<!-- src: scripts/scr_jogo.gml @troca: lanterna_sala = rm_teste; -->
```gml
        lanterna_sala = rm_praca;   // onde volta ao morrer antes de descansar
```

**obj_game → Room Start** (adicione no fim)
<!-- src: objects/obj_game/Other_4.gml @fim -->
```gml
// Tela de título: abre o menu do título.
if (room == rm_titulo) {
    menu_abrir("titulo");
}
```

**scr_menu** (substitua a função `menu_confirmar`)
<!-- src: scripts/scr_menu.gml #menu_confirmar -->
```gml
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
        case "titulo":
            if (sel == 0) {
                jogo_novo();
                trocar_room(rm_praca);
            } else {
                game_end();
            }
            instance_destroy();
            break;
    }
}
```

**scr_inimigo** (substitua a função `inimigo_morrer`)
<!-- src: scripts/scr_inimigo.gml #inimigo_morrer -->
```gml
function inimigo_morrer() {
    obj_game.almas += almas;
    array_push(obj_game.mortos, chave);   // não renasce até descansar
    fx_criar(x, y - 10, spr_fx_sangue, 0, 1);
    som(snd_morte);
    if (e_chefe) {
        obj_game.chefe_morto = true;
        obj_game.fim_timer = 240;         // 4 segundos até a tela de fim
        mostrar_texto("CAÇA ENCERRADA");
    }
    inimigo_trocar(INI.MORTE);
}
```

**obj_game → Step** (adicione no fim)
<!-- src: objects/obj_game/Step_0.gml @fim -->
```gml
// Chefe derrotado: depois de 4 segundos, tela de fim.
if (fim_timer > 0) {
    fim_timer -= 1;
    if (fim_timer == 0) {
        trocar_room(rm_fim);
    }
}

// Tela de fim: F volta ao título.
if (room == rm_fim && aperta_interagir && !fade_indo) {
    trocar_room(rm_titulo);
}
```

**obj_game → Draw GUI** (adicione antes da linha `// Fade: tela preta por cima de tudo.`)
<!-- src: objects/obj_game/Draw_64.gml @antes: // Fade: tela preta por cima de tudo. -->
```gml
// Tela de fim
if (room == rm_fim) {
    var _seg = tempo div 60;   // frames → segundos
    draw_set_halign(fa_center);
    draw_text(LARGURA_BASE / 2, 50, "FIM DA VERSÃO 1");
    draw_text(LARGURA_BASE / 2, 80, "Tempo: " + string(_seg div 60) + " min " + string(_seg mod 60) + " s");
    draw_text(LARGURA_BASE / 2, 96, "Mortes: " + string(mortes));
    draw_text(LARGURA_BASE / 2, 130, "F: voltar ao título");
    draw_set_halign(fa_left);
}

```

- **O "Começar" chama `jogo_novo()`**: tudo volta ao zero (almas, atributos, atalho, chefe), e o menu de armas aparece de novo ao chegar na praça.
- **`tempo div 60`**: o tempo é contado em frames; 60 frames = 1 segundo. `_seg div 60` são os minutos e `_seg mod 60` os segundos que sobram.

## Passo 2 — Sons (60 min)

**Os 9 sons já estão prontos em `audio/`**, com os nomes da tabela abaixo: é só criar cada som e importar o `.wav` (parte **Dia 19** do [Apêndice A](apendice-a-arte.md)). Se quiser trocar algum:

**Onde achar sons de graça:**
- **Kenney** (kenney.nl → Assets → Audio): pacotes em domínio público (CC0), podem ir no jogo sem créditos. "Impact Sounds" e "RPG Audio" têm quase tudo.
- **jsfxr** (sfxr.me): gera sons retrô no navegador (botões "Hit/Hurt", "Explosion"…). Exporta `.wav`.

Crie estes sons (botão direito → **Create → Sound**, e escolha o arquivo):

| Som | Quando toca | Sugestão |
|---|---|---|
| `snd_golpe` | começo de cada golpe | "swish", ar cortando |
| `snd_acerto` | inimigo apanha | impacto seco, carne |
| `snd_tiro` | pistola | estalo curto |
| `snd_escopeta` | escopeta | estouro grave |
| `snd_parry` | parry certo | metal agudo, "tink" |
| `snd_dano` | player apanha | impacto grave |
| `snd_morte` | inimigo morre | baque |
| `snd_lanterna` | descansar | sino ou chama |
| `snd_nevoa` | névoa fecha | grave longo |

**scr_util** (nova função, adicione no fim)
<!-- src: scripts/scr_util.gml #som -->
```gml
/// Toca um som com uma pequena variação de tom (repetido, cansa menos o ouvido).
function som(_som) {
    var _s = audio_play_sound(_som, 1, false);
    audio_sound_pitch(_s, random_range(0.92, 1.08));
}
```

Agora, uma linha em cada lugar:

**scr_player**, na função `player_comecar_golpe` (logo depois da linha `player_gastar_stamina(golpe.stamina);`)
<!-- src: scripts/scr_player.gml @depois: player_gastar_stamina(golpe.stamina); -->
```gml
    som(snd_golpe);
```

**scr_player**, na função `player_disparar` (logo depois da linha do `fx_criar` do clarão)
<!-- src: scripts/scr_player.gml @depois: spr_fx_disparo, ataque_dir, 1); -->
```gml
    if (_p.projeteis > 1) {
        som(snd_escopeta);
    } else {
        som(snd_tiro);
    }
```

**scr_combate**, na função `inimigo_dano` (logo depois da linha do `fx_criar` do sangue)
<!-- src: scripts/scr_combate.gml @depois: fx_criar(x, y - 10, spr_fx_sangue, irandom(359), 1); -->
```gml
            som(snd_acerto);
```

**scr_combate**, na função `player_dano` (logo depois da linha `tremer_tela(2);` — a primeira do arquivo)
<!-- src: scripts/scr_combate.gml @depois: tremer_tela(2); -->
```gml
            som(snd_dano);
```

**scr_combate**, na função `projetil_acertar_inimigo` (logo depois da linha do `fx_criar` do parry)
<!-- src: scripts/scr_combate.gml @depois: fx_criar(_alvo.x, _alvo.y - 12, spr_fx_parry, 0, 1); -->
```gml
        som(snd_parry);
```

**scr_jogo**, na função `lanterna_descansar` (logo depois da linha `function lanterna_descansar(_lanterna) {`)
<!-- src: scripts/scr_jogo.gml @depois: function lanterna_descansar(_lanterna) { -->
```gml
    som(snd_lanterna);
```

**obj_nevoa → Step** (logo depois da linha `obj_chefe.acordado = true;`)
<!-- src: objects/obj_nevoa/Step_0.gml @depois: obj_chefe.acordado = true; -->
```gml
        som(snd_nevoa);
```

(O `snd_morte` já entrou no `inimigo_morrer` do passo 1.)

## Passo 3 — Música (opcional, 15 min)

Se tiver uma música em loop (`snd_musica`), toque no começo da praça e deixe tocando:

```gml
// No Room Start do obj_game, no fim:
if (room == rm_praca && !audio_is_playing(snd_musica)) {
    audio_play_sound(snd_musica, 0, true);   // true = loop
}
```

---

## Arte do dia

Com a arte pronta, faça agora a parte **Dia 19** do [Apêndice A](apendice-a-arte.md).

## Teste do dia

- [ ] O jogo abre no título. "Começar" → praça → escolha de armas. "Sair" fecha.
- [ ] Cada ação faz barulho, e golpes repetidos variam um pouco o tom.
- [ ] Vença o chefe: "CAÇA ENCERRADA", 4 segundos depois a tela de fim com tempo e mortes.
- [ ] F na tela de fim volta ao título; "Começar" de novo zera tudo.
- [ ] Uma partida completa, do título ao fim, **sem apertar F3 nenhuma vez**.

## Se deu errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| Tela preta ao abrir | `rm_titulo` não existe ou o menu não abre | Passo 1 (Room Start). |
| `snd_... not set` | Som não criado ou nome diferente | Passo 2. |
| Som alto/baixo demais | Ajuste o **Volume** no editor do som | — |
| "Começar" leva ao chefe morto | `jogo_novo()` não chamado | Passo 1. |

## Commit

`dia 19: título, fim e sons`
