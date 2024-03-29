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
            if value[0] > best_value:
                best_value = value[0]
                best_move = move
            alpha = max(alpha, value[0])

        return best_move

    def Max_Value(self, game_state: GameState, alpha: float, beta: float, depth: int):
        if game_state.is_game_over() or depth == 0:
            return HeuristicFunction.evaluate(game_state)
        best_move = None
        value = float('-inf')

        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        for move in possible_moves:
            successor_state = GameStateUpdate(game_state, move).resulting_state
            successor_value = max(value, self.Min_Value(successor_state, alpha, beta, depth - 1))
            if successor_value >= value:
                value, best_move = successor_value, move
                alpha = max(alpha, value)
                if value >= beta:
                    break

        return value, best_move

    def Min_Value(self, game_state: GameState, alpha: float, beta: float, depth: int):
        if game_state.is_game_over() or depth == 0:
            return HeuristicFunction.evaluate(game_state)
        best_move = None
        value = float('inf')
        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        for move in possible_moves:
            successor_state = GameStateUpdate(game_state, move).resulting_state
            successor_value = min(value, self.Max_Value(successor_state, alpha, beta, depth - 1))
            if successor_value <= value:
                value, best_move = successor_value, move
                beta = min(beta, value)
                if value <= alpha:
                    break
        return value, best_move


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
        print(cls.manhattan_distance(game_state))
        score += 10 * cls.manhattan_distance(game_state)
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
    agent = AlphaBetaPruningAgent(max_depth=2)
    print("Initial Board")
    print(game_state.board)
    game_state = game_state
    i = 0
    while i < max_moves:
        best_move = agent.AlphaBetaPruningSearch(game_state)
        print(f"{game_state.turn.name}->({best_move})")

        game_state = GameStateUpdate(game_state, best_move).resulting_state

        print(game_state.board)
        i += 1


# simulate_moves(GameState(), 2)
agent = AlphaBetaPruningAgent(max_depth=2)
current_time = time.time()
best_move = agent.AlphaBetaPruningSearch(GameState())
finish_time = time.time()
print(finish_time - current_time)
print(best_move)
