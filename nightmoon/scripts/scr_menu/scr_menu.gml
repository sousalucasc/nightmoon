// Menus. Um objeto só (obj_menu); o "tipo" diz qual menu é.

/// Abre um menu. Tipos: "lanterna", "nivel", "arma", "pistola", "pausa", "titulo".
function menu_abrir(_tipo) {
    var _m = instance_create_depth(0, 0, -9000, obj_menu);
    _m.tipo = _tipo;
    switch (_tipo) {
        case "lanterna":
            _m.titulo = "Lanterna";
            _m.opcoes = ["Subir nivel", "Continuar"];
            break;
        case "nivel":
            _m.titulo = "Subir nivel";
            _m.opcoes = menu_textos_nivel();
            break;
        case "arma":
            _m.titulo = "Escolha sua arma";
            _m.opcoes = [global.armas.bengala.nome, global.armas.machado.nome, global.armas.cutelo.nome];
            break;
        case "pistola":
            _m.titulo = "Escolha sua pistola";
            _m.opcoes = [global.pistolas.pistola.nome, global.pistolas.escopeta.nome];
            break;
        case "pausa":
            _m.titulo = "Pausa";
            _m.opcoes = ["Continuar", "Sair do jogo"];
            break;
        case "titulo":
            _m.titulo = "NIGHTMOON";
            _m.opcoes = ["Comecar", "Sair"];
            break;
    }
    return _m;
}

/// Os textos do menu de nível, com o valor atual de cada atributo.
function menu_textos_nivel() {
    return [
        "Vida " + string(obj_game.atr_vida),
        "Stamina " + string(obj_game.atr_stamina),
        "Forca " + string(obj_game.atr_forca),
        "Destreza " + string(obj_game.atr_destreza),
        "Voltar"
    ];
}

/// Roda dentro do obj_menu quando o jogador confirma a opção "sel".
function menu_confirmar() {
    switch (tipo) {
        case "lanterna":
            if (sel == 0) {
                menu_abrir("nivel");
            }
            instance_destroy();
            break;
        case "nivel":
            if (sel == 4) {
                menu_abrir("lanterna");
                instance_destroy();
            } else {
                if (!nivel_comprar(sel)) {
                    mostrar_texto("Almas insuficientes");
                }
                opcoes = menu_textos_nivel();
            }
            break;
        case "arma":
            if (sel == 0) obj_game.arma = global.armas.bengala;
            if (sel == 1) obj_game.arma = global.armas.machado;
            if (sel == 2) obj_game.arma = global.armas.cutelo;
            menu_abrir("pistola");
            instance_destroy();
            break;
        case "pistola":
            if (sel == 0) obj_game.pistola = global.pistolas.pistola;
            if (sel == 1) obj_game.pistola = global.pistolas.escopeta;
            obj_game.escolheu = true;
            instance_destroy();
            break;
        case "pausa":
            if (sel == 0) {
                instance_destroy();
            } else {
                game_end();
            }
            break;
    }
}

/// Roda dentro do obj_menu quando o jogador aperta Esc.
/// (Não pode se chamar menu_voltar: esse já é o nome da variável do obj_game.)
function menu_cancelar() {
    switch (tipo) {
        case "nivel":
            menu_abrir("lanterna");
            instance_destroy();
            break;
        case "lanterna":
        case "pausa":
            instance_destroy();
            break;
    }
}

/// A tecla que mexeu no menu não pode disparar mais nada neste frame.
function menu_consumir_input() {
    with (obj_game) {
        aperta_interagir = false;
        aperta_cura = false;
        buf_leve = 0;
        buf_pesado = 0;
        buf_esquiva = 0;
        buf_tiro = 0;
    }
}

function nivel_custo() {
    return 100 + 50 * obj_game.niveis;
}

/// _atributo: 0 vida, 1 stamina, 2 força, 3 destreza. Devolve true se comprou.
function nivel_comprar(_atributo) {
    var _custo = nivel_custo();
    if (obj_game.almas < _custo) return false;
    obj_game.almas -= _custo;
    obj_game.niveis += 1;
    switch (_atributo) {
        case 0: obj_game.atr_vida += 1; break;
        case 1: obj_game.atr_stamina += 1; break;
        case 2: obj_game.atr_forca += 1; break;
        case 3: obj_game.atr_destreza += 1; break;
    }
    // Aplica na hora: o player já está descansado, então enche junto.
    with (obj_player) {
        hp_max = player_hp_max();
        st_max = player_st_max();
        hp = hp_max;
        st = st_max;
    }
    return true;
}