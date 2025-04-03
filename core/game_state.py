from core.piece import Color
from core.move import Move
from core.board import Board

class GameState:
    def __init__(self, board: Board):
        self.board = board
        self.current_turn = Color.WHITE
        self.move_history = []

    def is_game_over(self) -> bool:
        # You can expand this later
        return False

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
        legal_moves = self.get_all_legal_moves()
        # Since move objects may differ by instance, compare from/to coordinates.
        if not any(self._moves_equal(move, legal_move) for legal_move in legal_moves):
            return False, "Illegal move."

        self.board.apply_move(move)
        self.move_history.append(move)
        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
        return True, "ok"

    def _moves_equal(self, m1: Move, m2: Move) -> bool:
        return m1.from_pos == m2.from_pos and m1.to_pos == m2.to_pos

    def get_all_legal_moves(self) -> list[Move]:
        moves = self.board.generate_pseudo_legal_moves(self.current_turn)
        legal_moves = []
        for move in moves:
            self.board.apply_move(move)
            if not self.is_in_check(self.current_turn):
                legal_moves.append(move)
            self.board.undo_move(move)
        return legal_moves

    def is_in_check(self, color: Color) -> bool:
        king_pos = self.board.find_king(color)
        if king_pos is None:
            return True  # King missing; treat as check.
        enemy_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        enemy_moves = self.board.generate_pseudo_legal_moves(enemy_color)
        return any(move.to_pos == king_pos for move in enemy_moves)

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