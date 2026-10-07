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
invuneravel = false; // se esta invuneravel ou nao


