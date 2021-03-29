# Importa os modulos relevantes
import pygame, sys
import numpy as np

# Inicia o Pygame
pygame.init()

# As constantes do jogo
largura = 600
altura = 600
traco_largura = 10
WIN_traco_largura = 10
tabuleiro_linha = 3
tabuleiro_coluna = 3
tamanho_quadrado = 200
circulo_raio = 60
circulo_largura = 15
x_largura = 25
espaco = 55

RED = (255, 0, 0)
cor_fundo = (100, 10, 156)
traco_cor = (50, 130, 250)
circulo_cor = (239, 31, 100)
x_cor = (166, 66, 6)

# Chama a tela e define tamanho, nome e fundo
screen = pygame.display.set_mode( (largura, altura) )
pygame.display.set_caption( 'Jogo da Velha' )
screen.fill( cor_fundo )
tabuleiro = np.zeros( (tabuleiro_linha, tabuleiro_coluna) )


# Define as figuras a serem desenhadas
def draw_tracos():
	# 1 horizontal
	pygame.draw.line( screen, traco_cor, (0, tamanho_quadrado), (largura, tamanho_quadrado), traco_largura )
	# 2 horizontal
	pygame.draw.line( screen, traco_cor, (0, 2 * tamanho_quadrado), (largura, 2 * tamanho_quadrado), traco_largura )

	# 1 vertical
	pygame.draw.line( screen, traco_cor, (tamanho_quadrado, 0), (tamanho_quadrado, altura), traco_largura )
	# 2 vertical
	pygame.draw.line( screen, traco_cor, (2 * tamanho_quadrado, 0), (2 * tamanho_quadrado, altura), traco_largura )

def draw_figures():
	for row in range(tabuleiro_linha):
		for col in range(tabuleiro_coluna):
			if tabuleiro[row][col] == 1:
				pygame.draw.circle( screen, circulo_cor, (int( col * tamanho_quadrado + tamanho_quadrado//2 ), int( row * tamanho_quadrado + tamanho_quadrado//2 )), circulo_raio, circulo_largura )
			elif tabuleiro[row][col] == 2:
				pygame.draw.line( screen, x_cor, (col * tamanho_quadrado + espaco, row * tamanho_quadrado + tamanho_quadrado - espaco), (col * tamanho_quadrado + tamanho_quadrado - espaco, row * tamanho_quadrado + espaco), x_largura )	
				pygame.draw.line( screen, x_cor, (col * tamanho_quadrado + espaco, row * tamanho_quadrado + espaco), (col * tamanho_quadrado + tamanho_quadrado - espaco, row * tamanho_quadrado + tamanho_quadrado - espaco), x_largura )

def mark_square(row, col, player):
	tabuleiro[row][col] = player

def available_square(row, col):
	return tabuleiro[row][col] == 0

def is_tabuleiro_full():
	for row in range(tabuleiro_linha):
		for col in range(tabuleiro_coluna):
			if tabuleiro[row][col] == 0:
				return False

	return True


# Define a condicao de vitoria
def check_win(player):
	# Condicao Vitoria Vertical 
	for col in range(tabuleiro_coluna):
		if tabuleiro[0][col] == player and tabuleiro[1][col] == player and tabuleiro[2][col] == player:
			desenha_traco_vertical(col, player)
			return True

	# Condicao de vitoria horizontal
	for row in range(tabuleiro_linha):
		if tabuleiro[row][0] == player and tabuleiro[row][1] == player and tabuleiro[row][2] == player:
			desenha_traco_horizontal(row, player)
			return True

	# Vitoria diagonal ascendente
	if tabuleiro[2][0] == player and tabuleiro[1][1] == player and tabuleiro[0][2] == player:
		desenha_traco_diagonal_ascendente(player)
		return True

	# Vitoria diagonal descendente
	if tabuleiro[0][0] == player and tabuleiro[1][1] == player and tabuleiro[2][2] == player:
		desenha_traco_diagonal_descendente(player)
		return True

	return False

#Mostra a vitoria as linhas na vitoria
def desenha_traco_vertical(col, player):
	posX = col * tamanho_quadrado + tamanho_quadrado//2

	if player == 1:
		color = circulo_cor
	elif player == 2:
		color = x_cor

	pygame.draw.line( screen, color, (posX, 15), (posX, altura - 15), traco_largura )

def desenha_traco_horizontal(row, player):
	posY = row * tamanho_quadrado + tamanho_quadrado//2

	if player == 1:
		color = circulo_cor
	elif player == 2:
		color = x_cor

	pygame.draw.line( screen, color, (15, posY), (largura - 15, posY), WIN_traco_largura )

def desenha_traco_diagonal_ascendente(player):
	if player == 1:
		color = circulo_cor
	elif player == 2:
		color = x_cor

	pygame.draw.line( screen, color, (15, altura - 15), (largura - 15, 15), WIN_traco_largura )

def desenha_traco_diagonal_descendente(player):
	if player == 1:
		color = circulo_cor
	elif player == 2:
		color = x_cor

	pygame.draw.line( screen, color, (15, 15), (largura - 15, altura - 15), WIN_traco_largura )

def restart():
	screen.fill( cor_fundo )
	draw_tracos()
	for row in range(tabuleiro_linha):
		for col in range(tabuleiro_coluna):
			tabuleiro[row][col] = 0

draw_tracos()


player = 1
fim_de_jogo = False

# Loop principal, aqui 'e onde a logica do jogo vai rodar
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN and not fim_de_jogo:

			mouseX = event.pos[0] # x
			mouseY = event.pos[1] # y

			clicked_row = int(mouseY // tamanho_quadrado)
			clicked_col = int(mouseX // tamanho_quadrado)

			if available_square( clicked_row, clicked_col ):

				mark_square( clicked_row, clicked_col, player )
				if check_win( player ):
					fim_de_jogo = True
				player = player % 2 + 1

				draw_figures()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				restart()
				player = 1
				fim_de_jogo = False

	pygame.display.update()