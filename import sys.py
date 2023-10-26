import pygame
import random

pygame.init()

screen_width = 640
screen_height = 480
window_size = (screen_width, screen_height)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Two-Player 2048")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

grid_size = 4
tile_size = 100
tile_padding = 20
font_size = 32
score_font_size = 24
score_offset = 10
scoreboard_height = 50

grid = [[0] * grid_size for _ in range(grid_size)]
players = ["Player 1", "Player 2"]
scores = [0, 0]
active_player = 0

def generate_tile():
    tile_value = random.choice([2, 4])
    empty_tiles = [(row, col) for row in range(grid_size) for col in range(grid_size) if grid[row][col] == 0]
    if empty_tiles:
        row, col = random.choice(empty_tiles)
        grid[row][col] = tile_value

def draw_grid():
    for row in range(grid_size):
        for col in range(grid_size):
            tile_value = grid[row][col]
            x = col * (tile_size + tile_padding)
            y = row * (tile_size + tile_padding) + scoreboard_height
            color = WHITE if tile_value == 0 else GRAY
            pygame.draw.rect(window, color, (x, y, tile_size, tile_size))
            if tile_value != 0:
                font = pygame.font.Font(None, font_size)
                text = font.render(str(tile_value), True, BLACK)
                text_rect = text.get_rect(center=(x + tile_size // 2, y + tile_size // 2))
                window.blit(text, text_rect)

def draw_scores():
    font = pygame.font.Font(None, score_font_size)
    for i, player in enumerate(players):
        score_text = f"{player}: {scores[i]}"
        text = font.render(score_text, True, BLACK)
        x = i * (screen_width // 2)
        y = scoreboard_height // 2 - score_offset
        text_rect = text.get_rect(center=(x + screen_width // 4, y))
        window.blit(text, text_rect)

def merge_tiles(row, col, drow, dcol):
    if grid[row][col] == grid[drow][dcol]:
        grid[row][col] *= 2
        grid[drow][dcol] = 0
        scores[active_player] += grid[row][col]

def move_tiles(direction):
    moved = False
    if direction == "up":
        for col in range(grid_size):
            for row in range(1, grid_size):
                if grid[row][col] != 0:
                    for drow in range(row, 0, -1):
                        if grid[drow - 1][col] == 0:
                            grid[drow - 1][col] = grid[drow][col]
                            grid[drow][col] = 0
                            moved = True
                        else:
                            merge_tiles(drow - 1, col, drow, col)
                            break
    elif direction == "down":
        for col in range(grid_size):
            for row in range(grid_size - 2, -1, -1):
                if grid[row][col] != 0:
                    for drow in range(row, grid_size - 1):
                        if grid[drow + 1][col] == 0:
                            grid[drow + 1][col] = grid[drow][col]
                            grid[drow][col] = 0
                            moved = True
                        else:
                            merge_tiles(drow + 1, col, drow, col)
                            break
    elif direction == "left":
        for row in range(grid_size):
            for col in range(1, grid_size):
                if grid[row][col] != 0:
                    for dcol in range(col, 0, -1):
                        if grid[row][dcol - 1] == 0:
                            grid[row][dcol - 1] = grid[row][dcol]
                            grid[row][dcol] = 0
                            moved = True
                        else:
                            merge_tiles(row, dcol - 1, row, dcol)
                            break
    elif direction == "right":
        for row in range(grid_size):
            for col in range(grid_size - 2, -1, -1):
                if grid[row][col] != 0:
                    for dcol in range(col, grid_size - 1):
                        if grid[row][dcol + 1] == 0:
                            grid[row][dcol + 1] = grid[row][dcol]
                            grid[row][dcol] = 0
                            moved = True
                        else:
                            merge_tiles(row, dcol + 1, row, dcol)
                            break
    return moved

def is_game_over():
    for row in range(grid_size):
        for col in range(grid_size):
            if grid[row][col] == 0:
                return False
            if row > 0 and grid[row][col] == grid[row - 1][col]:
                return False
            if col > 0 and grid[row][col] == grid[row][col - 1]:
                return False
    return True

def reset_game():
    for row in range(grid_size):
        for col in range(grid_size):
            grid[row][col] = 0
    scores[0] = 0
    scores[1] = 0
    generate_tile()

generate_tile()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                moved = move_tiles("up")
            elif event.key == pygame.K_DOWN:
                moved = move_tiles("down")
            elif event.key == pygame.K_LEFT:
                moved = move_tiles("left")
            elif event.key == pygame.K_RIGHT:
                moved = move_tiles("right")
            if moved:
                active_player = (active_player + 1) % 2
                generate_tile()
                if is_game_over():
                    reset_game()

    window.fill(BLACK)
    draw_grid()
    draw_scores()
    pygame.display.flip()

pygame.quit()
