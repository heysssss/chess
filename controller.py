# pyright: strict
from model import ChessModel
from view import ChessView

class ChessController:
    def __init__(self, model: ChessModel, view: ChessView):
        self._model = model
        self._view = view

    def run(self):
        # checker if board is possible later
        self._model.set_board([['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                                ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
                                ['.', '.', '.', '.', '.', '.', '.', '.'],
                                ['.', '.', '.', '.', '.', '.', '.', '.'],
                                ['.', '.', '.', '.', '.', '.', '.', '.'],
                                ['.', '.', '.', '.', '.', '.', '.', '.'],
                                ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                                ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
                                ])
        while not self._model.is_game_done():
            self._view.display_board(self._model.board)

            cell_from, cell_to, promote = self._view.ask_for_move(self._model.turn, self._model.board)
            while not self._model.move(cell_from, cell_to, promote):
                print("Please input a valid move.")
                cell_from, cell_to, promote = self._view.ask_for_move(self._model.turn, self._model.board)

            self._model.next_turn()
        