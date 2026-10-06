var _mx = obj_game.mover_x;
var _my = obj_game.mover_y;

// na diagonal (1,1) o comprimento fica 1,41
// dividir pelo comprimento deixa a direção com comprimento 1

var _comp = point_distance(0,0,_mx,_my);
if (_comp > 0){
	move_and_collide(_mx/_comp*vel,_my/_comp*vel,obj_parede);
}

// o corpo vira pro lado do mouse

if(obj_game.mira_dir>90 && obj_game.mira_dir<270){
	lado = -1;	
}else{
	lado = 1;
}

depth = -y;