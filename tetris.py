import pygame
import random

from pygame.event import get

pygame.init()

# Screen variables
S_WIDTH = 800
S_HEIGHT = 700

# Play window variables
PLAY_WIDTH = 300
PLAY_HEIGHT = 600 
BLOCK_SIZE = 30 # 300 / 10, 600 / 20

# Top left corner of play window
TOP_LEFT_X = (S_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = S_HEIGHT - PLAY_HEIGHT

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Shapes
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# Possible shape combinations
shapes = [S, Z, I, O, J, L, T]
shape_colors = [GREEN, RED, CYAN, YELLOW, ORANGE, BLUE, PURPLE]

class Shape():
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_pos={}):
    """ Initializes a grid which contains a color value """
    grid = [[BLACK for _ in range(10)] for _ in range(20)]

    # If a shape is already locked on the grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c

    return grid

def draw_grid(surface, grid):
    """ Draws the grid """

    # Start positions
    st_x = TOP_LEFT_X
    st_y = TOP_LEFT_Y

    for i in range(len(grid)):
        pygame.draw.line(surface, GRAY, (st_x, st_y + i * BLOCK_SIZE), (st_x + PLAY_WIDTH, st_y + i * BLOCK_SIZE))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, GRAY, (st_x + j * BLOCK_SIZE, st_y) , (st_x + j * BLOCK_SIZE, st_y + PLAY_HEIGHT))

def draw_window(surface, grid):
    """ Draws the window """
    surface.fill(BLACK)

    # Title
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 60)
    label = font.render("Tetris", 1, WHITE)

    # Drawing the font
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2), 20))
    
    # Drawing the rectangles in the grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (TOP_LEFT_X + j * 30, TOP_LEFT_Y + i * 30, BLOCK_SIZE, BLOCK_SIZE), 0)

    # Drawing the border rectangle
    pygame.draw.rect(surface, RED, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 4)

    draw_grid(surface, grid)

    # Updating display
    pygame.display.update()

def get_shape():
    """ Returns a random shape """
    return Shape(5, 0, random.choice(shapes))

def main(win):
    """ The main function """
    locked_position = {}

    # Creating the grid
    grid = create_grid(locked_position)

    # Game variables
    change_shape = False
    current_shape = get_shape()
    next_shape = get_shape()
    fall_time = 0

    # Running variables
    run = True
    clock = pygame.time.Clock

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_shape.x -= 1
                    if not(valid_space(current_shape, grid)):
                        current_shape += 1
                if event.key == pygame.K_RIGHT:
                    current_shape.x += 1
                    if not(valid_space(current_shape, grid)):
                        current_shape -= 1
                if event.key == pygame.K_DOWN:
                    current_shape += 1
                    if not(valid_space(current_shape, grid)):
                        current_shape -= 1
                if event.key == pygame.K_UP:
                    current_shape.rotation += 1
                    if not(valid_space(current_shape, grid)):
                        current_shape -= 1

        draw_window(win, grid)

def main_menu(win):
    main(win)

win = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
pygame.display.set_caption("Tetris")

main_menu(win)
