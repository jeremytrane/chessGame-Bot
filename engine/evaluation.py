from core.piece import PieceType, Color

# --- Base Piece Values ---
PIECE_VALUES = {
    PieceType.PAWN: 100,
    PieceType.KNIGHT: 320,
    PieceType.BISHOP: 330,
    PieceType.ROOK: 500,
    PieceType.QUEEN: 900,
    PieceType.KING: 0  # King isn't scored directly
}

# --- Piece-Square Table (example: pawns only for now) ---
PAWN_TABLE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

PIECE_SQUARE_TABLES = {
    PieceType.PAWN: PAWN_TABLE
}

# --- Pawn Structure ---
def is_doubled_pawn(board, col, color):
    count = 0
    for row in range(8):
        piece = board.grid[row][col]
        if piece and piece.color == color and piece.type == PieceType.PAWN:
            count += 1
    return count > 1

def is_isolated_pawn(board, row, col, color):
    for dc in [-1, 1]:
        nc = col + dc
        if 0 <= nc < 8:
            for r in range(8):
                piece = board.grid[r][nc]
                if piece and piece.color == color and piece.type == PieceType.PAWN:
                    return False
    return True

def is_passed_pawn(board, row, col, color):
    direction = -1 if color == Color.WHITE else 1
    start = row + direction
    end = -1 if color == Color.BLACK else 8
    step = direction

    for r in range(start, end, step):
        for dc in [-1, 0, 1]:
            c = col + dc
            if 0 <= c < 8:
                p = board.grid[r][c]
                if p and p.color != color and p.type == PieceType.PAWN:
                    return False
    return True

# --- King Safety ---
def king_safety_penalty(board, king_pos, color):
    if not king_pos:
        return 100  # King is missing, shouldn't happen
    row, col = king_pos
    penalty = 0
    shield_row = row + (-1 if color == Color.WHITE else 1)
    if 0 <= shield_row < 8:
        for dc in [-1, 0, 1]:
            c = col + dc
            if 0 <= c < 8:
                piece = board.grid[shield_row][c]
                if not (piece and piece.color == color and piece.type == PieceType.PAWN):
                    penalty += 15
    return penalty

# --- Mobility ---
def mobility_score(game_state, color):
    legal_moves = game_state.get_all_legal_moves(color)
    return len(legal_moves) * 5  # adjust weight if needed

# --- Main Evaluation Function ---
def evaluate_board(game_state):
    board = game_state.board
    score = 0
    white_king_pos = None
    black_king_pos = None

    for row in range(8):
        for col in range(8):
            piece = board.grid[row][col]
            if piece:
                value = PIECE_VALUES[piece.type]

                # Piece-square table bonus
                pst_bonus = 0
                table = PIECE_SQUARE_TABLES.get(piece.type)
                if table:
                    pst_row = row if piece.color == Color.BLACK else 7 - row
                    pst_bonus = table[pst_row][col]

                # Pawn structure
                pawn_bonus = 0
                if piece.type == PieceType.PAWN:
                    if is_doubled_pawn(board, col, piece.color):
                        pawn_bonus -= 15
                    if is_isolated_pawn(board, row, col, piece.color):
                        pawn_bonus -= 10
                    if is_passed_pawn(board, row, col, piece.color):
                        pawn_bonus += 20

                piece_score = value + pst_bonus + pawn_bonus
                score += piece_score if piece.color == Color.WHITE else -piece_score

                # Store king position
                if piece.type == PieceType.KING:
                    if piece.color == Color.WHITE:
                        white_king_pos = (row, col)
                    else:
                        black_king_pos = (row, col)

    # King safety penalty
    if white_king_pos:
        score -= king_safety_penalty(board, white_king_pos, Color.WHITE)
    if black_king_pos:
        score += king_safety_penalty(board, black_king_pos, Color.BLACK)

    # Mobility
    score += mobility_score(game_state, Color.WHITE)
    score -= mobility_score(game_state, Color.BLACK)

    # Normalize: always from perspective of current player
    return score if game_state.current_turn == Color.WHITE else -score
