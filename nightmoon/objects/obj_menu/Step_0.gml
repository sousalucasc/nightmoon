if (espera > 0) {
    espera -= 1;
    exit;
}

var _n = array_length(opcoes);
if (obj_game.menu_cima) {
    sel = (sel - 1 + _n) mod _n;    // sobe; do primeiro vai para o último
}
if (obj_game.menu_baixo) {
    sel = (sel + 1) mod _n;         // desce; do último volta ao primeiro
}

if (obj_game.menu_ok) {
    menu_confirmar();
    menu_consumir_input();
} else if (obj_game.menu_voltar) {
    menu_cancelar();
    menu_consumir_input();
}