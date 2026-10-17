// begin step roda antes do step de todo mundo
// lê o input uma vez por frame

// hitstop
if (hitstop > 0) {
    hitstop -= 1;
}

// keyboard check devolve 1 (apertado) ou 0 (solto)

mover_x = keyboard_check(ord("D")) - keyboard_check(ord("A"));
mover_y = keyboard_check(ord("S")) - keyboard_check(ord("W"));

// lock-on: clicar a rodinha trava/solta a mira no inimigo mais proximo
if (mouse_check_button_pressed(mb_middle)) player_lock_toggle();

// valida o alvo travado (morreu, saiu de alcance, trocou de room)
player_lock_validar();

// mira no angulo do peito do player (o -10)
// travado, a mira ignora o mouse e aponta pro inimigo

if (instance_exists(obj_player)){
	if (lock_alvo != noone) {
		mira_dir = point_direction(obj_player.x, obj_player.y - 10, lock_alvo.x, lock_alvo.y);
	} else {
		mira_dir = point_direction(obj_player.x, obj_player.y - 10, mouse_x, mouse_y);
	}
}

// pressed, verdadeiro so no frame que a tecla descer

aperta_esquiva = keyboard_check_pressed(vk_space);
aperta_leve = mouse_check_button_pressed(mb_left);
aperta_pesado = mouse_check_button_pressed(mb_right);
aperta_tiro = keyboard_check_pressed(ord("Q"));
aperta_cura	= keyboard_check_pressed(ord("E"));
aperta_interagir = keyboard_check_pressed(ord("F"));

if(keyboard_check_pressed(vk_f3)){
	debug = !debug;
}

// buffer de botao
buf_esquiva = aperta_esquiva ? BUFFER_FRAMES : max(0, buf_esquiva - 1);
buf_leve    = aperta_leve    ? BUFFER_FRAMES : max(0, buf_leve - 1);
buf_pesado  = aperta_pesado  ? BUFFER_FRAMES : max(0, buf_pesado - 1);
buf_tiro    = aperta_tiro    ? BUFFER_FRAMES : max(0, buf_tiro - 1);

// teclas de teste (só com o F3 ligado)
if (debug) {
    if (keyboard_check_pressed(ord("1"))) arma = global.armas.bengala;
    if (keyboard_check_pressed(ord("2"))) arma = global.armas.machado;
    if (keyboard_check_pressed(ord("3"))) arma = global.armas.cutelo;
	if (keyboard_check_pressed(ord("4"))) pistola = global.pistolas.pistola;
    if (keyboard_check_pressed(ord("5"))) pistola = global.pistolas.escopeta;
    if (keyboard_check_pressed(ord("7"))) atr_forca += 1;
    if (keyboard_check_pressed(ord("8"))) atr_destreza += 1;
    if (keyboard_check_pressed(ord("0"))) {
        atr_forca = 0;
        atr_destreza = 0;
    }
}