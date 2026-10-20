// Fade: escurece, troca de room e clareia.
if (fade_indo) {
    fade = min(1, fade + 0.08);
    if (fade >= 1) {
        fade_indo = false;
        room_goto(fade_destino);
    }
} else if (fade > 0) {
    fade = max(0, fade - 0.08);
}

// Tempo de jogo (em frames), só enquanto joga.
if (instance_exists(obj_player) && !jogo_congelado()) {
    tempo += 1;
}
