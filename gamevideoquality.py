from pypearl import Model, ArrayD1, breed_models, copy_model
import sys, random
import pygame
from pygame.math import Vector2
from pathlib import Path
import csv

CSV_PATH = Path(__file__).with_name("frames.csv")


genspath = Path(__file__).with_name("generations.csv")
def load_single_value(path: Path) -> int:
    text = path.read_text(encoding="utf-8").strip()
    try:
        return int(text)
    except ValueError as exc:
        raise ValueError(f"{path} does not contain a single number") from exc

def write_single_int_to_csv(path: str | Path, value: int) -> None:
    with open(path, mode="w", newline="") as f:
        csv.writer(f).writerow([value])

def top_k_indices(seq, k=5):
    ranking = sorted(enumerate(seq), key=lambda p: p[1], reverse=True)[:k]

    return {rank + 1: idx for rank, (idx, _) in enumerate(ranking)}

input_size = 10
gen_size_const = 20
lives_const = 3
death_const = 40

frames = load_single_value(CSV_PATH)
class Generator:
    def __init__(self, gen_size):
        self.gen_size = gen_size
        self.scores = ArrayD1(gen_size)
        self.models = []

        self.gens = load_single_value(genspath)
        self.scores = []
        self.cur = 0
        for i in range(gen_size):
            m = Model()
            m.add_layer(10, 32)
            m.add_relu()
            m.add_layer(32, 32)
            m.add_relu()
            m.add_layer(32, 4)
            m.add_softmax()
            self.models.append(m)
        if self.gens >0:
            self.models[0].load_model(f"generation{self.gens:07d}/model{1}")
            self.models[1].load_model(f"generation{self.gens:07d}/model{2}")
            self.models[2].load_model(f"generation{self.gens:07d}/model{3}")
            self.models[3].load_model(f"generation{self.gens:07d}/model{4}")
            self.models[4].load_model(f"generation{self.gens:07d}/model{5}")

            self.gens+=1
        self.curmodel = self.models[0]

    def endEpisode(self, curFrames, apples):

        self.cur += 1
        s = curFrames + apples*20
        self.scores.append(s)
        if self.cur == self.gen_size:
            self.endGeneration()
        self.curmodel = self.models[self.cur]

    def endGeneration(self):
        self.cur = 0
        top = top_k_indices(self.scores)
        newmodels = []
        print(self.scores)
        print(max(self.scores))
        print(sum(self.scores))
        if max(self.scores)>3000:
            self.models[self.scores.index(max(self.scores))].save_model(f"/Users/brody/PycharmProjects/Snake/3000club/model{self.gens:07d}")
        if max(self.scores)>4000:
            self.models[self.scores.index(max(self.scores))].save_model(f"/Users/brody/PycharmProjects/Snake/4000club/model{self.gens:07d}")
        if max(self.scores)>10000:
            self.models[self.scores.index(max(self.scores))].save_model(f"/Users/brody/PycharmProjects/Snake/10000club/model{self.gens:07d}")
        if max(self.scores)>20000:
            self.models[self.scores.index(max(self.scores))].save_model(f"/Users/brody/PycharmProjects/Snake/20000club/model{self.gens:07d}")
        if max(self.scores)>50000:
            self.models[self.scores.index(max(self.scores))].save_model(f"/Users/brody/PycharmProjects/Snake/50000club/model{self.gens:07d}")

        if self.gens%20 == 0:
            base_dir = Path("/Users/brody/PycharmProjects/Snake")
            gen_dir = base_dir / f"generation{self.gens:07d}"
            gen_dir.mkdir(parents=True, exist_ok=True)

            write_single_int_to_csv(genspath, self.gens)
            write_single_int_to_csv(CSV_PATH, frames)
            for key, val in top.items():

                self.models[val].save_model(f"/Users/brody/PycharmProjects/Snake/generation{self.gens:07d}/model{key}")
        for key, val in top.items():
            newmodels.append(self.models[val])

            rmod = copy_model(self.models[val])
            rmod.randomize(0.05)
            newmodels.append(rmod)

        for i in range(5):
            for j in range(i, 5):
                if j != i:
                    newmodels.append(breed_models(self.models[i], self.models[j], 0.5))

        self.models = newmodels
        self.gens+=1

        self.scores = []

    def act(self, X, main):
        output = self.curmodel.forwardGA(X)
        max = 0
        index = 0
        for i in range(4):
            if output[i] > max:
                index = i
                max = output[i]
        if index == 0:
            main.snake.direction = Vector2(0, -1)
        elif index == 1:
            main.snake.direction = Vector2(0, 1)
        elif index == 2:
            main.snake.direction = Vector2(1, 0)
        elif index == 3:
            main.snake.direction = Vector2(-1, 0)
        for i in range(4):
            if i == index:
                X[i] = 1
            else:
                X[i] = 0



