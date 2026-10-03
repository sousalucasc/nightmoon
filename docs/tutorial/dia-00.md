# Dia 0 — Antes de começar

**Quando:** fim de semana antes do dia 1 (03–04/10) · **Tempo:** ~1 h

Este tutorial foi feito para você seguir sozinho. Tudo o que você precisa digitar está aqui, e cada bloco de código vem com a explicação do que ele faz.

---

## Como este tutorial funciona

Cada dia é um arquivo: `dia-01.md`, `dia-02.md`… Dentro dele:

1. **O que você vai aprender** — os conceitos do dia.
2. **Passos numerados** — o que fazer no GameMaker, na ordem.
3. **Blocos de código** — sempre com o lugar exato onde vão.
4. **Teste do dia** — como saber que funcionou.
5. **Se deu errado** — os erros mais prováveis e como resolver.

### Regras

- **Digite o código, não cole.** Digitando você lê cada linha, e é assim que aprende. Colar = amanhã você não sabe o que escreveu.
- **Os comentários (linhas com `//`) são opcionais.** Eles só explicam; o jogo funciona sem eles.
- **Rode o jogo (F5) toda vez que o tutorial mandar.** Erro achado cedo é erro fácil.
- **Não pule dias.** Cada dia usa o que o anterior construiu.
- **Fim do dia = commit** no GitHub Desktop, mesmo se algo ficou faltando.

### Como ler as instruções de código

Todo bloco de código vem com um título dizendo **onde** ele vai e **como**:

| Título | O que fazer |
|---|---|
| **obj_player → Step** (arquivo inteiro) | Apague tudo que está no evento e digite o bloco. |
| **obj_player → Create** (adicione no fim) | Mantenha o que já existe e digite o bloco embaixo. |
| **obj_game → Create** (adicione antes de `room_goto`) | Digite o bloco logo acima da linha indicada. |
| **scr_player** (substitua a função `player_estado_livre`) | Ache a função com esse nome, apague ela inteira (de `function` até o `}` que fecha) e digite a nova no lugar. |
| **scr_player** (nova função, adicione no fim) | Digite a função no fim do script. |
| **obj_game → Create** (troque a linha) | Ache a linha indicada e troque pelo bloco. |

---

## Passo 1 — GitHub Desktop (15 min)

O Git guarda uma "foto" do projeto a cada commit. Se você quebrar alguma coisa, dá pra voltar.

1. Baixe e instale o **GitHub Desktop** (desktop.github.com). Criar conta no GitHub é opcional; pra usar só no seu PC não precisa.
2. **File → Add local repository** → escolha `E:\gamemaker\darkogames\nightmoon`.
3. Ele vai dizer que a pasta não é um repositório. Clique em **create a repository** → **Create repository**.
4. Na lista da esquerda aparecem os arquivos. Embaixo, em **Summary**, escreva `projeto criado` e clique **Commit to main**.

**Todo fim de dia:** abra o GitHub Desktop, escreva um resumo (`dia 3: esquivas`) e clique **Commit to main**.

**Para desfazer tudo desde o último commit:** clique com o botão direito num arquivo da lista → **Discard changes**. Use com cuidado: some tudo que não foi commitado.

---

## Passo 2 — Tour pelo GameMaker (20 min)

Abra o projeto `nightmoon\nightmoon\nightmoon.yyp`.

| Parte da tela | Para que serve |
|---|---|
| **Asset Browser** (painel da direita) | Lista tudo do projeto: sprites, objetos, rooms, scripts. Botão direito → **Create** cria coisas novas. |
| **Workspace** (centro) | Onde abrem os editores. |
| **Output** (embaixo) | Mostra erros de compilação e as mensagens de `show_debug_message`. |
| Botão ▶ **Run** (F5) | Compila e roda o jogo. |
| Botão 🐞 **Debug** (F6) | Roda com o depurador (dá pra pausar e ver variáveis). |
| Botão 🧹 **Clean** (Ctrl+F7) | Limpa o cache. Use quando o jogo faz algo que não faz sentido com o código. |

### As 5 palavras que você precisa saber

