# pyright: strict
from common_types import PieceColor, Piece, Pawn, Rook, Knight, Bishop, King, Queen

class ChessModel:
    def __init__(self):
        self._turn: PieceColor = PieceColor.WHITE
        self._board: list[list[Piece | None]] = [[None for _ in range(8)] for _ in range(8)]

        # counters
        self._total_turns = 0

    ############
    # property #
    ############

    @property
    def board(self):
        return list(self._board)
    
    @property
    def turn(self):
        return self._turn
    
    ############
    # checkers #
    ############
    
    def legal_moves(self, row: int, col: int) -> set[tuple[int, int]]:
        # returns all legal moves of piece at row, col
        path: dict[tuple[int, int], set[tuple[int, int]]] = {} # path to be taken by piece, does not include start
        possible_moves: set[tuple[int, int]] = set()

        piece = self._board[row][col]
        match piece:
            case None:
                return set()
            case Pawn():
                possible_moves = piece.possible_moves
                special_moves = piece.special_moves
                # forward
                for m in possible_moves:
                    if self.turn == PieceColor.WHITE:
                        poss_path: set[tuple[int, int]] = {(m[0] + 1, m[1])} if not ((m[0] + 1, m[1]) == (row, col)) else set()
                        poss_path.add((m[0], m[1]))
                    else:
                        poss_path: set[tuple[int, int]] = {(m[0] - 1, m[1])} if not ((m[0] - 1, m[1]) == (row, col)) else set()
                        poss_path.add((m[0], m[1]))

                    poss_path = {
                        (pr, pc)
                        for pr, pc in poss_path
                        if 0 <= pr < 8 and 0 <= pc < 8
                    }
                
                    if any(self._board[pr][pc] is not None for pr, pc in poss_path):
                        continue  # skip this move
                    else:
                        path[m] = poss_path  # keep only valid moves

                # diagonal
                for m in special_moves:
                    # cant take own piece
                    if not self.in_bounds(m[0], m[1]):
                        continue

                    to_take = self._board[m[0]][m[1]]
                    if to_take is not None:
                        if to_take.color == self.turn:
                            continue
                        else:
                            poss_path: set[tuple[int, int]] = set()
                            poss_path.add((m[0], m[1]))

                            poss_path = {
                                (pr, pc)
                                for pr, pc in poss_path
                                if 0 <= pr < 8 and 0 <= pc < 8
                            }

                            path[m] = poss_path
                    
                return set(path.keys())
            
            case Rook():
                possible_moves = piece.possible_moves
                # forward
                for m in possible_moves:
                    # cant take own piece
                    if not self.in_bounds(m[0], m[1]):
                        continue

                    to_take = self._board[m[0]][m[1]]
                    if to_take is not None:
                        if to_take.color == self.turn:
                            continue

                    poss_path_row: set[tuple[int, int]] = {(m[0], j)
                                                           for j in range(min(col, m[1]) + 1, max(col, m[1]))
                                                          }
                    poss_path_col: set[tuple[int, int]] = {(i, m[1])
                                                           for i in range(min(row, m[0]) + 1, max(row, m[0])
                                                           )
                                                          }
                    poss_path = poss_path_row | poss_path_col

                    poss_path = {
                        (pr, pc)
                        for pr, pc in poss_path
                        if 0 <= pr < 8 and 0 <= pc < 8
                    }
                
                    if any(self._board[pr][pc] is not None for pr, pc in poss_path):
                        continue  # skip this move
                    else:
                        path[m] = poss_path  # keep only valid moves
                    
                return set(path.keys())
            
            case Knight():
                possible_moves = piece.possible_moves

                for m in possible_moves:
                    # cant take own piece
                    if not self.in_bounds(m[0], m[1]):
                        continue

                    to_take = self._board[m[0]][m[1]]
                    if to_take is not None:
                        if to_take.color == self.turn:
                            continue
                        else:
                            path[m] = set()
                    else:
                        path[m] = set()
                
                return set(path.keys())

            case Bishop():
                possible_moves = piece.possible_moves
                
                for m in possible_moves:
                    poss_path: set[tuple[int, int]] = set()

                    # cant take own piece
                    if not self.in_bounds(m[0], m[1]):
                        continue

                    to_take = self._board[m[0]][m[1]]
                    if to_take is not None:
                        if to_take.color == self.turn:
                            continue

                    # lower right
                    if m[0] > row and m[1] > col:
                        poss_path = {(row + i, col + i)
                                     for i in range(1, max(row, m[0]) - min(row, m[0]))
                                     }
                    # lower left
                    elif m[0] > row and m[1] < col:
                        poss_path = {(row + i, col - i)
                                     for i in range(1, max(row, m[0]) - min(row, m[0]))
                                     }
                    # upper right
                    elif m[0] < row and m[1] > col:
                        poss_path = {(row - i, col + i)
                                     for i in range(1, max(row, m[0]) - min(row, m[0]))
                                     }
                    # upper left
                    else:
                        poss_path = {(row - i, col - i)
                                     for i in range(1, max(row, m[0]) - min(row, m[0]))
                                     }
                        
                    poss_path = {
                        (pr, pc)
                        for pr, pc in poss_path
                        if 0 <= pr < 8 and 0 <= pc < 8
                    }

                    if any(self._board[pr][pc] is not None for pr, pc in poss_path):
                        continue  # skip this move
                    else:
                        path[m] = poss_path  # keep only valid moves
                    
                return set(path.keys())
            
            case King():
                possible_moves = piece.possible_moves
                special_moves = piece.special_moves

                # normal move
                for m in possible_moves:
                    if not self.in_bounds(m[0], m[1]):
                        continue

                    to_take = self._board[m[0]][m[1]]
                    if to_take is not None:
                        if to_take.color == self.turn:
                            continue

                    path[m] = set() 
                
                # castling (can't pass through checks)
                for s in special_moves:
                    # check path of whole castling
                    poss_path_row: set[tuple[int, int]] = {(s[0], j)
                                                           for j in range(min(col, s[1]) + 1, max(col, s[1]))
                                                          }

                    poss_path: set[tuple[int, int]] = set()

                    poss_path = {
                        (pr, pc)
                        for pr, pc in poss_path
                        if 0 <= pr < 8 and 0 <= pc < 8
                    }
                
                    if any(self._board[pr][pc] is not None for pr, pc in poss_path):
                        continue  # skip this move
                    else:
                        path[s] = poss_path  # keep only valid moves
                    
                return set(path.keys())
            
            case Queen():
                possible_moves = piece.possible_moves
                
                for m in possible_moves:
                    # cant take own piece
                    if not self.in_bounds(m[0], m[1]):
                        continue

                    to_take = self._board[m[0]][m[1]]
                    if to_take is not None:
                        if to_take.color == self.turn:
                            continue
                    
                    # rook movement
                    if m[0] == row:
                        poss_path: set[tuple[int, int]] = {(m[0], j)
                                                           for j in range(min(col, m[1]) + 1, max(col, m[1]))
                                                          }
                    elif m[1] == col:
                        poss_path: set[tuple[int, int]] = {(i, m[1])
                                                           for i in range(min(row, m[0]) + 1, max(row, m[0])
                                                           )
                                                          }
                    
                    # diagonals
                    # lower right
                    elif m[0] > row and m[1] > col:
                        poss_path = {(row + i, col + i)
                                     for i in range(1, max(row, m[0]) - min(row, m[0]))
                                     }
                    # lower left
                    elif m[0] > row and m[1] < col:
                        poss_path = {(row + i, col - i)
                                     for i in range(1, max(row, m[0]) - min(row, m[0]))
                                     }
                    # upper right
                    elif m[0] < row and m[1] > col:
                        poss_path = {(row - i, col + i)
                                     for i in range(1, max(row, m[0]) - min(row, m[0]))
                                     }
                    # upper left
                    else:
                        poss_path = {(row - i, col - i)
                                     for i in range(1, max(row, m[0]) - min(row, m[0]))
                                     }
                        
                    poss_path = {
                        (pr, pc)
                        for pr, pc in poss_path
                        if 0 <= pr < 8 and 0 <= pc < 8
                    }

                    if any(self._board[pr][pc] is not None for pr, pc in poss_path):
                        continue  # skip this move
                    else:
                        path[m] = poss_path  # keep only valid moves
                    
                return set(path.keys())
            
            case _:
                print("What piece is this bruh.")
                raise ValueError() 

    def is_under_attack(self, r: int, c: int, board: list[list[Piece | None]]) -> bool:
        # given a board, return true if a square is under attack
        board = [x for x in self._board]
        for i, row in enumerate(board):
            for j, chr in enumerate(row):
                if chr is not None:
                    if (r, c) in self.legal_moves(i, j):
                        return True
        return False
    
    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < 8 and 0 <= c < 8
    
    def locate_king(self, board: list[list[Piece | None]]) -> tuple[int, int]:
        board = [x for x in self._board]
        for i, row in enumerate(board):
            for j, chr in enumerate(row):
                if type(chr) == King:
                    if chr.color == self._turn:
                        return i, j
        
        print("The king is missing.")
        raise ValueError()
    
    def is_in_check(self, board: list[list[Piece | None]]) -> bool:
        # given a board, return true if the king is under attack
        board = [x for x in self._board]
        kr, kc = self.locate_king(board)
        if self.is_under_attack(kr, kc, self._board):
            return True
        return False
    
    def is_stalemated(self) -> bool:
        for i, row in enumerate(self._board):
            for j, _ in enumerate(row):
                if not self.legal_moves(i, j) == set():
                    return False
        return True

    def is_game_done(self) -> bool:
        # winner
        if self.winner():
            return True
        
        # draw
        # stalemate
        if self.is_stalemated():
            return True
        
        # dead position
        # insufficient materials
        # threefold repetition
        # mutual agreement
        # 50 move rule

        # game in progress
        return False     

    def winner(self) -> PieceColor | None:
        ...

    ########
    # move #
    ########

    def move(self, cell_from: str, cell_to: str, promote: str | None) -> bool:
        cf_row, cf_col = self.conv_to_coords(cell_from)
        piece_to_move = self._board[cf_row][cf_col]

        print("legal moves at starting:", self.legal_moves(cf_row, cf_col))

        ct_row, ct_col = self.conv_to_coords(cell_to)
        piece_to_take = self._board[ct_row][ct_col]

        # check cell_from (if has pieces)
        if self._board[cf_row][cf_col] is None:
            print("There is no piece to move in this square.")
            return False
        
        # check cell_to (if has same colored pieces)
        if piece_to_take is not None and piece_to_move is not None:
            if piece_to_take.color == piece_to_move.color:
                print("You can't take your own piece.")
                return False

        # check if piece to move pinned

        # check if path is blocked
        if not (ct_row, ct_col) in self.legal_moves(cf_row, cf_col):
            print("Not a valid move.")
            return False

        # check if valid move of piece
        # check if castle or en passant
        # check if in check
        if self.is_in_check(self.next_move_board((cf_row, cf_col), (ct_row, ct_col), promote)):
            print("This move will result in the elimination of your life. (King will be in check)")
            return False

        # move piece normally and capture and update board
        if piece_to_move is not None:
            piece_to_move.move((ct_row, ct_col))
            self._board[ct_row][ct_col] = piece_to_move
            self._board[cf_row][cf_col] = None

        return True

    def next_turn(self):
        if self._turn == PieceColor.WHITE:
            self._turn = PieceColor.BLACK
        else:
            self._turn = PieceColor.WHITE
        self._total_turns += 1

    ###########
    # helpers #
    ###########

    def next_move_board(self, cell_from: tuple[int, int], cell_to: tuple[int, int], promote: str | None) -> list[list[Piece | None]]:
        mock_board = [x for x in self._board]

        mock_board[cell_to[0]][cell_to[1]] = mock_board[cell_from[0]][cell_from[1]]
        mock_board[cell_from[0]][cell_from[1]] = None

        # en passant and castling not included yet

        return mock_board

    def set_board(self, str_board: list[list[str]]):
        row_list: list[list[Piece | None]] = []
        for i, row in enumerate(str_board):
            chr_list: list[Piece | None] = []
            for j, piece in enumerate(row):
                match piece.lower():
                    case '.':
                        chr_list.append(None)
                    case 'wp':
                        chr_list.append(Pawn(i, j, PieceColor.WHITE))
                    case 'wr':
                        chr_list.append(Rook(i, j, PieceColor.WHITE))
                    case 'wn':
                        chr_list.append(Knight(i, j, PieceColor.WHITE))
                    case 'wb':
                        chr_list.append(Bishop(i, j, PieceColor.WHITE))
                    case 'wk':
                        chr_list.append(King(i, j, PieceColor.WHITE))
                    case 'wq':
                        chr_list.append(Queen(i, j, PieceColor.WHITE))
                    case 'bp':
                        chr_list.append(Pawn(i, j, PieceColor.BLACK))
                    case 'br':
                        chr_list.append(Rook(i, j, PieceColor.BLACK))
                    case 'bn':
                        chr_list.append(Knight(i, j, PieceColor.BLACK))
                    case 'bb':
                        chr_list.append(Bishop(i, j, PieceColor.BLACK))
                    case 'bk':
                        chr_list.append(King(i, j, PieceColor.BLACK))
                    case 'bq':
                        chr_list.append(Queen(i, j, PieceColor.BLACK))
                    case _:
                        raise ValueError()
            row_list.append(chr_list)
        self._board = row_list

    def conv_to_coords(self, str_coords: str) -> tuple[int, int]:
        cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        rows = ['8', '7', '6', '5', '4', '3', '2', '1']

        col = cols.index(str_coords[0])
        row = rows.index(str_coords[1])

        return row, col
