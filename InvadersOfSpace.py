__author__ = '2307942949'
# coding: latin-1

import pygame, sys, os, random, thread, time, math
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
        self.surface = pygame.Surface((45, 45), SRCALPHA)
        self.surface.blit(self.image, self.rect)
        self.angle = 0

    def rotatePlayer(self, posMouse):

        playerPos = self.rect.center

        difx = posMouse[0] - playerPos[0]
        dify = posMouse[1] - playerPos[1]

        if (difx < -1 or difx > 1) and (dify < -1 or dify > 1):
            a = math.sqrt(difx ** 2 + dify ** 2)
            self.angle = (math.degrees(math.acos(difx / a)) + 90) * (-1)

            if dify < 0 :
                self.angle = math.degrees(math.acos(difx / a)) - 90

        temp_surface = pygame.transform.rotate(self.surface, self.angle)
        temp_base = temp_surface.get_rect()
        temp_base.center = self.rect.center

        self.image = pygame.transform.rotate(player_image, self.angle)

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:  # Left
            if player.rect.x < -60: # Wrap around
                player.rect.x = WINDOWWIDTH
            player.rect.x -= self.speed

        if key[pygame.K_d]:  # Right
            if player.rect.x > WINDOWWIDTH: # Wrap around
                player.rect.x = - 60
            player.rect.x += self.speed

        if key[pygame.K_w]:  # Up
            if player.rect.y <= 7:  # Border
                player.rect.y = 7
            player.rect.y -= self.speed

        if key[pygame.K_s]:  # Down
            if player.rect.y >= WINDOWHEIGHT - 35:  # Border
                player.rect.y = WINDOWHEIGHT - 35
            player.rect.y += self.speed

# Projectile
class Missile(pygame.sprite.Sprite):
    def __init__(self, posStart, posMouse, speed=7):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_image
        self.rect = self.image.get_rect()
        self.rect.x = posStart[0] + 14
        self.rect.y = posStart[1] - 10
        self.speed = speed

        # Angle calculation - Takk Alexey
        difx = posMouse[0] - posStart[0]
        dify = posMouse[1] - posStart[1]
        z = math.sqrt(difx**2 + dify**2)


        if dify < 0:
            self.angle = math.degrees(math.acos(difx / z)) - 90
        else:
            self.angle = (math.degrees(math.acos(difx / z)) + 90) * (-1)

        self.direction = [difx / z * speed, dify / z * speed]


    def moveMissile(self):

        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]

        # Border
        delete = False
        if self.rect.y < -60 or self.rect.y > WINDOWHEIGHT or self.rect.x < -60 or self.rect.x > WINDOWWIDTH:
                delete = True

        return delete

    def rotateMissile(self):
        self.image = pygame.transform.rotate(missile_image, self.angle)

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
player_image = pygame.image.load('img/alienblaster.png').convert_alpha()
asteroid_image = pygame.image.load('teacher shit/images/asteroid.png').convert_alpha()
missile_image = pygame.image.load('img/laser.png').convert_alpha()
background = pygame.image.load('img/blackhole.png').convert_alpha()
backgroundRect = background.get_rect()

MOUSEDOWN = False

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            MOUSEDOWN = True
        if event.type == pygame.MOUSEBUTTONUP:
            MOUSEDOWN = False

    # Mouse position
    mousePos = pygame.mouse.get_pos()

    # Player movement
    player.move()
    player.rotatePlayer(mousePos)

    # Shooting
    if MOUSEDOWN:
        # player position
        startPos = (player.rect.x, player.rect.y)

        # Create the missile
        shot = Missile(startPos, mousePos)

        # Rotate it
        shot.rotateMissile()

        # Add it to the sprite lists
        missile_list.add(shot)
        all_sprites_list.add(shot)


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