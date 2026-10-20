if (jogo_congelado() || !instance_exists(obj_player)) exit;

perto = point_distance(x, y, obj_player.x, obj_player.y) < 24;
if (perto && obj_game.aperta_interagir && obj_player.estado == PL.LIVRE) {
    lanterna_descansar(id);
}