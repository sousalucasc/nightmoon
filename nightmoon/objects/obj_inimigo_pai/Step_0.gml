if (jogo_congelado()) exit;

estado_timer += 1;
if (flash > 0) {
    flash -= 1;
}

switch (estado) {
    case INI.IDLE:      inimigo_estado_idle();      break;
    case INI.PERSEGUIR: inimigo_estado_perseguir(); break;
    case INI.VOLTAR:    inimigo_estado_voltar();    break;
    case INI.ATAQUE:    inimigo_estado_ataque();    break;
    case INI.HITSTUN:   inimigo_estado_hitstun();   break;
    case INI.MORTE:     inimigo_estado_morte();     break;
	case INI.STAGGER:   inimigo_estado_stagger();   break;
    case INI.VISCERAL:  inimigo_estado_visceral();  break;
    case INI.CAIDO:     inimigo_estado_caido();     break;
}

depth = -y;

// inimigos não se empilham, se desencostam lentamente
var _outro = instance_place(x, y, obj_inimigo_pai);
if (_outro != noone && _outro.estado != INI.MORTE && estado != INI.MORTE) {
    var _dir_fuga = point_direction(_outro.x, _outro.y, x, y);
    move_and_collide(lengthdir_x(0.5, _dir_fuga), lengthdir_y(0.5, _dir_fuga), obj_parede);
}

inimigo_animar();
