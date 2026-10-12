// Draw GUI: desenhado por cima de tudo, em coordenadas de tela (320x180).
if (debug) {
    draw_text(4, 4, "Arma: " + arma.nome);
    draw_text(4, 18, "Pistola: " + pistola.nome);
    draw_text(4, 32, "FOR " + string(atr_forca) + "  DES " + string(atr_destreza));
    if (instance_exists(obj_player)) {
        draw_text(4, 46, "Balas: " + string(obj_player.balas));
    }
}