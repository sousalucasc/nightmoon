// pequenas funcoes usadas em qualquer lugar

// desenha contorno debug dos golpes
function desenhar_setor(_x, _y, _dir, _alcance, _arco) {
    var _passos = 12;
    var _ini = _dir - _arco / 2;
    var _px = _x + lengthdir_x(_alcance, _ini);
    var _py = _y + lengthdir_y(_alcance, _ini);
    if (_arco < 360) {
        draw_line(_x, _y, _px, _py);
    }
    for (var i = 1; i <= _passos; i++) {
        var _a = _ini + _arco * i / _passos;
        var _nx = _x + lengthdir_x(_alcance, _a);
        var _ny = _y + lengthdir_y(_alcance, _a);
        draw_line(_px, _py, _nx, _ny);
        _px = _nx;
        _py = _ny;
    }
    if (_arco < 360) {
        draw_line(_x, _y, _px, _py);
    }
}

// true enquanto o jogo está parado, hitstop, fade, menus
function jogo_congelado() {
    return obj_game.hitstop > 0 || obj_game.fade_indo;
}


// congela o jogo por alguns frames
function aplicar_hitstop(_frames) {
    obj_game.hitstop = max(obj_game.hitstop, _frames);
}

// cria um efeito visual que roda 1 vez
// _escala_y = -1 espelha o efeito 
function fx_criar(_x, _y, _spr, _ang, _escala_y) {
    var _fx = instance_create_depth(_x, _y, -_y - 1, obj_fx);
    _fx.sprite_index = _spr;
    _fx.image_angle = _ang;
    _fx.escala_y = _escala_y;
    return _fx;
}

// qual quadro mostrar de uma animação que deve durar _dur frames.
function anim_quadro(_t, _dur, _spr) {
    var _n = sprite_get_number(_spr);
    return min(_n - 1, floor(_t / _dur * _n));
}

// treme a câmera. _forca: deslocamento máximo em pixels
function tremer_tela(_forca) {
    obj_game.tremor = max(obj_game.tremor, _forca);
}

/// Mostra uma mensagem no meio da tela por 3 segundos.
function mostrar_texto(_texto) {
    obj_game.texto = _texto;
    obj_game.texto_timer = 180;
}

var _font;
_font = font_get_name(fnt_hud);
scribble_font_bake_shadow(_font,"fnt_hud_novo",0,1,c_black,1,-1,false);
scribble_font_bake_outline_8dir("fnt_hud_novo","fnt_hud_oficial",c_black,false);
scribble_font_set_default("fnt_hud_oficial");
scribble_font_delete("fnt_hud_novo");