def display_board(board):
    print()
    for row in range(8):
        print(8 - row, end=' ')
        for col in range(8):
            piece = board.grid[row][col]
            print(piece.symbol() if piece else '.', end=' ')
        print()
    print("  a b c d e f g h\n")

def get_user_move_input():
    return input("Enter your move (e.g., e2e4): ").strip().lower()

def show_message(msg):
    print(msg)
