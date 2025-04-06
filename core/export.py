from core.move import Move


def move_to_pgn(move: Move) -> str:
    cols = "abcdefgh"
    rows = "87654321"

    from_row, from_col = move.from_pos
    to_row, to_col = move.to_pos

    # Promotion
    promo = f"={move.promotion.name[0].upper()}" if move.promotion else ""

    # Castling
    if move.piece.type.name == "KING" and abs(from_col - to_col) == 2:
        return "O-O" if to_col == 6 else "O-O-O"

    # PGN piece symbols
    piece_symbols = {
        "KING": "K",
        "QUEEN": "Q",
        "ROOK": "R",
        "BISHOP": "B",
        "KNIGHT": "N",
        "PAWN": ""
    }

    symbol = piece_symbols[move.piece.type.name]

    # Pawn captures (e.g., exd5)
    if move.piece.type.name == "PAWN" and move.captured:
        symbol = cols[from_col]

    capture = "x" if move.captured else ""
    dest = f"{cols[to_col]}{rows[to_row]}"

    return f"{symbol}{capture}{dest}{promo}"
