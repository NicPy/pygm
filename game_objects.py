import pygame
from settings import *
from pygame.math import Vector2
import math


class Rocket(pygame.sprite.Sprite):
	speed = -10
	def __init__(self, position):
		super(Rocket, self).__init__()
		self.image = pygame.image.load('assets/rocket.png')
		self.rect = self.image.get_rect()
		self.rect.midbottom = position

	def update(self):
		self.rect.move_ip((0, self.speed)) # deleting rockets when it is out of screen

class Player(pygame.sprite.Sprite):
	max_speed = 10
	shooting_cooldown = 450

	def __init__(self, clock, rockets):
		super(Player, self).__init__()
		self.rockets = rockets
		self.clock = clock
		self.image = pygame.image.load('assets/ball.bmp')
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH/2
		self.rect.bottom = HEIGHT - 10
		self.current_speed = 0

		self.current_shooting_cooldown = 0

		self.rocket_sound = pygame.mixer.Sound('assets/music/shoot.wav')

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
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.current_shooting_cooldown <= 0:
			self.rocket_sound.play()
			self.rockets.add(Rocket(self.rect.midtop))
			self.current_shooting_cooldown = self.shooting_cooldown

		else:
			self.current_shooting_cooldown -= self.clock.get_time()
		for rocket in list(self.rockets):
			if rocket.rect.bottom < 0:
				self.rockets.remove(rocket)


class Tank(pygame.sprite.Sprite):
	speed = 4

	def __init__(self):
		super(Tank, self).__init__()
		self.image = pygame.image.load('assets/tank.png')
		self.rect = self.image.get_rect()
		self.rect.bottom = HEIGHT - 50
		self.rect.left = 50 

	def update(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_LEFT]:
			self.current_speed = -self.speed

		elif keys[pygame.K_RIGHT]:
			self.current_speed = self.speed 
		else:
			self.current_speed = 0

		self.rect.move_ip((self.current_speed, 0))


class Gun(Tank):
	speed = 4
	cooldown = 10
	current_cooldown = 0
	max_speed = 0.1
	shooting_cooldown = 600
	
	def __init__(self, pos, shells):
		super(Gun, self).__init__()
		self.image = pygame.image.load('assets/gun.png')
		self.orig_image = self.image  # Store a reference to the original.
		self.rect = self.image.get_rect(center=pos)
		self.pos = Vector2(pos)
		self.shells = shells
		self.current_shooting_cooldown = 0

	def update(self):
		if self.current_cooldown <= 0:
			self.rotate()
			self.process_shooting()
			self.current_cooldown = self.cooldown
		else:
			self.current_cooldown-= 10

		keys = pygame.key.get_pressed()

		if keys[pygame.K_LEFT]:
			self.current_speed = -self.speed

		elif keys[pygame.K_RIGHT]:
			self.current_speed = self.speed 
		else:
			self.current_speed = 0

		self.rect.move_ip((self.current_speed, 0))
 	

	def rotate(self):
		 # The vector to the target (the mouse position).
		direction = pygame.mouse.get_pos() - self.pos
		# .as_polar gives you the polar coordinates of the vector,
		# i.e. the radius (distance to the target) and the angle.
		radius, angle = direction.as_polar()
		# Rotate the image by the negative angle (y-axis in pygame is flipped).
		self.image = pygame.transform.rotate(self.orig_image, -angle)
		# Create a new rect with the center of the old rect.
		self.rect = self.image.get_rect(left = self.rect.left, bottom = self.rect.bottom)

		# self.rect = self.image.get_rect(center=(self.rect.center))


	def process_shooting(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.current_shooting_cooldown <= 0:
			# self.rocket_sound.play()
			# print('yes')
			self.shells.add(Shell(self.rect.topright))
			self.current_shooting_cooldown = self.shooting_cooldown

		else:
			self.current_shooting_cooldown -= 10
		for shell in list(self.shells):
			if shell.rect.bottom < 0:
				self.shells.remove(shell)
			
		# for shell in list(self.shells):
		# 	if rocket.rect.bottom < 0:
		# 		self.rockets.remove(rocket)
			

class Shell(pygame.sprite.Sprite):
	# speed = -11
	# t = 2
	v= 11
	g= 9.81 
	def __init__(self, position):
		super(Shell, self).__init__()
		self.image = pygame.image.load('assets/shell.png')
		self.rect = self.image.get_rect()
		self.pos = Vector2(position)
		self.rect.midbottom = position
		self.y= position[1]
		self.x= position[0]
		# self.angle = 85
		self.t = 0
		# self.starting_shell = [self.x, self.y]

	def update(self):
		direction = pygame.mouse.get_pos() - self.pos
		# .as_polar gives you the polar coordinates of the vector,
		# i.e. the radius (distance to the target) and the angle.
		radius, anglee = direction.as_polar()

		# self.angle = anglee
		self.angle = 90 + ((math.atan2(self.pos[0]-pygame.mouse.get_pos()[0], self.pos[1]-pygame.mouse.get_pos()[1] ))/2)*100



		print(self.angle)
		if self.t <4: 
			self.rect.center = (self.x, self.y)
			# self.x = self.x + self.v*self.t*math.cos(self.angle*(math.pi/180 )) 
			# self.y -= self.v*self.t*math.sin(self.angle*(math.pi/180 )) -(self.g*self.t**2)/2 	
			
			self.x = self.x + self.v*self.t*math.cos(self.angle*(math.pi/180 )) 
			self.y -= self.v*self.t*math.sin(self.angle*(math.pi/180 )) -(self.g*self.t**2)/2 	
			
			self.t += 0.03
		# if self.y >= HEIGHT or self.x >= WIDTH:
			
		# else:	
		# 	# self.x += (12 - self.rect.midbottom[0])**2
		# 	# self.y += int(((self.x - self.rect.midbottom[0])*0.015)**2)
		# 	self.rect.center = (self.x, self.y)
		
		# self.x += 1
		# self.y += int(((self.x - self.starting_shell[0])*0.01)**2)
		# self.y += int(((self.x)**2 + 4*self.x)*0.00001)
		# self.x = self.x + self.v*self.t*math.cos(self.angle) 
		# self.y += (self.v*self.t*math.sin(self.angle) -(self.g*self.t**2)/2)*0.001 	
		# print(self.x, self.y)


		# self.rect.move_ip(2, 2)
		# self.rect 
		# print(self.x, self.y)


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
class Meteorit(pygame.sprite.Sprite):
	cooldown = 250
	current_cooldown = 0
	speed = 5

	def __init__(self):
		super(Meteorit, self).__init__()
		import random
		# self.image = pygame.image.load('assets/meteor%s.png' %(str(random.randint(1, 2))))
		self.image = pygame.image.load('assets/meteor1.png')
		self.rect = self.image.get_rect()

		self.rect.midbottom = (random.randint(0, WIDTH), 0)
	
	def update(self):
		self.rect.move_ip(0, self.speed)		

	@staticmethod
	def process_meteors(clock, meteorites):
		if Meteorit.current_cooldown <= 0:
			meteorites.add(Meteorit())
			Meteorit.current_cooldown = Meteorit.cooldown
		else:
			Meteorit.current_cooldown -= clock.get_time()

		for m in list(meteorites):
			if (m.rect.right < 0 or
					m.rect.left > WIDTH or
					m.rect.top >HEIGHT):

				meteorites.remove(m) 













