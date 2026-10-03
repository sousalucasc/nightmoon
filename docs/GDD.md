# Nightmoon — GDD enxuto (Versão 1)

Soulslike top-down 3/4, pixel art, GameMaker. Referência: Bloodborne.

| Parâmetro | Valor |
|---|---|
| Prazo da V1 | 3 semanas, ~60 h (2–3 h/dia) |
| Frame rate | 60 fps — toda duração neste documento é em frames |
| Resolução base | 320×180 (janela padrão 1280×720 = 4×; tela cheia 1920×1080 = 6×) |
| Tile | 16×16 |
| Controle | teclado + mouse (gamepad na V1.1) |
| Sprites | corpo em 2 lados (direita + espelho); arma e golpe são sprites separados que giram para a mira |

Todos os números são ponto de partida. Ajuste jogando.

---

## 1. Resumo

Uma cidade sob uma lua que não se põe. Os moradores viraram bestas. Você é um caçador.
Combate agressivo: esquiva com iframes, parry com arma de fogo no timing do ataque, visceral no inimigo atordoado. Almas sobem atributos.

## 2. Escopo

### V1 (3 semanas)

| Item | Quantidade |
|---|---|
| Player | 1, kit completo (seção 5) |
| Armas corpo a corpo | 3 (Destreza, Força, híbrida) |
| Pistolas | 2 (pistola, escopeta) |
| Inimigos | 2 (Aldeão, Brutamontes) |
| Chefes | 1 (Caçador caído, 2 fases) |
| Rooms | título, praça (lanterna), rua, mercado, portão, arena, fim |

**Pronto quando:** dá para jogar do título até o fim, derrotando o Chefe 1, com qualquer combinação de arma + pistola.

### V1.1 (depois, nesta ordem)

| Item | Horas estimadas |
|---|---|
| Chefe 2 (Dama do Relógio, inspirada na Lady Maria) + Área 2 + lanterna 2 | 12 |
| Inimigo 3: Cão | 4 |
| Gamepad | 2 |
| Rally | 3 |
| Save | 3 |

### Fora do escopo

- Armas transformáveis (trick weapons)
- Lock-on (a mira no mouse substitui)
- Loja, inventário, itens além de frasco e bala
- NPCs e diálogos
- Menu de equipamento (arma é escolhida uma vez, no início)

## 3. Loop

| Escala | Loop |
|---|---|
| Combate (segundos) | ler o windup → esquivar (seguro, gasta stamina) ou atirar no timing (arriscado, abre visceral) → punir no recovery → recuar antes da stamina zerar |
| Área (minutos) | lanterna → grupos de inimigos → almas → atalho de volta à lanterna → avançar → névoa do chefe |
| Build | almas → subir nível na lanterna → Força ou Destreza conforme a arma |
| Morte | almas ficam na mancha de sangue → inimigos renascem → pegar de volta, ou perder se morrer antes |

**Regras que empurram para a agressão**

- Parry bem-sucedido devolve a bala.
- Frascos e balas só recarregam na lanterna.

## 4. Controles

| Ação | Teclado + mouse | Gamepad (V1.1) |
|---|---|---|
| Mover | WASD | analógico esq. |
| Mirar | mouse | analógico dir. |
| Ataque leve | LMB | RB |
| Ataque pesado | RMB | RT |
| Tiro (parry) | Q | LB |
| Esquiva | Espaço | B |
| Cura | E | X |
| Interagir | F | A |
| Pausa | Esc | Start |

A divisão imita o Bloodborne: mão esquerda = pistola, mão direita (mouse) = arma.

## 5. Player

### Base

| Parâmetro | Valor |
|---|---|
| HP máx | 100 + 15 × pontos em Vida |
| Stamina máx | 100 + 10 × pontos em Stamina |
| Regeneração de stamina | 1 por frame, após 30 frames sem gastar |
| Velocidade de caminhada | 1,5 px/frame |
| Balas | máx 10 |
| Frascos | máx 5 |

Qualquer ação com custo exige stamina > 0. O custo pode levar a stamina a 0, nunca abaixo.

### Esquiva

