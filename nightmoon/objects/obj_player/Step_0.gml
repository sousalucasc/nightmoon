estado_timer += 1;


// estado livre e esquiva do player
switch(estado){
	case PL.LIVRE:
		player_estado_livre();
	break;
	case PL.ESQUIVA:
		player_estado_esquiva();
	break;
}


// corpo vira pro lado do mouse
if(obj_game.mira_dir>90 && obj_game.mira_dir<270){
	lado = -1;	
}else{
	lado = 1;
}

depth = -y;