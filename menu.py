import pygame
import time
from settings import *
def text_objects(text, font):
    textSurface = font.render(text, True, (0, 255, 0))
    return textSurface, textSurface.get_rect()

def game_intro(screen):
	global intro
	keys = pygame.key.get_pressed()            
	# screen.fill((0, 255, 0))
	largeText = pygame.font.Font('freesansbold.ttf',100)
	TextSurf, TextRect = text_objects("welcome to battle", largeText)
	TextRect.center = ((WIDTH/2),(HEIGHT/2))
	screen.blit(TextSurf, TextRect)
	pygame.display.update()
	CLOCK.tick(15)
	if keys[pygame.K_SPACE]:
		intro = False