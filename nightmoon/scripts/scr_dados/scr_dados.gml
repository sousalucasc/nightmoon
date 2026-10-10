//Dados do jogo, balanceamento

function dados_armas() {
    // GOLPE: windup, ativo e recovery em frames
    // alcance e avanço em pixels; arco em graus.

    // BENGALA LAMINA (DEX)
    var _bengala_leve = {
        windup: 5, ativo: 3, recovery: 8,
        dano: 9, stamina: 10,
        alcance: 22, arco: 90, avanco: 4,
        hyper: false, fx: spr_fx_corte
    };
    var _bengala_pesado = {
        windup: 14, ativo: 4, recovery: 14,
        dano: 22, stamina: 25,
        alcance: 34, arco: 30, avanco: 20,
        hyper: false, fx: spr_fx_corte
    };

    // MACHADO (STR)
    var _machado_leve = {
        windup: 14, ativo: 5, recovery: 16,
        dano: 24, stamina: 22,
        alcance: 28, arco: 180, avanco: 6,
        hyper: false, fx: spr_fx_corte
    };
    var _machado_pesado = {
        windup: 22, ativo: 8, recovery: 22,
        dano: 38, stamina: 35,
        alcance: 30, arco: 360, avanco: 0,
        hyper: true, fx: spr_fx_corte
    };

    // CUTELO (STR/DEX)
    var _cutelo_leve = {
        windup: 8, ativo: 4, recovery: 11,
        dano: 14, stamina: 15,
        alcance: 25, arco: 120, avanco: 5,
        hyper: false, fx: spr_fx_corte
    };
    var _cutelo_pesado = {
        windup: 16, ativo: 5, recovery: 16,
        dano: 28, stamina: 28,
        alcance: 32, arco: 60, avanco: 10,
        hyper: false, fx: spr_fx_corte
    };

    global.armas = {
        bengala: {
            nome: "Bengala-lâmina",
            esc_for: 0.1,
            esc_des: 1.0,
            sprite: spr_arma_bengala,
            leves: [_bengala_leve, _bengala_leve, _bengala_leve, _bengala_leve],
            pesado: _bengala_pesado
        },
        machado: {
            nome: "Machado de caça",
            esc_for: 1.0,
            esc_des: 0.1,
            sprite: spr_arma_machado,
            leves: [_machado_leve, _machado_leve],
            pesado: _machado_pesado
        },
        cutelo: {
            nome: "Cutelo serrado",
            esc_for: 0.6,
            esc_des: 0.6,
            sprite: spr_arma_cutelo,
            leves: [_cutelo_leve, _cutelo_leve, _cutelo_leve],
            pesado: _cutelo_pesado
        }
    };
}

