import sys, pygame, pyganim
from time import gmtime, strftime
from game_objects import *
from settings import *
from menu import *

pygame.init()
pygame.display.set_caption("Hi, it is me!")

clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)

explode_anim = pyganim.PygAnimation([
	('assets/meteor_exp{}.png'.format(1), 50) for i in range(17)
	], loop = False)

shell_rocket_anim = pyganim.PygAnimation([
	('assets/explode{}.png'.format(2), 10) for i in range(6)
	], loop = False)




# Game Groups
all_objects = pygame.sprite.OrderedUpdates()
rockets = pygame.sprite.Group()
meteors = pygame.sprite.Group()
shells = pygame.sprite.Group()
buttons = pygame.sprite.Group()
aliens = pygame.sprite.Group()


explosions = []

# music = pygame.mixer.Sound('assetss/music/bg.wav')
# music.play(-1)

# Game objects
player = Player(clock, rockets)
background = Background()
cloud1 = Cloud('assets/cloud1.png', 2)
cloud2 = Cloud('assets/cloud2.png', 1.5)
tank = Tank()
alien = Alien()
power = Power_scale()
rocket_wall = Rocket_wall()

gun = Gun((137, HEIGHT-80), shells, screen, power)

button_play = Menu_btn('assets/play_btn.png', (WIDTH - 150, 100))
button_exit = Menu_btn('assets/esc_btn.png', (WIDTH-150, 200))
button_repeat = Menu_btn('assets/repeat_btn.png', (150, HEIGHT/2 -50))
button_help = Menu_btn('assets/help_btn.png', (WIDTH-150, 150))
# rocket = Rocket(player.rect.midtop)


all_objects.add(background)
all_objects.add(power)
all_objects.add(cloud1)
all_objects.add(cloud2)
all_objects.add(tank)
all_objects.add(gun)
# all_objects.add(alien)
all_objects.add(rocket_wall)

buttons.add(button_play)
buttons.add(button_exit)
buttons.add(button_help)
aliens.add(alien)

# all_objects.add(player)
# all_objects.add(Meteorit())
# all_objects.add(rocket)
# menu_items = ['PLAY','EXIT']

MENU = True #variable to show or hide menu
GAME_OVER = False
GAME_STARTED = False

SCORE = 0
TIME_COUNTER = 0
START_TIME  = pygame.time.get_ticks()
ROCKET_DAMAGE = 5
HELP = False

#
# MAIN LOOP  --------------------------------------------------------------------------------------------
#

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)

	pressed = pygame.key.get_pressed()

	if GAME_OVER == True or TIME_COUNTER >= 60 or ROCKET_DAMAGE == 0:
				
			if pressed[pygame.K_ESCAPE]:
				MENU = True
				GAME_OVER = False

			screen.blit(GAME_OVER_IMAGE, (0, HEIGHT-400))
			screen.blit(text_objects('YOUR FINAL SCORE: '+ str(SCORE)), (250, 100))
			with open('SCORE.TXT', 'w') as f:
				f.write(str(SCORE))
	elif HELP == True:

		screen.blit(HELP_PAGE, (0, 0))
		pygame.display.flip()
		# pygame.time.delay(3000)

		if pressed[pygame.K_ESCAPE]:
			MENU = True
			HELP = False

	elif MENU == True:
		START_TIME  = pygame.time.get_ticks()
		if pressed[pygame.K_ESCAPE] and GAME_STARTED:
			MENU = False
			pygame.time.wait(250)

		if button_play.mouse_in() == True:
			button_play.rect.move_ip(1, 1)
			pygame.time.wait(100)
			GAME_STARTED = True
			MENU = False
		if button_exit.mouse_in() == True:
			pygame.time.wait(100)
			pygame.quit()
			button_play.rect.move_ip(1, 1)
			sys.exit(0)
		if button_help.mouse_in() == True:
			pygame.time.wait(100)
			button_play.rect.move_ip(2, 2)
			HELP = True


		screen.blit(menubg_image, (0, 0))
		buttons.update()
		buttons.draw(screen)


	else: 
		if pressed[pygame.K_ESCAPE]:
			MENU = True
			pygame.time.wait(250)
		screen.fill(WHITE)
		shells_and_alien_collided = pygame.sprite.groupcollide(aliens, shells, True, True)
		sehells_and_rocket_collide = pygame.sprite.spritecollide(rocket_wall, shells, True)

		if shells_and_alien_collided:
			aliens = pygame.sprite.Group()
			SCORE += 10
			aliens.add(Alien())

		if sehells_and_rocket_collide:
			SCORE -= 5
			ROCKET_DAMAGE -= 1
			

#
# HERE THE GAME STARTS ---------------------------------------------------------------------
#
		else: 

			screen.blit(text_objects('SCORE: '+ str(SCORE)), (50,0))

			screen.blit(text_objects('TIME: '+ str(round(TIME_COUNTER))), (300,0))
			screen.blit(text_objects('ROCKET HEALTH: '+ str(round(ROCKET_DAMAGE))), (50,20))
			TIME_COUNTER = (pygame.time.get_ticks()-START_TIME)/1000
			 # +=  round(CLOCK.tick())*0.01

			all_objects.update()
			shells.update()
			aliens.update()

			meteors_and_bomb_collided = pygame.sprite.groupcollide(meteors, rockets, True, True)

			for collied in sehells_and_rocket_collide:
				explosion = shell_rocket_anim.getCopy()
				explosion.play()
				explosions.append((explosion, (collied.rect.center)))	

			for collied in shells_and_alien_collided:
				explosion = shell_rocket_anim.getCopy()
				explosion.play()
				explosions.append((explosion, (collied.rect.center)))


			# player_and_metor_collided = pygame.sprite.spritecollide(player, meteors, True)


			all_objects.draw(screen)
			meteors.draw(screen)
			shells.draw(screen)
			aliens.draw(screen)

			for explosion, position in explosions.copy():
				if explosion.isFinished():

					explosions.remove((explosion, position))
				else:
					x, y = position
					explosion.blit(screen, (x, y))


	pygame.display.flip()
	clock.tick(30)
