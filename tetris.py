import os
os.environ["SDL_AUDIODRIVER"] = "dummy"  # Disable audio driver

import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
GRID_WIDTH = WIDTH // BLOCK_SIZE
GRID_HEIGHT = HEIGHT // BLOCK_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
BLUE = (0, 0, 255)
COLORS = [
    (255, 0, 0),   # Red
    (0, 255, 0),   # Green
    (0, 0, 255),   # Blue
    (255, 255, 0), # Yellow
    (0, 255, 255), # Cyan
    (255, 0, 255)  # Magenta
]

# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],                   # I
    [[1, 1], [1, 1]],                 # O
    [[0, 1, 0], [1, 1, 1]],           # T
    [[1, 1, 0], [0, 1, 1]],           # S
    [[0, 1, 1], [1, 1, 0]],           # Z
    [[1, 0, 0], [1, 1, 1]],           # L
    [[0, 0, 1], [1, 1, 1]]            # J
]

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Clock
clock = pygame.time.Clock()
FPS = 10

# Functions to rotate shapes
def rotate_clockwise(shape):
    return [list(row) for row in zip(*shape[::-1])]

# Draw the grid
def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

# Draw the board and tetrimino
def draw_board(board, tetrimino, offset):
    screen.fill(BLACK)
    draw_grid()
    
    # Draw existing blocks on the board
    for y, row in enumerate(board):
        for x, value in enumerate(row):
            if value:
                pygame.draw.rect(
                    screen,
                    value,
                    (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                )
    
    # Draw the current tetrimino
    if tetrimino:
        shape, color = tetrimino
        for y, row in enumerate(shape):
            for x, value in enumerate(row):
                if value:
                    pygame.draw.rect(
                        screen,
                        color,
                        ((x + offset[0]) * BLOCK_SIZE, (y + offset[1]) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    )

# Display the start screen with a play button
def start_screen():
    while True:
        screen.fill(BLACK)
        button_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2 - 25, WIDTH // 2, 50)
        pygame.draw.rect(screen, BLUE, button_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  # Exit the start screen and begin the game

# Check if a position is valid
def valid_position(board, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, value in enumerate(row):
            if value:
                if x + off_x < 0 or x + off_x >= GRID_WIDTH or y + off_y >= GRID_HEIGHT:
                    return False
                if y + off_y >= 0 and board[y + off_y][x + off_x]:
                    return False
    return True

# Merge tetrimino into the board
def merge_board(board, shape, offset, color):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, value in enumerate(row):
            if value:
                board[y + off_y][x + off_x] = color

# Clear full rows
def clear_rows(board):
    full_rows = [row for row in board if all(row)]
    cleared = len(full_rows)
    board[:] = [[0] * GRID_WIDTH] * cleared + [row for row in board if not all(row)]
    return cleared

# Main game function
def main():
    board = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    running = True
    current_shape = random.choice(SHAPES)
    current_color = random.choice(COLORS)
    tetrimino = (current_shape, current_color)
    offset = [GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0]
    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # Move left
                    new_offset = [offset[0] - 1, offset[1]]
                    if valid_position(board, current_shape, new_offset):
                        offset = new_offset
                elif event.key == pygame.K_RIGHT:  # Move right
                    new_offset = [offset[0] + 1, offset[1]]
                    if valid_position(board, current_shape, new_offset):
                        offset = new_offset
                elif event.key == pygame.K_UP:  # Rotate clockwise
                    new_shape = rotate_clockwise(current_shape)
                    if valid_position(board, new_shape, offset):
                        current_shape = new_shape

        # Move down automatically
        new_offset = [offset[0], offset[1] + 1]
        if valid_position(board, current_shape, new_offset):
            offset = new_offset
        else:
            merge_board(board, current_shape, offset, current_color)
            score += clear_rows(board)
            current_shape = random.choice(SHAPES)
            current_color = random.choice(COLORS)
            tetrimino = (current_shape, current_color)
            offset = [GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0]
            if not valid_position(board, current_shape, offset):
                print("Game Over! Your score:", score)
                running = False

        # Draw everything
        draw_board(board, tetrimino, offset)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    start_screen()
    main()
