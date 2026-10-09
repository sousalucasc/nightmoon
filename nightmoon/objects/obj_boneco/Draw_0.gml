var _cor = (flash > 0) ? c_red : c_white;
draw_sprite_ext(sprite_index, 0, x, y, 1, 1, 0, _cor, 1);

if (ultimo_dano > 0) {
    draw_set_halign(fa_center);
    draw_text(x, y - 40, string(ultimo_dano));
    draw_set_halign(fa_left);
}
