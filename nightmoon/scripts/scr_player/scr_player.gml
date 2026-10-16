	//Funcoes do player

// Troca de estado
function player_trocar(_novo){
	estado = _novo;
	estado_timer = 0;
}

// Estado livre
function player_estado_livre() {
    player_mover(1);
    if (player_tentar_esquivar()) return;
    if (player_tentar_atacar()) return;
    if (player_tentar_atirar()) return;
}

/* antes do tweak o codigo ficava assim
// Estado livre
function player_estado_livre(){
 player_mover(1);
    if (player_tentar_esquivar()) return;
    if (player_tentar_atacar()) return;
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

*/



// Movimentacao
function player_mover(_mult){
	var _mx = obj_game.mover_x;
	var _my = obj_game.mover_y;
	var _comp = point_distance(0,0,_mx,_my);
	if(_comp > 0){
			move_and_collide(_mx / _comp * vel * _mult, _my / _comp * vel * _mult, obj_parede);
	}
}

function player_comecar_esquiva(){
	if(obj_game.mover_x != 0 || obj_game.mover_y != 0){
		// andando, dash na direcao do movimento
		esq = dash;
		esq_dir = point_direction(0,0,obj_game.mover_x,obj_game.mover_y);
		esq_exp = true;
	}else{
		// parado, backstep para longe da mira (continua igual)
		esq = backstep;
		esq_dir = obj_game.mira_dir + 180;
		esq_exp = false;
	}

	if(esq_exp){
		// dash: arranque forte e freada seca (desaceleracao exponencial)
		esq_fator = 0.78;
		esq_vel = esq.distancia * 1.1* (1 - esq_fator) / (1 - power(esq_fator, esq.duracao));
	}else{
		// backstep: desaceleracao linear, como antes
		esq_vel = 2*esq.distancia/esq.duracao;
		esq_desacel = esq_vel/esq.duracao;
	}

	player_gastar_stamina(esq.custo);
	player_trocar(PL.ESQUIVA);
}

function player_estado_esquiva(){
	move_and_collide(lengthdir_x(esq_vel,esq_dir), lengthdir_y(esq_vel,esq_dir), obj_parede);

	if(esq_exp){
		esq_vel *= esq_fator;
	}else{
		esq_vel = max(0, esq_vel - esq_desacel);
	}

	// invulneravel so durante iframes
	invulneravel = (estado_timer >= esq.iframe_ini && estado_timer <= esq.iframe_fim);
	if(estado_timer >= esq.duracao){
		invulneravel = false;
		player_trocar(PL.LIVRE);
	}
}

// so esquiva se o botao foi apertado e st > 20, devolve true se comecou
function player_tentar_esquivar(){
	if (obj_game.buf_esquiva > 0 && st > 20){
		obj_game.buf_esquiva = 0;
		player_comecar_esquiva();
		return true;
	}
	return false;
}

// gasto de stamina
//function player_gastar_stamina(_custo) {
//    st = max(0, st - _custo);
//    st_espera = 120;   // meio segundo sem regenerar // era 30
//}

