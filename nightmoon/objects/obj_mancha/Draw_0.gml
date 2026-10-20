// Pulsa: a transparência sobe e desce com o tempo.
draw_sprite_ext(sprite_index, 0, x, y, 1, 1, 0, c_white, 0.6 + 0.4 * sin(current_time / 200));