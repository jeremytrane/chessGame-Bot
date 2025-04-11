import time
from engine.search import minimax
from core.piece import Color

def choose_best_move_iterative(game_state, time_limit=1.0):
    start_time = time.time()
    best_move = None
    depth = 1

    maximizing = game_state.current_turn == Color.WHITE

    while True:
        now = time.time()
        if now - start_time >= time_limit:
            break

        try:
            eval_score, move = minimax(game_state, depth, float('-inf'), float('inf'), maximizing)
        except TimeoutError:
            break

        if move:
            best_move = move

        if time.time() - start_time >= time_limit:
            break

        depth += 1  # Try searching one level deeper

    print(f"⏱ Depth {depth} complete in {time.time() - start_time:.2f}s")
    
    return best_move