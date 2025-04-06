import pygame
import random
import time

pygame.init()

width, height = 600, 400
block_size = 10
font_style = pygame.font.SysFont("comicsansms", 20)
button_font = pygame.font.SysFont("comicsansms", 30)

red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
blue = (50, 153, 213)
yellow_light = (255, 255, 153)
yellow_medium = (255, 204, 102)
dark_green = (0, 100, 0)
rainbow = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]
yin_color = (0, 0, 0)
yang_color = (255, 255, 255)

snake_color = dark_green
score = 0
yin_unlocked = False
yang_unlocked = False

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Змейка ГыГы')


def draw_chess_board():
    for row in range(height // block_size):
        for col in range(width // block_size):
            color = yellow_light if (row + col) % 2 == 0 else yellow_medium
            pygame.draw.rect(screen, color, [col * block_size, row * block_size, block_size, block_size])


def message(msg, font, color, center):
    mesg = font.render(msg, True, color)
    text_rect = mesg.get_rect(center=center)
    screen.blit(mesg, text_rect)


def show_score():
    score_text = font_style.render(f"Очки: {score}", True, black)
    screen.blit(score_text, (10, 10))


def main_menu():
    print("Главное меню запущено.")
    while True:
        screen.fill(blue)
        message("ГыГы Змейка", button_font, white, (width / 2, height / 4))
        show_score()
        pygame.draw.rect(screen, white, (width / 3, height / 2 - 30, 150, 50))
        pygame.draw.rect(screen, white, (width / 3, height / 2 + 50, 150, 50))
        message("Играть", font_style, black, (width / 3 + 75, height / 2 - 5))
        message("Магазин", font_style, black, (width / 3 + 75, height / 2 + 75))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if width / 3 <= x <= width / 3 + 150:
                    if height / 2 - 30 <= y <= height / 2 + 20:
                        print("Выбор: Играть.")
                        return "game"
                    elif height / 2 + 50 <= y <= height / 2 + 100:
                        print("Выбор: Магазин.")
                        return "shop"


def shop():
    global snake_color, score, yin_unlocked, yang_unlocked
    print("Магазин запущен.")
    while True:
        screen.fill(blue)
        message("МАГАЗИН", button_font, white, (width / 2, 40))
        show_score()

        pygame.draw.rect(screen, dark_green, (width / 3, height / 2 - 120, 150, 50))
        pygame.draw.rect(screen, black, (width / 3, height / 2 - 60, 150, 50))
        pygame.draw.rect(screen, white, (width / 3, height / 2, 150, 50))
        pygame.draw.rect(screen, (128, 128, 128), (width / 3, height / 2 + 60, 150, 50))
        pygame.draw.rect(screen, rainbow[0], (width / 3, height / 2 + 120, 150, 50))

        if snake_color == dark_green:
            message("Используется", font_style, white, (width / 3 + 75, height / 2 - 95))
        else:
            message("Бесплатно", font_style, white, (width / 3 + 75, height / 2 - 95))

        if snake_color == yin_color:
            message("Используется", font_style, white, (width / 3 + 75, height / 2 - 35))
        else:
            message("Инь (25)", font_style, white, (width / 3 + 75, height / 2 - 35))

        if snake_color == yang_color:
            message("Используется", font_style, black, (width / 3 + 75, height / 2 + 25))
        else:
            message("Янь (25)", font_style, black, (width / 3 + 75, height / 2 + 25))

        if snake_color == rainbow:
            message("Используется", font_style, white, (width / 3 + 75, height / 2 + 145))
        else:
            message("Радуга (50)", font_style, white, (width / 3 + 75, height / 2 + 145))

        yin_status = "✅" if yin_unlocked else "❌"
        yang_status = "✅" if yang_unlocked else "❌"
        message(f"Инь: {yin_status}", font_style, white, (width / 3 + 75, height / 2 + 100))
        message(f"Янь: {yang_status}", font_style, white, (width / 3 + 75, height / 2 + 115))

        pygame.draw.rect(screen, yellow_medium, (10, height - 40, 100, 30))
        message("Меню", font_style, black, (60, height - 25))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if width / 3 <= x <= width / 3 + 150:
                    if height / 2 - 120 <= y <= height / 2 - 70:
                        snake_color = dark_green
                    elif height / 2 - 60 <= y <= height / 2 - 10 and score >= 25:
                        yin_unlocked = True
                        snake_color = yin_color
                        score -= 25
                    elif height / 2 <= y <= height / 2 + 50 and score >= 25:
                        yang_unlocked = True
                        snake_color = yang_color
                        score -= 25
                    elif height / 2 + 60 <= y <= height / 2 + 110 and score >= 75 and yin_unlocked and yang_unlocked:
                        snake_color = rainbow
                        score -= 75
                    elif height / 2 + 120 <= y <= height / 2 + 170 and score >= 50:
                        snake_color = rainbow
                        score -= 50
                    else:
                        print("Не хватает очков!")
                        message("Не хватает очков!", font_style, red, (width / 2, height - 60))
                        pygame.display.update()
                        time.sleep(1)
                elif 10 <= x <= 110 and height - 40 <= y <= height - 10:
                    print("Возврат в главное меню.")
                    return


def game_loop():
    global score, snake_color
    print("Игровой цикл запущен.")
    x, y = width / 2, height / 2
    x_change, y_change = 0, 0
    snake_list = []
    length_of_snake = 1
    foodx = round(random.randrange(0, width - block_size) / 10.0) * 10.0
    foody = round(random.randrange(0, height - block_size) / 10.0) * 10.0

    game_over = False
    while not game_over:
        draw_chess_board()
        show_score()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a]:  # Влево
                    x_change = -block_size
                    y_change = 0
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:  # Вправо
                    x_change = block_size
                    y_change = 0
                elif event.key in [pygame.K_UP, pygame.K_w]:  # Вверх
                    y_change = -block_size
                    x_change = 0
                elif event.key in [pygame.K_DOWN, pygame.K_s]:  # Вниз
                    y_change = block_size
                    x_change = 0

        x += x_change
        y += y_change

        if x >= width or x < 0 or y >= height or y < 0:
            return

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                return

        pygame.draw.rect(screen, red, [foodx, foody, block_size, block_size])

        for segment in snake_list:
            color = snake_color if snake_color != rainbow else random.choice(rainbow)
            pygame.draw.rect(screen, color, [segment[0], segment[1], block_size, block_size])

        pygame.display.update()

        if x == foodx and y == foody:
            foodx = round(random.randrange(0, width - block_size) / 10.0) * 10.0
            foody = round(random.randrange(0, height - block_size) / 10.0) * 10.0
            length_of_snake += 1
            score += 1

        time.sleep(0.1)

    pygame.quit()

while True:
    mode = main_menu()
    if mode == "game":
        game_loop()
    elif mode == "shop":
        shop()
