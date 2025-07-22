import pypearl
import sys, random
import pygame
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.direction = Vector2(-1, 0)
        self.new_block = False
    def draw_snake(self):
        for block in self.body:
            snake_rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, (45, 64, 215), snake_rect)
    def move_snake(self):
        if not self.new_block:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0]+self.direction)
            self.body = body_copy[:]
        else:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0]+self.direction)
            self.body = body_copy[:]
            self.new_block = False

    def add_block(self):
        self.new_block = True

class FRUIT:
    def __init__(self):
        # create an x and y position
        # draw a square
        self.x = random.randint(0, cell_number-1)
        self.y = random.randint(0, cell_number-1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x*cell_size), int(self.pos.y*cell_size),cell_size, cell_size)
        pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self):
        self.pos.x = random.randint(0, cell_number-1)
        self.pos.y = random.randint(0, cell_number-1)
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
    def check_fail(self):
        if not 0 <= self.snake.body[0].x <= cell_number-1 or not 0 <= self.snake.body[0].y <= cell_number-1:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    def game_over(self):
        pygame.quit()
        sys.exit()

pygame.init()

cell_size = 40
cell_number = 20
dims = cell_size*cell_number
screen = pygame.display.set_mode((dims, dims))
clock = pygame.time.Clock()


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                main_game.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN:
                main_game.snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_RIGHT:
                main_game.snake.direction = Vector2(1, 0)
            elif event.key == pygame.K_LEFT:
                main_game.snake.direction = Vector2(-1, 0)
    screen.fill((175, 215, 70))
    main_game.draw()
    pygame.display.update()
    clock.tick(120)