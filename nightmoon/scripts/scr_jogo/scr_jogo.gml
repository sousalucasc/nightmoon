// game loop de começar, morrer, descansar

/// zera tudo ao começar o jogo
function jogo_novo() {
    with (obj_game) {
        arma = global.armas.cutelo;
        pistola = global.pistolas.pistola;
        atr_forca = 0;
        atr_destreza = 0;
        almas = 0;
        chefe_morto = false;
        lanterna_sala = rm_teste;   // onde volta ao morrer antes de descansar
        lanterna_x = -1;            // -1: usa o lugar do player na room
        lanterna_y = -1;
        chegar_na_lanterna = false;
        mancha = { ativa: false, sala: -1, x: 0, y: 0, almas: 0 };
        mortos = [];                // inimigos mortos desde o último descanso
        mortes = 0;
        tempo = 0;                  // frames jogados
        player_hp = -1;             // -1 = cheio
        player_frascos = -1;
        player_balas = -1;
    }
}

/// fx de troca de room
function trocar_room(_destino) {
    with (obj_game) {
        if (!fade_indo) {
            fade_indo = true;
            fade_destino = _destino;
        }
    }
}

/// descansar na lanterna enche tudo
function lanterna_descansar(_lanterna) {
    with (obj_player) {
        hp = hp_max;
        frascos = frascos_max;
        balas = balas_max;
    }
    with (obj_game) {
        lanterna_sala = room;
        lanterna_x = _lanterna.x;
        lanterna_y = _lanterna.y + 12;
        mortos = [];
        chegar_na_lanterna = true;
    }
    trocar_room(room);   // recarrega a room: os inimigos voltam
}

/// player morre e deixa mancha de souls
function jogo_player_morreu(_x, _y) {
    with (obj_game) {
        mortes += 1;
        // A mancha nova substitui a antiga: quem morre duas vezes perde as almas.
        mancha = { ativa: almas > 0, sala: room, x: _x, y: _y, almas: almas };
        almas = 0;
        mortos = [];
        player_hp = -1;
        player_frascos = -1;
        player_balas = -1;
        chegar_na_lanterna = true;
    }
    trocar_room(obj_game.lanterna_sala);
}