if(ativa){
	draw_set_colour(c_red);
	draw_circle(x,y,raio,false); // machuca
}else if(ciclo < 30 && (ciclo div 4) mod 2 == 0){
	draw_set_colour(c_yellow);
	draw_circle(x,y,raio,true); // avisa
}else{
	draw_set_colour(c_dkgray);
	draw_circle(x,y,raio,true);
}
draw_set_colour(c_white);