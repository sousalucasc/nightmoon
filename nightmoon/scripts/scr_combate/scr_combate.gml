// funcoes de combate, quem sofre dano, e quanto sofre

// aplica dano no player. _de_x, _de_y: de onde veio o golpe (para o empurrão).
/// _tiro_id: número do tiro, para os chumbos de um mesmo tiro acertarem uma vez só.
/// Golpes não passam _tiro_id (fica -1). Devolve true se o dano entrou.
function player_dano(_dano, _de_x, _de_y, _tiro_id = -1) {
    var _entrou = false;
    with (obj_player) {
        var _mesmo_tiro = (_tiro_id != -1 && _tiro_id == ultimo_tiro_levado);
        if (!invulneravel && invul_timer <= 0 && estado != PL.MORTE && !_mesmo_tiro) {
            _entrou = true;
			aplicar_hitstop(4);
            tremer_tela(2);
            if (_tiro_id != -1) {
                ultimo_tiro_levado = _tiro_id;
            }
            hp -= _dano;
            // Hyper armor: golpe com a flag não é interrompido no windup nem no ativo.
            var _hyper = (estado == PL.ATAQUE && golpe.hyper && estado_timer <= golpe.windup + golpe.ativo);
            if (hp <= 0) {
                hp = 0;
                player_trocar(PL.MORTE);
            } else if (_hyper) {
                invul_timer = 10;   // o dano entra, mas o golpe continua
            } else {
                kb_dir = point_direction(_de_x, _de_y, x, y);
                kb_vel = 2 * 10 / 18;
                kb_desacel = kb_vel / 18;
                player_trocar(PL.HITSTUN);
            }
        }
    }
    return _entrou;
}

// procura alvos do tipo _obj dentro de um setor
// devolve array com os que estão dentro e ainda não estão em _acertados
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

// aplica dano num inimigo 
function inimigo_dano(_inst, _dano) {
    with (_inst) {
        if (estado != INI.MORTE && estado != INI.TRANSFORMA && !no_ar) {
            hp -= _dano;
            flash = 6;
            ultimo_dano = _dano;
            fx_criar(x, y - 10, spr_fx_sangue, irandom(359), 1);
            if (tem_fase2 && fase == 1 && hp <= hp_max / 2) {
                // Chefe na metade da vida: transforma (e não morre neste golpe).
                hp = max(hp, 1);
                inimigo_trocar(INI.TRANSFORMA);
            } else if (hp <= 0) {
                hp = 0;
                inimigo_morrer();
            } else if (pode_hitstun && inimigo_pode_interromper()) {
                inimigo_trocar(INI.HITSTUN);
            }
        }
    }
}
// dano escalado com dex e str
function dano_escalado(_base, _esc_for, _esc_des) {
    var _bonus = _esc_for * 0.08 * obj_game.atr_forca + _esc_des * 0.08 * obj_game.atr_destreza;
    return round(_base * (1 + _bonus));
}

//varre o arco no ativo
function angulo_golpe(_timer, _windup, _ativo, _dir, _arco, _sentido) {
    var _ini = _dir + _arco / 2 * _sentido;
    var _fim = _dir - _arco / 2 * _sentido;
    if (_timer <= _windup) return _ini;
    if (_timer <= _windup + _ativo) return lerp(_ini, _fim, (_timer - _windup) / _ativo);
    return _fim;
}

// procura um alvo objeto que o seu raio encoste no caminho do projetil
// fez neste frame (de _x0, _y0 até _x1, _y1). Devolve o id, ou noone
function projetil_achar_alvo(_x0, _y0, _x1, _y1, _obj) {
    var _achou = noone;
    var _mx = (_x0 + _x1) / 2;   // meio do caminho
    var _my = (_y0 + _y1) / 2;
    with (_obj) {
        if (_achou == noone) {
            var _r = raio + 2;
            if (point_distance(_x1, _y1, x, y) <= _r || point_distance(_mx, _my, x, y) <= _r) {
                _achou = id;
            }
        }
    }
    return _achou;
}

// roda dentro do projetil, quando ele acerta um inimigo
function projetil_acertar_inimigo(_alvo) {
    // parry chega com a janela aberta, no ataque que aceita
    if (inimigo_janela_parry(_alvo, parry_bonus) && _alvo.ultimo_tiro_parry != tiro_id) {
        _alvo.ultimo_tiro_parry = tiro_id;   // chumbos do mesmo tiro
        with (_alvo) {
            inimigo_trocar(INI.STAGGER);
        }
        // parry certo devolve a bala 
        if (instance_exists(obj_player) && obj_player.ultimo_reembolso != tiro_id) {
            obj_player.ultimo_reembolso = tiro_id;
            obj_player.balas = min(obj_player.balas_max, obj_player.balas + 1);
        }
        fx_criar(_alvo.x, _alvo.y - 12, spr_fx_parry, 0, 1);
        aplicar_hitstop(6);
        tremer_tela(2);
    }
    inimigo_dano(_alvo, dano);
    aplicar_hitstop(2);
}

// true se o inimigo esta na janela de parry, ultimos 10 frames
function inimigo_janela_parry(_inst, _bonus) {
    var _aberta = false;
    with (_inst) {
        if (estado == INI.ATAQUE && ataque.parry) {
            var _ini = ataque.windup - 10 - _bonus;
            var _fim = ataque.windup + 2;
            _aberta = (estado_timer > _ini && estado_timer <= _fim);
        }
    }
    return _aberta;
}
