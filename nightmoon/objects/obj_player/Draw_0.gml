// Com o debug ligado, o player fica ciano enquanto está invulnerável.
var _cor = c_white;
if (obj_game.debug && (invulneravel || invul_timer > 0)) {
    _cor = c_aqua;
}
// lado = -1 espelha o desenho na horizontal.
draw_sprite_ext(sprite_index, image_index, x, y, lado, 1, 0, _cor, 1);

if (obj_game.debug) {
	draw_text(x, y - 50, "st=" + string(st) + " max=" + string(st_max) + " espera=" + string(st_espera));
    draw_set_colour(c_lime);
    draw_rectangle(bbox_left, bbox_top, bbox_right, bbox_bottom, true);
    draw_line(x, y, mouse_x, mouse_y);
    // Nome do estado em cima da cabeça
    draw_set_halign(fa_center);
    draw_text(x, y - 36, obj_game.nomes_pl[estado]);
    draw_set_halign(fa_left);
    // Barras: vida (vermelho) e stamina (amarelo)
    draw_healthbar(x - 10, y - 28, x + 10, y - 27, hp / hp_max * 100, c_black, c_red, c_red, 0, true, false);
    draw_healthbar(x - 10, y - 25, x + 10, y - 24, st / st_max * 100, c_black, c_yellow, c_yellow, 0, true, false);
    draw_set_colour(c_white);
	 // debug do golpe
	 // debug do golpe
    if (estado == PL.ATAQUE) {
        if (estado_timer > golpe.windup && estado_timer <= golpe.windup + golpe.ativo) {
            draw_set_colour(c_red);
        } else {
            draw_set_colour(c_gray);
        }
        desenhar_setor(x, y, ataque_dir, golpe.alcance, golpe.arco);
        draw_set_colour(c_lime);
    }
}