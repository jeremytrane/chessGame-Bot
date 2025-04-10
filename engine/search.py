from engine.evaluation import evaluate_board
from core.piece import Color

def minimax(game_state, depth, alpha, beta, maximizing_player):
    if depth == 0 or game_state.is_game_over():
        return evaluate_board(game_state), None

    best_move = None
    legal_moves = game_state.get_all_legal_moves()
    if not legal_moves:
        return evaluate_board(game_state), None

    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            game_state.board.apply_move(move)
            eval, _ = minimax(game_state, depth - 1, alpha, beta, False)
            game_state.board.undo_move(move)

            if eval > max_eval:
                max_eval = eval
                best_move = move

            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval, best_move

    else:
        min_eval = float('inf')
        for move in legal_moves:
            game_state.board.apply_move(move)
            eval, _ = minimax(game_state, depth - 1, alpha, beta, True)
            game_state.board.undo_move(move)

            if eval < min_eval:
                min_eval = eval
                best_move = move

            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_eval, best_move