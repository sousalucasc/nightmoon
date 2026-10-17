// A névoa é o sprite de 16x16 repetido pela área da instância (esticada na room),
// com a textura andando para o lado.
var _alpha = 0.4;
if (fechada) {
    _alpha = 0.8;
}
var _quadro = (current_time div 150) mod sprite_get_number(sprite_index);
for (var i = 0; i < image_xscale; i++) {
    for (var j = 0; j < image_yscale; j++) {
        draw_sprite_ext(sprite_index, _quadro, x + i * 16, y + j * 16, 1, 1, 0, c_white, _alpha);
    }
}
