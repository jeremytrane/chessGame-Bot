from enum import Enum

class Color(Enum):
    WHITE = 'white'
    BLACK = 'black'

class PieceType(Enum):
    PAWN = 'pawn'
    KNIGHT = 'knight'
    BISHOP = 'bishop'
    ROOK = 'rook'
    QUEEN = 'queen'
    KING = 'king'

class Piece:
    def __init__(self, color: Color, piece_type: PieceType):
        self.color = color
        self.type = piece_type
        self.has_moved = False

    def symbol(self) -> str:
        symbols = {
            PieceType.PAWN: 'P',
            PieceType.KNIGHT: 'N',
            PieceType.BISHOP: 'B',
            PieceType.ROOK: 'R',
            PieceType.QUEEN: 'Q',
            PieceType.KING: 'K',
        }
        symbol = symbols[self.type]
        return symbol if self.color == Color.WHITE else symbol.lower()
