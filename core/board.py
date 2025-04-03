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
        # Save captured piece in the move (if any)
        move.captured = self.get_piece_at(to)
        self.grid[to[0]][to[1]] = piece
        self.grid[fr[0]][fr[1]] = None
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

    def _pawn_moves(self, pos: tuple[int, int], piece: Piece) -> list[Move]:
        moves = []
        row, col = pos
        # White pawns move upward (-1 row); Black pawns move downward (+1 row)
        direction = -1 if piece.color == Color.WHITE else 1
        start_row = 6 if piece.color == Color.WHITE else 1

        # Single square forward
        new_row = row + direction
        if 0 <= new_row < 8 and self.grid[new_row][col] is None:
            moves.append(Move((row, col), (new_row, col), piece))
            # Double square forward on the pawn's first move
            if row == start_row:
                new_row2 = row + 2 * direction
                if self.grid[new_row2][col] is None:
                    moves.append(Move((row, col), (new_row2, col), piece))
        # Diagonal captures
        for new_col in [col - 1, col + 1]:
            if 0 <= new_col < 8 and 0 <= new_row < 8:
                target = self.grid[new_row][new_col]
                if target and target.color != piece.color:
                    moves.append(Move((row, col), (new_row, new_col), piece, captured=target))
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
                    moves.append(Move((row, col), (new_row, new_col), piece, captured=target))
        return moves

    def find_king(self, color: Color) -> tuple[int, int] | None:
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.type == PieceType.KING and piece.color == color:
                    return (row, col)
        return None
