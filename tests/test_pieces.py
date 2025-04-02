# tests/test_pieces.py
from core.piece import Piece, PieceType, Color

def test_piece_symbol():
    p = Piece(Color.WHITE, PieceType.ROOK)
    assert p.symbol() == 'R'
    p2 = Piece(Color.BLACK, PieceType.KNIGHT)
    assert p2.symbol() == 'n'
