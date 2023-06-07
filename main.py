import pygame
import random
import math
from pygame import mixer
import time

try:
    pygame.init()  # initialise pygame

    screen = pygame.display.set_mode((800,600))  # creates display screen

    # Background:
    background = pygame.image.load('death star background.jpg')

    # background sound:
    mixer.music.load('imperial_march.mp3')
    mixer.music.play(-1)

    # caption and icon:
    pygame.display.set_caption("Space Invaders")
    icon = pygame.image.load('space-invaders.png')
    pygame.display.set_icon(icon)

    # player
    playerimg = pygame.image.load('xwing1.png')
    playerX = 370
    playerY = 480
    movement = 0
    sensitivity = 2

    # enemy
    enemyimg = []
    enemyX = []
    enemyY = []
    enemymovementX = []
    enemymovementY = []
    num_of_enemies = 10

    for i in range(num_of_enemies):
        enemyimg.append(pygame.image.load('tiefighter_main.png'))
        enemyX.append(random.randint(0, 733))
        enemyY.append(random.randint(50, 150))
        enemymovementX.append(0.5)
        enemymovementY.append(50)

    # bullet
    bulletimg = pygame.image.load('redbullet.png')
    bulletX = 0
    bulletY = 480
    bulletmovementX = 0
    bulletmovementY = 20
    bullet_state = "ready"

    # score:
    score_value = 0
    font = pygame.font.Font('Starjedi.ttf', 32)
    textX = 20
    textY = 0

    over_font = pygame.font.Font('Starjedi.ttf', 64)
    repeat_font = pygame.font.Font('Starjedi.ttf', 24)


    def show_score(x, y):
        score = font.render("score: " + str(score_value), True, (255, 255, 31))
        screen.blit(score, (x, y))


    def game_over_text():
        over_text = over_font.render("game over", True, (255, 255, 31))
        screen.blit(over_text, (200, 250))
        repeat = repeat_font.render("press the spacebar to play again", True, (255, 255, 31))
        screen.blit(repeat, (150, 350))
        score = font.render("score: " + str(score_value), True, (255, 255, 31))
        screen.blit(score, (textX, textY))

    def player(x, y):
        screen.blit(playerimg, (x, y))


    def enemy(x, y, i):
        screen.blit(enemyimg[i], (x, y))


    def shoot(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bulletimg, (x + 16, y - 10))


    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
        if distance < 27:
            return True
        else:
            return False


    # game loop:
    running = True
    game_over = False  
    while running:

        # screen fill with solid colour (RGB) and background:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    movement = -sensitivity
                if event.key == pygame.K_RIGHT:
                    movement = sensitivity
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bullet_sound = mixer.Sound('blaster_firing.wav')
                        bullet_sound.play()
                        bulletX = playerX
                        shoot(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    movement = 0

        if not game_over:  
            # movement and boundaries
            playerX += movement

            if playerX <= 3:
                playerX = 3
            elif playerX >= 733:
                playerX = 733

            for i in range(num_of_enemies):

                if enemyY[i] > 440:
                    for j in range(num_of_enemies):
                        enemyY[j] = 2000
                    game_over = True  # set game_over flag
                    time.sleep(1)
                    break
                

                enemyX[i] += enemymovementX[i]
                if enemyX[i] <= 3:
                    enemymovementX[i] = 0.5
                    enemyY[i] += enemymovementY[i]
                elif enemyX[i] >= 747:
                    enemymovementX[i] = -0.5
                    enemyY[i] += enemymovementY[i]

                # collision
                collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
                if collision:
                    bulletY = 480
                    bullet_state = "ready"
                    enemyX[i] = random.randint(0, 733)
                    enemyY[i] = random.randint(50, 150)
                    score_value += 1
                    explosion_sound = mixer.Sound('explode.wav')
                    explosion_sound.play()

                enemy(enemyX[i], enemyY[i], i)

            if bulletY <= -30:
                bulletY = 480
                bullet_state = "ready"
            if bullet_state == "fire":
                shoot(bulletX, bulletY)
                bulletY -= bulletmovementY

            player(playerX, playerY)

            show_score(textX, textY)

        if game_over:  # display game over screen
            game_over_text()

            # check for spacebar press to restart the game
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                game_over = False
                score_value = 0
                for i in range(num_of_enemies):
                    enemyX[i] = random.randint(0, 733)
                    enemyY[i] = random.randint(50, 150)

        pygame.display.update()  # always update display


except pygame.error as e:
    print("An error occurred: ", str(e))
