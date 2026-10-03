# Dia 20 — Playtest e balanceamento

**Quando:** sáb 24/10 · **Tempo:** ~3 h · **Sem código novo.**

Hoje você descobre o que está quebrado ou chato, e ajusta números.

---

## Passo 1 — Duas partidas suas (60 min)

Jogue do título ao fim duas vezes, sem F3:

1. **Bengala + Pistola** (Destreza, parry).
2. **Machado + Escopeta** (Força, dano).

Anote, sem parar para consertar:
- onde morreu e por quê;
- qualquer coisa que pareceu injusta;
- qualquer erro, travada ou coisa estranha.

## Passo 2 — Uma pessoa de fora (60 min)

Chame alguém que nunca viu o jogo. Regras:
- **Não explique nada.** Só diga os controles (ou deixe ela descobrir).
- **Não ajude.** Se ela travar, anote onde.
- Olhe a cara dela: onde ela se diverte, onde fica irritada.

Anote: quantas vezes morreu para cada inimigo, se entendeu o parry sozinha, se achou a lanterna, se entendeu a mancha de almas.

## Passo 3 — Lista de bugs (15 min)

Junte tudo numa lista em 3 níveis:

| Nível | O que é | Exemplo |
|---|---|---|
| 1 — Trava | o jogo fecha, dá erro ou fica impossível continuar | erro ao voltar pela porta; player preso na parede |
| 2 — Atrapalha | dá para jogar, mas está errado | parry não entra às vezes; inimigo atravessa parede |
| 3 — Estético | só aparência | arma na posição errada |

Amanhã você corrige na ordem: todos os 1, depois os 2, e os 3 se sobrar tempo.

## Passo 4 — Balancear (resto do tempo)

Todos os números estão em poucos lugares. **Mude um por vez** e teste.

| Quero mudar | Onde |
|---|---|
| Dano, velocidade, alcance das armas | `scr_dados` → `dados_armas` |
| Pistolas | `scr_dados` → `dados_pistolas` |
| Vida, velocidade, ataques de um inimigo | Create do `obj_aldeao`, `obj_brutamontes`, `obj_chefe` |
| Janela de parry (10 e 2 frames) | `scr_combate` → `inimigo_janela_parry` |
| Dano do visceral (60) | `scr_player` → `player_estado_visceral` |
| Esquivas | Create do `obj_player` → `backstep` e `dash` |
| Stamina (regeneração, espera) | Step do `obj_player` e `player_gastar_stamina` |
| Cura (40%, 5 frascos) | `player_estado_cura` e Create do player |
| Custo de nível | `scr_menu` → `nivel_custo` |
| Almas por inimigo | `almas` no Create de cada inimigo |

**Guia rápido:**

| Sintoma | Tente |
|---|---|
| Chefe difícil demais | aumente os windups dele em 4 frames; ou `espera_entre` 15 → 25 |
| Chefe fácil demais | aumente `hp_max`; diminua `espera_entre` |
| Parry impossível | janela 10 → 14 frames |
| Parry fácil demais | janela 10 → 8 |
| Esquiva salva de tudo | iframes do dash 2–13 → 3–11 |
| Nunca tem stamina | regeneração 1 → 1,3 por frame |
| Nível sobe rápido demais | custo `100 + 50 × n` → `150 + 75 × n` |

## Commit

`dia 20: balanceamento` — e salve a lista de bugs em `docs/bugs.md`.
