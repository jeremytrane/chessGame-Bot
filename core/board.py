from .piece import Piece, PieceType, Color

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_position()

    def setup_position(self):
        for col in range(8):
            self.grid[1][col] = Piece(Color.BLACK, PieceType.PAWN)
            self.grid[6][col] = Piece(Color.WHITE, PieceType.PAWN)

        placement = [
            PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP,
            PieceType.QUEEN, PieceType.KING, PieceType.BISHOP,
            PieceType.KNIGHT, PieceType.ROOK
        ]

        for col, piece_type in enumerate(placement):
            self.grid[0][col] = Piece(Color.BLACK, piece_type)
            self.grid[7][col] = Piece(Color.WHITE, piece_type)

    def get_piece_at(self, pos: tuple[int, int]):
        row, col = pos
        return self.grid[row][col]

    def apply_move(self, move):
        fr, to = move.from_pos, move.to_pos
        piece = move.piece
        self.grid[to[0]][to[1]] = piece
        self.grid[fr[0]][fr[1]] = None
        piece.has_moved = True
