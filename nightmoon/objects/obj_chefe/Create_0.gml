event_inherited();

nome = "cacador caido";
e_chefe = true;
hp_max = 900;
hp = hp_max;
vel = 1.3;
raio = 12;
almas = 800;
pode_hitstun = false;
aggro = 400;          // na arena, vê o player de qualquer lugar
desiste = 99999;      // nunca desiste
dist_parar = 24;
espera_entre = 15;
mask_index = spr_mask_grande;
acordado = false;     // a névoa acorda ele

// --- Fase 1 ---
// Machadada dupla: o segundo golpe sempre vem (chance 1).
var _machadada2 = ataque_novo(14, 5, 24, 25, 30, 140, true);
var _machadada1 = ataque_novo(20, 5, 0, 25, 30, 140, true);
_machadada1.seguinte = _machadada2;
_machadada1.chance = 1;
_machadada1.dist_max = 40;

// Tiro de escopeta: média distância, não aceita parry (desvie).
var _tiro = ataque_novo(30, 1, 30, 20, 80, 40, false);
_tiro.tipo = "tiro";
_tiro.dist_min = 40;
_tiro.dist_max = 100;

// Salto: de longe; cai onde o player estava.
var _salto = ataque_novo(30, 28, 30, 30, 28, 360, false);
_salto.tipo = "salto";
_salto.voo = 24;
_salto.dist_min = 100;
_salto.dist_max = 9999;

ataques = [_machadada1, _tiro, _salto];
tem_arma = true;
arma_sprite = spr_arma_machado;
// No desenho do chefe: a mão do machado e a boca do bacamarte (em px a partir dos pés).
mao_x = 4;
mao_y = 12;
boca_x = 20;
boca_y = 22;

// --- Fase 2 (besta, abaixo de 50%) ---
tem_fase2 = true;

// Garras: combo de 3, rápido, aceita parry.
var _garra3 = ataque_novo(8, 4, 20, 15, 26, 120, true);
var _garra2 = ataque_novo(8, 4, 0, 15, 26, 120, true);
var _garra1 = ataque_novo(10, 4, 0, 15, 26, 120, true);
_garra1.seguinte = _garra2;
_garra1.chance = 1;
_garra2.seguinte = _garra3;
_garra2.chance = 1;
_garra1.dist_max = 36;

// Investida: atravessa 120 px; acerta quem estiver em volta dele no caminho.
var _investida = ataque_novo(24, 20, 30, 30, 14, 360, false);
_investida.avanco = 120;
_investida.dist_min = 40;
_investida.dist_max = 110;

// Salto rápido
var _salto2 = ataque_novo(20, 24, 24, 30, 28, 360, false);
_salto2.tipo = "salto";
_salto2.voo = 20;
_salto2.dist_min = 110;
_salto2.dist_max = 9999;

ataques_fase2 = [_garra1, _investida, _salto2];
vel_fase2 = 2.0;
spr = {
    parado: spr_chefe_idle, andando: spr_chefe_walk, ataque: spr_chefe_ataque,
    hit: spr_chefe_stagger, stagger: spr_chefe_stagger, caido: spr_chefe_caido,
    morte: spr_chefe_stagger, transforma: spr_chefe_transforma
};
spr_fase2 = {
    parado: spr_chefe_besta_idle, andando: spr_chefe_besta_corrida, ataque: spr_chefe_besta_garra,
    hit: spr_chefe_besta_stagger, stagger: spr_chefe_besta_stagger, caido: spr_chefe_besta_caido,
    morte: spr_chefe_besta_morte
};
// Ataques com animação própria
_tiro.spr = spr_chefe_tiro;
_salto.spr = spr_chefe_salto;
_investida.spr = spr_chefe_besta_investida;
_salto2.spr = spr_chefe_besta_salto;

// O chefe nunca renasce, nem depois de descansar.
if (obj_game.chefe_morto) {
    instance_destroy();
}