import pygame
import random
import sys
from pygame.locals import *

FPS = 7
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
CELL_SIZE = 40
assert WINDOW_WIDTH % CELL_SIZE == 0, "Window width must be a multiple of " \
                                      "cell size. "
assert WINDOW_HEIGHT % CELL_SIZE == 0, "Window height must be a multiple of " \
                                       "cell size. "
CELL_WIDTH = int(WINDOW_WIDTH / CELL_SIZE)
CELL_HEIGHT = int(WINDOW_HEIGHT / CELL_SIZE)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (0, 250, 154)
DARK_GREEN = (0, 155, 0)
GREY = (169, 169, 169)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0


def main():
    global FPS_CLOCK, DISPLAY_SURF, BASIC_FONT

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')
    show_message('START', 'GAME')

    while True:
        runGame()
        show_message('GAME', 'OVER')


def get_direction(event, direction):
    if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
        return LEFT
    elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
        return RIGHT
    elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
        return UP
    elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
        return DOWN
    elif event.key == K_ESCAPE:
        terminate()


def get_new_head(direction, coordinates):
    if direction == UP:
        return {'x': coordinates[HEAD]['x'],
                'y': coordinates[HEAD]['y'] - 1}
    elif direction == DOWN:
        return {'x': coordinates[HEAD]['x'],
                'y': coordinates[HEAD]['y'] + 1}
    elif direction == LEFT:
        return {'x': coordinates[HEAD]['x'] - 1,
                'y': coordinates[HEAD]['y']}
    elif direction == RIGHT:
        return {'x': coordinates[HEAD]['x'] + 1,
                'y': coordinates[HEAD]['y']}


def check_game_over(coordinates):
    if coordinates[HEAD]['x'] == -1 or \
            coordinates[HEAD]['x'] == CELL_WIDTH or \
            coordinates[HEAD]['y'] == -1 or \
            coordinates[HEAD]['y'] == CELL_HEIGHT:
        return True

    if coordinates[HEAD] in coordinates[1:]:
        return True

    return False


def runGame():
    start_x = random.randint(5, CELL_WIDTH - 6)
    start_y = random.randint(5, CELL_HEIGHT - 6)
    coordinates = [{'x': start_x, 'y': start_y},
                   {'x': start_x - 1, 'y': start_y},
                   {'x': start_x - 2, 'y': start_y}]
    direction = RIGHT

    apple = get_random_location()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                direction = get_direction(event, direction)

        if direction is None:
            return

        if check_game_over(coordinates):
            return

        if coordinates[HEAD] == apple:
            while apple in coordinates:
                apple = get_random_location()
        else:
            del coordinates[-1]

        new_head = get_new_head(direction, coordinates)
        coordinates.insert(0, new_head)
        DISPLAY_SURF.fill(BLACK)
        draw_worm(coordinates)
        draw_apple(apple)
        draw_score(len(coordinates) - 3)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def draw_press_key_message():
    press_key_surf = BASIC_FONT.render('Press a key to play.', True, GREY)
    press_key_rect = press_key_surf.get_rect()
    press_key_rect.topleft = (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 30)
    DISPLAY_SURF.blit(press_key_surf, press_key_rect)


def check_for_key_press():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    key_up_events = pygame.event.get(KEYUP)
    if len(key_up_events) == 0:
        return None
    if key_up_events[0].key == K_ESCAPE:
        terminate()
    return key_up_events[0].key


def terminate():
    pygame.quit()
    sys.exit()


def get_random_location():
    return {'x': random.randint(0, CELL_WIDTH - 1),
            'y': random.randint(0, CELL_HEIGHT - 1)}


def show_message(first_word, second_word):
    message_font = pygame.font.Font('freesansbold.ttf', 150)
    first_surf = message_font.render(first_word, True, WHITE)
    second_surf = message_font.render(second_word, True, WHITE)
    first_rect = first_surf.get_rect()
    second_rect = second_surf.get_rect()
    first_rect.midtop = (WINDOW_WIDTH / 2, 10)
    second_rect.midtop = (WINDOW_WIDTH / 2, first_rect.height + 10 + 25)

    DISPLAY_SURF.blit(first_surf, first_rect)
    DISPLAY_SURF.blit(second_surf, second_rect)
    draw_press_key_message()
    pygame.display.update()
    pygame.time.wait(500)
    check_for_key_press()

    while True:
        if check_for_key_press():
            pygame.event.get()
            return


def draw_score(score):
    score_surf = BASIC_FONT.render(f'Score: {score}', True, WHITE)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (WINDOW_WIDTH - 120, 10)
    DISPLAY_SURF.blit(score_surf, score_rect)


def draw_worm(coordinates):
    for coord in coordinates:
        x = coord['x'] * CELL_SIZE
        y = coord['y'] * CELL_SIZE
        worm_segment_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(DISPLAY_SURF, DARK_GREEN, worm_segment_rect)
        worm_inner_segment_rect = pygame.Rect(x + 4, y + 4, CELL_SIZE - 8,
                                              CELL_SIZE - 8)
        pygame.draw.rect(DISPLAY_SURF, GREEN, worm_inner_segment_rect)


def draw_apple(coord):
    x = coord['x'] * CELL_SIZE
    y = coord['y'] * CELL_SIZE
    apple_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(DISPLAY_SURF, RED, apple_rect)


if __name__ == '__main__':
    main()
