engine/ — 🤖 AI & Search
This is the chess bot brain.

bot.py
The interface for your bot

Entry point: choose_move(board, game_state)

Calls search.py to compute best move

evaluation.py
Scores a board position

Uses:

Material values

Piece-square tables

Mobility

King safety, pawn structure

Core method: evaluate(board, game_state) -> score

search.py
Implements your bot’s logic:

Minimax

Alpha-beta pruning

Iterative deepening

Quiescence search

Handles depth limits and time controls