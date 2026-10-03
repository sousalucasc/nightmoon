# Caderno — inimigos e chefe (2ª rodada)

## Diagnóstico da 1ª rodada (recusada em 2026-10-02: "lixo slop")

Só o caçador e a Dama tinham sido pintados à mão. Aldeão, brutamontes, chefe humano e besta
saíram do `kit/esboco.py`: máscara de partes + luz automática. Medido contra o caçador
(`idle 0`, mesma auditoria):

| | aglomerados/100 px | órfãos/100 px | pequenos | cores |
|---|---|---|---|---|
| caçador (régua) | 30,7 | 4,9 | 70% | 20 |
| aldeão da 1ª rodada | 56,1 | 16,0 | 86% | 26 |
| aldeão novo | 41,5 | 6,5 | 72% | 20 |

O dobro de ruído miúdo, tons demais por material e, no desenho, a mesma ideia dos antigos
(aldeão de capuz de saco e bata oliva, brutamontes atarracado de carne crua, chefe de cabelo
branco e venda). Regra tirada: **inimigo nasce na bancada, pintado à mão, com no máximo 3 tons
por material e a régua de ruído do caçador; nada de esboço no quadro final.**

## Referências (fonte de verdade: Bloodborne)

- **Turba de Yharnam (huntsmen)**: boina ou cartola, cachecol, tocha numa mão e foice/forcado
  na outra, corcunda. → aldeão: a tocha acesa é o gancho e o ponto mais claro da sprite.
- **Gigantes da igreja**: altos, magros, braços que passam do joelho. **Gaiolas de
  Byrgenwerth**: a cabeça presa numa gaiola de ferro. → brutamontes: gigante esquelético com a
  gaiola enferrujada e os grilhões; a ameaça vem da altura e do alcance, não da massa.
- **Caçadores da Igreja de Cura (trajes brancos)**: capuz, manto nos ombros, sobretudo claro.
  → chefe: o caçador da igreja oposta ao jogador (branco contra o escuro quente).
- **Bestas clericais / lobisomens**: o crânio exposto, a crina, pernas digitígradas. → besta:
  crânio de osso no lugar do focinho, pelo preto-avermelhado, os restos do manto branco.
- Pixel art na mesma escala: a régua é o caçador do próprio jogo (massa escura lida pela
  aresta clara, um ponto claro, acento minúsculo).

## Voltas

1. Aldeão, montagem direta das peças: lê, mas com 26 cores e o dobro de ruído. Volta 2:
   planos grandes, tons cortados (linho0, madeira, chama0 e o tom 4 da ardósia saíram), boina
   achatada com aba (era um capacete redondo), mão da foice em (19, 20) em todos os quadros
   com arma; pés apontando pra frente (a 1ª versão apontava pra trás).
2. Brutamontes: a versão A (volumosa) lia como golem genérico; a B (esquelética, braços até
   abaixo do joelho) ficou. Corrente em elos de ferro e ferrugem; cadeado na gola.
3. Chefe: a 1ª versão lia como "fantasma de lençol" (estreita, branca chapada). Manto em sino
   mais largo, dobras em `alvo1`, a abertura escura do casaco na frente e a ponta da faixa
   caída quebraram a massa. Bacamarte de sino com a boca em (44, 23).
4. Besta: o pelo saiu vermelho vivo (lia como dragão); desceu um degrau inteiro na rampa. As
   pernas da corrida quebravam com deslocamento em blocos; agora a perna inclina linha a linha
   (0 no quadril, dx na pata). Garras e dentes sólidos de marfim (eram xadrez).
5. Transformação: o código desliga o machado no frame 1, então o machado está no desenho —
   na mão a 30° no quadro 0 (a -40° do idle ele sairia pela borda de baixo) e no chão nos
   quadros 1-3. A crina rompe atrás do ombro esquerdo do manto; o quadro 7 é igual ao idle 0.
