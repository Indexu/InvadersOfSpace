__author__ = '2307942949'
# coding: latin-1

import pygame, sys, os, random
from pygame.locals import *

# ==== CLASSES ====

# Asteroid
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = asteroid_image
        self.rect = self.image.get_rect()

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.speed = 5

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:  # Left
            if player.rect.x < -60: # Wrap around
                player.rect.x = WINDOWWIDTH
            player.rect.x -= self.speed
            self.image = pygame.transform.rotate(self.image, 270)

        elif key[pygame.K_RIGHT]:  # Right
            if player.rect.x > WINDOWWIDTH: # Wrap around
                player.rect.x = - 60
            player.rect.x += self.speed
            self.image = pygame.transform.rotate(self.image, 90)

# Projectile
class Missile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_image
        self.rect = self.image.get_rect()

# ==== INIT ====
pygame.init()

FPS = 60 # FPS
fpsClock = pygame.time.Clock() # Clock
WINDOWWIDTH = 700 # Width
WINDOWHEIGHT = 400 # Height
TITLE = 'Skilaverkefni 3' # Caption
os.environ["SDL_VIDEO_CENTERED"] = "1"

SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption(TITLE)

# ==== VARIABLES ====
player_image = pygame.image.load('teacher shit/images/spaceship.png').convert_alpha()
asteroid_image = pygame.image.load('teacher shit/images/asteroid.png').convert_alpha()
missile_image = pygame.image.load('teacher shit/images/missile.png').convert_alpha()
WHITE = (255, 255, 255)
SCORE = 0

# ==== SPRITES ====

# Asteroids list
asteroid_list = pygame.sprite.Group()
# Missiles
missile_list = pygame.sprite.Group()
# All sprites
all_sprites_list = pygame.sprite.Group()

# Populate invaders
for i in range(50):
    block = Asteroid()
    # Set a random location for the block
    block.rect.x = random.randrange(WINDOWWIDTH - 20)
    block.rect.y = random.randrange(WINDOWHEIGHT - 160)

    asteroid_list.add(block)
    all_sprites_list.add(block)

# Player
player = Player()
# Starting pos
player.rect.x = 340
player.rect.y = 380

all_sprites_list.add(player)

# Game loop
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shot = Missile()
                shot.rect.x = player.rect.x + 30
                shot.rect.y = player.rect.y - 15
                missile_list.add(shot)
                all_sprites_list.add(shot)

    # Player movement
    player.move()

    SCREEN.fill(WHITE)

    # == Collision detection ==
    # Player and blocks
    blocks_hit_list = pygame.sprite.spritecollide(player, asteroid_list, True) # Ef player collider við block, þá kill-block = true

    # Missiles and Asteroids
    pygame.sprite.groupcollide(missile_list, asteroid_list, True, True) # Kill both

    # Move blocks down
    for block in asteroid_list:
        block.rect.y += 1

    # Move missiles up
    for shot in missile_list:
        shot.rect.y -= 5

    # Stigagjöf
    for block in blocks_hit_list:
        SCORE += 1
        print(SCORE)

    # Draw all sprites
    all_sprites_list.draw(SCREEN)

    # Flip&Clock
    pygame.display.flip()
    fpsClock.tick(FPS)