| Parâmetro | Backstep | Dash |
|---|---|---|
| Quando | Espaço sem direção apertada | Espaço com direção apertada |
| Direção | oposta à mira | direção do movimento |
| Duração total | 16 | 22 |
| Iframes | frames 2–7 | frames 2–13 |
| Distância | 36 px | 64 px |
| Velocidade | começa alta e desacelera | começa alta e desacelera |
| Stamina | 15 | 25 |

### Cura (frasco)

- Recupera 40% do HP máximo.
- Duração 24 frames; a cura acontece no frame 12.
- Pode andar a 50% da velocidade durante a cura.
- Tomar dano antes do frame 12 cancela e não gasta o frasco.

### Dano recebido

- Hitstun de 18 frames, empurrão de 10 px.
- 10 frames de invulnerabilidade depois do hitstun (evita dois inimigos acertarem no mesmo instante).

### Morte

- Animação de 60 frames + 30 de fade.
- Volta na última lanterna usada. Almas ficam numa mancha de sangue onde morreu.
- Pegar a mancha devolve as almas. Morrer de novo antes disso apaga a mancha.
- Todos os inimigos renascem.

## 6. Estados do player

`idle`, `move`, `backstep`, `dash`, `ataque_leve`, `ataque_pesado`, `tiro`, `cura`, `hitstun`, `visceral`, `morte`, `descanso`

| Ação | Pode começar a partir de |
|---|---|
| Esquiva | idle, move, 2ª metade do recovery de ataque ou tiro |
| Ataque leve / pesado | idle, move, recovery do golpe anterior (combo), fim de esquiva |
| Tiro | idle, move, 2ª metade do recovery de ataque |
| Cura | idle, move |

- Buffer de input: 8 frames para esquiva, ataque e tiro.
- Durante o windup o player ainda gira para a mira. Do ativo em diante a direção trava.

## 7. Armas corpo a corpo

Escolhidas uma vez, na primeira lanterna. Mesmo código para as três; só os dados mudam.

**Formas de golpe** — todo golpe é um setor (distância + ângulo) centrado na mira:
- `arco N°`: acerta quem está a até *alcance* px e dentro de N° da mira.
- `círculo`: acerta tudo a até *alcance* px (360°).

### Bengala-lâmina — Destreza (≈ Threaded Cane)

Escala: Força E, Destreza A. Rápida, curta, combo longo.

| Golpe | Windup | Ativo | Recovery | Dano | Stamina | Alcance | Forma | Avanço |
|---|---|---|---|---|---|---|---|---|
| Leve 1–4 | 5 | 3 | 8 | 9 | 10 | 22 | arco 90° | 4 px |
| Pesado (estocada) | 14 | 4 | 14 | 22 | 25 | 34 | arco 30° | 20 px |

### Machado de caça — Força (≈ Hunter Axe)

Escala: Força A, Destreza E. Lento, largo, dano alto.

| Golpe | Windup | Ativo | Recovery | Dano | Stamina | Alcance | Forma | Avanço |
|---|---|---|---|---|---|---|---|---|
| Leve 1–2 | 14 | 5 | 16 | 24 | 22 | 28 | arco 180° | 6 px |
| Pesado (giro) | 22 | 8 | 22 | 38 | 35 | 30 | círculo | 0 |

O giro tem hyper armor no windup e no ativo: tomar dano não interrompe.

### Cutelo serrado — Híbrida (≈ Saw Cleaver)

Escala: Força C, Destreza C. Médio, versátil.

| Golpe | Windup | Ativo | Recovery | Dano | Stamina | Alcance | Forma | Avanço |
|---|---|---|---|---|---|---|---|---|
| Leve 1–3 | 8 | 4 | 11 | 14 | 15 | 25 | arco 120° | 5 px |
| Pesado (vertical) | 16 | 5 | 16 | 28 | 28 | 32 | arco 60° | 10 px |

### Combo

- Apertar ataque durante o recovery (ou até 8 frames antes, pelo buffer) encadeia o próximo golpe.
- Depois do último golpe do combo, volta ao primeiro.
- Pesado não encadeia; sempre termina o combo.

## 8. Pistolas, parry e visceral

### Pistolas

Escolhidas uma vez, na primeira lanterna, junto com a arma.

