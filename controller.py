# pyright: strict
import pygame
import sys

from model import ChessModel
from view import ChessView


class ChessController:
    def __init__(self, model: ChessModel, view: ChessView):
        self._model = model
        self._view = view

        self._selected: tuple[int, int] | None = None
        self._clock = pygame.time.Clock()

    ##################
    # main game loop #
    ##################

    def run(self):
        # initial board
        self._model.set_board([
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bP','bP','bP','bP','bP','bP','bP','bP'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['wP','wP','wP','wP','wP','wP','wP','wP'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR']
        ])

        running = True

        while running:
            # events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click()

            # draw
            self._view.draw(self._model.board, self._selected)

            # update screen
            pygame.display.flip()

            # fps
            self._clock.tick(60)

        pygame.quit()
        sys.exit()

    #################
    # click handler #
    #################

    def handle_click(self):
        x, y = pygame.mouse.get_pos()

        col = x // self._view.tile_size
        row = y // self._view.tile_size

        if self._selected is None:
            piece = self._model.board[row][col]

            if piece is None:
                return

            if piece.color != self._model.turn:
                return

            self._selected = (row, col)
            return

        start = self._selected
        end = (row, col)

        move_from = self.to_notation(start)
        move_to = self.to_notation(end)

        success = self._model.move(move_from, move_to, None)

        if success:
            self._model.next_turn()

        # reset selection regardless
        self._selected = None

    #################
    # helper method #
    #################

    def to_notation(self, pos: tuple[int, int]) -> str:
        row, col = pos

        cols = ['a','b','c','d','e','f','g','h']
        rows = ['8','7','6','5','4','3','2','1']

        return cols[col] + rows[row]