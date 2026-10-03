# Caderno — caçador (e direção de arte do jogo)

## Por que refazer

A arte antiga inteira foi recusada (2026-10-02): "não quero ver uma bosta melhorada, quero ver
algo novo real". Diagnóstico do caçador antigo (`arte/player`, 32×32): chibi de ~3 cabeças com
tricórnio enorme, lenço vermelho na cara, casaco cinza-marrom; paleta cinza apagada, contorno
quase preto igual em tudo, luz de cima-direita, sem ponto de interesse claro além do lenço. O chão
(paralelepípedo cinza-azulado quadriculado) tinha o mesmo valor do personagem. Nada disso volta.

## Referências

### Fonte de verdade — trajes de caçador de Bloodborne
- Fextralife, página Armor (https://bloodborne.wiki.fextralife.com/Armor), miniaturas dos conjuntos.
  - **Black Church**: chapéu de aba redonda, sobretudo até o tornozelo com capa curta, luva branca.
    → coluna alta e escura com um ponto claro na mão.
  - **Crowfeather (Eileen)**: máscara de bico + manto de penas eriçado. → gancho = o bico.
  - **Bone Ash / Executioner**: chapéu cônico enorme / elmo cônico. (Não usado: ficaria caricato a 32 px.)
  - **Gascoigne / Gehrman**: aba larga + capinha nos ombros + cachecol. (Não usado: aba larga lembra o tricórnio antigo.)
  - **Old Hunter / Henryk / Ashen**: capuz ou turbante, manto curto, máscara de pano. → conceito A.
  - Regra tirada: o caçador de Bloodborne é **casaco longo + algo marcante na cabeça + máscara na parte de baixo do rosto**; o gancho tem que estar na cabeça e no contorno do casaco.

### Pixel art do mesmo gênero e escala (~32 px, virado pra direita, chão top-down)
- **Vampire Survivors, Trevor Belmont** (https://www.spriters-resource.com/pc_computer/vampiresurvivors/asset/242769/):
  figura de 31-33 px, 14-16 cores por quadro, contorno escuro contínuo, cabeça de ~7 px (≈4,5 cabeças),
  luz forte na pele e no pano claro. → **cabeça de 6-7 px numa figura de 28-30 px; até ~17 cores.**
- **Vampire Survivors, Alucard** (asset 242282): 32 px, 17 cores; a capa preta é uma massa escura
  com o forro cinza-claro do lado da luz, cabelo branco como ponto de interesse, dourado só em
  frisos de 1-2 px. → **massa escura lida pela aresta clara + um ponto claro + acento minúsculo.**
  Mesma estrutura do nosso jogo: sprite de lado, espelhado, em chão visto de cima.
- Usam sombra no chão desenhada na sprite; **nós não** (o `gpu_set_fog` do flash pintaria a sombra de branco).

### Bonecos-base (E:\gamemaker\claude-comida)
- Templates de corpo com as partes coloridas: Eris Esra 16x32 (top-down, 5 direções, uso
  comercial liberado; chibi, serve só pra tempo de animação), "2D Pixel Art Character Template"
  (36 px, 3/4, partes coloridas), "Metroidvania - Roguelike Template" (28 px, cabeça de 7 px,
  guarda com pernas abertas — **a proporção-alvo**), Ozzbit (só uso não comercial: só estudo).
  → poses e tempos de golpe, rolamento, dano e morte. Nenhum pixel deles entra no jogo.

### Tutoriais (base da skill)
- Saint11 *Darkness*, *Outlines*, *Fabric*; Slynyrd *Light and Shadow*: luz de um lado só, sombra
  projetada dura, preto lido pela aresta, dobra que irradia do ponto de apoio.

## Voltas

1. Rascunho à mão dos três (cacador_conceitos.py): formas certas, valores fracos (massa marrom
   chapada, sem plano de luz), rosto de C grande e laranja, manto de A em "cogumelo".
2. Esboço por partes (`kit/esboco.py`): silhuetas em máscara de partes + luz de cima-esquerda
   automática. IoU A×C caiu de 0,82 pra 0,68 depois de encurtar o casaco de A (pernas e botas à
   mostra, lanterna na cintura); B ficou curvado (IoU A×B 0,66).
3. Chão de esboço por direção (Voronoi): lajes grandes (A), placas quadradas molhadas (B),
   paralelepípedo miúdo (C). Só pra ver o caçador no lugar; o tileset é feito à mão depois.
4. **Escolha do dono (PARADA 1):** conceito C com o tricórnio do caçador antigo; "sem paradas" daí
   em diante. Paleta sépia e ouro passou a valer pro jogo inteiro.
5. Quadro-base pintado à mão (`cacador_pinta.py`): tricórnio com galão dourado em aglomerados
   (não em degradê de 1 px), rosto pálido sob a sombra da aba, gravata e punho marfim, capa com
   o plano de luz em cima-esquerda, casaco escuro (a massa fica nos tons 0-2) e fio frio de
   recorte em 2-3 px da borda direita. No chão de teste, o casaco marrom sumia no paralelepípedo
   marrom; resolvido com o chão mais claro e menos saturado que o casaco (separação por VALOR).
6. Rig (`cacador.py`): cabeça, capa e mão em carimbos; sobretudo em pano (u, v) que balança com a
   barra (`kit/tecido.py`); 40 quadros. Auditoria: teto de cores 25 → 20 (cabelo e linha interna
   viraram tons do casaco, couro e pele perderam um tom); órfãos do chapéu limpos; quadros da
   morte que encostavam na borda refeitos. Dano com IoU 0,56 contra o parado (silhueta própria).
