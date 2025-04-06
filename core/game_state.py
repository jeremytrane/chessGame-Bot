from core.piece import Color, PieceType
from core.move import Move
from core.board import Board

class GameState:
    def __init__(self, board: Board):
        self.board = board
        self.current_turn = Color.WHITE
        self.move_history = []
        self.en_passant_target = None  # e.g., (3, 4) after e2e4
        self.halfmove_clock = 0
        self.position_history = {}
        self.move_history = []
        self.redo_stack = []  # 🔁 for redo support

    def is_game_over(self) -> bool:
        # 50-move rule
        if self.halfmove_clock >= 100:
            print("Draw by 50-move rule.")
            return True

        # Threefold repetition
        for pos, count in self.position_history.items():
            if count >= 3:
                print("Draw by threefold repetition.")
                return True

        legal_moves = self.get_all_legal_moves()
        if legal_moves:
            return False  # Game continues

        if self.is_in_check(self.current_turn):
            print(f"Checkmate! {self.current_turn.name} is checkmated.")
        else:
            print("Stalemate!")

        return True

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
        self.board.en_passant_target = self.en_passant_target
        legal_moves = self.get_all_legal_moves()
        if not any(self._moves_equal(move, legal_move) for legal_move in legal_moves):
            return False, "Illegal move."

        self.en_passant_target = None

        # Reset or increment 50-move clock
        if move.piece.type == PieceType.PAWN:
            self.halfmove_clock = 0

            # En passant target
            r1, _ = move.from_pos
            r2, _ = move.to_pos
            if abs(r2 - r1) == 2:
                row = (r1 + r2) // 2
                col = move.from_pos[1]
                self.en_passant_target = (row, col)

            # Detect promotion
            promotion_row = 0 if move.piece.color == Color.WHITE else 7
            if r2 == promotion_row:
                from ui.cli import ask_promotion_choice
                choice = ask_promotion_choice()
                move.promotion = {
                    'q': PieceType.QUEEN,
                    'r': PieceType.ROOK,
                    'b': PieceType.BISHOP,
                    'n': PieceType.KNIGHT
                }.get(choice, PieceType.QUEEN)  # Default to queen

        elif move.captured:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        self.board.apply_move(move)
        self.move_history.append(move)
        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE

        # Track repetition state
        key = self._position_key()
        self.position_history[key] = self.position_history.get(key, 0) + 1
        self.redo_stack.clear()  # Any new move invalidates future redos

        return True, "ok"
    
    def _position_key(self) -> str:
        def piece_repr(piece):
            if piece is None:
                return "."
            symbol = piece.type.name[0]
            return symbol.upper() if piece.color == Color.WHITE else symbol.lower()

        rows = []
        for row in self.board.grid:
            rows.append(''.join(piece_repr(p) for p in row))

        board_str = '/'.join(rows)
        turn_str = self.current_turn.name
        ep_str = f"{self.en_passant_target}" if self.en_passant_target else "-"
        return f"{board_str} {turn_str} {ep_str}"

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

    def undo_last_move(self) -> bool:
        if not self.move_history:
            return False

        last_move = self.move_history.pop()
        self.board.undo_move(last_move)
        self.redo_stack.append(last_move)  # 🔁 Save for redo

        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
        return True

    def redo_last_move(self) -> bool:
        if not self.redo_stack:
            return False

        move = self.redo_stack.pop()
        self.board.apply_move(move)
        self.move_history.append(move)

        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
        return True

    def print_move_history(self):
        print("\nMove History:")
        for i, move in enumerate(self.move_history):
            move_num = i // 2 + 1
            prefix = f"{move_num}. " if i % 2 == 0 else ""
            print(f"{prefix}{move}", end=' ' if i % 2 == 0 else '\n')
        print()
