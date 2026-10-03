# Dia 2 — Colisão, câmera, profundidade e debug

**Quando:** ter 06/10 · **Tempo:** ~3 h

**No fim do dia:** o player colide com paredes e desliza encostado nelas, passa na frente e atrás de pilares, vira para o lado do mouse, e a câmera segue ele sem tremer.

## O que você vai aprender

- **Máscara de colisão**: por que a colisão usa só os pés.
- **`move_and_collide`**: andar e parar (ou deslizar) na parede com uma linha.
- **Objeto pai (parent)**: o pilar "é uma parede" sem repetir código.
- **Profundidade (`depth`)**: quem é desenhado na frente.
- **Câmera** com `lerp` e `clamp`.

---

## Passo 1 — Sprites (15 min)

Crie estes três sprites provisórios:

| Sprite | Tamanho | Cor | Origem |
|---|---|---|---|
| `spr_mask_player` | 10×6 | verde | x 5, y 6 |
| `spr_parede` | 16×16 | cinza escuro | x 0, y 0 (Top Left) |
| `spr_pilar` | 16×32 | cinza médio | x 8, y 32 |

No `spr_pilar`, ajuste a **máscara de colisão** (painel **Collision Mask** do editor de sprite):
- **Mode: Manual**, **Type: Rectangle**.
- **Left 0, Top 22, Right 15, Bottom 31**.

Isso faz só os 10 pixels de baixo do pilar colidirem. O resto é "altura": o player pode passar atrás dele.

**Por que a colisão é só nos pés?** Numa visão 3/4, o topo de um personagem ou de um pilar está "no ar". Duas coisas só batem se a **base** delas se encosta. Se a colisão fosse o sprite inteiro, a cabeça do player bateria na base de um pilar que está atrás dele.

## Passo 2 — Paredes e pilares (15 min)

1. Crie o objeto **`obj_parede`** com o sprite `spr_parede`. Deixe **Visible** marcado por enquanto: sem arte, é bom ver as paredes. Nenhum evento.
2. Crie o objeto **`obj_pilar`** com o sprite `spr_pilar`.
3. No `obj_pilar`, clique em **Parent** e escolha **`obj_parede`**.
4. No `obj_pilar`, adicione o evento **Create**:

**obj_pilar → Create** (arquivo inteiro)
<!-- src: objects/obj_pilar/Create_0.gml -->
```gml
// O pilar não se mexe: basta calcular a profundidade uma vez.
depth = -y;
```

**O que é Parent?** Um objeto filho herda tudo do pai: eventos, e também **identidade**. Quando o código perguntar "estou encostando num `obj_parede`?", os pilares contam, porque são filhos de `obj_parede`. Vamos usar muito isso: todos os inimigos vão ser filhos de um `obj_inimigo_pai`.

## Passo 3 — Montar a rm_teste (20 min)

Abra a `rm_teste`. No topo do editor, deixe o grid em **16×16**. Na camada Instances, coloque:

| Objeto | x | y | Scale X | Scale Y | Para quê |
|---|---|---|---|---|---|
| `obj_parede` | 0 | 0 | 40 | 1 | borda de cima |
| `obj_parede` | 0 | 344 | 40 | 1 | borda de baixo |
| `obj_parede` | 0 | 16 | 1 | 21 | borda da esquerda |
| `obj_parede` | 624 | 16 | 1 | 21 | borda da direita |
| `obj_parede` | 192 | 96 | 4 | 1 | bloco |
| `obj_parede` | 416 | 224 | 1 | 4 | bloco |
| `obj_pilar` | 272 | 128 | 1 | 1 | pilar |
| `obj_pilar` | 360 | 264 | 1 | 1 | pilar |

Para digitar x, y e escala: duplo clique na instância. O player continua em (320, 180).

Como `spr_parede` tem 16×16, **Scale X 40** faz uma parede de 640 pixels (a largura da room).

## Passo 4 — Player com colisão (30 min)

**obj_player → Create** (arquivo inteiro)
<!-- src: objects/obj_player/Create_0.gml -->
```gml
vel = 1.5;  // pixels por frame
lado = 1;   // 1 = olhando para a direita, -1 = para a esquerda

// A colisão usa só os pés, e não muda quando a animação muda.
mask_index = spr_mask_player;
```

**`mask_index`** é o sprite usado para colisão. Sem ele, a colisão seria o próprio `spr_player`. Pior: quando a animação trocar de sprite (andando, atacando), a máscara mudaria de tamanho e o player poderia **entrar na parede** e ficar preso. Com uma máscara fixa, isso nunca acontece.

**obj_player → Step** (arquivo inteiro)
<!-- src: objects/obj_player/Step_0.gml -->
```gml
var _mx = obj_game.mover_x;
var _my = obj_game.mover_y;

// Na diagonal, (1, 1) tem comprimento 1,41.
// Dividir pelo comprimento deixa qualquer direção com comprimento 1.
var _comp = point_distance(0, 0, _mx, _my);
if (_comp > 0) {
    // Anda e, se encostar numa parede, para ou desliza por ela.
    move_and_collide(_mx / _comp * vel, _my / _comp * vel, obj_parede);
}

// O corpo vira para o lado do mouse.
if (obj_game.mira_dir > 90 && obj_game.mira_dir < 270) {
    lado = -1;
} else {
    lado = 1;
}

// Quem está mais embaixo na tela é desenhado por cima.
depth = -y;
```