| Palavra | O que é |
|---|---|
| **Sprite** | Uma imagem (ou várias, formando uma animação). Tem uma **origem**: o ponto que fica exatamente em `x, y`. |
| **Objeto** | Uma "receita" de coisa do jogo: player, inimigo, parede. Tem **eventos** com código. |
| **Instância** | Uma cópia viva de um objeto dentro da room. Um objeto `obj_aldeao` pode ter 10 instâncias. |
| **Evento** | Um momento em que o código roda: **Create** (quando nasce), **Step** (todo frame), **Draw** (quando desenha)… |
| **Room** | Uma fase/cena. O jogo está sempre dentro de uma room. |

### O jogo roda 60 vezes por segundo

A cada **frame** (1/60 de segundo), o GameMaker:

1. roda o **Begin Step** de todas as instâncias,
2. roda o **Step** de todas,
3. roda o **End Step** de todas,
4. desenha tudo (**Draw**, depois **Draw GUI**).

Quase todo o código deste jogo roda uma vez por frame. Quando o tutorial diz "16 frames", quer dizer 16/60 de segundo (~0,27 s).

### Coordenadas

- `x` cresce para a **direita**.
- `y` cresce para **baixo** (diferente da escola).
- Ângulos: **0° = direita, 90° = cima, 180° = esquerda, 270° = baixo**.

---

## Passo 3 — Como criar cada coisa no GameMaker (referência)

Volte aqui sempre que o tutorial mandar criar algo.

### Onde cada coisa fica

O projeto já tem as pastas criadas no Asset Browser. **Crie cada coisa direto na pasta certa:** botão direito na pasta → **Create**. Se criar no lugar errado, arraste para a pasta certa.

| Pasta | O que vai nela |
|---|---|
| Sprites / Player | `spr_player`, `spr_mask_player` e as animações do player |
| Sprites / Armas | `spr_arma_*` |
| Sprites / Inimigos | `spr_boneco`, `spr_aldeao`, `spr_brutamontes`, `spr_mask_grande` |
| Sprites / Chefe | `spr_chefe`, `spr_chefe_besta` |
| Sprites / Efeitos | `spr_fx_*`, `spr_projetil` |
| Sprites / Cenario | `spr_parede`, `spr_pilar`, `spr_lanterna`, `spr_mancha`, `spr_nevoa`, `spr_porta`, `spr_chegada`, `spr_atalho`, tilesets |
| Sprites / UI | `spr_icone_*` |
| Objects / Sistema | `obj_game`, `obj_menu`, `obj_fx` |
| Objects / Player | `obj_player`, `obj_projetil` |
| Objects / Inimigos | `obj_inimigo_pai`, `obj_boneco`, `obj_aldeao`, `obj_brutamontes`, `obj_chefe` |
| Objects / Mundo | `obj_parede`, `obj_pilar`, `obj_armadilha`, `obj_lanterna`, `obj_mancha`, `obj_nevoa`, `obj_porta`, `obj_chegada`, `obj_atalho` |
| Scripts | todos os `scr_*` |
| Rooms / Sistema | `rm_init` (hoje ainda `Room1`), `rm_titulo`, `rm_fim` |
| Rooms / Teste | `rm_teste`, `rm_teste_chefe` |
| Rooms / Mapa | `rm_praca`, `rm_rua`, `rm_mercado`, `rm_portao`, `rm_arena_1` |
| Tile Sets, Fonts, Sounds | tilesets, `fnt_hud`, `snd_*` |

Fora do GameMaker, na pasta `E:\gamemaker\darkogames\nightmoon`:

