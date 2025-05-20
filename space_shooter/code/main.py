# import pygame
import pygame

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


# game loop
while running:
    # handle quitting game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # pygame.draw.rect(display_surface, color="Red", rect=pygame.Rect(20,30,50,100))

    display_surface.fill('darkgray')

    # blit = Block image transfer (Just a way to put one surface over another surface)
    display_surface.blit(surf,(100, 150))

    # draw the game
    pygame.display.update()

# quit game
pygame.quit()
