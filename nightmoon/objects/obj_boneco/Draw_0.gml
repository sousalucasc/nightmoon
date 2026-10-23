// pisca pisca kkkkkk
if (flash > 0) gpu_set_fog(true, c_white, 1, 0);
draw_sprite_ext(sprite_index, 0, x, y, 1, 1, 0, c_white, 1);
if (flash > 0) gpu_set_fog(false, c_white, 0, 1);

if (ultimo_dano > 0) {
    scribble(string(ultimo_dano)).align(fa_center, fa_top).blend(c_white).draw(x, y - 40);
}