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
player_rect = player_surface.get_frect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
# is_right = True
direction = 1

star_surface = pygame.image.load(join('images', 'star.png')).convert_alpha()

meteor_surface = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surface.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

laser_surface = pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surface.get_frect(bottomleft=(20,WINDOW_HEIGHT -20))

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
    # x += 0.5
   
    for pos in star_positions:
        display_surface.blit(star_surface,pos)
    
    display_surface.blit(meteor_surface, meteor_rect)
    display_surface.blit(laser_surface, laser_rect)

     # display_surface.blit(surf,(x, y))
     #player movement
    # if player_rect.right < WINDOW_WIDTH and is_right:
    #     player_rect.left += 0.5

    # if player_rect.right == WINDOW_WIDTH:
    #     is_right= False

    # if not is_right and player_rect.left >0:
    #     player_rect.left -= 0.5

    # if player_rect.left == 0:
    #     is_right= True

    if player_rect.left < 0 or player_rect.right > WINDOW_WIDTH:
        direction = -1 * direction
    player_rect.left += direction * 0.5
    display_surface.blit(player_surface, player_rect)

    # draw the game
    pygame.display.update()

# quit game
pygame.quit()
