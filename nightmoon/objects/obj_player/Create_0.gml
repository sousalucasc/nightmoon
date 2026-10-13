vel = 1.5; //px por frame
lado = 1; // 1 direita -1 esquerda

mask_index = spr_mask_player;
estado = PL.LIVRE;
estado_timer = 0; //frames desde que entrou no state atual

//ESQUIVA
//dados de cada esquiva em frames, duracao, distancia, iframes iniciais e finais, custo de stamina
backstep = {duracao:16,distancia:36,iframe_ini:2,iframe_fim:7,custo:15};
dash = {duracao:22,distancia:64,iframe_ini:2,iframe_fim:13,custo:25};
esq = backstep; // default para botao de dash/esquiva e o backstap, se nao houver direcao 
esq_dir = 0; // direcao
esq_vel = 0; // velocidade
esq_desacel = 0; // quanto decai por frame
invulneravel = false; // se esta invuneravel ou nao

hp_max = 100;
hp = hp_max;
st_max = 100;
st = st_max;
st_espera = 0; // frames ate stamina voltar a encher
invul_timer = 0; // invulnerabilidade apos tomar dano
kb_dir = 0; // knockback direcao
kb_vel = 0; // knockback velocidade	(velocidade atual)
kb_desacel = 0; // quanto cai por frame

// ataque
golpe = undefined;      // struct do golpe atual (scr_dados)
golpe_pesado = false;
combo_i = 0;            // posição no combo (0 = primeiro golpe)
ataque_dir = 0;         // direção do golpe (trava no ativo)
acertados = [];         // quem este golpe já acertou
raio = 6;               // tamanho do corpo, para os golpes inimigos

// animacao
image_speed = 0;    // quem escolhe o quadro é o código (player_animar)
anim_timer = 0;
sentido = 1;        // lado do giro da arma (alterna no combo)

// sprite de cada estado, so trocar aqui quando chegar na parte da arte
spr = {
    parado: spr_player_idle,
    andando: spr_player_walk,
    backstep: spr_player_backstep,
    dash: spr_player_dash,
    ataque: spr_player_ataque,
    tiro: spr_player_tiro,
    cura: spr_player_cura,
    hit: spr_player_hit,
    visceral: spr_player_visceral,
    morte: spr_player_morte
};

// tiro
balas_max = 10;
balas = balas_max;
tiro_id = -1;       // número do último tiro
