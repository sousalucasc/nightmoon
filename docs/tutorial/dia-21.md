# Dia 21 — Correções e build

**Quando:** dom 25/10 · **Tempo:** ~2,5 h

**No fim do dia:** o jogo está num `.exe` que roda em qualquer Windows, sem o GameMaker aberto.

---

## Passo 1 — Corrigir os bugs (90 min)

Pegue a lista de ontem, na ordem. Para cada bug:

1. **Reproduza**: descubra o passo a passo que faz ele acontecer toda vez.
2. **Ligue o F3** e olhe estado, setores e vida no momento do bug.
3. **Ache o estado culpado**: o bug acontece em qual estado (do player ou do inimigo)? O código está na função desse estado.
4. **Mude uma coisa só** e teste de novo.
5. Consertou? Commit (`corrige: ...`). Assim, se o próximo conserto quebrar algo, dá para voltar.

O [Apêndice C](apendice-c-erros.md) tem os erros mais comuns e como usar o depurador (F6).

## Passo 2 — Limpar o debug (10 min)

As teclas de teste (F3, 1–5, 7–9, 0, B, T) funcionam só com o debug ligado, então não atrapalham o jogador. Mas a sala `rm_teste` e a `rm_teste_chefe` podem ficar no projeto: não aparecem no jogo, porque ninguém leva até elas (só as teclas B e T, com F3).

Se quiser tirar o F3 da versão final: no **Begin Step** do `obj_game`, apague o bloco do `vk_f3`.

## Passo 3 — Gerar o executável (20 min)

1. Na barra de cima do GameMaker, confira que o alvo é **Windows** e a configuração **Default**.
2. Menu **Build → Create Executable** (ou o ícone de pacote na barra de cima).
3. Escolha **Package as Zip** (mais simples: um zip com o jogo dentro) ou **Installer**.
4. Escolha a pasta, por exemplo `E:\gamemaker\darkogames\nightmoon\build`.
5. Espere compilar.

**Teste o executável fora do GameMaker:** extraia o zip numa pasta qualquer, rode o `.exe`, jogue do título ao fim. Às vezes algo funciona na IDE e não no executável (quase sempre arquivo faltando).

## Passo 4 — Fechar a versão 1 (10 min)

1. GitHub Desktop: commit `v1.0`.
2. **History** (aba de cima) → botão direito no commit → **Create Tag** → `v1.0`.

Pronto: a V1 do Nightmoon existe.

---

## E depois? (V1.1)

Na ordem do [GDD](../GDD.md#v11-depois-nesta-ordem):

| Item | Como começar |
|---|---|
| Chefe 2 + Área 2 + lanterna 2 | novo filho de `obj_inimigo_pai`, igual ao chefe 1; rooms novas com o mesmo método do dia 18 |
| Cão | filho de `obj_inimigo_pai`: vida baixa, `vel` alta, um ataque com `avanco` (bote) |
| Gamepad | no Begin Step do `obj_game`: `gamepad_axis_value` para mover/mirar, `gamepad_button_check_pressed` para os botões. **Só lá.** |
| Rally | no `player_dano`, guarde parte do dano como "vida cinza"; no ataque que acerta, devolva parte dela |
| Save | `json_stringify` do que está em `jogo_novo()` + `file_text_write_string`; carregar é o contrário |
