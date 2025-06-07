import pygame
from random import randint, uniform
from os.path import join # import join function for file paths



class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        original_image = pygame.image.load(join("images", "player.png")).convert_alpha()
        scale_factor = 3  
        new_size = (original_image.get_width() * scale_factor, original_image.get_height() * scale_factor)
        self.image = pygame.transform.scale(original_image, new_size)
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
            Laser(laser_surface, self.rect.midtop, (all_sprites, laser_sprites)) 
            self.shoot_timer = pygame.time.get_ticks()
            self.can_shoot = False
    
        self.laser_timer()

# class Star(pygame.sprite.Sprite):
#     def __init__(self, groups, surf):
#         super().__init__(groups)
#         self.image = surf
#         self.rect = self.image.get_frect(center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))
class Star(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.visible = True
        self.blink_time = randint(800, 2000)
        self.last_blink = pygame.time.get_ticks()
        # Use 1x1 or 2x2 for a more "star-like" look
        self.image = pygame.Surface((2, 2), pygame.SRCALPHA)
        brightness = randint(180, 255)
        self.image.fill((brightness, brightness, brightness))
        self.rect = self.image.get_frect(center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

    def update(self, dt):
        now = pygame.time.get_ticks()
        if now - self.last_blink > self.blink_time:
            self.visible = not self.visible
            self.last_blink = now
            self.blink_time = randint(800, 2000)
        if self.visible:
            brightness = randint(180, 255)
            self.image.fill((brightness, brightness, brightness))
        else:
            self.image.fill((0, 0, 0, 0))

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
def display_score():
    current_time = pygame.time.get_ticks()//100  # Update the timer
    text_surf = font.render(f'Score: {str(current_time)}', True, (255, 255, 255))
    text_rect = text_surf.get_frect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 10))
    display_surface.blit(text_surf, text_rect)

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
meteor_surface = pygame.transform.scale(meteor_surface, (
    meteor_surface.get_width() // 5,
    meteor_surface.get_height() // 5
))
laser_surface = pygame.image.load(join('images', 'laser.png')).convert_alpha()
# star_surf = pygame.image.load(join("images", "star.png")).convert_alpha()
font = pygame.font.Font(join("images", "Oxanium-Bold.ttf"), 30)
display_score()


# game loop variable
running = True

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

for i in range(20):
    Star(all_sprites)

player = Player(all_sprites)


meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)  # every half second

def collisions():
    global running
    collision_sprites=  pygame.sprite.spritecollide(player, meteor_sprites, False)
    if collision_sprites:
        running = False
    for laser in laser_sprites:
        meteor_hit = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if meteor_hit:
            laser.kill()

# game loop
while running:
    #clock
    dt = clock.tick()/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor(meteor_surface, (randint(0, WINDOW_WIDTH), randint(-200,-100)), (all_sprites, meteor_sprites))

    display_surface.fill('#000000')
    
    all_sprites.update(dt)
    

    collisions()

    all_sprites.draw(display_surface)

    display_score()

    pygame.display.update()

# quit game
pygame.quit()
