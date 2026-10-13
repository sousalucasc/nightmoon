event_inherited();

hp_max = 60;
hp = hp_max;
vel = 1.0;
raio = 7;
almas = 20;
mask_index = spr_mask_player;   // colisao nos pes

// golpe: windup 24, ativo 5, recovery 18, dano 18, alcance 22, arco 100°, aceita parry
var _golpe = ataque_novo(24, 5, 18, 18, 22, 100, true);
ataques = [_golpe];