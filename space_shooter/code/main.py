# import pygame
import pygame
from random import randint
from os.path import join # for fixing imports

# initialize pygame
pygame.init()

# set window and height dimensions
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# create a screen using pygame.display.set_mode
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")

# game loop variable
running = True

# surface
surf = pygame.Surface((100, 200))
x = 100
y = 150



# importing an image
player_surface = pygame.image.load(join('images', 'player.png')).convert_alpha()
star_surface = pygame.image.load(join('images', 'star.png')).convert_alpha()

# star positions
star_positions = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for i in range(20)]
# game loop
while running:
    # handle quitting game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # pygame.draw.rect(display_surface, color="Red", rect=pygame.Rect(20,30,50,100))

    display_surface.fill('darkgray')

    # blit = Block image transfer (Just a way to put one surface over another surface)
    x += 0.5
   
    for pos in star_positions:
        display_surface.blit(star_surface,pos)
    
     # display_surface.blit(surf,(x, y))
    display_surface.blit(player_surface, (x,y))

    # draw the game
    pygame.display.update()

# quit game
pygame.quit()
