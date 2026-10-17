fechada = false;
parede = noone;     // a parede invisível que ela cria ao fechar

// Chefe já morto: a névoa nem aparece.
if (obj_game.chefe_morto) {
    instance_destroy();
}