| Parâmetro | Pistola | Escopeta de cano serrado |
|---|---|---|
| Startup (até sair o tiro) | 3 | 8 |
| Projéteis | 1 | 5, em leque de 40° |
| Velocidade | 8 px/frame | 6 px/frame |
| Alcance | 120 px | 56 px |
| Dano | 8 × escala Destreza | 6 por chumbo × escala Força |
| Recovery | 14 | 22 |
| Bônus de parry | +4 frames de janela | 0 |
| Custo | 1 bala | 1 bala |

- A pistola é a ferramenta de timing: sai rápido, a bala chega rápido, e a janela é mais generosa.
- A escopeta é a ferramenta de área: precisa estar perto, sai devagar, mas pode dar parry em mais de um inimigo com o mesmo tiro.

### Parry

- Cada ataque inimigo tem `parry: sim/não` e uma janela: dos **10 frames antes do ativo** até o **2º frame do ativo** (12 frames).
- Projétil que acerta o inimigo dentro da janela → **stagger** de 90 frames. Hitstop de 6 frames. Devolve 1 bala (no máximo 1 por tiro).
- Projétil fora da janela → só dano. Interrompe o Aldeão; não interrompe Brutamontes nem chefe.
- Aviso visual no windup: **flash branco** = aceita parry. **Flash vermelho** = não aceita.

### Visceral

- Condição: inimigo em stagger, a até 28 px, e dentro de 60° da mira. Botão: ataque leve.
- 40 frames. Player invulnerável durante tudo.
- Dano: 60 × (1 + 0,08 × Destreza), para qualquer arma. Parry é o caminho da Destreza.
- Hitstop de 10 frames.
- Se o inimigo sobreviver: fica caído 40 frames (vulnerável) e levanta.

## 9. Progressão

### Atributos

| Atributo | Efeito por ponto |
|---|---|
| Vida | +15 HP máx |
| Stamina | +10 stamina máx |
| Força | +8% de dano em armas com escala em Força |
| Destreza | +8% de dano em armas com escala em Destreza (e no visceral) |

Todos começam em 0 pontos.

### Dano da arma

`dano = base × (1 + escala_FOR × 0,08 × FOR + escala_DES × 0,08 × DES)`

| Letra | Valor |
|---|---|
| A | 1,0 |
| C | 0,6 |
| E | 0,1 |

### Custo de nível

`custo = 100 + 50 × níveis já comprados` → 100, 150, 200, 250…

Subir nível só na lanterna, um ponto por vez.

### Almas por inimigo

| Fonte | Almas |
|---|---|
| Aldeão | 20 |
| Brutamontes | 60 |
| Chefe 1 | 800 |

Uma limpeza completa do mapa dá ~420 almas. Esperado: 4–6 níveis antes do chefe.

## 10. Inimigos

Ciclo comum: `idle → alerta → aproximar → windup → ativo → recovery`, mais `hitstun`, `stagger`, `visceral`, `caído`, `morte`.

- Aggro: player a até 100 px.
- Desistem (voltam ao ponto inicial) se o player passar de 250 px do ponto inicial.
- Escolhem o ataque pela distância ao player.

### Aldeão

HP 60 · velocidade 1,0 · 32×32 · arma: foice (sprite separado, gira como a do player)

| Ataque | Windup | Ativo | Recovery | Dano | Alcance | Forma | Parry |
|---|---|---|---|---|---|---|---|
| Golpe 1 | 24 | 5 | 18 | 18 | 22 | arco 100° | sim |
| Golpe 2 (50% de chance após o 1) | 12 | 5 | 26 | 18 | 22 | arco 100° | sim |

Qualquer acerto interrompe (hitstun de 12 frames), exceto durante o ativo. Ensina a esquiva.

### Brutamontes

HP 180 · velocidade 0,7 · 48×48 · ataca com os punhos (golpe desenhado no corpo)

| Ataque | Windup | Ativo | Recovery | Dano | Alcance | Forma | Parry |
|---|---|---|---|---|---|---|---|
| Pancada | 40 | 6 | 30 | 40 | 30 | arco 120° | sim |
| Agarrão (avança 24 px) | 30 | 8 | 36 | 50 | 18 | arco 60° | não |

Nunca é interrompido por dano. Só parry e visceral param ele. Ensina o parry.

## 11. Chefe 1 — Caçador caído (≈ Padre Gascoigne)

