from core.move import Move
from core.piece import PieceType


def move_to_pgn(move: Move) -> str:
    piece = move.piece
    from_row, from_col = move.from_pos
    to_row, to_col = move.to_pos

    cols = "abcdefgh"
    rows = "87654321"

    fr = f"{cols[from_col]}{rows[from_row]}"
    to = f"{cols[to_col]}{rows[to_row]}"

    # Promotion
    if move.promotion:
        to += f"={move.promotion.name[0].upper()}"

    # Piece notation
    if piece.type == PieceType.PAWN:
        if move.captured:
            prefix = cols[from_col]  # e.g., "exd5"
        else:
            prefix = ''
    elif piece.type == PieceType.KNIGHT:
        prefix = "N"
    else:
        prefix = piece.type.name[0].upper()

    capture = "x" if move.captured else ""

    # Special cases (TODO: castling, ambiguity)
    if piece.type == PieceType.KING and abs(from_col - to_col) == 2:
        return "O-O" if to_col == 6 else "O-O-O"

    return f"{prefix}{capture}{to}"
