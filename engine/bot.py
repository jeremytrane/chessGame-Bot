from engine.search import minimax
from core.piece import Color

def choose_best_move(game_state, depth=3):
    maximizing = game_state.current_turn == Color.WHITE
    _, best_move = minimax(game_state, depth, float('-inf'), float('inf'), maximizing)
    return best_move
