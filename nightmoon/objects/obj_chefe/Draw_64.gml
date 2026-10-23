// Barra do chefe: só depois que ele acorda.
if (acordado && estado != INI.MORTE) {
    var _larg = 200;
    var _x1 = (LARGURA_BASE - _larg) / 2;
    var _y1 = ALTURA_BASE - 16;
    draw_set_colour(c_black);
    draw_rectangle(_x1 - 1, _y1 - 1, _x1 + _larg + 1, _y1 + 4, false);
    draw_set_colour(c_maroon);
    draw_rectangle(_x1, _y1, _x1 + _larg * hp / hp_max, _y1 + 3, false);
    scribble(nome).align(fa_center, fa_top).blend(c_white).draw(LARGURA_BASE / 2, _y1 - 16);
}