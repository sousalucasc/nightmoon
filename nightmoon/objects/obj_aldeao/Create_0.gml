event_inherited();

hp_max = 60;
hp = hp_max;
vel = 1.0;
raio = 7;
almas = 20;
mask_index = spr_mask_player;   // colisao no pezinho

// golpe 2, chained apos o 1
var _golpe2 = ataque_novo(12, 5, 26, 18, 22, 100, true);
// golpe 1, 50% de chance de chainar no 2
var _golpe1 = ataque_novo(24, 5, 18, 18, 22, 100, true);
_golpe1.seguinte = _golpe2;
_golpe1.chance = 0.5;
ataques = [_golpe1];// o golpe 2 só vem pelo combo

tem_arma = true;
arma_sprite = spr_arma_foice;

spr = {
    parado: spr_aldeao_idle,
    andando: spr_aldeao_walk,
    ataque: spr_aldeao_ataque,
    hit: spr_aldeao_hit,
    stagger: spr_aldeao_stagger,
    caido: spr_aldeao_caido,
    morte: spr_aldeao_morte
};