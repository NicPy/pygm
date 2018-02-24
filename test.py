import sys, pygame, pyganim
from game_objects import *
from settings import *


pygame.init()
pygame.display.set_caption("Hi, it is me!")

clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)

explode_anim = pyganim.PygAnimation([
	('assets/meteor_exp{}.png'.format(1), 50) for i in range(17)
	], loop = False)

# Game Groups
all_objects = pygame.sprite.OrderedUpdates()
rockets = pygame.sprite.Group()
meteors = pygame.sprite.Group()

explosions = []

music = pygame.mixer.Sound('assets/music/bg.wav')
music.play(-1)

# Game objects
player = Player(clock, rockets)
background = Background()
cloud1 = Cloud('assets/cloud1.png', 2)
cloud2 = Cloud('assets/cloud2.png', 1.5)
# rocket = Rocket(player.rect.midtop)


all_objects.add(background)
all_objects.add(player)
all_objects.add(cloud1)
all_objects.add(cloud2)
all_objects.add(Meteorit())
# all_objects.add(rocket)



while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)

	fast_esc = pygame.key.get_pressed()
	if fast_esc[pygame.K_ESCAPE]:
		sys.exit()

	screen.fill(WHITE)

	Meteorit.process_meteors(clock, meteors)

	all_objects.update()
	rockets.update()
	meteors.update()

	meteors_and_bomb_collided = pygame.sprite.groupcollide(meteors, rockets, True, True)
	for collied in meteors_and_bomb_collided:
		explosion = explode_anim.getCopy()
		explosion.play()
		explosions.append((explosion, (collied.rect.center)))

	player_and_metor_collided = pygame.sprite.spritecollide(player, meteors, True)

	if player_and_metor_collided:
		all_objects.remove(player) 

	all_objects.draw(screen)
	rockets.draw(screen)
	meteors.draw(screen)


	for explosion, position in explosions.copy():
		if explosion.isFinished():
			# print(explosions)
			# print('/************************/')
			# print(explosion)
			explosions.remove((explosion, position))
		else:
			x, y = position
			explosion.blit(screen, (x-30, y-50))

	pygame.display.flip()
	clock.tick(30)
