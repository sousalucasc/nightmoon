// funcoes de combate, quem sofre dano, e quanto sofre

// aplica dano no player e devolve true quando da dano
function player_dano(_dano,_de_x,_de_y){
	var _entrou = false;
	with(obj_player){
		if(!invulneravel && invul_timer <= 0 &&estado != PL.MORTE){
			_entrou = true;
			hp -= _dano;
			kb_dir = point_direction(_de_x,_de_y,x,y); // knockback para longe de quem deu dano
			kb_vel = 2* 10/18; //	10 pixels em 18 frames
			kb_desacel = kb_vel /18;
			if(hp<=0){
				hp = 0;
				player_trocar(PL.MORTE);
			}else{
				player_trocar(PL.HITSTUN);
			}
		}
	}
	return _entrou;
}
