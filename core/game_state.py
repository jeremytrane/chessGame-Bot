from core.piece import Color
from core.move import Move
from core.board import Board

class GameState:
    def __init__(self, board: Board):
        self.board = board
        self.current_turn = Color.WHITE
        self.move_history = []

    def is_game_over(self) -> bool:
        return False  # Full implementation in later phases
    
    def print_move_history(self):
        print("Move history:")
        for i, move in enumerate(self.move_history):
            print(f"{i + 1}. {move}")
    
    def is_valid_input_format(self, move_str: str) -> bool:
        return len(move_str) == 4 and all(c.isalnum() for c in move_str)

    def parse_move(self, move_str: str) -> Move | None:
        try:
            from_square = self.algebraic_to_coords(move_str[:2])
            to_square = self.algebraic_to_coords(move_str[2:4])
            piece = self.board.get_piece_at(from_square)

            if not piece or piece.color != self.current_turn:
                return None

            target = self.board.get_piece_at(to_square)
            return Move(from_square, to_square, piece, captured=target)

        except Exception as e:
            print(f"Error parsing move: {e}")
            return None

    def make_move(self, move: Move) -> tuple[bool, str]:
        if not self.is_move_legal(move):
            return False, "Illegal move."

        self.board.apply_move(move)
        self.move_history.append(move)
        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
        return True, "ok"

    def is_move_legal(self, move: Move) -> bool:
        # For Phase 1, accept all inputs as legal
        return True

    def algebraic_to_coords(self, notation: str) -> tuple[int, int]:
        col = ord(notation[0]) - ord('a')
        row = 8 - int(notation[1])
        return (row, col)
    
    def undo_last_move(self):
        if not self.move_history:
            return False

        last_move = self.move_history.pop()
        self.board.undo_move(last_move)
        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
        return True