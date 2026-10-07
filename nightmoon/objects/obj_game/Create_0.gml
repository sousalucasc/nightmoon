//obj_game: ele controla todo o jogo, nascendo na rm_init e persiste troca de rooms

//RESOLUCAO 
//o jogo e desenhado em 320x180 e ampliado na janela

surface_resize(application_surface,LARGURA_BASE,ALTURA_BASE); // surface - tela, resize deixa essa tela em 320x180
display_set_gui_size(LARGURA_BASE,ALTURA_BASE); // GUI size

//camera = camera_create_view(0,0,LARGURA_BASE,ALTURA_BASE); // cria uma camera que enxerga os 320x180 pixels da room
camera = camera_create_view(0,0,LARGURA_BASE,ALTURA_BASE);
cam_x = 0;
cam_y = 0;

//INPUT
//variaveis começam todas zeradas já que são preenchidas no Begin Step
mover_x = 0;
mover_y = 0;
mira_dir = 0;
aperta_esquiva = false;
aperta_leve = false;
aperta_pesado = false;
aperta_tiro = false;
aperta_cura = false;
aperta_interagir = false;

//DEBUG
debug = false;
room_goto(rm_teste); // manda o jogo para room de teste

//PLAYER STATE
nomes_pl = ["LIVRE","ESQUIVA","ATAQUE","TIRO","CURA","HITSTUN","VISCERAL","MORTE"];