| Pasta | O que vai nela |
|---|---|
| `arte\` | os PNG e GIF originais da arte, antes de importar |
| `audio\` | os sons originais, antes de importar |
| `build\` | o executável do dia 21 |

### Criar um objeto
1. Asset Browser → botão direito → **Create → Object**.
2. Digite o nome (ex.: `obj_player`) e Enter.
3. No editor do objeto: clique no quadro do **Sprite** para escolher o sprite.
4. **Add Event** → escolha o evento. Abre o editor de código daquele evento.

Eventos que vamos usar:

| Evento | Onde fica no menu | Arquivo (se você olhar a pasta) |
|---|---|---|
| Create | Create | `Create_0` |
| Step | Step → Step | `Step_0` |
| Begin Step | Step → Begin Step | `Step_1` |
| End Step | Step → End Step | `Step_2` |
| Draw | Draw → Draw | `Draw_0` |
| Draw GUI | Draw → Draw GUI | `Draw_64` |
| Room Start | Other → Room Start | `Other_4` |
| Room End | Other → Room End | `Other_5` |

### Criar um sprite provisório (retângulo colorido)
1. Asset Browser → botão direito → **Create → Sprite**. Dê o nome.
2. Clique em **Resize Sprite** (ícone de redimensionar ao lado do tamanho). Desmarque "manter proporção", digite largura e altura, **Apply**.
3. Clique em **Edit Image**. No editor de imagem, pegue o **balde (Fill)**, escolha uma cor e clique na imagem. Feche a aba.
4. Em **Origin**, escolha **Custom** e digite o x e o y que o tutorial pedir.

### Colocar instâncias numa room
1. Abra a room (duplo clique).
2. No painel **Layers**, clique na camada **Instances**.
3. Arraste o objeto do Asset Browser para dentro da room.
4. Para esticar (paredes): selecione a instância e arraste as bordas, ou dê duplo clique nela e mude **Scale X / Scale Y**.
5. Deixe o grid em 16×16 (barra de cima do editor de room): tudo encaixa melhor.

### Criar um script
1. Asset Browser → botão direito → **Create → Script**. Dê o nome (ex.: `scr_player`).
2. Ele abre com um `function scr_player() {}` de exemplo. **Apague tudo** e digite o que o tutorial mandar.

---

## Passo 4 — Nomes que vamos usar

| Prefixo | Tipo | Exemplo |
|---|---|---|
| `spr_` | Sprite | `spr_player` |
| `obj_` | Objeto | `obj_player` |
| `rm_` | Room | `rm_teste` |
| `scr_` | Script | `scr_player` |
| `fnt_` | Fonte | `fnt_hud` |
| `snd_` | Som | `snd_tiro` |

Dentro do código:
- **Variáveis de instância:** `hp`, `estado`, `vel` — cada instância tem as suas.
- **Variáveis locais** começam com `var` e `_`: `var _dist = 10;` — só existem até o fim do evento ou da função.
- **Globais** começam com `global.`: `global.armas` — existem uma vez só, pro jogo inteiro.

---

## Passo 5 — O mínimo de GML (a linguagem)

Leia agora, e volte aqui quando esquecer algo. O [apêndice de GML](apendice-b-gml.md) tem mais.

```gml
// Isto é um comentário. O jogo ignora.

vida = 100;                 // cria (ou muda) uma variável
vida = vida - 10;           // agora vale 90
vida -= 10;                 // mesma coisa, mais curto: agora 80

if (vida <= 0) {            // se...
    morreu = true;
} else {                    // senão...
    morreu = false;
}

// && = "e", || = "ou", ! = "não", == compara, != "diferente"
if (vida > 0 && !morreu) { }

// Função: um pedaço de código com nome, que dá pra chamar de vários lugares
function curar(_quanto) {
    vida = vida + _quanto;
}
curar(20);                  // chama a função

// Array: uma lista
var _lista = [10, 20, 30];
_lista[0];                  // 10 (começa do zero)
array_length(_lista);       // 3

// Struct: vários valores com nome, num pacote
var _golpe = { dano: 14, alcance: 25 };
_golpe.dano;                // 14
```

---

## Passo 6 — Quando der erro

Você não vai ter ninguém pra perguntar. Então:

1. **Leia a mensagem inteira.** O GameMaker diz o objeto, o evento e a **linha**.
2. **Erro ao compilar** (antes do jogo abrir, aparece no Output): quase sempre é digitação — parêntese faltando, `;`, vírgula, nome errado.
3. **Erro com o jogo rodando** (janela de erro): o texto diz o que faltou. Os três mais comuns:

| Mensagem | O que quer dizer |
|---|---|
| `variable not set before reading it` | Você usou uma variável que ninguém criou. Falta no Create, ou o nome está diferente. |
| `unable to find instance for object index` | Você usou `obj_algo.x`, mas não existe nenhum `obj_algo` na room. |
| `unable to convert string to number` / `wrong type` | Misturou texto com número. Use `string(numero)` para juntar número com texto. |

4. **Compare com o tutorial letra por letra.** 90% dos erros são uma letra.
5. O [apêndice de erros](apendice-c-erros.md) tem mais casos e mostra como usar o depurador (F6).

---

## Checklist do dia 0

- [ ] GitHub Desktop instalado e primeiro commit feito
- [ ] Sabe criar objeto, sprite, script e colocar instância na room
- [ ] Leu o mínimo de GML
- [ ] Leu o [GDD](../GDD.md) uma vez
