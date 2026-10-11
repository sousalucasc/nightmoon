if (jogo_congelado()) exit;
estado_timer += 1;


// estado livre e esquiva do player
switch(estado){
	case PL.LIVRE: player_estado_livre(); break;
	case PL.ESQUIVA: player_estado_esquiva(); break;
	case PL.HITSTUN: player_estado_hitstun(); break;
	case PL.MORTE: player_estado_morte(); break;
	case PL.ATAQUE:  player_estado_ataque();  break;
}

// stamina volta a encher depois de player_gastar_stamina
if(st_espera > 0){
	st_espera -= 1;
}else{
	st = min(st_max, st + 1);
}

// invulnerabilidade depois de apanhar
if(invul_timer > 0){
	invul_timer -=1;
}

// corpo vira pro lado do mouse
var _olhar = obj_game.mira_dir;
if (estado == PL.ATAQUE) {
    _olhar = ataque_dir;
}
if (_olhar > 90 && _olhar < 270) {
    lado = -1;
} else {
    lado = 1;
}

player_animar();

depth = -y;