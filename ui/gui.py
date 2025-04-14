import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from core.game_state import GameState
from core.board import Board
from core.piece import Color
from engine.bot import choose_best_move_iterative

# Settings
WIDTH, HEIGHT = 512, 512
SQ_SIZE = WIDTH // 8

# Load piece images
IMAGES = {}
def load_images():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for p in pieces:
        IMAGES[p] = pygame.transform.scale(pygame.image.load(f"../assets/{p}.png"), (SQ_SIZE, SQ_SIZE))

def piece_to_code(piece):
    color = 'w' if piece.color == Color.WHITE else 'b'
    return f"{color}{piece.type.name[0]}"

def draw_board(screen, board):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(8):
        for c in range(8):
            color = colors[(r + c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

            piece = board.grid[r][c]
            if piece:
                code = piece_to_code(piece)
                screen.blit(IMAGES[code], pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()
    load_images()

    game = GameState(Board())

    selected_square = None
    running = True

    while running:
        draw_board(screen, game.board)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQ_SIZE, pos[0] // SQ_SIZE
                if selected_square is None:
                    selected_square = (row, col)
                else:
                    move = game.parse_move_coords(selected_square, (row, col))
                    if move:
                        success, _ = game.make_move(move)
                        if success:
                            # Bot plays
                            bot_move = choose_best_move_iterative(game, time_limit=1)
                            if bot_move:
                                game.make_move(bot_move)
                    selected_square = None

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
