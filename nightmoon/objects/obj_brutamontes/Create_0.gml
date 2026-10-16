event_inherited();

hp_max = 180;
hp = hp_max;
vel = 0.7;
raio = 12;
almas = 60;
pode_hitstun = false;   // so toma hitstun com o parry
dist_parar = 24;
espera_entre = 40;
mask_index = spr_mask_grande;

// pancada, pode tomar parry
var _pancada = ataque_novo(40, 6, 30, 40, 30, 120, true);
_pancada.dist_max = 34;

// agarrao, nao toma parry
var _agarrao = ataque_novo(30, 8, 36, 50, 18, 60, false);
_agarrao.avanco = 24;
_agarrao.dist_min = 20;
_agarrao.dist_max = 48;

ataques = [_pancada, _agarrao];

spr = {
    parado: spr_brutamontes_idle,
    andando: spr_brutamontes_walk,
    ataque: spr_brutamontes_pancada,
    hit: spr_brutamontes_stagger,     // ele não sofre hitstun, so safeguard
    stagger: spr_brutamontes_stagger,
    caido: spr_brutamontes_caido,
    morte: spr_brutamontes_morte
};
// cada ataque com sua animacao
_pancada.spr = spr_brutamontes_pancada;
_agarrao.spr = spr_brutamontes_agarrao;