function player_gastar_stamina(_custo) {
    var _debito = max(0, _custo - st);       // quanto passou do que você tinha
    st = max(0, st - _custo);                // continua nunca ficando negativo
    st_espera = ceil(30 + _custo * 0.8 + _debito * 3);	    // delay curto + débito vira tempo travado
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

/// começa um golpe leve ou pesado se o botão está no buffer e tem stamina.
/// se for num inimigo atordoado pega visceral
function player_tentar_atacar() {
    var _arma = obj_game.arma;
    if (obj_game.buf_leve > 0) {
        var _alvo = player_procurar_visceral();
        if (_alvo != noone) {
            obj_game.buf_leve = 0;
            player_comecar_visceral(_alvo);   // visceral nao gasta stamina!!
            return true;
        }
    }
    if (obj_game.buf_leve > 0 && st > 0) {
        obj_game.buf_leve = 0;
        // vindo de um golpe leve, segue o combo
        if (estado == PL.ATAQUE && !golpe_pesado) {
            combo_i = (combo_i + 1) mod array_length(_arma.leves);
        } else {
            combo_i = 0;
        }
        player_comecar_golpe(_arma.leves[combo_i], false);
        return true;
    }
    if (obj_game.buf_pesado > 0 && st > 0) {
        obj_game.buf_pesado = 0;
        player_comecar_golpe(_arma.pesado, true);
        return true;
    }
    return false;
}

function player_comecar_golpe(_golpe, _pesado) {
    golpe = _golpe;
    golpe_pesado = _pesado;
    acertados = [];                 // golpe novo
    ataque_dir = obj_game.mira_dir;
    // golpes do combo alternam o lado do corte
    if (_pesado || combo_i mod 2 == 0) {
        sentido = 1;
    } else {
        sentido = -1;
    }
    player_gastar_stamina(golpe.stamina);
    player_trocar(PL.ATAQUE);
}


function player_estado_ataque() {
    var _arma = obj_game.arma;
    var _fim_windup = golpe.windup;
    var _fim_ativo  = golpe.windup + golpe.ativo;
    var _fim_total  = _fim_ativo + golpe.recovery;

    if (estado_timer <= _fim_windup) {
        // windup gira para mira
        ataque_dir = obj_game.mira_dir;
    } else if (estado_timer <= _fim_ativo) {
        // primeiro frame de corte
        if (estado_timer == _fim_windup + 1) {
            fx_criar(x, y - 10, golpe.fx, ataque_dir, sentido * lado);
        }
        // quando ativo avanca um pouco
        var _passo = golpe.avanco / golpe.ativo;
        move_and_collide(lengthdir_x(_passo, ataque_dir), lengthdir_y(_passo, ataque_dir), obj_parede);

        var _dano = dano_escalado(golpe.dano, _arma.esc_for, _arma.esc_des);
        var _novos = golpe_setor(x, y, ataque_dir, golpe.alcance, golpe.arco, obj_inimigo_pai, acertados);
        for (var i = 0; i < array_length(_novos); i++) {
            array_push(acertados, _novos[i]);
            inimigo_dano(_novos[i], _dano);
        }
        if (array_length(_novos) > 0) {
            aplicar_hitstop(3);
            tremer_tela(1);
        }
    } else {
        // recovery.
        if (!golpe_pesado && player_tentar_atacar()) return;
        if (estado_timer > _fim_ativo + golpe.recovery / 2) {
			if (player_tentar_atirar()) return;
            if (player_tentar_esquivar()) return;
        }
    }

    if (estado_timer >= _fim_total) {
        player_trocar(PL.LIVRE);
    }
}

// escolhe sprite e quadro conforme o estado.
function player_animar() {
    anim_timer += 1;
    switch (estado) {
        case PL.LIVRE:
            if (obj_game.mover_x != 0 || obj_game.mover_y != 0) {
                sprite_index = spr.andando;
                image_index = (anim_timer div 6) mod sprite_get_number(sprite_index);
            } else {
                sprite_index = spr.parado;
                image_index = (anim_timer div 10) mod sprite_get_number(sprite_index);
            }
            break;
        case PL.ESQUIVA:
            sprite_index = (esq == dash) ? spr.dash : spr.backstep;
            image_index = anim_quadro(estado_timer, esq.duracao, sprite_index);
            break;
        case PL.ATAQUE:
            // 3 quadros: windup, ativo, recovery
            sprite_index = spr.ataque;
            if (estado_timer <= golpe.windup) {
                image_index = 0;
            } else if (estado_timer <= golpe.windup + golpe.ativo) {
                image_index = 1;
            } else {
                image_index = 2;
            }
            break;
		case PL.TIRO:
            // 3 quadros: preparando, disparo, recovery
            sprite_index = spr.tiro;
            if (estado_timer < obj_game.pistola.startup) {
                image_index = 0;
            } else if (estado_timer <= obj_game.pistola.startup + 4) {
                image_index = 1;
            } else {
                image_index = 2;
            }
            break;
		case PL.VISCERAL:
            sprite_index = spr.visceral;
            image_index = anim_quadro(estado_timer, 40, sprite_index);
            break;
        case PL.HITSTUN:
            sprite_index = spr.hit;
            image_index = anim_quadro(estado_timer, 18, sprite_index);
            break;
        case PL.MORTE:
            sprite_index = spr.morte;
            image_index = anim_quadro(estado_timer, 60, sprite_index);
            break;
    }
}

/// desenha a arma na mao girando conforme golpe
function player_desenhar_arma() {
    var _ang;
    if (estado == PL.ATAQUE) {
        _ang = angulo_golpe(estado_timer, golpe.windup, golpe.ativo, ataque_dir, golpe.arco, sentido * lado);
    } else {
        // Parada: apontando para a mira, um pouco para baixo.
        _ang = obj_game.mira_dir - 30 * lado;
    }
    draw_sprite_ext(obj_game.arma.sprite, 0, x + 2 * lado, y - 10, 1, 1, _ang, c_white, 1);

    // No tiro, a pistola aparece apontando para o alvo.
    if (estado == PL.TIRO) {
        // Apontando para a esquerda, espelha na vertical para não ficar de cabeça para baixo.
        var _esc_y = 1;
        if (ataque_dir > 90 && ataque_dir < 270) {
            _esc_y = -1;
        }
        // A mão da pistola, no desenho do tiro, fica 3 px à frente e 12 acima dos pés.
        draw_sprite_ext(obj_game.pistola.sprite, 0, x + 3 * lado, y - 12, 1, _esc_y, ataque_dir, c_white, 1);
    }
}
// começa um tiro se Q esta no buffer e tem bala.
function player_tentar_atirar() {
    if (obj_game.buf_tiro > 0 && balas > 0) {
        obj_game.buf_tiro = 0;
        balas -= 1;
        obj_game.contador_tiros += 1;
        tiro_id = obj_game.contador_tiros;
        ataque_dir = obj_game.mira_dir;
        player_trocar(PL.TIRO);
        return true;
    }
    return false;
}

function player_estado_tiro() {
    var _p = obj_game.pistola;
    // ate o tiro sair da pra mirar
    if (estado_timer <= _p.startup) {
        ataque_dir = obj_game.mira_dir;
    }
    if (estado_timer == _p.startup) {
        player_disparar(_p);
    }
    // segunda metade do recovery, pode esquivar
    if (estado_timer > _p.startup + _p.recovery / 2) {
        if (player_tentar_esquivar()) return;
    }
    if (estado_timer >= _p.startup + _p.recovery) {
        player_trocar(PL.LIVRE);
    }
}

/// cria os projéteis da pistola 
function player_disparar(_p) {
    for (var i = 0; i < _p.projeteis; i++) {
        var _ang = ataque_dir;
        if (_p.projeteis > 1) {
            // espalha igualmente dentro do leque: de -leque/2 até +leque/2.
            _ang = ataque_dir - _p.leque / 2 + _p.leque * i / (_p.projeteis - 1);
        }
        var _b = instance_create_depth(x, y, depth - 1, obj_projetil);
        _b.do_player = true;
        _b.dir = _ang;
        _b.vel = _p.vel;
        _b.alcance = _p.alcance;
        _b.dano = dano_escalado(_p.dano, _p.esc_for, _p.esc_des);
        _b.parry_bonus = _p.parry_bonus;
        _b.tiro_id = tiro_id;
    }
    // Clarão na boca do cano: da mão da pistola até a ponta do sprite dela.
    var _cano = sprite_get_width(_p.sprite) - sprite_get_xoffset(_p.sprite);
    fx_criar(x + 3 * lado + lengthdir_x(_cano, ataque_dir), y - 12 + lengthdir_y(_cano, ataque_dir), spr_fx_disparo, ataque_dir, 1);
    tremer_tela(1);
}

/// procura um inimigo em stagger perto e na direção da mira
function player_procurar_visceral() {
    var _achou = noone;
    var _px = x;
    var _py = y;
    var _mira = obj_game.mira_dir;
    with (obj_inimigo_pai) {
        if (estado == INI.STAGGER) {
            var _dist = point_distance(_px, _py, x, y);
            var _ang = point_direction(_px, _py, x, y);
            if (_dist <= 28 + raio && abs(angle_difference(_mira, _ang)) <= 60) {
                _achou = id;
            }
        }
    }
    return _achou;
}

function player_comecar_visceral(_alvo) {
    visceral_alvo = _alvo;
    ataque_dir = point_direction(x, y, _alvo.x, _alvo.y);
    with (_alvo) {
        inimigo_trocar(INI.VISCERAL);
    }
    player_trocar(PL.VISCERAL);
}

function player_estado_visceral() {
    invulneravel = true;
    // frame 20: o golpe entra. dano escala com dex
    if (estado_timer == 20 && instance_exists(visceral_alvo)) {
        var _dano = round(60 * (1 + 0.08 * obj_game.atr_destreza));
        inimigo_dano(visceral_alvo, _dano);
        fx_criar(visceral_alvo.x, visceral_alvo.y - 10, spr_fx_sangue, ataque_dir, 1);
        aplicar_hitstop(10);
        tremer_tela(3);
    }
    if (estado_timer >= 40) {
        invulneravel = false;
        // se ele sobreviveu, fica caido um tempinho
        if (instance_exists(visceral_alvo) && visceral_alvo.estado == INI.VISCERAL) {
            with (visceral_alvo) {
                inimigo_trocar(INI.CAIDO);
            }
        }
        player_trocar(PL.LIVRE);
    }
}