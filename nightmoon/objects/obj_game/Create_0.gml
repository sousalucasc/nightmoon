//obj_game: ele controla todo o jogo, nascendo na rm_init e persiste troca de rooms

//RESOLUCAO 
//o jogo e desenhado em 320x180 e ampliado na janela

surface_resize(application_surface, LARGURA_BASE, ALTURA_BASE);
display_set_gui_size(LARGURA_BASE, ALTURA_BASE);
camera = camera_create_view(0, 0, LARGURA_BASE, ALTURA_BASE);
cam_x = 0;
cam_y = 0;
depth = -10000;     // o draw GUI do obj_game fica por cima 

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
// buffer: por quantos frames ainda vale um botão apertado
buf_esquiva = 0;
buf_leve = 0;
buf_pesado = 0;
buf_tiro = 0;
// lock-on (mira travada estilo dark souls)
lock_alvo = noone;   // inimigo travado, ou noone
lock_dist = 190;     // alcance em pixels para travar a mira

//DEBUG
debug = false;
// Nomes dos estados, na mesma ordem dos enums (para o debug)
nomes_pl = ["LIVRE", "ESQUIVA", "ATAQUE", "TIRO", "CURA", "HITSTUN", "VISCERAL", "MORTE"];
nomes_ini = ["IDLE", "PERSEGUIR", "VOLTAR", "ATAQUE", "HITSTUN", "STAGGER", "VISCERAL", "CAIDO", "TRANSFORMA", "MORTE"];

//IMPACTO
hitstop = 0;    // frames que o jogo fica congelado
tremor = 0;     // força do tremor da câmera

//MENSAGEM TELA
texto = "";
texto_timer = 0;

//FADE TRANSICAO
fade = 0;             // 0 = transparente, 1 = tela preta
fade_indo = false;
fade_destino = -1;

//DADOS
dados_armas();
dados_pistolas();
contador_tiros = 0;

//GAME LOOP
jogo_novo();

typist = scribble_typist();
typist.in(.8,3);


room_goto(rm_teste);

