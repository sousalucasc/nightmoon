// valores padrao de todo inimigo
// heranca em sua melhor forma
// cada filho chama event_inherited()
hp_max = 50;
hp = hp_max;
vel = 1;
raio = 8;            // tamanho do corpo para golpes
almas = 10;          // quanto dá ao morrer
aggro = 100;         // distância em que percebe o player
desiste = 250;       // distância do ponto inicial em que desiste e volta
dist_parar = 18;     // para de andar a esta distância do player
espera_entre = 30;   // frames de pausa entre ataques
pode_hitstun = true; // golpes interrompem?
acordado = true;     // o chefe começa dormindo (dia 14)
ataques = [];        // lista de ataques (ataque_novo)

// estado
estado = INI.IDLE;
estado_timer = 0;
ataque = undefined;
ataque_dir = 0;
acertados = [];
espera = 0;
flash = 0;
ultimo_dano = 0;
lado = 1;
inicio_x = x;
inicio_y = y;
depth = -y;

// animacao e arma
image_speed = 0;
anim_timer = 0;
// sprite de cada estado, trocar dps ai caralho
spr = {
    parado: sprite_index,
    andando: sprite_index,
    ataque: sprite_index,
    hit: sprite_index,
    stagger: sprite_index,
    caido: sprite_index,
    morte: sprite_index
};
tem_arma = false; // desenha uma arma separada girando? (Aldeão: foice)
arma_sprite = -1;
// onde fica a mão da arma no desenho: 3 px à frente do centro, 10 acima dos pés 
mao_x = 3;
mao_y = 10;

