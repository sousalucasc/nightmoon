draw_self();
gpu_set_blendmode(bm_add);
draw_sprite_ext(spr_luz, 0, x, y - 40, 1, 1, 0, make_colour_rgb(255, 150, 60), 0.3);
gpu_set_blendmode(bm_normal);
