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
	
	scribble(string(_p.frascos)).draw(16, ALTURA_BASE - 16);
	
    draw_sprite(spr_icone_bala, 0, 36, ALTURA_BASE - 13);
	
	scribble(string(_p.balas)).draw(44, ALTURA_BASE - 16);

	// almas
	var _txt_almas = scribble(string(almas), "hud_almas").align(fa_right, fa_top);
	_txt_almas.draw(LARGURA_BASE - 6, ALTURA_BASE - 16);
	draw_sprite(spr_icone_almas, 0, LARGURA_BASE - 16 - _txt_almas.get_width(), ALTURA_BASE - 13);
}

// debug
if (debug) {
    //draw_text(4, 22, "Arma: " + arma.nome);
    //draw_text(4, 34, "Pistola: " + pistola.nome);
    //draw_text(4, 46, "FOR " + string(atr_forca) + "  DES " + string(atr_destreza));
	
	//scribble("[fa_middle][fa_center][scale,1]Arma: " + arma.nome).transform(0.5,0.5,182).draw(70,30);
	
	//scribble_anim_wave(.5,.5,0.25);
	//scribble("[rainbow][wave]Arma: " + arma.nome).align(fa_center,fa_middle).draw(70,30);
	
	scribble_anim_wave(.5,.25,0.1);
	scribble_anim_rainbow(.25,3);
	scribble("[rainbow][wave]Arma: " + arma.nome).draw(4, 22);
	scribble("[rainbow][wave]Pistola: " + pistola.nome).draw(4, 34);
	scribble("[rainbow][wave]FOR " + string(atr_forca) + "  DES " + string(atr_destreza)).draw(4, 46);

	
}

// mensagem na tela
if (texto_timer > 0) {
    scribble(texto).align(fa_center, fa_top).blend(c_yellow).draw(LARGURA_BASE / 2, 70);
}

// fade transicao
if (fade > 0) {
    draw_set_alpha(fade);
    draw_set_colour(c_black);
    draw_rectangle(0, 0, LARGURA_BASE, ALTURA_BASE, false);
    draw_set_alpha(1);
    draw_set_colour(c_white);
}