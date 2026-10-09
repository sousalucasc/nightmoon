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

