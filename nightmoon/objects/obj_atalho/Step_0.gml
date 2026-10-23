if (jogo_congelado() || !instance_exists(obj_player)) exit;

var _p = obj_player;
if (point_distance(x, y, _p.x, _p.y) < 32 && obj_game.aperta_interagir) {
    var _lado_certo = (abre_por == "cima" && _p.y < y)
        || (abre_por == "baixo" && _p.y > y)
        || (abre_por == "esquerda" && _p.x < x)
        || (abre_por == "direita" && _p.x > x);
    if (_lado_certo) {
        obj_game.atalho_aberto = true;
        mostrar_texto("O portao abriu.");
        instance_destroy();
    } else {
        mostrar_texto("Nao abre por este lado.");
    }
}