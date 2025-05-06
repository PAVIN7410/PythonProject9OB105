import pygame
import random

pygame.init()

# Константы
WIDTH, HEIGHT = 500, 800
CELL_SIZE = 30
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Тетрис')

# Цвета
COLORS = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128),
    (0, 255, 255),
]

# Формы блоков (текущие вращения)
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
]

class Piece:
    def __init__(self, shape):
        self.shape = shape
        self.color = random.randint(1, len(COLORS) - 1)
        self.x = COLS // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def create_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

def check_collision(board, piece, dx=0, dy=0):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = piece.x + x + dx
                new_y = piece.y + y + dy
                if new_x < 0 or new_x >= COLS or new_y >= ROWS or (new_y >= 0 and board[new_y][new_x]):
                    return True
    return False

def lock_piece(board, piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                px = piece.x + x
                py = piece.y + y
                if 0 <= py < ROWS and 0 <= px < COLS:
                    board[py][px] = piece.color

def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = ROWS - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [0 for _ in range(COLS)])
    return new_board, lines_cleared

def draw_board(screen, board):
    for y in range(ROWS):
        for x in range(COLS):
            color = COLORS[board[y][x]]
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (50, 50, 50), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_piece(screen, piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                color = COLORS[piece.color]
                px = (piece.x + x) * CELL_SIZE
                py = (piece.y + y) * CELL_SIZE
                pygame.draw.rect(screen, color, (px, py, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, (50, 50, 50), (px, py, CELL_SIZE, CELL_SIZE), 1)

def main():
    clock = pygame.time.Clock()
    board = create_board()
    current_piece = Piece(random.choice(SHAPES))
    fall_time = 0
    fall_speed = 500  # миллисекунды

    running = True
    while running:
        delta_time = clock.tick(60)
        fall_time += delta_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(board, current_piece, dx=-1):
                        current_piece.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(board, current_piece, dx=1):
                        current_piece.x += 1
                elif event.key == pygame.K_DOWN:
                    if not check_collision(board, current_piece, dy=1):
                        current_piece.y += 1
                elif event.key == pygame.K_UP:
                    original_shape = current_piece.shape
                    current_piece.rotate()
                    if check_collision(board, current_piece):
                        current_piece.shape = original_shape

        if fall_time > fall_speed:
            if not check_collision(board, current_piece, dy=1):
                current_piece.y += 1
            else:
                lock_piece(board, current_piece)
                board, _ = clear_lines(board)
                current_piece = Piece(random.choice(SHAPES))
                if check_collision(board, current_piece):
                    print("Игра окончена!")
                    running = False
            fall_time = 0

        SCREEN.fill((0, 0, 0))
        draw_board(SCREEN, board)
        draw_piece(SCREEN, current_piece)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
