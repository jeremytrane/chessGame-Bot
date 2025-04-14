from engine.bot import choose_best_move_iterative
from core.game_state import GameState
from core.board import Board
from ui.cli import display_board

def bot_vs_bot():
    game = GameState(Board())
    while not game.is_game_over():
        display_board(game.board)
        bot_move = choose_best_move_iterative(game, time_limit=1.0)
        if not bot_move:
            print("Bot has no legal moves.")
            break
        game.make_move(bot_move)
    print("Game Over")

# Uncomment to run:
bot_vs_bot()
