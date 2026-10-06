//draw sprite que respeita o lado
draw_sprite_ext(sprite_index,image_index,x,y,lado,1,0,c_white,1); 


// linha de debug
if (obj_game.debug) {
    draw_set_colour(c_lime);
	draw_rectangle(bbox_left,bbox_top,bbox_right,bbox_bottom,true);
	draw_line(x,y,mouse_x,mouse_y);
	draw_set_colour(c_white);
}