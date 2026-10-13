if (jogo_congelado()) exit;

estado_timer += 1;
if (flash > 0) {
    flash -= 1;
}

switch (estado) {
    case INI.IDLE:      inimigo_estado_idle();      break;
    case INI.PERSEGUIR: inimigo_estado_perseguir(); break;
    case INI.VOLTAR:    inimigo_estado_voltar();    break;
    case INI.ATAQUE:    inimigo_estado_ataque();    break;
    case INI.HITSTUN:   inimigo_estado_hitstun();   break;
    case INI.MORTE:     inimigo_estado_morte();     break;
}

depth = -y;