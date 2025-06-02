import pygame
from random import randint, uniform
from os.path import join # import join function for file paths



class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
           
        self.direction = pygame.math.Vector2()
        self.speed = 300

        # timer
        self.can_shoot = True
        self.shoot_timer = 0
        self.cooldown_duration = 400
    
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_timer >= self.cooldown_duration:
                self.can_shoot = True

    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])  
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])  
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surface, self.rect.midtop, all_sprites) 
            self.shoot_timer = pygame.time.get_ticks()
            self.can_shoot = False
    
        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=pos)
    
    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400,500)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time > self.lifetime:
            self.kill()

# initialize pygame
pygame.init()

# set window and height dimensions
WINDOW_WIDTH = 1280    
WINDOW_HEIGHT = 720


# create a screen using pygame.display.set_mode
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")

# import images
meteor_surface = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laser_surface = pygame.image.load(join('images', 'laser.png')).convert_alpha()
star_surf = pygame.image.load(join("images", "star.png")).convert_alpha()

# game loop variable
running = True

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

for i in range(20):
    Star(all_sprites, star_surf)

player = Player(all_sprites)


meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)  # every half second

# star positions
# game loop
while running:
    #clock
    dt = clock.tick()/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor(meteor_surface, (randint(0, WINDOW_WIDTH), randint(-200,-100)), all_sprites)

    display_surface.fill('darkgray')
    
    all_sprites.update(dt)
    all_sprites.draw(display_surface)

    pygame.display.update()

# quit game
pygame.quit()
