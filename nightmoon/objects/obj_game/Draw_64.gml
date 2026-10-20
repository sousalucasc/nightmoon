// vem por cima de tudo
draw_set_font(fnt_hud);

// --- HUD ---
if (instance_exists(obj_player)) {
    var _p = obj_player;

    // barra cresce com o HP máximo (100 de vida = 50 px).
    var _larg_hp = _p.hp_max / 2;
    draw_set_colour(c_black);
    draw_rectangle(6, 6, 8 + _larg_hp, 11, false);
    draw_set_colour(c_red);
    if (_p.hp > 0) {
        draw_rectangle(7, 7, 7 + _larg_hp * _p.hp / _p.hp_max, 10, false);
    }

    // stamina
    var _larg_st = _p.st_max / 2;
    draw_set_colour(c_black);
    draw_rectangle(6, 13, 8 + _larg_st, 16, false);
    draw_set_colour(c_yellow);
    if (_p.st > 0) {
        draw_rectangle(7, 14, 7 + _larg_st * _p.st / _p.st_max, 15, false);
    }
    draw_set_colour(c_white);

    // frascos e balas
    draw_sprite(spr_icone_frasco, 0, 6, ALTURA_BASE - 14);
    draw_text(16, ALTURA_BASE - 16, string(_p.frascos));
    draw_sprite(spr_icone_bala, 0, 32, ALTURA_BASE - 13);
    draw_text(40, ALTURA_BASE - 16, string(_p.balas));

    // almas
    draw_set_halign(fa_right);
    draw_text(LARGURA_BASE - 6, ALTURA_BASE - 16, string(almas));
    draw_set_halign(fa_left);
    draw_sprite(spr_icone_almas, 0, LARGURA_BASE - 16 - string_width(string(almas)), ALTURA_BASE - 13);
}

// debug
if (debug) {
    draw_text(4, 22, "Arma: " + arma.nome);
    draw_text(4, 34, "Pistola: " + pistola.nome);
    draw_text(4, 46, "FOR " + string(atr_forca) + "  DES " + string(atr_destreza));
}

// mensagem na tela
if (texto_timer > 0) {
    draw_set_halign(fa_center);
    draw_set_colour(c_yellow);
    draw_text(LARGURA_BASE / 2, 70, texto);
    draw_set_colour(c_white);
    draw_set_halign(fa_left);
}

// fade transicao
if (fade > 0) {
    draw_set_alpha(fade);
    draw_set_colour(c_black);
    draw_rectangle(0, 0, LARGURA_BASE, ALTURA_BASE, false);
    draw_set_alpha(1);
    draw_set_colour(c_white);
}