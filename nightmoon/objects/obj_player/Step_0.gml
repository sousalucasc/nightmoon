estado_timer += 1;


// estado livre e esquiva do player
switch(estado){
	case PL.LIVRE: player_estado_livre(); break;
	case PL.ESQUIVA: player_estado_esquiva(); break;
	case PL.HITSTUN: player_estado_hitstun(); break;
	case PL.MORTE: player_estado_morte(); break;
}

// stamina volta a encher depois de 30 frames sem gastar
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
if(obj_game.mira_dir>90 && obj_game.mira_dir<270){
	lado = -1;	
}else{
	lado = 1;
}

depth = -y;