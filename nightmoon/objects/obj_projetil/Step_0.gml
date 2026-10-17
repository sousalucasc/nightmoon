if (jogo_congelado()) exit;

var _x0 = x;
var _y0 = y;
x += lengthdir_x(vel, dir);
y += lengthdir_y(vel, dir);
dist += vel;

// Bateu numa parede no caminho?
if (collision_line(_x0, _y0, x, y, obj_parede, false, true) != noone) {
    instance_destroy();
    exit;
}

if (do_player) {
    // Tiro do player: acertou algum inimigo no caminho?
    var _alvo = projetil_achar_alvo(_x0, _y0, x, y, obj_inimigo_pai);
    if (_alvo != noone) {
        projetil_acertar_inimigo(_alvo);
        instance_destroy();
        exit;
    }
} else {
    // Tiro de inimigo: acertou o player?
    if (projetil_achar_alvo(_x0, _y0, x, y, obj_player) != noone) {
        player_dano(dano, _x0, _y0, tiro_id);
        instance_destroy();
        exit;
    }
}

// Passou do alcance: some.
if (dist >= alcance) {
    instance_destroy();
    exit;
}

depth = -y;
