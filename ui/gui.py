
import pygame
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.board import Board
from core.game_state import GameState
from core.piece import Color
from engine.bot import choose_best_move_iterative

# === CONFIG ===
WIDTH, HEIGHT = 512, 512
SQ_SIZE = WIDTH // 8
HIGHLIGHT_COLOR = (0, 255, 0, 100)
FPS = 60

# Load piece images
IMAGES = {}
def load_images():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for p in pieces:
        IMAGES[p] = pygame.transform.scale(pygame.image.load(f"../assets/{p}.png"), (SQ_SIZE, SQ_SIZE))

def piece_to_code(piece):
    color = 'w' if piece.color == Color.WHITE else 'b'
    return f"{color}{piece.type.name[0]}"

def draw_board(screen, board, selected_square=None, legal_moves=[]):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(8):
        for c in range(8):
            color = colors[(r + c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # Highlight selected square and legal moves
    if selected_square:
        s_row, s_col = selected_square
        highlight = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
        highlight.fill(HIGHLIGHT_COLOR)
        screen.blit(highlight, (s_col * SQ_SIZE, s_row * SQ_SIZE))
        for move in legal_moves:
            t_row, t_col = move.to_pos
            screen.blit(highlight, (t_col * SQ_SIZE, t_row * SQ_SIZE))

    # Draw pieces
    for r in range(8):
        for c in range(8):
            piece = board.grid[r][c]
            if piece:
                code = piece_to_code(piece)
                screen.blit(IMAGES[code], pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_clocks(screen, game, font):
    white = game.clocks[Color.WHITE]
    black = game.clocks[Color.BLACK]
    text_w = font.render(f"White: {white:.1f}s", True, (0, 0, 0))
    text_b = font.render(f"Black: {black:.1f}s", True, (0, 0, 0))
    screen.blit(text_w, (10, HEIGHT + 5))
    screen.blit(text_b, (WIDTH - 150, HEIGHT + 5))

def animate_move(screen, board, move):
    from_row, from_col = move.from_pos
    to_row, to_col = move.to_pos
    piece = move.piece
    frames = 10
    for i in range(frames):
        progress = i / frames
        x = from_col * (1 - progress) + to_col * progress
        y = from_row * (1 - progress) + to_row * progress
        draw_board(screen, board)
        screen.blit(IMAGES[piece_to_code(piece)], (x * SQ_SIZE, y * SQ_SIZE))
        pygame.display.flip()
        pygame.time.delay(20)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + 40))
    pygame.display.set_caption("Chess GUI")
    clock = pygame.time.Clock()
    load_images()
    font = pygame.font.SysFont("Arial", 20)

    game = GameState(Board())
    game.clocks = {Color.WHITE: 300.0, Color.BLACK: 300.0}

    selected_square = None
    legal_moves_for_selection = []

    running = True
    while running:
        draw_board(screen, game.board, selected_square, legal_moves_for_selection)
        draw_clocks(screen, game, font)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    game.undo_last_move()
                    game.undo_last_move()
                    selected_square = None
                    legal_moves_for_selection = []

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQ_SIZE, pos[0] // SQ_SIZE
                if row >= 8:
                    continue
                if selected_square is None:
                    selected_square = (row, col)
                    piece = game.board.grid[row][col]
                    if piece and piece.color == game.current_turn:
                        legal_moves_for_selection = [
                            m for m in game.get_all_legal_moves() if m.from_pos == selected_square
                        ]
                else:
                    move = game.parse_move_coords(selected_square, (row, col))
                    if move:
                        start = time.time()
                        success, _ = game.make_move(move)
                        if success:
                            animate_move(screen, game.board, move)
                            game.clocks[game.current_turn] -= time.time() - start
                            # Bot move
                            start = time.time()
                            bot_move = choose_best_move_iterative(game, time_limit=1)
                            if bot_move:
                                game.make_move(bot_move)
                                animate_move(screen, game.board, bot_move)
                                game.clocks[game.current_turn] -= time.time() - start
                    selected_square = None
                    legal_moves_for_selection = []

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
