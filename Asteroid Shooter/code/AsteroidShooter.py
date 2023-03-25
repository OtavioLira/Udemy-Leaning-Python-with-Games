import pygame, sys
from random import randint, uniform

def laser_update(laser_list, speed = 300):
	for rect in laser_list:
		rect.y -= speed * dt
		if rect.bottom < 0:
			laser_list.remove(rect)

def meteor_update(meteor_list, speed = 300):
	for meteor_tuple in meteor_list:

		direction = meteor_tuple[1]
		meteor_rect = meteor_tuple[0]
		meteor_rect.center += direction * speed * dt 
		if meteor_rect.top > WINDOW_HEIGHT:
			meteor_list.remove(meteor_tuple)

def display_score():
	score_text = f"Score: {pygame.time.get_ticks() // 100}"
	text_surf = font.render(score_text, True, (255,255,255))
	text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))
	display_surface.blit(text_surf,text_rect)
	pygame.draw.rect(display_surface,'purple',text_rect.inflate(30,30),8,5)

def laser_timer(can_shoot, duration = 500):
	if not can_shoot:
		current_time = pygame.time.get_ticks()
		if current_time - shoot_time > duration:
			can_shoot = True
	return can_shoot


# Game Init
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 900,500
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Asteroid Shooter")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

# background import
bg_surf = pygame.image.load('../graphics/background.png').convert()

# ship import
ship_surf = pygame.image.load('../graphics/ship.png').convert_alpha()
ship_rect = ship_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

# laser import
laser_surf = pygame.image.load('../graphics/laser.png').convert_alpha()
laser_list = []
# laser_rect = laser_surf.get_rect(midbottom = ship_rect.midtop)

# laser timer
can_shoot = True
shoot_time = None

# Importing texts
font = pygame.font.Font('../graphics/subatomic.ttf', 30)

# meteor
meteor_surf = pygame.image.load('../graphics/meteor.png').convert_alpha()
meteor_list = []


# meteor timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer,500)

#import sound
laser_sound = pygame.mixer.Sound("../sounds/laser.ogg")
explosion_sound = pygame.mixer.Sound("../sounds/explosion.wav")
background_music = pygame.mixer.Sound("../sounds/music.wav")
background_music.play(loops = -1)

while True: #--> start

	# event loop
	for event in pygame.event.get(): #--> start
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN and can_shoot: # 0.5 seconds of delay berofe shoot

			# laser
			laser_rect = laser_surf.get_rect(midbottom = ship_rect.midtop)
			laser_list.append(laser_rect)

			#timer
			can_shoot = False
			shoot_time = pygame.time.get_ticks()

			# play laser sound
			laser_sound.play()

		if event.type == meteor_timer:

			# random position
			x_pos = randint(-100,WINDOW_WIDTH + 100)
			y_pos = randint(-100,-50)

			# creating  a rect
			meteor_rect = meteor_surf.get_rect(center = (x_pos,y_pos))
			
			# create a random direction
			direction = pygame.math.Vector2(uniform(-0.5,0.5),2)

			meteor_list.append((meteor_rect,direction))

	#--> end

	# framerate limit
	dt = clock.tick(120) / 1000

	# mouse input
	ship_rect.center = pygame.mouse.get_pos()

	# update
	laser_update(laser_list)
	meteor_update(meteor_list)
	can_shoot = laser_timer(can_shoot,400)

	# meteor ship colissions
	for meteor_tuple in meteor_list:
		meteor_rect = meteor_tuple[0]
		if ship_rect.colliderect(meteor_rect):
			print("You Lose")
			pygame.quit()
			sys.exit()

	# laser meteor collision
	for laser_rect in laser_list:
		for meteor_tuple in meteor_list:
			if laser_rect.colliderect(meteor_tuple[0]):
				meteor_list.remove(meteor_tuple)
				laser_list.remove(laser_rect)
				explosion_sound.play()

	# drawing
	display_surface.fill((0,0,0))
	display_surface.blit(bg_surf,(0,0))

	pygame.draw.lines(display_surface,'red',False,[(0,0),(WINDOW_WIDTH,0)], 1)
	# credits_surf = font.render('@Otavio Lira', True, (255,255,255))
	# credits_rect = credits_surf.get_rect(midbottom = (20, WINDOW_HEIGHT - 20))
	# display_surface.blit(credits_surf,credits_rect)
	display_score()

	for rect in laser_list:
		display_surface.blit(laser_surf,rect)
	for meteor_tuple in meteor_list:
		display_surface.blit(meteor_surf,meteor_tuple[0])
	display_surface.blit(ship_surf,ship_rect)
	
	
	# draw the final frame
	pygame.display.update()
	#--> end