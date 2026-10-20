// Saindo da room: guarda vida, frascos e balas para a próxima.
// Morto não guarda: quem morreu volta cheio.
if (estado != PL.MORTE) {
    obj_game.player_hp = hp;
    obj_game.player_frascos = frascos;
    obj_game.player_balas = balas;
}