- **`move_and_collide(dx, dy, obj_parede)`** tenta andar `dx, dy`. Se encostar num `obj_parede` (ou filho dele), para colado na parede. Se estiver andando na diagonal contra uma parede, desliza ao longo dela.
- **`lado`**: se a mira aponta para a esquerda (entre 90° e 270°), `lado = -1`.
- **`depth`**: quanto **menor** o depth, mais **na frente** é desenhado. Com `depth = -y`, quem está mais embaixo na tela (y maior) fica com depth menor, portanto na frente. É o truque clássico de jogo top-down.

**obj_player → Draw** (arquivo inteiro)
<!-- src: objects/obj_player/Draw_0.gml -->
```gml
// lado = -1 espelha o desenho na horizontal.
draw_sprite_ext(sprite_index, image_index, x, y, lado, 1, 0, c_white, 1);

if (obj_game.debug) {
    draw_set_colour(c_lime);
    draw_rectangle(bbox_left, bbox_top, bbox_right, bbox_bottom, true);
    draw_line(x, y, mouse_x, mouse_y);
    draw_set_colour(c_white);
}
```

- **`draw_sprite_ext(sprite, quadro, x, y, escala_x, escala_y, ângulo, cor, alpha)`** desenha com opções. Escala x = -1 espelha. Cor `c_white` = cores originais.
- **`bbox_left/top/right/bottom`** são as bordas da máscara de colisão. Com F3, você vê o retângulo verde nos pés: é o que realmente colide.
- **`draw_set_colour`** muda a cor de tudo que for desenhado depois (linhas, textos). Sempre volte para `c_white` no fim, senão outros objetos desenham na cor errada.

## Passo 5 — Câmera (30 min)

**obj_game → Create** (troque a linha `camera = camera_create_view(...)` por este bloco)
<!-- src: objects/obj_game/Create_0.gml @troca: camera = camera_create_view -->
```gml
camera = camera_create_view(0, 0, LARGURA_BASE, ALTURA_BASE);
cam_x = 0;
cam_y = 0;
```

**obj_game → Room Start** (adicione no fim)
<!-- src: objects/obj_game/Other_4.gml @fim -->
```gml
// A câmera já começa em cima do player, sem "viajar" do canto da room.
if (instance_exists(obj_player)) {
    cam_x = obj_player.x - LARGURA_BASE / 2;
    cam_y = obj_player.y - ALTURA_BASE / 2;
}
```

Adicione o evento **End Step** no `obj_game`:

**obj_game → End Step** (arquivo inteiro)
<!-- src: objects/obj_game/Step_2.gml -->
```gml
// End Step: roda depois do Step de todo mundo.

// Câmera: segue o player devagar e não mostra fora da room.
if (instance_exists(obj_player)) {
    var _alvo_x = obj_player.x - LARGURA_BASE / 2;
    var _alvo_y = obj_player.y - ALTURA_BASE / 2;
    cam_x = lerp(cam_x, _alvo_x, 0.15);
    cam_y = lerp(cam_y, _alvo_y, 0.15);
}
cam_x = clamp(cam_x, 0, room_width - LARGURA_BASE);
cam_y = clamp(cam_y, 0, room_height - ALTURA_BASE);

// Pixel art: a câmera só para em pixel inteiro.
camera_set_view_pos(camera, round(cam_x), round(cam_y));
```

- **A posição da câmera é o canto de cima-esquerda** do que ela mostra. Para o player ficar no centro, a câmera vai para `player.x - 160`.
- **`lerp(a, b, 0.15)`** anda 15% do caminho de `a` até `b`. Todo frame chega 15% mais perto: a câmera "persegue" suave em vez de grudar.
- **`clamp(valor, mín, máx)`** prende o valor entre os limites. A câmera não passa da borda da room.
- **`round`** arredonda. Uma câmera em x = 100,4 faz a pixel art tremer.
- **Por que End Step?** Porque roda depois que o player já se moveu neste frame. Se a câmera andasse antes, ficaria um frame atrasada.

---

## Arte do dia

Com a arte pronta, faça agora a parte **Dia 2** do [Apêndice A](apendice-a-arte.md).

## Teste do dia

- [ ] O player para nas paredes e desliza encostado quando anda na diagonal contra elas.
- [ ] Andando por cima de um pilar (y menor), o player passa **atrás** dele. Por baixo, passa **na frente**.
- [ ] O corpo espelha quando o mouse passa para o outro lado.
- [ ] A câmera segue, não mostra fora da room e não treme.
- [ ] F3 mostra o retângulo verde nos pés.

## Se deu errado

| Sintoma | Causa provável | Solução |
|---|---|---|
| Player atravessa paredes | O terceiro argumento do `move_and_collide` não é `obj_parede` | Passo 4. |
| Player atravessa o pilar | O pilar não tem Parent `obj_parede` | Passo 2. |
| Player bate no pilar longe da base | Máscara do `spr_pilar` não está em Manual | Passo 1. |
| Player fica sempre na frente do pilar | Falta `depth = -y` no Create do pilar ou no Step do player | Passos 2 e 4. |
| Paredes não aparecem | `obj_parede` sem sprite ou Visible desmarcado | Passo 2. |
| Câmera treme | Faltou o `round` | Passo 5. |
| `variable not set before reading it: cam_x` | O bloco novo do Create não foi digitado | Passo 5. |

## Commit

`dia 2: colisão, câmera, profundidade`
