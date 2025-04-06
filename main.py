from core.board import Board
from core.game_state import GameState
from ui.cli import display_board, get_user_move_input, show_message

def main():
    board = Board()
    game = GameState(board)

    while not game.is_game_over():
        display_board(board)
        show_message(f"{game.current_turn.name}'s move")

        move_str = get_user_move_input()

        if move_str == "undo":
            if game.undo_last_move():
                show_message("Undid last move.")
            else:
                show_message("No move to undo.")
            continue

        if move_str == "redo":
            if game.redo_last_move():
                show_message("Redid last move.")
            else:
                show_message("No move to redo.")
            continue

        if move_str == "history":
            game.print_move_history()
            continue

        if move_str == "export":
            game.export_pgn()
            continue

        if not game.is_valid_input_format(move_str):
            show_message("Invalid format. Use e.g. 'e2e4'")
            continue

        move = game.parse_move(move_str)
        if move is None:
            show_message("Invalid move.")
            continue

        success, result = game.make_move(move)

        if not success:
            show_message(f"Illegal move: {result}")
            continue

    display_board(board)
    show_message("Game Over.")

if __name__ == "__main__":
    main()
