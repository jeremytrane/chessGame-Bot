class Move:
    def __init__(self, from_pos, to_pos, piece, captured=None, promotion=None):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.piece = piece
        self.captured = captured
        self.promotion = promotion

    def __repr__(self):
        fr = f"{chr(self.from_pos[1] + ord('a'))}{8 - self.from_pos[0]}"
        to = f"{chr(self.to_pos[1] + ord('a'))}{8 - self.to_pos[0]}"
        return f"{fr}{to}"
