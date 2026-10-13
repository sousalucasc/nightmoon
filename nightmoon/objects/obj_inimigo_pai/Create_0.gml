// valores padrao de todo inimigo
// heranca em sua melhor forma
// cada filho chama event_inherited()
hp_max = 50;
hp = hp_max;
vel = 1;
raio = 8;            // tamanho do corpo para golpes
almas = 10;          // quanto dá ao morrer
aggro = 100;         // distância em que percebe o player
desiste = 250;       // distância do ponto inicial em que desiste e volta
dist_parar = 18;     // para de andar a esta distância do player
espera_entre = 30;   // frames de pausa entre ataques
pode_hitstun = true; // golpes interrompem?
acordado = true;     // o chefe começa dormindo (dia 14)
ataques = [];        // lista de ataques (ataque_novo)

// estado
estado = INI.IDLE;
estado_timer = 0;
ataque = undefined;
ataque_dir = 0;
acertados = [];
espera = 0;
flash = 0;
ultimo_dano = 0;
lado = 1;
inicio_x = x;
inicio_y = y;
depth = -y;