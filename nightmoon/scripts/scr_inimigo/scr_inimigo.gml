// funcoes dos inimigos, chamados por eles mesmos: x, y, estado etc. sao dele

/// cria um ataque de inimigo com os valores mais comuns
function ataque_novo(_windup, _ativo, _recovery, _dano, _alcance, _arco, _parry) {
    return {
        windup: _windup, ativo: _ativo, recovery: _recovery,
        dano: _dano, alcance: _alcance, arco: _arco,
        parry: _parry, // se aceita parry
        avanco: 0, // pixels que anda durante o ativo
        dist_min: 0, // so usa este ataque com o player
        dist_max: _alcance + 6,// entre dist_min e dist_max
        seguinte: undefined, //combo
        chance: 0,// chance de emendar, de 0 a 1
        tipo: "golpe"// "golpe", "tiro" ou "salto"
    };
}

function inimigo_trocar(_novo) {
    estado = _novo;
    estado_timer = 0;
}

function inimigo_dist_player() {
    if (!instance_exists(obj_player)) return 99999;
    return point_distance(x, y, obj_player.x, obj_player.y);
}

function inimigo_player_vivo() {
    return instance_exists(obj_player) && obj_player.estado != PL.MORTE;
}

function inimigo_estado_idle() {
    if (acordado && inimigo_player_vivo() && inimigo_dist_player() <= aggro) {
        inimigo_trocar(INI.PERSEGUIR);
    }
}

function inimigo_estado_perseguir() {
    // volta se player morreu, ou se longe demais do ponto
    if (!inimigo_player_vivo() || point_distance(x, y, inicio_x, inicio_y) > desiste) {
        inimigo_trocar(INI.VOLTAR);
        return;
    }

    var _dist = inimigo_dist_player();
    var _dir = point_direction(x, y, obj_player.x, obj_player.y);
    lado = (obj_player.x < x) ? -1 : 1;

    // entre um ataque e outro, esperar
    if (espera > 0) {
        espera -= 1;
    } else {
        var _a = inimigo_escolher_ataque(_dist);
        if (_a != undefined) {
            inimigo_comecar_ataque(_a);
            return;
        }
    }

    if (_dist > dist_parar) {
        move_and_collide(lengthdir_x(vel, _dir), lengthdir_y(vel, _dir), obj_parede);
    }
}

function inimigo_estado_voltar() {
    var _dist = point_distance(x, y, inicio_x, inicio_y);
    // chegou (ou ficou preso tentando): volta a esperar.
    if (_dist < 4 || estado_timer > 300) {
        inimigo_trocar(INI.IDLE);
        return;
    }
    var _dir = point_direction(x, y, inicio_x, inicio_y);
    move_and_collide(lengthdir_x(vel, _dir), lengthdir_y(vel, _dir), obj_parede);
    lado = (lengthdir_x(1, _dir) < 0) ? -1 : 1;
}

// sorteia um ataque entre todos que puderem
function inimigo_escolher_ataque(_dist) {
    var _validos = [];
    for (var i = 0; i < array_length(ataques); i++) {
        var _a = ataques[i];
        if (_dist >= _a.dist_min && _dist <= _a.dist_max) {
            array_push(_validos, _a);
        }
    }
    if (array_length(_validos) == 0) return undefined;
    return _validos[irandom(array_length(_validos) - 1)];
}

function inimigo_comecar_ataque(_a) {
    ataque = _a;
    acertados = [];
    if (instance_exists(obj_player)) {
        ataque_dir = point_direction(x, y, obj_player.x, obj_player.y);
    }
    inimigo_trocar(INI.ATAQUE);
}

function inimigo_estado_ataque() {
    var _a = ataque;
    var _fim_windup = _a.windup;
    var _fim_ativo  = _a.windup + _a.ativo;
    var _fim_total  = _fim_ativo + _a.recovery;

    if (estado_timer <= _fim_windup) {
        // segue o player, mas trava nos ultimos 8 frames
        if (estado_timer < _fim_windup - 8 && instance_exists(obj_player)) {
            ataque_dir = point_direction(x, y, obj_player.x, obj_player.y);
        }
    } else if (estado_timer <= _fim_ativo) {
        if (_a.avanco > 0) {
            var _passo = _a.avanco / _a.ativo;
            move_and_collide(lengthdir_x(_passo, ataque_dir), lengthdir_y(_passo, ataque_dir), obj_parede);
        }
        inimigo_golpear(_a);
        // combo, no ultimo frame do ativo, pode emendar o proximo
        if (estado_timer == _fim_ativo && _a.seguinte != undefined && random(1) < _a.chance) {
            inimigo_comecar_ataque(_a.seguinte);
            return;
        }
    }

    lado = (lengthdir_x(1, ataque_dir) < 0) ? -1 : 1;

    if (estado_timer >= _fim_total) {
        espera = espera_entre;
        inimigo_trocar(INI.PERSEGUIR);
    }
}

// acerta o player
function inimigo_golpear(_a) {
    var _alvos = golpe_setor(x, y, ataque_dir, _a.alcance, _a.arco, obj_player, acertados);
    if (array_length(_alvos) > 0 && player_dano(_a.dano, x, y)) {
        array_push(acertados, _alvos[0]);
    }
}

function inimigo_estado_hitstun() {
    if (estado_timer >= 12) {
        inimigo_trocar(INI.PERSEGUIR);
    }
}

function inimigo_estado_morte() {
    if (estado_timer >= 30) {
        instance_destroy();
    }
}

// golpes so interrompem quem esta parado
function inimigo_pode_interromper() {
    if (estado == INI.ATAQUE) {
        var _no_ativo = (estado_timer > ataque.windup && estado_timer <= ataque.windup + ataque.ativo);
        return !_no_ativo;
    }
    return (estado == INI.IDLE || estado == INI.PERSEGUIR || estado == INI.VOLTAR || estado == INI.HITSTUN);
}

function inimigo_morrer() {
    inimigo_trocar(INI.MORTE);
}


