//Altura e largura
#macro LARGURA_BASE 320
#macro ALTURA_BASE 180

//state machine do player

enum PL{
	LIVRE,
	ESQUIVA,
	ATAQUE,
	TIRO,
	CURA,
	HITSTUN,
	VISCERAL,
	MORTE,
}
