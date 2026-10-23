// Com o debug ligado, o player fica ciano enquanto está invulnerável.
var _cor = c_white;
if (obj_game.debug && (invulneravel || invul_timer > 0)) {
    _cor = c_aqua;
}

// Arma apontando para cima fica atrás do corpo; para baixo, na frente.
var _dir_arma = obj_game.mira_dir;
if (estado == PL.ATAQUE) {
    _dir_arma = ataque_dir;
}
var _arma_atras = (_dir_arma > 20 && _dir_arma < 160);
// Morto, curando ou no visceral: sem arma.
var _com_arma = (estado != PL.MORTE && estado != PL.CURA && estado != PL.VISCERAL);

if (_arma_atras && _com_arma) player_desenhar_arma();
// lado = -1 espelha o desenho na horizontal.
draw_sprite_ext(sprite_index, image_index, x, y, lado, 1, 0, _cor, 1);
if (!_arma_atras && _com_arma) player_desenhar_arma();


// DEBUG
if (obj_game.debug) {
    // stamina (branco), centralizado e acima do nome do estado
    scribble("st=" + string(st) + "/" + string(st_max) + " esp=" + string(st_espera)).align(fa_center, fa_bottom).blend(c_white).draw(x, y - 46);

    // nome do estado, logo acima das barras
    scribble(obj_game.nomes_pl[estado]).align(fa_center, fa_bottom).blend(c_lime).draw(x, y - 32);

    draw_set_colour(c_white);
    draw_rectangle(bbox_left, bbox_top, bbox_right, bbox_bottom, true);
    draw_line(x, y, mouse_x, mouse_y);

    // Barras: vida (vermelho) e stamina (amarelo)
    draw_healthbar(x - 10, y - 28, x + 10, y - 27, hp / hp_max * 100, c_black, c_red, c_red, 0, true, false);
    draw_healthbar(x - 10, y - 25, x + 10, y - 24, st / st_max * 100, c_black, c_yellow, c_yellow, 0, true, false);
    draw_set_colour(c_white);

    // debug do golpe
	if (estado == PL.ATAQUE) {
    if (estado_timer > golpe.windup && estado_timer <= golpe.windup + golpe.ativo) {
        draw_set_colour(c_red);
    } else {
        draw_set_colour(c_gray);
    }
    desenhar_setor(x, y, ataque_dir, golpe.alcance, golpe.arco);
    draw_set_colour(c_white);
}
}