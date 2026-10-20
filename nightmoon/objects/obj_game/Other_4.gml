// roda sempre que uma room começa
// toda room usa a mesma camera 320x180

view_enabled = true;
view_visible[0] = true;
view_camera[0] = camera;
view_xport[0] = 0;
view_yport[0] = 0;
view_wport[0] = LARGURA_BASE;
view_hport[0] = ALTURA_BASE;

// Voltando de uma morte ou de um descanso: o player aparece na lanterna.
if (chegar_na_lanterna && instance_exists(obj_player)) {
    chegar_na_lanterna = false;
    if (lanterna_x >= 0) {
        obj_player.x = lanterna_x;
        obj_player.y = lanterna_y;
    }
}

// A mancha de almas, se ela ficou nesta room.
if (mancha.ativa && mancha.sala == room) {
    instance_create_depth(mancha.x, mancha.y, 0, obj_mancha);
}

// A câmera já começa em cima do player.
if (instance_exists(obj_player)) {
    cam_x = obj_player.x - LARGURA_BASE / 2;
    cam_y = obj_player.y - ALTURA_BASE / 2;
}