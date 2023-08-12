### TETRIS GAME ###


### LIBRARIES

import pygame
import random
import numpy as np


### GRID

GRID = np.zeros((20, 10), dtype=int)


### SHAPES

SHAPES = [
    np.array([[1, 1, 1, 1]]),
    np.array([[1, 1], [1, 1]]),
    np.array([[1, 1, 0], [0, 1, 1]]),
    np.array([[0, 1, 1], [1, 1, 0]]),
    np.array([[1, 1, 1], [0, 1, 0]]),
    np.array([[1, 1, 1], [1, 0, 0]]),
    np.array([[1, 1, 1], [0, 0, 1]])
]


### COLORS

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 155, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 128, 0)

COLORS = [CYAN, YELLOW, GREEN, RED, PURPLE, ORANGE, BLUE]


### TETRIS GAME

class TetrisGame:

    def __init__(self, width, height):
        
        self.width = width
        self.height = height
        
        self.n = random.randint(0, len(SHAPES)-1)
        self.shape = SHAPES[self.n]
        self.color = COLORS[self.n]
        
        self.next_n = random.randint(0, len(SHAPES)-1)
        self.next_shape = SHAPES[self.next_n]
        self.next_color = COLORS[self.next_n]
        
        self.held_n = None
        self.held_shape = None
        self.held_color = None

        self.x = 4
        self.y = 0
        
        self.score = 0
        self.lines = 0
        self.game_over = False

    def draw(self, surface):
        for i in range(20):
            for j in range(10):
                if GRID[i][j] != 0:
                    pygame.draw.rect(surface, COLORS[GRID[i][j]-1], (j*30, i*30, 30, 30))
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j] != 0:
                    pygame.draw.rect(surface, self.color, ((self.x+j)*30, (self.y+i)*30, 30, 30))

    def draw_grid(self, surface):
        for i in range(20):
            pygame.draw.line(surface, (128, 128, 128), (0, i*30), (300, i*30))
        for j in range(10):
            pygame.draw.line(surface, (128, 128, 128), (j*30, 0), (j*30, 600))

    def move(self, dx):
        if not self.collision(self.shape, self.x+dx, self.y):
            self.x += dx

    def rotate(self):
        self.shape = np.rot90(self.shape)

    def fall(self):
        if not self.collision(self.shape, self.x, self.y+1):
            self.y += 1
        else:
            self.place()
    
    def collision(self, shape, x, y):
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j] == 1:
                    if x+j < 0 or x+j > 9 or y+i > 19 or GRID[y+i][x+j] != 0:
                        return True
            # Game over
            if y+i > 19:
                self.game_over = True
        return False

    def place(self):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j] == 1:
                    GRID[self.y+i][self.x+j] = self.n+1
        self.check_lines()
        self.new_shape()

    def check_lines(self):
        for i in range(len(GRID)):
            if 0 not in GRID[i]:
                self.score += 100
                self.lines += 1
                for j in range(i, 0, -1):
                    GRID[j] = GRID[j-1]
                GRID[0] = [0 for i in range(10)]

    def new_shape(self):
        self.shape = self.next_shape
        self.color = self.next_color
        self.n = self.next_n
        self.x = 4
        self.y = 0
        self.next_n = random.randint(0, len(SHAPES)-1)
        self.next_shape = SHAPES[self.next_n]
        self.next_color = COLORS[self.next_n]
        if self.collision(self.shape, self.x, self.y):
            self.game_over = True

    def get_score(self):
        return self.score

    def get_game_over(self):
        return self.game_over
    
    def hold(self):
        if self.held_n is None:
            self.held_n = self.n
            self.held_shape = self.shape
            self.held_color = self.color
            self.new_shape()
        else:
            temp_n = self.n
            temp_shape = self.shape
            temp_color = self.color
            self.n = self.held_n
            self.shape = self.held_shape
            self.color = self.held_color
            self.held_n = temp_n
            self.held_shape = temp_shape
            self.held_color = temp_color
    

### MAIN

def main():

    pygame.init()
    pygame.display.set_caption("Tetris Game")

    screen = pygame.display.set_mode((500, 600))
    surface = pygame.Surface((300, 600))    # 300x600 subscreen for the game at 0,0
    next_surface = pygame.Surface((200, 200))   # 300x300 subscreen for the next shape at 300,0
    held_surface = pygame.Surface((200, 200))   # 300x300 subscreen for the piece held at 300,200
    score_surface = pygame.Surface((200, 200))  # 300x300 subscreen for the score at 300,400

    # add subscreens to the main screen
    screen.blit(surface, (0, 0))
    screen.blit(next_surface, (300, 0))
    screen.blit(held_surface, (300, 200))
    screen.blit(score_surface, (300, 400))

    surface.fill(BLACK)

    clock = pygame.time.Clock()
    
    game = TetrisGame(10, 20)
    last_fall_time = pygame.time.get_ticks()

    FALL_TIME = 1

    while game.game_over == False:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.game_over = True
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1)
                    if game.collision(game.shape, game.x, game.y):
                        game.move(1)
                if event.key == pygame.K_RIGHT:
                    game.move(1)
                    if game.collision(game.shape, game.x, game.y):
                        game.move(-1)
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    game.fall()
                if event.key == pygame.K_SPACE:
                    game.hold()
                    game.y = 0

        surface.fill((0, 0, 0))

        # Make the piece fall according to the FALL_TIME
        if pygame.time.get_ticks() - last_fall_time > FALL_TIME * 1000:
            game.fall()
            last_fall_time = pygame.time.get_ticks()

        # When the lines are multiple of 10, update the FALL_TIME
        if game.lines % 10 == 0 and game.lines != 0:
            FALL_TIME *= 0.6
            
        # Update the game
        game.draw(surface)
        game.draw_grid(surface)

        # Update the held shape
        held_surface.fill((0, 0, 0))
        held_text = pygame.font.SysFont('Arial', 30).render("Held shape:", True, (255, 255, 255))
        held_surface.blit(held_text, (10, 10))

        # Draw the held shape
        if game.held_n is not None:
            for i in range(len(game.held_shape)):
                for j in range(len(game.held_shape[0])):
                    if game.held_shape[i][j] == 1:
                        pygame.draw.rect(held_surface, game.held_color, (50 + j * 30, 80 + i * 30, 30, 30), 0)

        # Update the score
        score_surface.fill((0, 0, 0))
        score_text = pygame.font.SysFont('Arial', 30).render("Score: " + str(game.get_score()), True, (255, 255, 255))
        score_text2 = pygame.font.SysFont('Arial', 30).render("Lines: " + str(game.lines), True, (255, 255, 255))
        score_surface.blit(score_text, (10, 10))
        score_surface.blit(score_text2, (10, 50))
        screen.blit(score_surface, (300, 300))

        # Update the next shape
        next_surface.fill((0, 0, 0))
        next_text = pygame.font.SysFont('Arial', 30).render("Next shape:", True, (255, 255, 255))
        next_surface.blit(next_text, (10, 10))

        # Draw the next shape
        for i in range(len(game.next_shape)):
            for j in range(len(game.next_shape[0])):
                if game.next_shape[i][j] == 1:
                    pygame.draw.rect(next_surface, game.next_color, (j*30+50, i*30+80, 30, 30))

        # Draw the subscreens
        screen.blit(surface, (0, 0))
        screen.blit(next_surface, (300, 0))
        screen.blit(held_surface, (300, 200))
        screen.blit(score_surface, (300, 400))

        pygame.display.update()


if __name__ == "__main__":
    main()