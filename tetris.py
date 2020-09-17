from typing import NewType
import pygame
import random

from pygame.event import clear

pygame.init()

# Screen variables
S_WIDTH = 800
S_HEIGHT = 750

# Play window variables
PLAY_WIDTH = 300
PLAY_HEIGHT = 600 
BLOCK_SIZE = 30 # 300 / 10, 600 / 20

# Top left corner of play window
TOP_LEFT_X = (S_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = S_HEIGHT - PLAY_HEIGHT - 50

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

def convert_shape_format(shape):
    """ Convert the shape string into actual rotations and positons """
    positions = []

    # Current shape format based on rotation
    format = shape.shape[shape.rotation % len(shape.shape)] 

    # For every string line
    for i, line in enumerate(format):
        row = list(line)
        # For every element in row
        for j, column in enumerate(row):
            # If it's a zero, then it's a shape cell
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    # For every shape position
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4) # Offsetting the position because of the string

    return positions

def valid_space(shape, grid):
    """ If the space is free (valid) """

    # What positions are valid
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == BLACK] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub] # Flattens the list

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1: # If it's above the screen
                return False

    return True

def check_lost(positions):
    """ If the shape is at the top of the screen """
    for pos in positions:
        x, y = pos

        if y < 1:
            return True

    return False

def clear_row(grid, locked):
    """ Clears a filled row """
    inc = 0 
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if BLACK not in row: # if the row is filled 
            inc += 1 # How many rows to shift
            ind = i
            for j in range(len(row)): # For every position in a row
                try:
                    del locked[(j, i)] # Delete the position
                except:
                    continue
    
    # If a row is cleared
    if inc > 0:
        # For a key in a list sorted by the y value
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)

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

def draw_next_shape(shape, surface):
    """ Draws the upcoming shape at the side of the screen """
    font = pygame.font.SysFont('Arial', 30)
    label = font.render("Next shape", 1, WHITE)

    st_x = TOP_LEFT_X + PLAY_WIDTH + 50
    st_y = TOP_LEFT_Y + PLAY_HEIGHT // 2 - 100

    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (st_x + j * BLOCK_SIZE, st_y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    surface.blit(label, (st_x, st_y - 20))

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
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH // 2 - (label.get_width() // 2), 20))
    
    # Drawing the rectangles in the grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (TOP_LEFT_X + j * 30, TOP_LEFT_Y + i * 30, BLOCK_SIZE, BLOCK_SIZE), 0)

    # Drawing the border rectangle
    pygame.draw.rect(surface, RED, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 4)

    # Draws the grid
    draw_grid(surface, grid)

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
    fall_speed = 0.27

    # Running variables
    run = True
    clock = pygame.time.Clock()

    while run:
        # Grid needs to be updated
        grid = create_grid(locked_position)

        # Speed of the program
        fall_time += clock.get_rawtime() 
        clock.tick()

        if fall_time // 1000 > fall_speed:
            fall_time = 0
            current_shape.y += 1 # Moving the shape

            if not(valid_space(current_shape, grid)) and current_shape.y > 0:
                current_shape.y -= 1
                change_shape = True # Locking the grid

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_shape.x -= 1
                    if not(valid_space(current_shape, grid)):
                        current_shape.x += 1
                if event.key == pygame.K_RIGHT:
                    current_shape.x += 1
                    if not(valid_space(current_shape, grid)):
                        current_shape.x -= 1
                if event.key == pygame.K_DOWN:
                    current_shape.y += 1
                    if not(valid_space(current_shape, grid)):
                        current_shape.y -= 1
                if event.key == pygame.K_UP:
                    current_shape.rotation += 1
                    if not(valid_space(current_shape, grid)):
                        current_shape.rotation -= 1

        shape_pos = convert_shape_format(current_shape)

        # Drawing the shape colors
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_shape.color

        if change_shape:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_position[p] = current_shape.color # Locking the position

            current_shape = next_shape
            next_shape = get_shape()
            change_shape = False
            clear_row(grid, locked_position)

        draw_window(win, grid)
        draw_next_shape(next_shape, win)

        # Updating the display
        pygame.display.update()

        if check_lost(locked_position):
            run = False
    
    pygame.display.quit()

def main_menu(win):
    main(win)

win = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
pygame.display.set_caption("Tetris")

main_menu(win)
