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

// último tiro que deu parry em mim
ultimo_tiro_parry = -1;   

// chefe e ataques especiais
nome = "";
e_chefe = false;
tem_fase2 = false;
fase = 1;
no_ar = false;      // no meio do salto: não apanha
altura = 0;         // quanto o corpo está acima do chão (só para desenhar)
salto_x0 = x;       // de onde saltou
salto_y0 = y;
salto_x1 = x;       // onde vai cair
salto_y1 = y;
boca_x = 12;        // onde fica a boca da arma de fogo no desenho (clarão e chumbos saem dali)
boca_y = 12;

// Já morto desde o último descanso? Então não aparece.
// A chave é única por inimigo: room + posição onde foi colocado.
chave = room_get_name(room) + "_" + string(x) + "_" + string(y);
if (array_contains(obj_game.mortos, chave)) {
    instance_destroy();
}