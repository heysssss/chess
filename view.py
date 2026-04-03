# pyright: strict
import pygame
import os

from common_types import Piece

class ChessView:
    def __init__(self, screen: pygame.Surface):
        # variables should be able to be changed from main.py later
        self.width = 600
        self.rows = 8
        self.tile_size = self.width // self.rows

        self.screen = screen
        self.images = self.load_images(self.tile_size)

    def draw(self, board: list[list[Piece | None]], selected: tuple[int, int] | None):
        # draw board
        for row in range(self.rows):
            for col in range(self.rows):
                # alternating colors (chessboard style)
                if (row + col) % 2 == 0:
                    color = (240, 217, 181)  # light
                else:
                    color = (181, 136, 99)   # dark

                # board
                pygame.draw.rect(
                    self.screen,
                    color,
                    (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
                )

        # pieces
        for row in range(self.rows):
            for col in range(self.rows):
                piece = board[row][col]
                if piece is not None:
                    str_piece = piece.str_rep
                    self.screen.blit(
                        self.images[str_piece],
                        (col * self.tile_size, row * self.tile_size)
                    )
    
    # def ask_for_move(self, turn: PieceColor, board: list[list[Piece | None]]) -> tuple[str, str, str | None]:
    #     print()
    #     move = "lmfao xd"
    #     is_valid = False
    #     cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    #     rows = ['1', '2', '3', '4', '5', '6', '7', '8']
    #     promote_pieces = ['R', 'N', 'B', 'Q']
    #     final_move: tuple[str, str, str | None] = "lmao", "lol", None

    #     while not is_valid:
    #         move = input(f"{turn.value}'s Turn [<i> <f> <p>]: ")
    #         split_move = move.split()

    #         if len(split_move) == 2:
    #             is_valid = True

    #             for m in split_move:
    #                 if not len(m) == 2:
    #                     is_valid = False
    #                     break
    #                 if (m[0] not in cols) or (m[1] not in rows):
    #                     is_valid = False
                
    #             final_move = split_move[0], split_move[1], None

    #         elif len(split_move) == 3:
    #             is_valid = True

    #             for i in range(2):
    #                 if not len(split_move[i]) == 2:
    #                     is_valid = False
    #                     break
    #                 if (split_move[i][0] not in cols) or (split_move[i][1] not in rows):
    #                     is_valid = False

    #             if split_move[2] not in promote_pieces:
    #                 is_valid = False

    #             final_move = split_move[0], split_move[1], split_move[2]

    #     # initial, final, promote
    #     return final_move
    
    def load_images(self, tile_size: int) -> dict[str, pygame.Surface]:
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