HP 900 · almas 800 · arena com névoa na entrada · barra de vida com nome na parte de baixo da tela

Nunca é interrompido por dano; só o parry abre stagger.

### Fase 1 (100%–50%) — humano, 48×48, velocidade 1,3

| Ataque | Distância | Windup | Ativo | Recovery | Dano | Forma | Parry |
|---|---|---|---|---|---|---|---|
| Machadada dupla | perto (< 40 px) | 20 / 14 | 5 / 5 | 24 | 25 cada | arco 140°, alcance 30 | sim |
| Tiro de escopeta | média (40–100 px) | 30 | — | 30 | 20 | 5 chumbos, leque de 40°, alcance 80 | não |
| Salto | longe (> 100 px) | 30 | 24 no ar + 4 no impacto | 30 | 30 | círculo 28 px no ponto de pouso | não |

### Transição

Aos 50% de HP: 90 frames invulnerável, rugido, troca de sprite para besta.

### Fase 2 (< 50%) — besta, 64×64, velocidade 2,0

| Ataque | Distância | Windup | Ativo | Recovery | Dano | Forma | Parry |
|---|---|---|---|---|---|---|---|
| Garras (combo de 3) | perto | 10 / 8 / 8 | 4 cada | 20 | 15 cada | arco 120°, alcance 26 | sim |
| Investida | média | 24 | dura o trajeto (120 px) | 30 | 30 | círculo 14 px em volta dele | não |
| Salto | longe | 20 | 20 no ar + 4 | 24 | 30 | círculo 28 px | não |

## 12. Mapa da V1

| Room | Tamanho | Conteúdo |
|---|---|---|
| rm_titulo | 320×180 | título, "Começar", "Sair" |
| rm_praca | 480×270 | lanterna 1; na primeira visita, escolha de arma + pistola |
| rm_rua | 960×360 | 5 Aldeões (grupos de 2 e 3), 1 Brutamontes |
| rm_mercado | 640×540 | 5 Aldeões, 2 Brutamontes; portão-atalho que abre por dentro e volta para a praça |
| rm_portao | 480×270 | 2 Aldeões; corredor antes da névoa |
| rm_arena_1 | 480×360 | Chefe 1 |
| rm_fim | 320×180 | "Fim da V1", tempo de jogo e número de mortes |

Fluxo: praça → rua → mercado → (atalho abre) → portão → arena → fim.

## 13. HUD e telas

| Elemento | Posição |
|---|---|
| Barra de HP (largura cresce com HP máx) | canto superior esquerdo |
| Barra de stamina | logo abaixo do HP |
| Frascos (ícone + número) | canto inferior esquerdo |
| Balas (ícone + número) | ao lado dos frascos |
| Almas | canto inferior direito |
| Barra do chefe + nome | centro, parte de baixo |

**Telas:** título · escolha de arma e pistola (primeira lanterna) · lanterna (Subir nível / Continuar) · subir nível (4 atributos, custo, efeito) · pausa (Continuar / Sair) · morte ("VOCÊ MORREU" + fade) · fim.

HUD desenhado na resolução base (320×180), com fonte bitmap.

## 14. Especificação de arte

Tudo desenhado **virado para a direita**; o código espelha para a esquerda.
Arquivos em tira horizontal: `spr_nome_stripN.png` (o GameMaker importa já cortado em N quadros).
Origem sempre informada em (x, y) dentro do quadro.

A animação de ataque do corpo tem 3 quadros fixos — **windup, ativo, recovery** — e o código mostra cada um pela duração da frame data. Assim a arte não depende dos números da seção 7.

### Player — 32×32, origem (16, 30)

| Sprite | Quadros | Uso |
|---|---|---|
| spr_player_idle | 4 | loop, ~6 fps |
| spr_player_walk | 6 | loop, ~10 fps |
| spr_player_backstep | 4 | esticado sobre 16 frames |
| spr_player_dash | 4 | esticado sobre 22 frames |
| spr_player_ataque | 3 | windup / ativo / recovery (todas as armas) |
| spr_player_tiro | 3 | startup / disparo / recovery |
| spr_player_cura | 4 | 24 frames |
| spr_player_hit | 2 | hitstun |
| spr_player_visceral | 4 | 40 frames |
| spr_player_morte | 6 | 60 frames |

