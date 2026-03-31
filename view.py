# pyright: strict
from common_types import PieceColor, Piece, Pawn, Knight, Bishop, Rook, King, Queen

class ChessView:
    def display_board(self, board: list[list[Piece | None]]):
        print()
        for row in board:
            chr_list: list[str] = []
            for chr in row:
                match chr:
                    case None:
                        chr_list.append('  ')
                    case Pawn():
                        if chr.color == PieceColor.WHITE:
                            chr_list.append('wP')
                        else:
                            chr_list.append('bP')
                    case Rook():
                        if chr.color == PieceColor.WHITE:
                            chr_list.append('wR')
                        else:
                            chr_list.append('bR')
                    case Knight():
                        if chr.color == PieceColor.WHITE:
                            chr_list.append('wN')
                        else:
                            chr_list.append('bN')
                    case Bishop():
                        if chr.color == PieceColor.WHITE:
                            chr_list.append('wB')
                        else:
                            chr_list.append('bB')
                    case King():
                        if chr.color == PieceColor.WHITE:
                            chr_list.append('wK')
                        else:
                            chr_list.append('bK')
                    case Queen():
                        if chr.color == PieceColor.WHITE:
                            chr_list.append('wQ')
                        else:
                            chr_list.append('bQ')
                    case _:
                        raise ValueError()
            print(' '.join(chr_list))
    
    def ask_for_move(self, turn: PieceColor, board: list[list[Piece | None]]) -> tuple[str, str, str | None]:
        print()
        move = "lmfao xd"
        is_valid = False
        cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        rows = ['1', '2', '3', '4', '5', '6', '7', '8']
        promote_pieces = ['R', 'N', 'B', 'Q']
        final_move: tuple[str, str, str | None] = "lmao", "lol", None

        while not is_valid:
            move = input(f"{turn.value}'s Turn [<i> <f> <p>]: ")
            split_move = move.split()

            if len(split_move) == 2:
                is_valid = True

                for m in split_move:
                    if not len(m) == 2:
                        is_valid = False
                        break
                    if (m[0] not in cols) or (m[1] not in rows):
                        is_valid = False
                
                final_move = split_move[0], split_move[1], None

            elif len(split_move) == 3:
                is_valid = True

                for i in range(2):
                    if not len(split_move[i]) == 2:
                        is_valid = False
                        break
                    if (split_move[i][0] not in cols) or (split_move[i][1] not in rows):
                        is_valid = False

                if split_move[2] not in promote_pieces:
                    is_valid = False

                final_move = split_move[0], split_move[1], split_move[2]

        # initial, final, promote
        return final_move