class SNAKE:
    def __init__(self):
        self.body = [Vector2(10, 10), Vector2(11, 10), Vector2(12, 10)]
        self.direction = Vector2(-1, 0)
        self.new_block = False

        # --- heads -------------------------------------------------
        self.head_up = pygame.image.load("Graphics/head_up.png").convert_alpha()
        self.head_down = pygame.image.load("Graphics/head_down.png").convert_alpha()
        self.head_left = pygame.image.load("Graphics/head_left.png").convert_alpha()
        self.head_right = pygame.image.load("Graphics/head_right.png").convert_alpha()

        # --- tails -------------------------------------------------
        self.tail_up = pygame.image.load("Graphics/tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("Graphics/tail_down.png").convert_alpha()
        self.tail_left = pygame.image.load("Graphics/tail_left.png").convert_alpha()
        self.tail_right = pygame.image.load("Graphics/tail_right.png").convert_alpha()

        # --- body segments ----------------------------------------
        self.body_vertical = pygame.image.load("Graphics/body_vertical.png").convert_alpha()
        self.body_horizontal = pygame.image.load("Graphics/body_horizontal.png").convert_alpha()
        self.body_tl = pygame.image.load("Graphics/body_tl.png").convert_alpha()
        self.body_tr = pygame.image.load("Graphics/body_tr.png").convert_alpha()
        self.body_bl = pygame.image.load("Graphics/body_bl.png").convert_alpha()
        self.body_br = pygame.image.load("Graphics/body_br.png").convert_alpha()

    def draw_snake(self):
        for i, block in enumerate(self.body):
            if i == 0:
                snake_rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
                #pygame.draw.rect(screen, (45, 64, 215), snake_rect)
                if block.y < self.body[i+1].y:
                    screen.blit(self.head_up, snake_rect)
                elif block.y > self.body[i+1].y:
                    screen.blit(self.head_down, snake_rect)
                elif block.x < self.body[i + 1].x:
                    screen.blit(self.head_left, snake_rect)
                elif block.x > self.body[i + 1].x:
                    screen.blit(self.head_right, snake_rect)
            elif i == len(self.body)-1:
                snake_rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
                if block.y < self.body[i-1].y:
                    screen.blit(self.tail_up, snake_rect)
                elif block.y > self.body[i-1].y:
                    screen.blit(self.tail_down, snake_rect)
                elif block.x < self.body[i - 1].x:
                    screen.blit(self.tail_left, snake_rect)
                elif block.x > self.body[i - 1].x:
                    screen.blit(self.tail_right, snake_rect)
            else:
                snake_rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
                xd = self.body[i-1].x-self.body[i+1].x
                xf = self.body[i-1].x - block.x
                xb = self.body[i+1].x - block.x
                yd = self.body[i-1].y-self.body[i+1].y
                yf = self.body[i-1].y - block.y
                yb = self.body[i+1].y - block.y

                if xd == 0:
                    screen.blit(self.body_vertical, snake_rect)
                if yd == 0:
                    screen.blit(self.body_horizontal, snake_rect)
                if (xf > 0 and yb > 0) or (xb > 0 and yf > 0):
                    screen.blit(self.body_br, snake_rect)
                if (xf < 0 and yb > 0) or (xb < 0 and yf > 0):
                    screen.blit(self.body_bl, snake_rect)
                if (xf < 0 and yb < 0) or (xb < 0 and yf < 0):
                    screen.blit(self.body_tl, snake_rect)
                if (xf > 0 and yb < 0) or (xb > 0 and yf < 0):
                    screen.blit(self.body_tr, snake_rect)




    def move_snake(self):
        #if not self.new_block:
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0]+self.direction)
        self.body = body_copy[:]
        '''else:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0]+self.direction)
            self.body = body_copy[:]
            self.new_block = False
            '''
    def add_block(self):
        self.new_block = True
    def respawn(self, X):
        i = random.randint(-3, 4)
        j = random.randint(-3, 4)
        index= random.randint(0, 4)
        if index == 0:
            self.direction = Vector2(0, -1)
        elif index == 1:
            self.direction = Vector2(0, 1)
        elif index == 2:
            self.direction = Vector2(1, 0)
        else:
            self.direction = Vector2(-1, 0)
        for i in range(4):
            if i == index:
                X[i] = 1
            else:
                X[i] = 0

        self.body = [Vector2(10+i, 10+j), Vector2(10+i, 10+j)-self.direction, Vector2(10+i, 10+j)-2*self.direction]



