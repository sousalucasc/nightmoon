draw_set_font(fnt_hud);

// Fundo escurecido
draw_set_alpha(0.75);
draw_set_colour(c_black);
draw_rectangle(0, 0, LARGURA_BASE, ALTURA_BASE, false);
draw_set_alpha(1);

draw_set_halign(fa_center);
draw_set_colour(c_white);
draw_text(LARGURA_BASE / 2, 30, titulo);

for (var i = 0; i < array_length(opcoes); i++) {
    if (i == sel) {
        draw_set_colour(c_yellow);
        draw_text(LARGURA_BASE / 2, 60 + i * 14, "> " + opcoes[i] + " <");
    } else {
        draw_set_colour(c_white);
        draw_text(LARGURA_BASE / 2, 60 + i * 14, opcoes[i]);
    }
}

draw_set_colour(c_white);
if (tipo == "nivel") {
    draw_text(LARGURA_BASE / 2, 140, "Almas: " + string(obj_game.almas) + "   Custo: " + string(nivel_custo()));
}
draw_set_halign(fa_left);