import time

from abalone.ai.state_space_generator import StateSpaceGenerator
from abalone.state import GameStateUpdate, GameState


class AlphaBetaPruningAgent:
    def __init__(self, max_depth: int):
        self.max_depth = max_depth

    def AlphaBetaPruningSearch(self, game_state: GameState):
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for move in StateSpaceGenerator.generate_all_possible_moves(game_state):
            successor_state = GameStateUpdate(game_state, move).resulting_state
            value = self.Min_Value(successor_state, alpha, beta, self.max_depth - 1)
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, value)

        return best_move

    def Max_Value(self, game_state: GameState, alpha: float, beta: float, depth: int):
        if game_state.is_game_over() or depth == 0:
            return HeuristicFunction.evaluate(game_state)
        value = float('-inf')

        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        for move in possible_moves:
            successor_state = GameStateUpdate(game_state, move).resulting_state
            value = max(value, self.Min_Value(successor_state, alpha, beta, depth - 1))
            alpha = max(alpha, value)
            if value >= beta:
                break

        return value

    def Min_Value(self, game_state: GameState, alpha: float, beta: float, depth: int):
        if game_state.is_game_over() or depth == 0:
            return HeuristicFunction.evaluate(game_state)
        value = float('inf')
        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        for move in possible_moves:
            successor_state = GameStateUpdate(game_state, move).resulting_state
            value = min(value, self.Max_Value(successor_state, alpha, beta, depth - 1))
            beta = min(beta, value)
            if value <= alpha:
                break
        return value


class HeuristicFunction:
    DEFAULT_WEIGHTS = [1000000, 10000, 10, 10, 2, 2, 1, 1]
    EMPTY = [
        [-1, -1, -1, -1, 0, 0, 0, 0, 0],
        [-1, -1, -1, 0, 0, 0, 0, 0, 0],
        [-1, -1, 0, 0, 0, 0, 0, 0, 0],
        [-1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, -1],
        [0, 0, 0, 0, 0, 0, 0, -1, -1],
        [0, 0, 0, 0, 0, 0, -1, -1, -1],
        [0, 0, 0, 0, 0, -1, -1, -1, -1],
    ]

    @classmethod
    def evaluate(cls, game_state: GameState) -> float:
        score = 0
        return score


def simulate_moves(game_state: GameState, max_moves: int):
    agent = AlphaBetaPruningAgent(max_depth=3)
    print("Initial Board")
    print(game_state.board)
    game_state = game_state
    i = 0
    start_time = time.time()
    while i < max_moves:
        best_move = agent.AlphaBetaPruningSearch(game_state)
        print(f"{game_state.turn.name}->({best_move})")

        game_state = GameStateUpdate(game_state, best_move).resulting_state

        i += 1
    finish_time = time.time()
    print(finish_time - start_time)
    print(game_state.board)
    print(game_state.remaining_player_marbles)
    print(game_state.remaining_opponent_marbles)

# simulate_moves(GameState(), 10)
# agent = AlphaBetaPruningAgent(max_depth=3)
# current_time = time.time()
# best_move = agent.AlphaBetaPruningSearch(GameState())
# finish_time = time.time()
# print(finish_time - current_time)
# print(best_move)
