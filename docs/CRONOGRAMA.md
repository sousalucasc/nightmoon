# Nightmoon — Cronograma da V1

Base: [GDD.md](GDD.md). Meta: V1 jogável do título ao fim em 21 dias, 2,5–3 h por dia (~61 h).

**Início: segunda, 05/10/2026. Fim: domingo, 25/10/2026.**

Cada dia é um tutorial completo, com todo o código explicado: [tutorial/](tutorial/). Comece pelo [Dia 0](tutorial/dia-00.md).

## Como usar

- Siga a ordem. Cada dia usa o que os anteriores construíram.
- Estourou o dia: termine no dia seguinte. Os dias 7, 14 e 21 são mais leves, para recuperar.
- Atrasou mais de um dia inteiro: aplique a [ordem de corte](#ordem-de-corte).
- Até a arte chegar, tudo é retângulo colorido. Nenhum dia depende de arte.
- Fim de todo dia: commit no GitHub Desktop.

## Dias

| Dia | Data | Tema | Tutorial |
|---|---|---|---|
| 0 | 03–04/10 | Antes de começar: Git, tour do GameMaker, GML mínimo | [dia-00](tutorial/dia-00.md) |
| **Semana 1** | | **Player e combate contra boneco** | |
| 1 | seg 05/10 | Projeto, resolução 320×180, input, andar | [dia-01](tutorial/dia-01.md) |
| 2 | ter 06/10 | Colisão, câmera, profundidade, debug | [dia-02](tutorial/dia-02.md) |
| 3 | qua 07/10 | Máquina de estados, backstep e dash | [dia-03](tutorial/dia-03.md) |
| 4 | qui 08/10 | Buffer, stamina, tomar dano | [dia-04](tutorial/dia-04.md) |
| 5 | sex 09/10 | Frame data e ataque (Cutelo) | [dia-05](tutorial/dia-05.md) |
| 6 | sáb 10/10 | As 3 armas, escala, hyper armor | [dia-06](tutorial/dia-06.md) |
| 7 | dom 11/10 | Hitstop, tremor, arma na mão, animação | [dia-07](tutorial/dia-07.md) |
| **Semana 2** | | **Pistolas, parry, inimigos, chefe** | |
| 8 | seg 12/10 (feriado) | Pistolas | [dia-08](tutorial/dia-08.md) |
| 9 | ter 13/10 | Inimigo pai e primeiro Aldeão | [dia-09](tutorial/dia-09.md) |
| 10 | qua 14/10 | Aldeão completo e almas | [dia-10](tutorial/dia-10.md) |
| 11 | qui 15/10 | Parry e visceral | [dia-11](tutorial/dia-11.md) |
| 12 | sex 16/10 | Brutamontes | [dia-12](tutorial/dia-12.md) |
| 13 | sáb 17/10 | Chefe, fase 1 | [dia-13](tutorial/dia-13.md) |
| 14 | dom 18/10 | Chefe, fase 2 e arena | [dia-14](tutorial/dia-14.md) |
| **Semana 3** | | **Sistemas souls, mapa, fechamento** | |
| 15 | seg 19/10 | HUD e frascos | [dia-15](tutorial/dia-15.md) |
| 16 | ter 20/10 | Lanterna, morte, almas no chão | [dia-16](tutorial/dia-16.md) |
| 17 | qua 21/10 | Menus: armas, nível, pausa | [dia-17](tutorial/dia-17.md) |
| 18 | qui 22/10 | O mapa (5 rooms, portas, atalho) | [dia-18](tutorial/dia-18.md) |
| 19 | sex 23/10 | Título, fim, sons | [dia-19](tutorial/dia-19.md) |
| 20 | sáb 24/10 | Playtest e balanceamento | [dia-20](tutorial/dia-20.md) |
| 21 | dom 25/10 | Correções e build | [dia-21](tutorial/dia-21.md) |

**Apêndices:** [A — Importar a arte](tutorial/apendice-a-arte.md) · [B — GML rápido](tutorial/apendice-b-gml.md) · [C — Erros e depuração](tutorial/apendice-c-erros.md)

## Checkpoints

| Fim da | Tem que funcionar | Se não |
|---|---|---|
| Semana 1 | andar, colidir, esquivas com iframes, stamina, 3 armas contra o boneco | termine no dia 8 e aplique os cortes 1 e 2 |
| Semana 2 | pistolas, parry, visceral, Aldeão, Brutamontes, chefe jogável | termine no dia 15; aplique os cortes 1, 2 e 3 |
| Semana 3 | partida completa do título ao fim | use o dia 21 inteiro para correções |

## Ordem de corte

Aplique de cima para baixo, só o necessário.

| # | Corte | Economiza |
|---|---|---|
| 1 | Salto do chefe (nas duas fases): tire o `_salto` das listas de ataque | ~1,5 h |
| 2 | Fase 2 sem sprite novo: `spr_fase2` aponta para `spr_chefe` | ~1,5 h |
| 3 | `rm_mercado` e atalho: a porta leste da rua leva direto ao portão | ~1,5 h |
| 4 | Golpe 2 do Aldeão | ~0,5 h |
| 5 | Pausa (Esc não faz nada) | ~0,5 h |
| 6 | Tela de fim sem tempo e mortes | ~0,5 h |

**Nunca cortar:** esquiva com iframes, parry, visceral, as 3 armas, as 2 pistolas, frascos, lanterna, morte com almas, subir nível.

## Quando cada arte entra

Importe no dia indicado, depois de terminar o código do dia, seguindo a parte daquele dia no [Apêndice A](tutorial/apendice-a-arte.md). A arte pronta está em `arte/`; a origem de cada sprite, em `arte/origens.md`.

| Dia | Arte | Situação |
|---|---|---|
| 2 | pilar | pronta |
| 5 | boneco de treino | pronta |
| 7 | player (todas as animações), 3 armas, efeitos de corte | pronta |
| 8 | pistola, escopeta, projétil, clarão | pronta |
| 10 | Aldeão, foice, sangue | pronta |
| 11 | anel de parry | pronta |
| 12 | Brutamontes | pronta |
| 14 | chefe humano, transformação, besta, névoa (depois do dia 14, que reescreve o Create do chefe) | pronta |
| 15 | ícones do HUD, molduras das barras | pronta |
| 16 | lanterna, mancha, brilho | pronta |
| 18 | tileset, objetos do cenário, portão | pronta |
| 19 | fonte, mira, logo, fundo do título, ícones dos menus, sons | pronta |

Toda a arte e os sons da V1 estão prontos. Se pular a importação de algum dia, o retângulo provisório continua funcionando.
