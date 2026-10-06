// roda depois do step de todo mundo

// camera, segue o player devagar sem mostrar oque ta de fora da room

if(instance_exists(obj_player)){
	var _alvo_x = obj_player.x - LARGURA_BASE /2;
	var _alvo_Y = obj_player.y - ALTURA_BASE /2;
	cam_x = lerp(cam_x, _alvo_x, 0.15);
	cam_y = lerp(cam_y, _alvo_Y, 0.15);
}

cam_x = clamp(cam_x,0,room_width - LARGURA_BASE);
cam_y = clamp(cam_y,0,room_height - ALTURA_BASE);

camera_set_view_pos(camera,round(cam_x),round(cam_y));