class FRUIT:
    def __init__(self):
        # create an x and y position
        # draw a square
        self.x = random.randint(0, cell_number-1)
        self.y = random.randint(0, cell_number-1)
        self.pos = Vector2(self.x, self.y)


    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x*cell_size), int(self.pos.y*cell_size),cell_size, cell_size)
        #pygame.draw.rect(screen, (215, 48, 68), fruit_rect)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.pos.x = random.randint(0, cell_number-1)
        self.pos.y = random.randint(0, cell_number-1)
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.lives = lives_const
        self.curFrames = 0
        self.curApples = 0
        self.deathcount = death_const

    def update(self, gen, X):
        self.curFrames +=1
        self.deathcount -= 1
        self.snake.move_snake()
        self.check_collision()
        self.check_fail(gen, X)


    def draw(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def draw_grass(self):
        grass_color = (150, 200, 40)
        for col in range(cell_number):
            for row in range(cell_number):
                if (col+row)%2 == 0:
                    grass_rect = pygame.Rect(col*cell_size,row*cell_size,cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.curApples += 1
            self.deathcount=death_const
    def check_fail(self, gen, X):
        if not 0 <= self.snake.body[0].x <= cell_number-1 or not 0 <= self.snake.body[0].y <= cell_number-1:
            self.game_over(gen, X)
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over(gen, X)
        if self.deathcount == 0:
            self.deathcount = death_const
            self.game_over(gen, X)
    def game_over(self, gen, X):
        self.lives -= 1
        if self.lives == 0:
            gen.endEpisode(self.curFrames, self.curApples)
            self.lives = lives_const
            self.curFrames = 0
            self.curApples = 0
        self.snake.respawn(X)
        self.fruit.randomize()


ais = Generator(gen_size_const)

pygame.init()

cell_size = 40
cell_number = 20
dims = cell_size*cell_number
screen = pygame.display.set_mode((dims, dims))
clock = pygame.time.Clock()


SCREEN_UPDATE = pygame.USEREVENT
#pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()
gen = Generator(gen_size_const)
X = ArrayD1(input_size)
X[3] = 1
apple = pygame.image.load("Graphics/apple.png").convert_alpha()



while True:
    frames += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #if event.type == SCREEN_UPDATE:
    main_game.update(gen, X)
    X[6] = (main_game.snake.body[0].y) / 20
    X[7] = (20 - main_game.snake.body[0].y) / 20
    X[8] = (main_game.snake.body[0].x) / 20
    X[9] = (20 - main_game.snake.body[0].x) / 20

    dist = main_game.fruit.pos - main_game.snake.body[0]

    X[4] = dist.x / (abs(dist.x)+abs(dist.y)+1)
    X[5] = dist.y / (abs(dist.x)+abs(dist.y)+1)
    #print(X[4])
    #print(X[5])
    gen.act(X, main_game)
    screen.fill((175, 215, 70))
    main_game.draw()
    pygame.display.update()
    clock.tick(5)

    #1000000