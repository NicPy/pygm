import pygame
from settings import *

class Rocket(pygame.sprite.Sprite):
	speed = -10
	def __init__(self, position):
		super(Rocket, self).__init__()
		self.image = pygame.image.load('assets/rocket.png')
		self.rect = self.image.get_rect()
		self.rect.midbottom = position

	def update(self):
		self.rect.move_ip((0, self.speed))

class Player(pygame.sprite.Sprite):
	max_speed = 10

	def __init__(self, clock, rockets):
		super(Player, self).__init__()
		self.rockets = rockets
		self.clock = clock
		self.image = pygame.image.load('assets/ball.bmp')
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH/2
		self.rect.bottom = HEIGHT - 10
		self.current_speed = 0

	def update(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_LEFT]:
			self.current_speed = -self.max_speed
		elif keys[pygame.K_RIGHT]:
			self.current_speed = self.max_speed
		else:
			self.current_speed = 0

		self.rect.move_ip((self.current_speed, 0))
		self.process_shooting()

	def process_shooting(self):
		pass

class Background(pygame.sprite.Sprite):
	def __init__(self):
		super(Background, self).__init__()
		self.image = pygame.image.load('assets/bg.jpg')
		self.rect = self.image.get_rect()
		self.rect.bottom = HEIGHT

	def update(self):
		pass
		
class Cloud(pygame.sprite.Sprite):
	def __init__(self, img, speed):
		super(Cloud, self).__init__()
		''' You can create many clouds
			image should be the same size as screen(check settings)
		'''

		self.speed = speed 					# pixels at frame 
		self.image = pygame.image.load(img)	# string with img url
		self.rect = self.image.get_rect()
		self.rect.bottom = HEIGHT			# img start position

	def update(self):
		self.rect.left += self.speed

		if self.rect.left >= self.rect.width:
			self.rect.right = 0
		