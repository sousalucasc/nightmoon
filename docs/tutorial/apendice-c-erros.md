# Apêndice C — Erros e como achar bugs sozinho

---

## 1. Erro de compilação (o jogo nem abre)

Aparece na janela **Output**, com objeto, evento e **linha**. Exemplo:

```
gml_Object_obj_player_Step_0(12) : unexpected symbol ")"
```

= no `obj_player`, evento Step, linha 12.

| Mensagem | Quase sempre é |
|---|---|
| `unexpected symbol` | parêntese, chave ou vírgula sobrando/faltando |
| `malformed assignment` | `=` onde era `==`, ou o contrário |
| `unexpected end of file` | uma `{` que nunca fechou |
| `Assignment operator expected` | nome escrito errado virou "coisa solta" |

**Dica:** o erro às vezes aponta a linha **seguinte** ao problema. Olhe a linha de cima também.

## 2. Erro com o jogo rodando (janela de erro)

A janela mostra a mensagem e o **stack** (a sequência de funções até o erro). A primeira linha diz onde:

```
ERROR in action number 1 of Step Event0 for object obj_player:
Variable obj_player.golpe(100045, -2147483648) not set before reading it.
 at gml_Script_player_estado_ataque (line 5)
```

| Mensagem | Causa | Onde olhar |
|---|---|---|
| `Variable ... not set before reading it` | a variável nunca foi criada | o Create daquele objeto; nome digitado igual? |
| `unable to find instance for object index` | usou `obj_x.algo` sem nenhum `obj_x` na room | coloque na room, ou proteja com `instance_exists(obj_x)` |
| `unable to convert ... to number` / `DoAdd` | somou texto com número | use `string(numero)` |
| `Variable Index [n] out of range` | leu posição que o array não tem | a lista tem menos itens do que você pensa |
| `trying to index a variable which is not an array` | a variável não é um array | confira onde ela recebeu valor |
| `not a struct` / `struct ... undefined` | `golpe.dano` com `golpe` ainda `undefined` | o código roda num estado em que o struct não existe |

## 3. Bug sem mensagem (o jogo faz a coisa errada)

### Olhe com o F3
O F3 mostra estado, setores, iframes, janelas de parry e vida. Metade dos bugs de combate aparece ali: "ah, ele está em HITSTUN, e não em ATAQUE".

### Escreva no Output
```gml
show_debug_message("estado: " + string(estado) + " timer: " + string(estado_timer));
```
Cole isso dentro da função suspeita e rode: a mensagem aparece na janela Output todo frame. **Apague depois.**

### Use o depurador (F6)
1. Clique na margem esquerda de uma linha de código: aparece uma bolinha vermelha (**breakpoint**).
2. Rode com **F6** (Debug).
3. Quando o jogo passar por aquela linha, ele **pausa** e mostra todas as variáveis da instância.
4. **F10** avança uma linha; **F11** entra na função; **F5** continua.

### Pense em estados
Todo bug de personagem acontece **num estado**. Pergunte:
1. Em qual estado ele está quando o bug acontece? (F3)
2. O código desse estado faz o que eu acho?
3. Ele deveria ter trocado de estado e não trocou? Procure o `trocar` que faltou.

## 4. Os 10 erros mais prováveis neste projeto

| Sintoma | Causa |
|---|---|
| Algo não acontece nunca | falta o `case` no `switch` do Step |
| Duas coisas acontecem juntas | falta `break` num `case` |
| Estado nunca termina | trocou de estado sem zerar o timer (use `player_trocar`) |
| Um aperto faz duas ações | o buffer não foi zerado ao usar |
| Filho dá `not set` | faltou `event_inherited()` no Create do filho |
| Tudo fica branco | `gpu_set_fog(true...)` sem o `gpu_set_fog(false...)` |
| Texto do jogo inteiro na cor/alinhamento errado | `draw_set_colour`/`draw_set_halign` sem voltar ao padrão |
| Personagem preso na parede | máscara mudando com o sprite (falta `mask_index`) |
| Coisa duplicada ao voltar para uma room | objeto persistente colocado numa room que é recarregada |
| O jogo "trava" | hitstop que nunca desce, ou menu invisível aberto (`jogo_congelado`) |
| Uma condição é sempre verdadeira, sem motivo | uma variável com o mesmo nome de uma função: o GameMaker lê a função. O compilador não avisa. Renomeie uma das duas |

## 5. Quando tudo falha

1. **Clean** (vassoura, Ctrl+F7) e rode de novo.
2. Compare o arquivo com o tutorial, **linha por linha**, em voz alta.
3. GitHub Desktop → **History**: o que mudou desde o último commit que funcionava? O bug está nessas linhas.
4. Último recurso: **Discard changes** no arquivo quebrado e refaça o passo do dia.
