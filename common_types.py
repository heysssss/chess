# pyright: strict

from enum import Enum
from abc import ABC, abstractmethod

class PieceColor(Enum):
    BLACK = 'Black'
    WHITE = 'White'

class Piece(ABC):
    def __init__(self, row: int, col: int, color: PieceColor):
        self._moves = 0 # how many times the piece has moved
        self._position: tuple[int, int] = row, col
        self._color: PieceColor = color

    @property
    def moves(self):
        return self._moves
    
    @property
    def row(self):
        return self._position[0]
    
    @property
    def col(self):
        return self._position[1]
    
    @property
    def color(self):
        return self._color

    # @abstractmethod
    # @property
    # def str_rep(self) -> str:
    #     ...

    @property
    @abstractmethod
    def possible_moves(self) -> set[tuple[int, int]]:
        ...

    @property
    @abstractmethod
    def special_moves(self) -> set[tuple[int, int]]:
        ...

    # @abstractmethod
    # @property
    # def get_row(self) -> str:
    #     rows_dict = {0: "8", 1: "7", 2: "6", 3: "5", 4: "4", 5: "3", 6: "2", 7: "1"}
    #     return rows_dict[self._row]
    
    # @abstractmethod
    # @property
    # def get_col(self) -> str:
    #     cols_dict = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
    #     return cols_dict[self._col]
    
    # @abstractmethod
    # def set_position(self, position: tuple[int, int]):
    #     self._position = position

    # @abstractmethod
    # def set_color(self, color: PieceColor):
    #     self._color = color
    
    def move(self, target: tuple[int, int]):
        self._position = target
        self._moves += 1


class Pawn(Piece):
    @property
    def possible_moves(self) -> set[tuple[int, int]]:
        poss_moves: set[tuple[int, int]] = set()

        poss_moves = set((i, j) for i in range(8) 
                      for j in range(8)
                      if ((self.color == PieceColor.WHITE) and ((j == self.col and (self.row - i == 1)) or ((j == self.col and (self.row - i == 2)) and self.moves == 0))) or
                      ((self.color == PieceColor.BLACK) and ((j == self.col and (i -self.row == 1)) or ((j == self.col and (i - self.row == 2)) and self.moves == 0)))
                    )

        return poss_moves
    
    @property
    def special_moves(self) -> set[tuple[int, int]]:
        # check in model if en passant or can take
        poss_moves: set[tuple[int, int]] = set()

        poss_moves = set((i, j) for i in range(8) 
                      for j in range(8)
                      if ((self.color == PieceColor.WHITE) and ((abs(self.col - j) == 1) and (self.row - i == 1))) or
                      ((self.color == PieceColor.BLACK) and ((abs(self.col - j) == 1) and (i - self.row == 1)))
                    )   

        return poss_moves


class Rook(Piece):
    @property
    def possible_moves(self) -> set[tuple[int, int]]:
        poss_moves: set[tuple[int, int]] = set()

        poss_moves = set((i, j) 
                      for i in range(8) 
                      for j in range(8) 
                      if not ((i == self.row) and (j == self.col)) and
                      (i == self.row or j == self.col)
                    )

        return poss_moves

    @property
    def special_moves(self) -> set[tuple[int, int]]:
        # no special move
        ...

class Knight(Piece):
    @property
    def possible_moves(self) -> set[tuple[int, int]]:
        poss_moves: set[tuple[int, int]] = set()

        poss_moves = set((i, j) 
                      for i in range(8) 
                      for j in range(8) 
                      if not ((i == self.row) and (j == self.col)) and
                      ((abs(self.row - i) == 1 and abs(self.col - j) == 2) or 
                       (abs(self.row - i) == 2 and abs(self.col - j) == 1))
                    )

        return poss_moves

    @property
    def special_moves(self) -> set[tuple[int, int]]:
        # no special move
        ...

class Bishop(Piece):
    @property
    def possible_moves(self) -> set[tuple[int, int]]:
        poss_moves: set[tuple[int, int]] = set()

        poss_moves = set((i, j) 
                      for i in range(8) 
                      for j in range(8) 
                      if not ((i == self.row) and (j == self.col)) and
                      (abs(i - self.row) == abs(j - self.col))
                    )

        return poss_moves

    @property
    def special_moves(self) -> set[tuple[int, int]]:
        # no special move
        ...

class King(Piece):
    @property
    def possible_moves(self) -> set[tuple[int, int]]:
        poss_moves: set[tuple[int, int]] = set()

        poss_moves = set((i, j) 
                      for i in range(8) 
                      for j in range(8) 
                      if not ((i == self.row) and (j == self.col)) and
                      ((abs(i - self.row) == abs(j - self.col) == 1) or 
                       (abs(i - self.row) + abs(j - self.col) == 1))
                    )

        return poss_moves

    @property
    def special_moves(self) -> set[tuple[int, int]]:
        poss_moves: set[tuple[int, int]] = set()
        if self.moves == 0:
            # castling (check also if rooks first move in model)
            poss_moves.add((self.row, self.col + 2))
            poss_moves.add((self.row, self.col - 2))
        return poss_moves

class Queen(Piece):
    @property
    def possible_moves(self) -> set[tuple[int, int]]:
        poss_moves: set[tuple[int, int]] = set()

        poss_moves = set((i, j) 
                      for i in range(8) 
                      for j in range(8) 
                      if not ((i == self.row) and (j == self.col)) and
                      ((i == self.row or j == self.col) or 
                       (abs(i - self.row) == abs(j - self.col)))
                    )

        return poss_moves
    
    @property
    def special_moves(self) -> set[tuple[int, int]]:
        # no special move
        ...
    

    

