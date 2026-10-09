//Dados do jogo, balanceamento

function dados_armas(){
	// golpe eh um windup ativo com frames de recovery com alcance e avanco em pixels
	var _cutelo_leve = {
		windup: 8, ativo: 4, recovery: 11,
		dano: 14, stamina: 15,
		alcance: 25, arco: 120, avanco: 5,
		hyper: false
	};
	 var _cutelo_pesado = {
        windup: 16, ativo: 5, recovery: 16,
        dano: 28, stamina: 28,
        alcance: 32, arco: 60, avanco: 10,
        hyper: false
    };
    global.armas = {
        cutelo: {
            nome: "Cutelo serrado",
            esc_for: 0.6,
            esc_des: 0.6,
            leves: [_cutelo_leve, _cutelo_leve, _cutelo_leve],
            pesado: _cutelo_pesado
        }
    };
}

