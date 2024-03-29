import time

from abalone.ai.state_space_generator import StateSpaceGenerator
from abalone.movement import Move
from abalone.state import GameStateUpdate, GameState


class MiniMaxAgent:
    def __init__(self, max_depth: int):
        self.max_depth = max_depth

    def get_best_move(self, game_state: GameState) -> Move:
        best_move = None
        max_eval = float('-inf')
        for move in StateSpaceGenerator.generate_all_possible_moves(game_state):
            successor_state = GameStateUpdate(game_state, move).resulting_state
            evaluated_value = self.minimax(successor_state, self.max_depth, False, float('-inf'), float('inf'))
            if evaluated_value > max_eval:
                max_eval = evaluated_value
                best_move = move
        return best_move

    def minimax(self, game_state: GameState, depth: int, max_turn: bool, alpha: float, beta: float) -> float:
        if depth == 0 or game_state.is_game_over():
            return HeuristicFunction.evaluate(game_state)
        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        if max_turn:
            max_eval = float('-inf')
            for move in possible_moves:
                next_state = GameStateUpdate(game_state, move).resulting_state
                max_eval = max(max_eval, self.minimax(next_state, depth - 1, False, alpha, beta))
                if max_eval > beta:
                    return max_eval
                alpha = max(alpha, max_eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in possible_moves:
                next_state = GameStateUpdate(game_state, move).resulting_state
                min_eval = min(min_eval, self.minimax(next_state, depth - 1, True, alpha, beta))
                if min_eval < alpha:
                    return min_eval
                beta = min(beta, min_eval)
            return min_eval


class HeuristicFunction:
    DEFAULT_WEIGHTS = [1000000, 10000, 10, 10, 2, 2, 1, 1]
    MANHATTAN_WEIGHT_FLAT = [
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 3, 3, 3, 0, 0,
        0, 0, 0, 4, 5, 4, 0, 0, 0,
        0, 0, 3, 3, 3, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0
    ]

    @classmethod
    def evaluate(cls, game_state: GameState) -> float:
        score = 0
        score += cls.DEFAULT_WEIGHTS[2] * cls.manhattan_distance(game_state)
        return score

    @classmethod
    def manhattan_distance(cls, game_state):
        player_score = 0
        opponent_score = 0
        player_value = game_state.turn.value
        opponent_value = 2 if player_value == 1 else 1
        board = game_state.board.array

        for index in range(len(board)):
            if board[index] == player_value:
                player_score += cls.MANHATTAN_WEIGHT_FLAT[index]
            elif board[index] == opponent_value:
                opponent_score += cls.MANHATTAN_WEIGHT_FLAT[index]

        differential_score = player_score - opponent_score
        return differential_score


def simulate_moves(game_state: GameState, max_moves: int):
    agent = MiniMaxAgent(max_depth=2)
    print("Initial Board")
    print(game_state.board)
    game_state = game_state
    i = 0
    while i < max_moves:
        best_move = agent.get_best_move(game_state)
        print(f"{game_state.turn.name}->({best_move})")

        game_state = GameStateUpdate(game_state, best_move).resulting_state

        print(game_state.board)
        i += 1


# simulate_moves(GameState(), 2)
agent = MiniMaxAgent(max_depth=2)
current_time = time.time()
best_move = agent.get_best_move(GameState())
finish_time = time.time()
print(finish_time - current_time)
print(best_move)
