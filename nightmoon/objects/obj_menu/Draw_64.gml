draw_set_font(fnt_hud);

// Fundo escurecido
draw_set_alpha(0.75);
draw_set_colour(c_black);
draw_rectangle(0, 0, LARGURA_BASE, ALTURA_BASE, false);
draw_set_alpha(1);

// textos com o mesmo estilo do HUD (fonte Scribble com contorno e sombra)
scribble(titulo).align(fa_center, fa_top).blend(c_white).draw(LARGURA_BASE / 2, 30);

for (var i = 0; i < array_length(opcoes); i++) {
    if (i == sel) {
        scribble("> " + opcoes[i] + " <").align(fa_center, fa_top).blend(c_yellow).draw(LARGURA_BASE / 2, 60 + i * 14);
    } else {
        scribble(opcoes[i]).align(fa_center, fa_top).blend(c_white).draw(LARGURA_BASE / 2, 60 + i * 14);
    }
}

if (tipo == "nivel") {
    scribble("Almas: " + string(obj_game.almas) + "   Custo: " + string(nivel_custo())).align(fa_center, fa_top).blend(c_white).draw(LARGURA_BASE / 2, 140);
}