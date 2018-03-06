import pygame
import time
from settings import *

menubg_image = pygame.image.load('assets/menubg.jpg')

def text_objects(text):
	largeText = pygame.font.Font('freesansbold.ttf',15)
	textSurface = largeText.render(text, True, (0, 0, 0))
	return textSurface

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

def button_check(pos, x, y, x1, y1): 
    return pos[0] >= x and pos[0] < x + x1 and pos[1] >= y and pos[1] < y + y1


def make_button(surface,color,text_color,x,y,width,height,text):
    pygame.draw.rect(surface, (0,0,0),(x-1,y-1,width+2,height+2),1) #makes outline around the box
    pygame.draw.rect(surface, color,(x,y,width,height))#mkes the box

    myfont = pygame.font.SysFont('Arial Black', 15) #creates the font, size 15 (you can change this)
    label = myfont.render(text, 1, text_color) #creates the label
    surface.blit(label, (x+2, y)) #renders the label


class Menu_btn(pygame.sprite.Sprite):
	"""docstring for Menu_btn"""
	def __init__(self, img_path, pos):
		super(Menu_btn, self).__init__()
		
		self.image = pygame.image.load(img_path)
		self.rect = self.image.get_rect()
		self.rect.midtop = pos
		
	def update(self):
		self.mouse_in()

	def mouse_in(self):
		mkeys = pygame.mouse.get_pressed()
		mouse_pos = pygame.mouse.get_pos()

		if mkeys == MOUSE_BUTTON_LEFT:
			if mouse_pos[0] >= self.rect.left and mouse_pos[0] <= self.rect.right \
				and mouse_pos[1] >= self.rect.top and mouse_pos[1] <= self.rect.bottom:
				# print(self.rect)
				# print(mouse_pos)
				return True
