if (jogo_congelado()) exit;

if (!fechada && instance_exists(obj_player) && instance_exists(obj_chefe)) {
    // O player está do mesmo lado da névoa que o chefe? Então já atravessou.
    var _cx = x + sprite_width / 2;
    var _cy = y + sprite_height / 2;
    var _lado_player;
    var _lado_chefe;
    if (sprite_width >= sprite_height) {
        // Névoa deitada: compara em cima/embaixo.
        _lado_player = sign(obj_player.y - _cy);
        _lado_chefe = sign(obj_chefe.y - _cy);
    } else {
        // Névoa em pé: compara esquerda/direita.
        _lado_player = sign(obj_player.x - _cx);
        _lado_chefe = sign(obj_chefe.x - _cx);
    }
    if (_lado_player == _lado_chefe && !place_meeting(x, y, obj_player)) {
        fechada = true;
        parede = instance_create_depth(x, y, 0, obj_parede);
        parede.image_xscale = image_xscale;
        parede.image_yscale = image_yscale;
        parede.visible = false;
        obj_chefe.acordado = true;
    }
}

// Chefe morreu (e sumiu): a névoa abre.
if (fechada && !instance_exists(obj_chefe)) {
    if (instance_exists(parede)) {
        instance_destroy(parede);
    }
    instance_destroy();
}
