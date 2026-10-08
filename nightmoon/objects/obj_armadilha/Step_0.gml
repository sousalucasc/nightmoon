// 30 frames antes de comecar, 6 ativo, 60 desligado (96)
ciclo = (ciclo + 1) mod 96;
ativa = (ciclo >= 30 && ciclo < 36);

if (ativa && instance_exists(obj_player)){
	if(point_distance(x,y,obj_player.x,obj_player.y) <= raio){
		player_dano(dano,x,y);
	}
}
