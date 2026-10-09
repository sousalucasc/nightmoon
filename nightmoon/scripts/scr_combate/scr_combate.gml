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

/// procura alvos do tipo _obj dentro de um setor
/// devolve array com os que estão dentro e ainda não estão em _acertados
function golpe_setor(_x, _y, _dir, _alcance, _arco, _obj, _acertados) {
    var _novos = [];
    with (_obj) {
        if (!array_contains(_acertados, id)) {
            var _dist = point_distance(_x, _y, x, y);
            var _ang = point_direction(_x, _y, x, y);
            // angle_difference dá a diferença entre dois ângulos, de -180 a 180.
            var _no_arco = (_arco >= 360) || (abs(angle_difference(_dir, _ang)) <= _arco / 2);
            if (_dist <= _alcance + raio && _no_arco) {
                array_push(_novos, id);
            }
        }
    }
    return _novos;
}

/// aplica dano num inimigo 
function inimigo_dano(_inst, _dano) {
    with (_inst) {
        hp -= _dano;
        flash = 6;
        ultimo_dano = _dano;
    }
}
