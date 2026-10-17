// morto: o corpo some devagar 
var _alpha = 1;
if (estado == INI.MORTE) {
    _alpha = clamp((100 - estado_timer) / 30, 0, 1);
}

// desenho normal, ou todo branco se tomar dano
if (flash > 0) gpu_set_fog(true, c_white, 1, 0);
draw_sprite_ext(sprite_index, image_index, x, y, lado, 1, 0, c_white, _alpha);
if (flash > 0) gpu_set_fog(false, c_white, 0, 1);

// arma separada gira
if (tem_arma && estado != INI.MORTE) {
    var _ang = (lado == 1) ? -40 : 220;
    if (estado == INI.ATAQUE) {
        _ang = angulo_golpe(estado_timer, ataque.windup, ataque.ativo, ataque_dir, ataque.arco, lado);
    }
    draw_sprite_ext(arma_sprite, 0, x + mao_x * lado, y - mao_y, 1, 1, _ang, c_white, 1);
}

// aviso no começo do windup: branco = aceita parry, vermelho = não aceita.
if (estado == INI.ATAQUE && estado_timer <= 8 && flash <= 0) {
    var _cor = c_red;
    if (ataque.parry) {
        _cor = c_white;
    }
    gpu_set_fog(true, _cor, 1, 0);
    draw_sprite_ext(sprite_index, image_index, x, y, lado, 1, 0, c_white, 0.6);
    gpu_set_fog(false, c_white, 0, 1);
}

// atordoado fica com sinal amarelo piscando em cima da cabeça (sinaliza visceral)
if (estado == INI.STAGGER && (estado_timer div 6) mod 2 == 0) {
    draw_set_colour(c_yellow);
    draw_circle(x, y - sprite_get_yoffset(sprite_index) + sprite_get_bbox_top(sprite_index) - 6, 3, false);
    draw_set_colour(c_white);
}

// marcador da mira travada (estilo dark souls): losango branco pulsando
if (obj_game.lock_alvo == id && estado != INI.MORTE) {
    var _topo = y - sprite_get_yoffset(sprite_index) + sprite_get_bbox_top(sprite_index) - 14;
    var _r = 3 + 0.8 * dsin(current_time / 6);
    draw_set_colour(c_white);
    draw_line(x, _topo - _r, x + _r, _topo);
    draw_line(x + _r, _topo, x, _topo + _r);
    draw_line(x, _topo + _r, x - _r, _topo);
    draw_line(x - _r, _topo, x, _topo - _r);
    draw_circle(x, _topo, 1, true);
    draw_set_colour(c_white);
}

if (obj_game.debug) {
    draw_set_halign(fa_center);
    draw_text(x, y - 44, obj_game.nomes_ini[estado] + " " + string(hp) + " (-" + string(ultimo_dano) + ")");
    draw_set_halign(fa_left);
    if (estado == INI.ATAQUE) {
        if (estado_timer > ataque.windup && estado_timer <= ataque.windup + ataque.ativo) {
            draw_set_colour(c_red);
        } else {
            draw_set_colour(c_gray);
        }
        desenhar_setor(x, y, ataque_dir, ataque.alcance, ataque.arco);
    }
	    // janela de parry aberta
    if (inimigo_janela_parry(id, 4)) {
        draw_set_colour(c_yellow);
        draw_circle(x, y - 10, 12, true);
    }
	
    draw_set_colour(c_orange);
    draw_circle(inicio_x, inicio_y, 2, false);   // ponto inicial
    draw_set_colour(c_white);
}