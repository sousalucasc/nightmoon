//Funcoes do player

// Troca de estado
function player_trocar(_novo){
	estado = _novo;
	estado_timer = 0;
}


// Movimentacao
function player_mover(_mult){
	var _mx = obj_game.mover_x;
	var _my = obj_game.mover_y;
	var _comp = point_distance(0,0,_mx,_my);
	if(_comp > 0){
			move_and_collide(_mx / _comp * vel * _mult, _my / _comp * vel * _mult, obj_parede);
	}
}

// Estado livre
function player_estado_livre(){
	player_mover(1);
	if(obj_game.aperta_esquiva){
		player_comecar_esquiva();
	}
}

// Esquiva, backstep ou dash dependendo do movimento do player
function player_comecar_esquiva(){
	if(obj_game.mover_x !=0 || obj_game.mover_y != 0){
		//andando, dash na direcao do movimento
		esq = dash;
		esq_dir = point_direction(0,0,obj_game.mover_x,obj_game.mover_y);
	}else{
		//parado, backstep para longe da mira
		esq = backstep;
		esq_dir = obj_game.mira_dir + 180;
	}
	
	// velocidade, distancia e duracao
	esq_vel = 2*esq.distancia/esq.duracao;
	esq_deacel = esq_vel/esq.duracao;
	player_trocar(PL.ESQUIVA);
}

function player_estado_esquiva(){
	move_and_collide(lengthdir_x(esq_vel,esq_dir), lengthdir_y(esq_vel,esq_dir),obj_parede);
	esq_vel = max(0,esq_vel - esq_desacel);
	
	//invulneravel so durante iframes
	invulneravel = (estado_timer >= esq.iframe_ini && estado_timer <= esq.iframe_fim);
	if(estado_timer >= esq.duracao){
		invulneravel = false;
		player_trocar(PL.LIVRE);
	}
}