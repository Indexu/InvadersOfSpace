__author__ = '2307942949'
# coding: latin-1

import pygame, sys, os, random, thread, time
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
        self.direction = "up"

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:  # Left
            if player.rect.x < -60: # Wrap around
                player.rect.x = WINDOWWIDTH
            player.rect.x -= self.speed
            self.image = pygame.transform.rotate(player_image, 90)
            self.direction = "left"

        elif key[pygame.K_RIGHT]:  # Right
            if player.rect.x > WINDOWWIDTH: # Wrap around
                player.rect.x = - 60
            player.rect.x += self.speed
            self.image = pygame.transform.rotate(player_image, 270)
            self.direction = "right"

        elif key[pygame.K_UP]:  # Up
            if player.rect.y <= 7:  # Border
                player.rect.y = 7
            player.rect.y -= self.speed
            self.image = pygame.transform.rotate(player_image, 0)
            self.direction = "up"

        elif key[pygame.K_DOWN]:  # Down
            if player.rect.y >= WINDOWHEIGHT - 35:  # Border
                player.rect.y = WINDOWHEIGHT - 35
            player.rect.y += self.speed
            self.image = pygame.transform.rotate(player_image, 180)
            self.direction = "down"

# Projectile
class Missile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_image
        self.rect = self.image.get_rect()
        self.direction = "up"
        self.speed = 7

    def moveMissile(self):
        delete = False
        if self.direction == "up":
            if self.rect.y < -60:  # Border
                delete = True
            self.rect.y -= self.speed

        elif self.direction == "down":
            if self.rect.y > WINDOWHEIGHT:  # Border
                delete = True
            self.rect.y += self.speed

        elif self.direction == "left":
            if self.rect.x < -60:  # Border
                delete = True
            self.rect.x -= self.speed

        elif self.direction == "right":
            if self.rect.x > WINDOWWIDTH:  # Border
                delete = True
            self.rect.x += self.speed

        return delete

    def rotateMissile(self):
        if self.direction == "up":
            self.image = pygame.transform.rotate(missile_image, 0)

        elif self.direction == "down":
            self.image = pygame.transform.rotate(missile_image, 180)

        elif self.direction == "left":
            self.image = pygame.transform.rotate(missile_image, 90)

        elif self.direction == "right":
            self.image = pygame.transform.rotate(missile_image, 270)

# === Threads ===
# Populate asteroids
def populate():
    global MAX_ASTEROIDS
    global asteroid_list
    global all_sprites_list

    asteroids = 0
    while True:
        if MAX_ASTEROIDS > 20:
            asteroids = random.randint(5,20)
            MAX_ASTEROIDS -= asteroids
        else:
            asteroids = random.randint(0,MAX_ASTEROIDS)
            MAX_ASTEROIDS -= asteroids

        for i in range(asteroids):
            block = Asteroid()
            # Set a random location for the block
            block.rect.x = random.randrange(20, (WINDOWWIDTH - 30))
            block.rect.y = random.randrange(-200, 0)

            asteroid_list.add(block)
            all_sprites_list.add(block)

        print MAX_ASTEROIDS
        time.sleep(1)

# ==== INIT ====
pygame.init()

FPS = 60 # FPS
fpsClock = pygame.time.Clock() # Clock
WINDOWWIDTH = 500 # Width
WINDOWHEIGHT = 800 # Height
TITLE = 'Skilaverkefni 4' # Caption
os.environ["SDL_VIDEO_CENTERED"] = "1"

SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption(TITLE)

# ==== VARIABLES ====
player_image = pygame.image.load('img/ship.png').convert_alpha()
asteroid_image = pygame.image.load('teacher shit/images/asteroid.png').convert_alpha()
missile_image = pygame.image.load('img/laser.png').convert_alpha()
background = pygame.image.load('img/blackhole.png').convert_alpha()
backgroundRect = background.get_rect()

WHITE = (255, 255, 255)
SCORE = 0
MAX_ASTEROIDS = random.randint(150, 200)

# ==== SPRITES ====

# Asteroids list
asteroid_list = pygame.sprite.Group()
# Missiles
missile_list = pygame.sprite.Group()
# All sprites
all_sprites_list = pygame.sprite.Group()

# Player
player = Player()
# Starting pos
player.rect.x = WINDOWWIDTH / 2
player.rect.y = WINDOWHEIGHT - 50

all_sprites_list.add(player)

# Thread for population
thread.start_new_thread(populate, ())

# Game loop
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shot = Missile()

                # Horizontal
                if player.direction == "left" or player.direction == "right":
                    shot.rect.x = player.rect.x + 14
                    shot.rect.y = player.rect.y + 15
                # Vertical
                else:
                    shot.rect.x = player.rect.x + 14
                    shot.rect.y = player.rect.y - 15

                shot.direction = player.direction
                shot.rotateMissile()
                missile_list.add(shot)
                all_sprites_list.add(shot)

    # Player movement
    player.move()

    SCREEN.fill(WHITE)

    # == Collision detection ==
    # Player and blocks
    playerHit = pygame.sprite.spritecollide(player, asteroid_list, True)  # Ef player collider við block, þá kill-both = true

    #if playerHit:
        #raise SystemExit, "You Lose!"

    # Missiles and Asteroids
    asteroidsShot = pygame.sprite.groupcollide(missile_list, asteroid_list, True, True)  # Kill both

    # Move blocks down
    for block in asteroid_list:
        block.rect.y += 1

    # Move missiles up
    for shot in missile_list:
        delete = shot.moveMissile()

        if delete:
            missile_list.remove(shot)

    # Stigagjöf
    for shot in asteroidsShot:
        SCORE += 1
        print(SCORE)

    # Draw all sprites
    SCREEN.blit(background, backgroundRect)
    all_sprites_list.draw(SCREEN)

    # Flip&Clock
    pygame.display.flip()
    fpsClock.tick(FPS)