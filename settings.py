import pygame

SIZE = (WIDTH, HEIGHT) = (700, 600)
WHITE = (255, 255, 255)
GREEN = (0, 222, 0)
BLACK = (0, 0, 0)
MOUSE_BUTTON_LEFT = (1, 0, 0)
MOUSE_BUTTON_RIGHT = (0, 0, 1)
CLOCK = pygame.time.Clock()
GAME_DURATION = 60

#some images
GAME_OVER_IMAGE = pygame.image.load('assets/game_over_bg.jpg')
HELP_PAGE = pygame.image.load('assets/help_page.jpg')