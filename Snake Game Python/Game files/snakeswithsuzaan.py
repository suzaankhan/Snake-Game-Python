import os
import pygame
import random
x = pygame.init()

#Creating game window
screen_width = 800
screen_height = 500
gameWindow = pygame.display.set_mode((screen_width, screen_height))

#game title
pygame.display.set_caption("SnakesWithSuzaan")
pygame.display.update()

#colours
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)

from pygame import mixer
mixer.init()

font = pygame.font.SysFont('sigmar one', 50)
clock = pygame.time.Clock()

bgimg = pygame.image.load("snake back.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

def score_on_screen(text, colour, x, y):
    screen_text = font.render(text, True, colour)
    gameWindow.blit(screen_text, [x,y])

def plot_snake(gameWindow, color, snake_list, snake_size):
    for x,y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def stop_music():
    mixer.music.stop()

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.blit(bgimg, (0, 0))
        pygame.draw.rect(gameWindow, black, [100, 300, 600, 130])
        score_on_screen("Welcome to SnakesWithSuzaan", white, 140, 320)
        score_on_screen("Press Enter To Play", white, 200, 370)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()

#Creating Game Loop
def game_loop():
    # Game specific Variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_size = 20
    fps = 30
    if(not os.path.exists("highscore.py")):
        with open("highscore.py", "w") as f:
            f.write("0")
    with open("highscore.py", "r") as f:
        hiscore = f.read()
    food_x = random.randint(50, 650)
    food_y = random.randint(50, 350)
    food_size = 20
    init_velocity = 7
    velocity_x = 0
    velocity_y = 0
    score = 0
    snake_list = []
    snake_length = 1

    while not exit_game:
        if game_over:
            with open("highscore.py", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            score_on_screen("Game Over! Press Enter To Continue", red, screen_width/10, screen_height/2.5)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        stop_music()
                        game_loop()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_RETURN:
                        stop_music()

                    # if event.key == pygame.K_q:
                    #     score = score + 10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y
            if abs(snake_x-food_x)<8 and abs(snake_y-food_y)<8:
                score = score + 10
                food_x = random.randint(50, 650)
                food_y = random.randint(50, 350)
                pygame.mixer.music.load("beep.wav")
                pygame.mixer.music.play()
                snake_length = snake_length + 5
                if score > int(hiscore):
                    hiscore = score

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load("game over.wav")
                pygame.mixer.music.play()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            stop_music()

            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load("game over.wav")
                pygame.mixer.music.play()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            stop_music()

            gameWindow.fill(black)
            score_on_screen("Score: " + str(score) + "    HighScore: " + str(hiscore), white, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, food_size,food_size])
            # pygame.draw.rect(gameWindow, green, [snake_x, snake_y, snake_size, snake_size])
            plot_snake(gameWindow, green, snake_list, snake_size)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()

welcome()