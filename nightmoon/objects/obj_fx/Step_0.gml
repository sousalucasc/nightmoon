if (jogo_congelado()) exit;

quadro += velocidade;
if (quadro >= sprite_get_number(sprite_index)) {
    instance_destroy();
}