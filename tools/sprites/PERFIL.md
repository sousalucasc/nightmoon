# Perfil do projeto — Nightmoon

Soulslike top-down 3/4 inspirado em Bloodborne, em GameMaker. Este arquivo diz o que é "certo"
pra arte deste jogo. Atualize quando o dono decidir algo.

## Direção escolhida (2026-10-02): SÉPIA E OURO

O dono escolheu o conceito C (capa de ombros + sobretudo até o tornozelo + gravata marfim, na
paleta sépia e ouro) **com o tricórnio do caçador antigo**. A partir daí pediu o lote inteiro
pronto, sem paradas.

| Item | Decisão |
|---|---|
| engine e export | GameMaker 2026. Cada sprite é um PNG em tira `spr_nome_stripN.png` em `arte/<tipo>/`; o dono importa à mão seguindo o Apêndice A (`docs/tutorial/apendice-a-arte.md`) e digita a origem de `arte/origens.md`. **Gerado por `python tools/sprites/sprites.py exporta`** (audita antes e recusa com ERRO). |
| resolução e escala | base 320×180, janela 4× (1280×720), tela cheia 6×. Câmera 1:1, sem zoom. |
| tiers (quadro → figura) | caçador, aldeão e Dama: 32×32, figura de 25 a 28 px (aldeão curvado: 20 de corpo, 28 com a tocha); brutamontes 48×48, 40 px, magro e alto; chefe humano 48×48, 41 px; besta 64×64, 55 px; tiles 16; ícones 5 a 11 px. |
| origem | sola na linha da origem: (16, 30) no 32×32, (24, 45) no 48×48, (32, 60) no 64×64. |
| hitbox | NÃO é a sprite: o código usa `spr_mask_*`. Só o sinal de atordoado lê o desenho (`sprite_get_bbox_top`). |
| direção | tudo virado pra DIREITA, 3/4 de frente; o código espelha. |
| armas | sprites separados, apontando pra direita, origem no cabo; mão fixa por personagem (abaixo). |
| paleta | **guia**, registrada em `tools/sprites/paleta.py` (e `nightmoon.gpl`). Rampas com matiz girando (sombra pro violeta, luz pro quente). Acentos: OURO (precioso/interativo: galão, botão, moldura da HUD, chama) e SANGUE (vida, dano, frasco, olhos dos inimigos). |
| famílias de cor | caçador: escuro quente (`casaco`) + pele sépia + marfim + ouro; aldeão: `linho` + `ardosia` + `doente`, acento na chama da tocha; brutamontes: `pelecinza` (defunto) + `ferrugem` + `trapo`; chefe: `alvo` (branco da Igreja Branca) + `forro` na faixa; besta: `pelosangue` (preto-avermelhado) + `marfim` no crânio e nas garras; Dama: `vinho` + `prata` + ouro. Ninguém se confunde com o caçador. |
| luz | **assada na sprite**: morna, de cima-esquerda; fio frio de recorte (`recorte`) em poucos pixels da borda direita do caçador pra separar do chão. A engine só soma o brilho `spr_luz` (branco em degraus, tingido pelo código) em lanterna e poste. |
| contorno | 1 px automático, cor única `contorno` (#120a0e, violeta-quase-preto); linhas internas com o tom mais escuro do material. Efeitos sem contorno. |
| chão | lajes grandes de pedra gasta (`pedra`), quentes e mais claras que os personagens; detalhes em camada separada. |
| animações | as da seção 14 do GDD, mesmos números de quadros (o código conta com eles). Ataque = 3 quadros (windup, ativo, recovery) com a mão PARADA no ponto da arma; o corpo gira em volta dela. |
| flash | inimigo apanha → `gpu_set_fog` pinta a sprite de BRANCO; windup → silhueta BRANCA/VERMELHA. O windup de cada inimigo tem silhueta própria: o aldeão empina e puxa a tocha pra trás; o brutamontes ergue os dois punhos acima da gaiola (pancada) ou abre os braços em X (agarrão); o chefe ergue o braço de trás; a besta arma a garra atrás da cabeça. Sem sombra no chão desenhada na sprite. |
| referência (régua) | a arte exportada desta direção é a régua daqui pra frente. Caderno: `tools/sprites/referencias/cacador.md`. |
| o que já foi recusado | toda a arte antiga (2026-10-02): caçador chibi de lenço vermelho, paleta cinza-azulada apagada, paralelepípedo cinza quadriculado, HUD fina vermelha e verde, logo branco com gotas, lua cinza redonda. Os conceitos A (capuz, verdete) e B (corvo, lua de sangue) e a cartola do C. No caminho do chão: tijolo em cestaria (miúdo, cansativo) e pedra em losango (parecia acolchoado). A 1ª rodada dos inimigos desta direção (aldeão, brutamontes, chefe e besta: "lixo slop"): corpo de esboço com sombreamento automático, ruído miúdo (o dobro de aglomerados do caçador) e desenho parecido com o antigo; refeitos do zero e pintados à mão (caderno `referencias/inimigos.md`). |

## Lido do código (não mudar sem mudar o tutorial)

- Nomes, tamanhos de quadro, número de quadros e origens: `arte/origens.md` (gerado).
- Mão da arma (a partir da origem, x pra frente, y pra cima): caçador (2, 10) → pixel (18, 20) em TODOS os quadros com arma; pistola no tiro (3, 12) → pixel (19, 18); aldeão (3, 10) → (19, 20); chefe humano (4, 12) → (28, 33) no 48×48; Dama (2, 10) → (18, 20). A arma some na morte, na cura e no visceral (o desenho não tem arma nesses quadros; a Dama crava a lâmina desenhada na morte).
- Boca do bacamarte do chefe: boca_x 20, boca_y 22 → pixel (44, 23) nos 3 quadros de tiro (no disparo o corpo recua, o cano fica).
- Transformação: 8 quadros em 90 frames; tremor do rugido no frame 57 = quadro 5 (o rugido); o último quadro é igual ao idle 0 da besta. O código desliga o machado no frame 1: ele está desenhado no quadro 0 (na mão, apoiado no chão a 30°) e caído no chão nos quadros 1 a 3.
- Fonte: `spr_fonte`, 106 quadros 8×12 na ordem de `arte/ui/fonte_ordem.txt`, proporcional, espaço com 2 px de alfa 1. Maiúscula nas linhas 2-8, altura-x 4-8, descendente até 10, acento de maiúscula 0-1; corpo marfim (tingível) + sombra.
- HUD: moldura nine-slice 8×8 (borda 2), preenchimentos esticados (vida 4×4, stamina 4×2, chefe 4×4).
- Cenário: os 48 lugares do tileset com os nomes que o Apêndice cita; máscaras dos objetos (poste 5,43-10,47; caixote 1,10-14,19; barril 2,12-13,19; carroça 4,16-43,31; caixão 2,20-13,27; cerca 0,20-15,23; pilar 0,22-15,31).

## Exceções registradas (a auditoria sabe)

- Alfa parcial de propósito: `spr_nevoa`, `spr_luz`, o espaço da fonte, e no tileset a sombra do muro, a poça e a passagem escura.
- Cores fora da paleta de propósito: o branco da `spr_luz` (o código tinge) e o pixel de alfa 1 do espaço da fonte. As cores do fundo do título estão registradas na rampa `titulo`.
- Sola fora da linha de propósito: backstep[1] e passo[1] (no ar), garra[1] e investida[1] da besta (bote), corrida da besta (galope com as patas no ar), morte/caído/salto/transforma.
- Rampas escuras do cenário (`pedra`, `muro`) têm vizinhos com ΔE 4,3-4,8: degraus sutis de chão, de propósito.

## Onde mora

- `tools/sprites/sprites.py` — `audita`, `exporta`, `previa`.
- `tools/sprites/kit/` — tela, carimbo, tecido (pano em u,v), boneco (montador), esboço (base de volume), paleta (ΔE, OKLCh), prévia, auditoria, aseprite, exporta.
- Um módulo por sprite: `personagens/cacador.py`, `inimigos/aldeao.py`, `inimigos/brutamontes.py`, `chefes/chefe_humano.py`, `chefes/chefe_besta.py` (+ transformação), `chefes/dama.py` (+ aura), `armas/armas.py`, `fx/efeitos.py`, `cenario/tiles.py`, `cenario/props.py`, `cenario/guias.py`, `hud/hud.py`, `hud/fonte.py`, `hud/titulo.py`.
- Bancadas de pintura (o quadro-base de cada inimigo pintado à mão, de onde saem os carimbos): `inimigos/aldeao_pinta.py`, `inimigos/brutamontes_pinta.py`, `chefes/chefe_humano_pinta.py`, `chefes/chefe_besta_pinta.py`.
- `.aseprite` (uma tag por animação, pivô na origem, paleta nas amostras) + `_sheet.png/.json` ao lado de cada personagem.
- `personagens/cacador_conceitos.py`, `conceito_esboco.py`, `conceitos_prancha.py`, `cacador_base.py`, `cacador_pinta.py`, `cenario/conceito_chao.py`: histórico da PARADA 1 (não geram nada pro jogo).
