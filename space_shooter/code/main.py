# import pygame
import pygame
from random import randint
from os.path import join # for fixing imports

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
           
        self.direction = pygame.math.Vector2()
        self.speed = 300

    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])  
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])  
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE]:
            print("SPACE")

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))



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

clock = pygame.time.Clock()

# surface
surf = pygame.Surface((100, 200))
x = 100
y = 150

all_sprites = pygame.sprite.Group()
surf = pygame.image.load(join("images", "star.png")).convert_alpha()
for i in range(20):
    Star(all_sprites, surf)

player = Player(all_sprites)

meteor_surface = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surface.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

laser_surface = pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surface.get_frect(bottomleft=(20,WINDOW_HEIGHT -20))

# star positions
# game loop
while running:
    #clock
    dt = clock.tick()/1000

    # handle quitting game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill('darkgray')
    
    all_sprites.update(dt)
    display_surface.blit(meteor_surface, meteor_rect)
    all_sprites.draw(display_surface)
    pygame.display.update()

# quit game
pygame.quit()
