from engine.evaluation import PIECE_VALUES, evaluate_board
from core.piece import Color

def mvv_lva_score(move):
    if not move.captured:
        return 0
    victim_value = PIECE_VALUES.get(move.captured.type, 0)
    attacker_value = PIECE_VALUES.get(move.piece.type, 1)
    return victim_value * 10 - attacker_value  

def order_moves(moves):
    # Captures first, sorted by MVV-LVA
    return sorted(moves, key=mvv_lva_score, reverse=True)

def is_quiet_position(game_state) -> bool:
    for move in game_state.get_all_legal_moves():
        if move.captured:
            return False
    return True

def minimax(game_state, depth, alpha, beta, maximizing_player):
    if depth == 0 or game_state.is_game_over():
        quiet_score = quiescence_search(game_state, alpha, beta, maximizing_player)
        return quiet_score, None

    best_move = None
    legal_moves = order_moves(game_state.get_all_legal_moves())
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
    
def quiescence_search(game_state, alpha, beta, maximizing_player, depth=4):
    if depth == 0 or game_state.is_game_over():
        return evaluate_board(game_state)

    stand_pat = evaluate_board(game_state)

    if maximizing_player:
        if stand_pat >= beta:
            return beta
        alpha = max(alpha, stand_pat)
    else:
        if stand_pat <= alpha:
            return alpha
        beta = min(beta, stand_pat)

    legal_moves = order_moves(game_state.get_all_legal_moves())
    for move in legal_moves:
        if not move.captured:
            continue

        game_state.board.apply_move(move)
        score = quiescence_search(game_state, alpha, beta, not maximizing_player, depth - 1)
        game_state.board.undo_move(move)

        if maximizing_player:
            if score > alpha:
                alpha = score
                if alpha >= beta:
                    break
        else:
            if score < beta:
                beta = score
                if beta <= alpha:
                    break

    return alpha if maximizing_player else beta
