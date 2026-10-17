// Salto: sombra no chão durante o voo; no windup, a área do impacto em vermelho.
if (estado == INI.ATAQUE && ataque.tipo == "salto") {
    draw_set_alpha(0.4);
    if (no_ar) {
        draw_set_colour(c_black);
        draw_ellipse(x - 10, y - 4, x + 10, y + 2, false);
    } else if (estado_timer <= ataque.windup) {
        draw_set_colour(c_red);
        draw_ellipse(salto_x1 - ataque.alcance, salto_y1 - ataque.alcance / 2, salto_x1 + ataque.alcance, salto_y1 + ataque.alcance / 2, true);
    }
    draw_set_alpha(1);
    draw_set_colour(c_white);
}

var _dy = y - altura;   // no salto, o corpo sobe

// Morto: o corpo some devagar nos últimos 30 frames (de 70 a 100).
var _alpha = 1;
if (estado == INI.MORTE) {
    _alpha = clamp((100 - estado_timer) / 30, 0, 1);
}

// Desenho normal, ou todo branco se acabou de apanhar.
if (flash > 0) gpu_set_fog(true, c_white, 1, 0);
draw_sprite_ext(sprite_index, image_index, x, _dy, lado, 1, 0, c_white, _alpha);
if (flash > 0) gpu_set_fog(false, c_white, 0, 1);

// Arma separada (Aldeão, chefe): gira no golpe igual à do player, a partir da mão.
// No tiro, a arma de fogo já está desenhada nas mãos: a arma separada não aparece.
var _atirando = (estado == INI.ATAQUE && ataque.tipo == "tiro");
if (tem_arma && estado != INI.MORTE && !_atirando) {
    var _ang = (lado == 1) ? -40 : 220;
    if (estado == INI.ATAQUE) {
        _ang = angulo_golpe(estado_timer, ataque.windup, ataque.ativo, ataque_dir, ataque.arco, lado);
    }
    draw_sprite_ext(arma_sprite, 0, x + mao_x * lado, _dy - mao_y, 1, 1, _ang, c_white, 1);
}

// Aviso no começo do windup: branco = aceita parry, vermelho = não aceita.
if (estado == INI.ATAQUE && estado_timer <= 8 && flash <= 0) {
    var _cor = c_red;
    if (ataque.parry) {
        _cor = c_white;
    }
    gpu_set_fog(true, _cor, 1, 0);
    draw_sprite_ext(sprite_index, image_index, x, _dy, lado, 1, 0, c_white, 0.6);
    gpu_set_fog(false, c_white, 0, 1);
}

// Atordoado: sinal amarelo piscando em cima da cabeça (hora do visceral).
if (estado == INI.STAGGER && (estado_timer div 6) mod 2 == 0) {
    draw_set_colour(c_yellow);
    draw_circle(x, _dy - sprite_get_yoffset(sprite_index) + sprite_get_bbox_top(sprite_index) - 6, 3, false);
    draw_set_colour(c_white);
}

if (obj_game.debug) {
    draw_set_halign(fa_center);
    draw_text(x, _dy - 44, obj_game.nomes_ini[estado] + " " + string(hp) + " (-" + string(ultimo_dano) + ")");
    draw_set_halign(fa_left);
    if (estado == INI.ATAQUE) {
        if (estado_timer > ataque.windup && estado_timer <= ataque.windup + ataque.ativo) {
            draw_set_colour(c_red);
        } else {
            draw_set_colour(c_gray);
        }
        desenhar_setor(x, y, ataque_dir, ataque.alcance, ataque.arco);
    }
    // Janela de parry aberta (contando o bônus da pistola): círculo amarelo
    if (inimigo_janela_parry(id, 4)) {
        draw_set_colour(c_yellow);
        draw_circle(x, y - 10, 12, true);
    }
    draw_set_colour(c_orange);
    draw_circle(inicio_x, inicio_y, 2, false);   // ponto inicial
    draw_set_colour(c_white);
}
