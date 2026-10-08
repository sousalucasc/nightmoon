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
	player_tentar_esquivar();
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
	esq_desacel = esq_vel/esq.duracao;
	player_gastar_stamina(esq.custo);	
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

// so esquiva se o botao foi apertado e houver stamina, devolve true se comecou
function player_tentar_esquivar(){
	if (obj_game.buf_esquiva > 0 && st > 0){
		obj_game.buf_esquiva = 0; // gasta o buffer
		player_comecar_esquiva();
		return true;
	}
	return false;
}

// gasto de stamina
function player_gastar_stamina(_custo) {
    st = max(0, st - _custo);
    st_espera = 30;   // meio segundo sem regenerar
}

function player_estado_hitstun() {
    // Empurrão que desacelera, igual à esquiva.
    move_and_collide(lengthdir_x(kb_vel, kb_dir), lengthdir_y(kb_vel, kb_dir), obj_parede);
    kb_vel = max(0, kb_vel - kb_desacel);
    if (estado_timer >= 18) {
        invul_timer = 10;
        player_trocar(PL.LIVRE);
    }
}

function player_estado_morte(){
	if (estado_timer >= 60){
		room_restart();	
	}
}	
