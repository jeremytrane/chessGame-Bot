class Move:
    def __init__(self, from_pos, to_pos, piece, captured=None, promotion=None, captured_pos=None, castling=False):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.piece = piece
        self.captured = captured
        self.promotion = promotion
        self.captured_pos = captured_pos if captured_pos else to_pos
        self.castling = castling

    def __repr__(self):
        fr = f"{chr(self.from_pos[1] + ord('a'))}{8 - self.from_pos[0]}"
        to = f"{chr(self.to_pos[1] + ord('a'))}{8 - self.to_pos[0]}"
        return f"{fr}{to}"
