from core import game_state
from engine.evaluation import evaluate_board

score = evaluate_board(game_state)
print("Eval:", score)
