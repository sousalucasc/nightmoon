if (jogo_congelado()) exit;

var _x0 = x;
var _y0 = y;
x += lengthdir_x(vel, dir);
y += lengthdir_y(vel, dir);
dist += vel;

// se bater na parede, destruir instancia
if (collision_line(_x0, _y0, x, y, obj_parede, false, true) != noone) {
    instance_destroy();
    exit;
}

// se acertar alvo
if (do_player) {
    var _alvo = projetil_achar_alvo(_x0, _y0, x, y, obj_boneco);
    if (_alvo != noone) {
        projetil_acertar_inimigo(_alvo);
        instance_destroy();
        exit;
    }
}

// se passar do alcance
if (dist >= alcance) {
    instance_destroy();
    exit;
}

depth = -y;