### Armas — apontando para a direita, origem no cabo

| Sprite | Tamanho aprox. |
|---|---|
| spr_arma_bengala | 24×6 |
| spr_arma_machado | 28×12 |
| spr_arma_cutelo | 24×8 |
| spr_arma_pistola | 10×6 |
| spr_arma_escopeta | 14×6 |
| spr_arma_foice (Aldeão) | 20×10 |

### Efeitos — origem no centro do atacante, giram para a mira

| Sprite | Quadros |
|---|---|
| spr_fx_corte_90 | 4 |
| spr_fx_corte_120 | 4 |
| spr_fx_corte_180 | 4 |
| spr_fx_giro_360 | 4 |
| spr_fx_estocada | 3 |
| spr_fx_disparo (boca do cano) | 3 |
| spr_bala (4×4) | 1 |
| spr_chumbo (2×2) | 1 |
| spr_fx_impacto | 4 |
| spr_fx_sangue | 5 |
| spr_fx_parry (anel de luz) | 4 |
| spr_fx_poeira (pés no dash) | 4 |

### Inimigos

**Aldeão — 32×32, origem (16, 30)**

| Sprite | Quadros |
|---|---|
| idle | 4 |
| walk | 6 |
| ataque (windup / ativo / recovery) | 3 |
| hit | 2 |
| stagger | 2 |
| caído | 2 |
| morte | 6 |

**Brutamontes — 48×48, origem (24, 45)**

| Sprite | Quadros |
|---|---|
| idle | 4 |
| walk | 6 |
| pancada (windup / ativo / recovery) | 3 |
| agarrão (windup / ativo / recovery) | 3 |
| stagger | 2 |
| caído | 2 |
| morte | 6 |

**Chefe 1 humano — 48×48, origem (24, 45)** · o machado é o spr_arma_machado (girado pelo código); o bacamarte do tiro está desenhado no corpo

| Sprite | Quadros |
|---|---|
| idle | 4 |
| walk | 6 |
| ataque (windup / ativo / recovery) | 3 |
| tiro (windup / disparo / recovery) | 3 |
| salto (agacha / no ar / pouso) | 3 |
| stagger | 2 |
| caído (um joelho no chão) | 2 |

**Chefe 1 besta — 64×64, origem (32, 60)**

| Sprite | Quadros |
|---|---|
| transformação (`spr_chefe_transforma`): larga o machado, o manto incha, a crina rompe nas costas, o crânio de osso cresce, ruge e termina na pose do idle da besta | 8 |
| idle | 4 |
| corrida | 6 |
| garra (windup / ativo / recovery) | 3 |
| investida (windup / ativo / recovery) | 3 |
| salto (agacha / no ar / pouso) | 3 |
| stagger | 2 |
| caído | 2 |
| morte | 8 |

**Chefe 2 — Dama do Relógio (V1.1) — 32×32, origem (16, 30)** · mesmo tamanho e traço do caçador; use a máscara `spr_mask_player`

Inspirada na Lady Maria: caçadora jovem e esguia, casaco vinho com acabamento dourado, babado branco no peito, tricórnio com pena branca, rabo de cavalo prateado. Lâmina longa (`spr_arma_dama_longa`, 27×5, girada pelo código) e adaga na outra mão (desenhada no corpo).

- **Fase 1:** cortes rápidos, estocada longa, passo de esquiva para trás.
- **Fase 2 (abaixo de 50%):** "desperta o sangue" — aura vermelha (`spr_fx_aura_sangue`, desenhada atrás dela), lâmina em sangue (`spr_arma_dama_longa_sangue`), golpes mais rápidos.

| Sprite | Quadros |
|---|---|
| idle | 4 |
| walk | 6 |
| ataque (windup / ativo / recovery) | 3 |
| estocada (windup / ativo / recovery) | 3 |
| passo (esquiva) | 3 |
| stagger | 2 |
| caído (ajoelhada) | 2 |
| transformação (desperta o sangue) | 6 |
| morte (ajoelha e crava a lâmina no chão) | 8 |

### Cenário — tiles 16×16

