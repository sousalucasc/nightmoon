// draw gui por cima de tudo

// debug draw gui
if (debug) {
    draw_text(4, 4, "Arma: " + arma.nome);
    draw_text(4, 18, "Pistola: " + pistola.nome);
    draw_text(4, 32, "FOR " + string(atr_forca) + "  DES " + string(atr_destreza));
    draw_text(4, 46, "Almas: " + string(almas));
    if (instance_exists(obj_player)) {
        draw_text(4, 60, "Balas: " + string(obj_player.balas));
    }
    if (lock_alvo != noone) {
        draw_text(4, 74, "Lock: " + string(lock_alvo));
    }
}