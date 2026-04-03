# pyright: strict
import pygame
import os
import sys
from model import ChessModel 

# initialize pygame
pygame.init()

# window size
WIDTH = 600
ROWS = 8
TILE_SIZE = WIDTH // ROWS

screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Chess")

clock = pygame.time.Clock()

def load_images(tile_size: int) -> dict[str, pygame.Surface]:
    pieces: dict[str, pygame.Surface] = {}

    names = [
        "wp","wr","wn","wb","wq","wk",
        "bp","br","bn","bb","bq","bk"
    ]

    for name in names:
        path = os.path.join("assets", "images", f"{name}.png")
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (tile_size, tile_size))
        pieces[name] = img

    return pieces

IMAGES = load_images(TILE_SIZE)

board = [
    ["br","bn","bb","bq","bk","bb","bn","br"],
    ["bp","bp","bp","bp","bp","bp","bp","bp"],
    [None]*8,
    [None]*8,
    [None]*8,
    [None]*8,
    ["wp","wp","wp","wp","wp","wp","wp","wp"],
    ["wr","wn","wb","wq","wk","wb","wn","wr"],
]

selected = None
selected_2 = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            
            x, y = pygame.mouse.get_pos()

            col = x // TILE_SIZE
            row = y // TILE_SIZE

            if selected == (row, col):
                selected = None
                selected_2 = None
            elif selected == None:
                selected = (row, col)
                selected_2 = None
            else:
                if selected_2 == (row, col):
                    selected_2 = None
                else:
                    selected_2 = (row, col)

    # draw board
    for row in range(ROWS):
        for col in range(ROWS):
            # alternating colors (chessboard style)
            if (row + col) % 2 == 0:
                color = (240, 217, 181)  # light
            else:
                color = (181, 136, 99)   # dark

            # board
            pygame.draw.rect(
                screen,
                color,
                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )

    # pieces
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                screen.blit(
                    IMAGES[piece],
                    (col * TILE_SIZE, row * TILE_SIZE)
                )
    
    if selected:
        r, c = selected
        pygame.draw.rect(
            screen,
            (0, 255, 0),  # green
            (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE),
            3  # border thickness
        )

    if selected_2:
        r, c = selected_2
        pygame.draw.rect(
            screen,
            (0, 0, 255),  # blue
            (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE),
            3  # border thickness
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()