| Item | Detalhe |
|---|---|
| Tileset rua (`spr_tiles_rua`, 47 tiles + o vazio) | lajes de pedra gasta (4), calçada (2), meio-fio (4), terra, grama morta (2), grama na pedra (2), face do muro (7), topo do muro (9) e cantos internos (4), escada (3), detalhes: sombra do muro, passagem escura, rachadura, folhas, sangue, poça, bueiro, pedrinhas |
| Lanterna | 16×32, chama animada 4 quadros |
| Névoa do chefe | 16×16 que se repete, 4 quadros (a textura anda para o lado) |
| Mancha de sangue (almas) | 16×16, 4 quadros em loop |
| Portão-atalho | 32×16, fechado (o objeto some ao abrir) |
| Pilar, boneco de treino | 16×32, 16×24 |
| Objetos (filhos do `obj_pilar`) | poste aceso 16×48, caixote, barril, carroça 48×32, caixão, cerca 16×24 |
| Brilho | `spr_luz` 48×48, desenhado com blend aditivo em lanterna e poste |

### Interface

| Item | Detalhe |
|---|---|
| Fonte bitmap | `spr_fonte`, 106 quadros de 8×12: A–Z, a–z, 0–9, pontuação, acentos do português |
| Moldura das barras | `spr_hud_moldura` (nine-slice 8×8, borda 2) + preenchimentos de vida, stamina e chefe |
| Ícones | frasco, bala, almas (HUD); vida, stamina, força, destreza, 3 armas e 2 pistolas (menus, 11×11) |
| Mira | cursor 9×9 |
| Logo | "NIGHTMOON" 115×34, capitais douradas de gravura; a lua faz o primeiro O; filete com losango embaixo |
| Fundo do título | 320×180: lua grande e baixa atrás da catedral, cidade em camadas com janelas acesas, neblina quente |

Direção de arte: **sépia e ouro** (escolhida em 2026-10-02). Luz morna de cima-esquerda, sombra puxando pro violeta, fio frio de recorte do lado de trás; acentos: ouro (o que é precioso ou interativo) e sangue (vida, dano, frasco). Caçador em escuro quente com rosto, gravata e galão claros; inimigos em famílias próprias (aldeão de boina, linho sujo e pele doente, com a tocha acesa; brutamontes esquelético de pele cinza-violeta com a gaiola enferrujada na cabeça; chefe no branco da Igreja Branca, capuz e faixa vermelha; besta de pelo preto-avermelhado com crânio de osso no lugar do focinho; Dama vinho e prata). Paleta registrada em `tools/sprites/paleta.py` (e `tools/sprites/nightmoon.gpl` pro Aseprite); a arte inteira é gerada pelos módulos de `tools/sprites/`.

## 15. Notas técnicas

- **Input num lugar só.** Um objeto lê teclado e mouse e grava em variáveis (`mover_x`, `mover_y`, `mira_dir`, `ataque_leve`...). Ninguém mais chama `keyboard_check`. O gamepad da V1.1 vira 2 h por causa disso.
- **Máquina de estados** com `enum` + `switch`, contador de frames próprio por estado (não Alarm).
- **Golpe = setor.** A cada frame ativo: para cada alvo, distância ≤ alcance e diferença de ângulo ≤ metade do arco → dano, se ainda não acertou esse alvo neste golpe. A mesma função serve player e inimigos.
- **Projéteis** são objetos (bala, chumbo), com dono, dano, velocidade e alcance.
- **Frame data em struct**, num script de dados. As 3 armas, as 2 pistolas e os ataques dos inimigos são dados lidos pelo mesmo código.
- **Inimigo pai.** Aldeão, Brutamontes e Chefe herdam do mesmo objeto; os filhos só trocam dados e sprites.
- **3/4:** máscara de colisão fixa nos pés (sprite de máscara próprio, não muda com a animação), `depth = -y`.
- **Paredes:** objetos invisíveis por cima dos tiles de muro.
- **Estado global** (almas, nível, atributos, arma escolhida, lanterna atual, mancha de sangue, atalhos abertos) num objeto persistente.
- **Game feel:** hitstop global (3 frames acerto, 6 parry, 10 visceral, 4 ao tomar dano) e screenshake leve.
- **Debug:** F3 liga hitboxes, iframes e nome do estado em cima de cada personagem.

## 16. Em aberto

- Nome das áreas e texto de abertura.
- Se a volta até o chefe ficar longa: lanterna 2 no portão.
