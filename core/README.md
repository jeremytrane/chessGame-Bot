core/ — 🧠 Game Logic Layer
This is where the rules of chess live.

board.py
The central class for the 8x8 board

Holds the grid of squares/pieces

Handles initialization (starting position)

Might include helper methods (e.g. get_piece_at(square), move_piece(from, to))

piece.py
Defines:

Color (White/Black)

PieceType (Pawn, Knight, etc.)

Piece class

Each piece has attributes like color, type, has_moved

move.py
Defines the Move class

Stores:

start_square, end_square

moved_piece, captured_piece

Special flags: castling, promotion, en passant

Used for both making/unmaking moves and for move history

game_state.py
Manages turns, history, legality, and special rules

Tracks:

Current player to move

Castling rights

En passant target square

50-move counter

Repetition history

Exposes methods like:

is_check(), is_checkmate(), generate_legal_moves()

make_move(), undo_move()