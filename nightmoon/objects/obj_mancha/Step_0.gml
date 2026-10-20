if (jogo_congelado() || !instance_exists(obj_player)) exit;

// Encostou: as almas voltam.
if (point_distance(x, y, obj_player.x, obj_player.y) < 12) {
    obj_game.almas += obj_game.mancha.almas;
    obj_game.mancha.ativa = false;
    mostrar_texto("Almas recuperadas");
    instance_destroy();
}