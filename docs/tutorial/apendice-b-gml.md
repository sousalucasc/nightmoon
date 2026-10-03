# Apêndice B — GML: referência rápida

Tudo que o projeto usa, em um lugar.

---

## Variáveis

| Tipo | Como | Vive até |
|---|---|---|
| De instância | `hp = 100;` | a instância ser destruída |
| Local | `var _dist = 10;` | o fim do evento ou da função |
| Global | `global.armas = {...};` | o jogo fechar |
| Macro | `#macro LARGURA_BASE 320` | é trocada pelo valor antes de compilar |

Ler a variável de outra instância: `obj_player.hp`. Se existir mais de um `obj_player`, pega o primeiro.

## Operadores

| Operador | Significa |
|---|---|
| `=` | recebe |
| `==` / `!=` | igual / diferente |
| `<` `>` `<=` `>=` | comparações |
| `&&` / `\|\|` / `!` | e / ou / não |
| `+=` `-=` | soma/subtrai na própria variável |
| `div` | divisão inteira (`7 div 2 = 3`) |
| `mod` | resto (`7 mod 2 = 1`) |
| `a ? b : c` | se `a`, `b`; senão, `c` |

## Controle

```gml
if (cond) { } else if (outra) { } else { }

switch (estado) {
    case PL.LIVRE: ...; break;    // sem break, continua no case de baixo
    case "texto":  ...; break;    // funciona com texto também
}

for (var i = 0; i < 10; i++) { }  // repete com i = 0, 1, ..., 9
while (cond) { }                  // repete enquanto cond for verdadeira
return valor;                     // sai da função devolvendo valor
exit;                             // sai do evento (ou da função) na hora
```

## Funções

```gml
function somar(_a, _b = 0) {      // _b é opcional (vale 0 se não passar)
    return _a + _b;
}
```

Uma função de script chamada por uma instância enxerga as variáveis **dessa instância**.

## Arrays e structs

```gml
var _l = [10, 20];
array_push(_l, 30);               // [10, 20, 30]
array_length(_l);                 // 3
array_contains(_l, 20);           // true
_l[0];                            // 10

var _s = { dano: 14, nome: "Cutelo" };
_s.dano;                          // 14
_s.novo_campo = 5;                // cria campo na hora
```

Arrays e structs são **referências**: `b = a` faz os dois apontarem para o mesmo.

## Instâncias

| Código | Faz |
|---|---|
| `instance_create_depth(x, y, depth, obj)` | cria; devolve o id |
| `instance_destroy()` / `instance_destroy(id)` | destrói a si / outra |
| `instance_exists(obj)` | existe alguma? |
| `instance_number(obj)` | quantas existem |
| `with (obj) { }` | roda o bloco dentro de cada instância de `obj` |
| `other` | dentro do `with`, quem chamou |
| `id` | a própria instância |
| `noone` | "nenhuma instância" |
| `event_inherited()` | roda o mesmo evento do pai |

## Movimento e colisão

| Código | Faz |
|---|---|
| `move_and_collide(dx, dy, obj)` | anda e para/desliza em `obj` |
| `place_meeting(x, y, obj)` | encostaria em `obj` nessa posição? |
| `instance_place(x, y, obj)` | quem de `obj` está encostando (ou `noone`) |
| `collision_line(x1, y1, x2, y2, obj, preciso, sem_mim)` | alguém de `obj` cruza a linha? |
| `point_distance(x1, y1, x2, y2)` | distância |
| `point_direction(x1, y1, x2, y2)` | ângulo (0 = direita, 90 = cima) |
| `lengthdir_x(dist, dir)` / `lengthdir_y` | quanto andar em x / y |
| `angle_difference(a, b)` | diferença de ângulos, de -180 a 180 |

## Matemática

| Código | Faz |
|---|---|
| `min(a, b)` / `max(a, b)` | menor / maior |
| `clamp(v, mín, máx)` | prende entre limites |
| `lerp(a, b, t)` | caminho de `a` até `b` (t de 0 a 1) |
| `round` / `floor` | arredonda / arredonda para baixo |
| `abs(v)` | valor sem sinal |
| `sign(v)` | -1, 0 ou 1 |
| `sin(v)` | seno (v em radianos; `pi` = meia volta) |
| `random(n)` / `random_range(a, b)` / `irandom(n)` | sorteios |

## Desenho

| Código | Faz |
|---|---|
| `draw_self()` | desenha o sprite normalmente |
| `draw_sprite_ext(spr, quadro, x, y, esc_x, esc_y, ang, cor, alpha)` | desenha com opções |
| `draw_text(x, y, texto)` | texto (use `string(numero)` para números) |
| `draw_set_colour(cor)` / `draw_set_alpha(a)` | cor / transparência do que vem depois |
| `draw_set_halign(fa_center)` | alinhamento do texto |
| `draw_rectangle(x1, y1, x2, y2, contorno)` | retângulo |
| `draw_circle(x, y, r, contorno)` | círculo |
| `draw_healthbar(...)` | barra pronta |
| `gpu_set_fog(true, cor, 1, 0)` ... `gpu_set_fog(false, c_white, 0, 1)` | pinta tudo de uma cor (flash) |

## Eventos usados

| Evento | Quando |
|---|---|
| Create | ao nascer |
| Begin Step / Step / End Step | todo frame, nessa ordem |
| Draw | desenho no mundo (segue a câmera) |
| Draw GUI | desenho na tela (HUD, menus) |
| Room Start / Room End | ao entrar / sair de uma room |
