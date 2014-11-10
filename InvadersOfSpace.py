__author__ = '2307942949'
# coding: latin-1

import pygame, sys, os, random, thread, time, math
from pygame.locals import *

# ==== CLASSES ====

# Asteroid
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, asteroid_image, speed, points):
        pygame.sprite.Sprite.__init__(self)
        self.image = asteroid_image
        self.rect = self.image.get_rect()
        self.speed = speed
        self.points = points

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.speed = 5

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

    def faceMouse(self, angle):
        self.image = pygame.transform.rotate(player_image, angle)

# Projectile
class Missile(pygame.sprite.Sprite):
    def __init__(self, mouse):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_image
        self.rect = self.image.get_rect()
        self.speed = 7

        # Vector calc - CREDIT: Alexey
        difx = mouse[0] - player.rect.centerx
        dify = mouse[1] - player.rect.centery
        a = math.sqrt(difx**2 + dify**2)
        if dify < 0:
            angle = (math.degrees(math.acos(difx / a)) - 90)
        else:
            angle = (math.degrees(math.acos(difx / a)) + 90) * (-1)

        self.direction = [difx / a * self.speed, dify / a * self.speed]
        self.image = pygame.transform.rotate(missile_image, angle)

    def moveMissile(self):
        delete = False

        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]

        if self.direction[0] < 0:
            if self.rect.x < 0:
                delete = True
        else:
            if self.rect.x > WINDOWWIDTH:
                delete = True

        if self.direction[1] < 0:
            if self.rect.y < 0:
                delete = True
        else:
            if self.rect.y > WINDOWHEIGHT:
                delete = True

        return delete

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
            dice = random.randrange(0,100)

            if dice < 70:
                asteroid = brownAsteroid_image
                speed = 1
                points = 1
            elif dice < 90:
                asteroid = redAsteroid_image
                speed = 2.5
                points = 3
            else:
                asteroid = silverAsteroid_image
                speed = 4
                points = 5

            block = Asteroid(asteroid, speed, points)
            # Set a random location for the block
            block.rect.x = random.randrange(10, (WINDOWWIDTH - 50))
            block.rect.y = random.randrange(-200, -50)

            asteroid_list.add(block)
            all_sprites_list.add(block)

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
brownAsteroid_image = pygame.image.load('img/brown_asteroid.png').convert_alpha()
redAsteroid_image = pygame.image.load('img/red_asteroid.png').convert_alpha()
silverAsteroid_image = pygame.image.load('img/silver_asteroid.png').convert_alpha()
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

# Shooting
shooting = False
timeShot = time.time()

# Hotfix
hotfix = 0

# Game loop
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Facing mouse
        if event.type == MOUSEMOTION:
            mousex, mousey = event.pos  # Mouse pos
            moveVector = (mousex-player.rect.centerx, mousey-player.rect.centery)  # Vector
            angle = 180 + math.degrees(math.atan2(*moveVector))  # Angle
            player.faceMouse(angle)  # Rotate

        # Shooting
        if event.type == pygame.MOUSEBUTTONDOWN:
            shooting = True  # Is shooting


        if event.type == pygame.MOUSEBUTTONUP:
            shooting = False  # Is not shooting any more

    # Check if finished
    if not asteroid_list.sprites():
        if hotfix:
            raise SystemExit, "You Win! | Points: " + str(SCORE)
        else:
            hotfix = 1

    # Player movement
    player.move()

    # Shooting
    if shooting:
        if timeShot + 0.1 < time.time():
            timeShot = time.time()
            mousePos = pygame.mouse.get_pos()  # Mouse Position
            shot = Missile(mousePos)  # Create shot
            shot.rect.x = player.rect.centerx  # Originating position
            shot.rect.y = player.rect.centery  # Originating position

            missile_list.add(shot)
            all_sprites_list.add(shot)

    # == Collision detection ==
    # Player and blocks
    playerHit = pygame.sprite.spritecollide(player, asteroid_list, True)  # Ef player collider við block, þá kill-both = true

    if playerHit:
        raise SystemExit, "You Lose! | Points: " + str(SCORE)

    # Missiles and Asteroids
    asteroidsShot = pygame.sprite.groupcollide(asteroid_list, missile_list, True, True)  # Kill both

    # Move blocks down
    for block in asteroid_list:
        block.rect.y += block.speed

        if block.rect.y > WINDOWHEIGHT:
            asteroid_list.remove(block)

    # Move missiles up
    for shot in missile_list:
        delete = shot.moveMissile()

        if delete:
            missile_list.remove(shot)
            all_sprites_list.remove(shot)

    # Stigagjöf
    for hit in asteroidsShot:
        SCORE += hit.points

    # Draw all sprites
    SCREEN.blit(background, backgroundRect)
    all_sprites_list.draw(SCREEN)

    # Flip&Clock
    pygame.display.flip()
    fpsClock.tick(FPS)