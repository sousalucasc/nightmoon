// Por qual lado o portão abre: "cima", "baixo", "esquerda", "direita" ou "nenhum".
// Mude no Creation Code.
abre_por = "nenhum";

// Já foi aberto nesta partida? Então não existe mais.
if (obj_game.atalho_aberto) {
    instance_destroy();
}