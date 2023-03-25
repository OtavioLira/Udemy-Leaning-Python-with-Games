import pygame, sys

#Game Init
pygame.init()
WIDTH,HEIGHT = 800,400
display_surface = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("2D game")

#Background
bg_surf = pygame.Surface((WIDTH,HEIGHT))
bg_surf.fill((0,0,100))
bg_rect = bg_surf.get_rect()

# Player
player_surf = pygame.Surface((100,100))
player_surf.fill((255,255,0))
player_rect = player_surf.get_rect()


while True:
	#Event Loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				player_rect.x -= 10
			if event.key == pygame.K_d:
				player_rect.x += 10
			if event.key == pygame.K_w:
				player_rect.y -= 10
			if event.key == pygame.K_s:
				player_rect.y += 10




	display_surface.blit(bg_surf,bg_rect)
	display_surface.blit(player_surf,player_rect)

	#Draw the final frame
	pygame.display.update()