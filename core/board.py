from core.piece import Piece, PieceType, Color
from core.move import Move

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_position()

    def setup_position(self):
        # Set up pawns
        for col in range(8):
            self.grid[1][col] = Piece(Color.BLACK, PieceType.PAWN)
            self.grid[6][col] = Piece(Color.WHITE, PieceType.PAWN)

        # Back rank setup
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

    def apply_move(self, move: Move):
        fr, to = move.from_pos, move.to_pos
        piece = move.piece

        self.grid[to[0]][to[1]] = piece
        self.grid[fr[0]][fr[1]] = None

        # 🏰 Handle castling rook movement
        if piece.type == PieceType.KING and abs(to[1] - fr[1]) == 2:
            row = fr[0]
            if to[1] == 6:  # Kingside
                self.grid[row][5] = self.grid[row][7]
                self.grid[row][7] = None
                self.grid[row][5].has_moved = True
            elif to[1] == 2:  # Queenside
                self.grid[row][3] = self.grid[row][0]
                self.grid[row][0] = None
                self.grid[row][3].has_moved = True

        piece.has_moved = True

    def undo_move(self, move: Move):
        from_row, from_col = move.from_pos
        to_row, to_col = move.to_pos
        # Move the piece back and restore captured piece
        self.grid[from_row][from_col] = move.piece
        self.grid[to_row][to_col] = move.captured
        # Reset the piece’s moved flag (for our simple undo)
        move.piece.has_moved = False

    def generate_pseudo_legal_moves(self, color: Color) -> list[Move]:
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color == color:
                    moves += self.generate_piece_moves((row, col), piece)
        return moves

    def generate_piece_moves(self, pos: tuple[int, int], piece: Piece) -> list[Move]:
        if piece.type == PieceType.PAWN:
            return self._pawn_moves(pos, piece, en_passant_target=self.en_passant_target)
        if piece.type == PieceType.PAWN:
            return self._pawn_moves(pos, piece)
        elif piece.type == PieceType.KNIGHT:
            return self._knight_moves(pos, piece)
        elif piece.type == PieceType.BISHOP:
            return self._sliding_moves(pos, piece, directions=[(1,1), (-1,-1), (1,-1), (-1,1)])
        elif piece.type == PieceType.ROOK:
            return self._sliding_moves(pos, piece, directions=[(0,1), (0,-1), (1,0), (-1,0)])
        elif piece.type == PieceType.QUEEN:
            return self._sliding_moves(pos, piece, directions=[
                (1,1), (-1,-1), (1,-1), (-1,1), (0,1), (0,-1), (1,0), (-1,0)
            ])
        elif piece.type == PieceType.KING:
            return self._king_moves(pos, piece)
        return []

    def _pawn_moves(self, pos, piece: Piece, en_passant_target=None) -> list[Move]:
        moves = []
        row, col = pos
        direction = -1 if piece.color == Color.WHITE else 1
        start_row = 6 if piece.color == Color.WHITE else 1

        # Standard forward moves
        next_row = row + direction
        if 0 <= next_row < 8 and self.grid[next_row][col] is None:
            moves.append(Move(pos, (next_row, col), piece))
            if row == start_row and self.grid[row + 2 * direction][col] is None:
                moves.append(Move(pos, (row + 2 * direction, col), piece))

        # Captures
        for dc in [-1, 1]:
            target_col = col + dc
            target_row = row + direction
            if 0 <= target_col < 8 and 0 <= target_row < 8:
                target_piece = self.grid[target_row][target_col]
                if target_piece and target_piece.color != piece.color:
                    moves.append(Move(pos, (target_row, target_col), piece, captured=target_piece))

        # 🔥 En Passant
        if en_passant_target:
            ep_row, ep_col = en_passant_target
            if row == (3 if piece.color == Color.WHITE else 4) and abs(col - ep_col) == 1:
                if ep_row == row + direction and ep_col == col + (1 if ep_col > col else -1):
                    captured_pawn_pos = (row, ep_col)
                    captured_piece = self.grid[captured_pawn_pos[0]][captured_pawn_pos[1]]
                    if captured_piece and captured_piece.type == PieceType.PAWN and captured_piece.color != piece.color:
                        moves.append(Move(
                            pos,
                            (ep_row, ep_col),
                            piece,
                            captured=captured_piece,
                            captured_pos=captured_pawn_pos
                        ))

        return moves

    def _knight_moves(self, pos: tuple[int, int], piece: Piece) -> list[Move]:
        moves = []
        row, col = pos
        knight_offsets = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]
        for dr, dc in knight_offsets:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.grid[new_row][new_col]
                if target is None or target.color != piece.color:
                    moves.append(Move((row, col), (new_row, new_col), piece, captured=target))
        return moves

    def _sliding_moves(self, pos: tuple[int, int], piece: Piece, directions: list[tuple[int, int]]) -> list[Move]:
        moves = []
        row, col = pos
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.grid[new_row][new_col]
                if target is None:
                    moves.append(Move((row, col), (new_row, new_col), piece))
                elif target.color != piece.color:
                    moves.append(Move((row, col), (new_row, new_col), piece, captured=target))
                    break
                else:
                    break
                new_row += dr
                new_col += dc
        return moves

    def _king_moves(self, pos: tuple[int, int], piece: Piece) -> list[Move]:
        moves = []
        row, col = pos
        king_offsets = [
            (1, 0), (1, 1), (0, 1), (-1, 1),
            (-1, 0), (-1, -1), (0, -1), (1, -1)
        ]
        for dr, dc in king_offsets:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.grid[new_row][new_col]
                if target is None or target.color != piece.color:
                    moves.append(Move(pos, (new_row, new_col), piece, captured=target))

        # 🏰 Castling (simplified - assumes legality checked via filtering)
        if not piece.has_moved and (row, col) == (7, 4) or (row, col) == (0, 4):
            # Kingside
            if self._can_castle_kingside(piece.color):
                moves.append(Move(pos, (row, 6), piece))  # e1 → g1 or e8 → g8
            # Queenside
            if self._can_castle_queenside(piece.color):
                moves.append(Move(pos, (row, 2), piece))  # e1 → c1 or e8 → c8
        return moves

    def find_king(self, color: Color) -> tuple[int, int] | None:
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.type == PieceType.KING and piece.color == color:
                    return (row, col)
        return None

    def _can_castle_kingside(self, color: Color) -> bool:
        row = 7 if color == Color.WHITE else 0
        king = self.grid[row][4]
        rook = self.grid[row][7]

        if not rook or rook.type != PieceType.ROOK or rook.color != color or rook.has_moved:
            return False
        if self.grid[row][5] or self.grid[row][6]:  # f1/g1 or f8/g8
            return False
        return not self._squares_under_attack(color, [(row, 4), (row, 5), (row, 6)])

    def _can_castle_queenside(self, color: Color) -> bool:
        row = 7 if color == Color.WHITE else 0
        king = self.grid[row][4]
        rook = self.grid[row][0]

        if not rook or rook.type != PieceType.ROOK or rook.color != color or rook.has_moved:
            return False
        if self.grid[row][1] or self.grid[row][2] or self.grid[row][3]:  # b1/c1/d1 or b8/c8/d8
            return False
        return not self._squares_under_attack(color, [(row, 4), (row, 3), (row, 2)])

    def _squares_under_attack(self, color: Color, squares: list[tuple[int, int]]) -> bool:
        enemy_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        enemy_moves = self.generate_pseudo_legal_moves(enemy_color)
        attacked = set(move.to_pos for move in enemy_moves)
        return any(square in attacked for square in squares)
