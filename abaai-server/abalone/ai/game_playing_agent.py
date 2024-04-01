import time

from abalone.ai.state_space_generator import StateSpaceGenerator
from abalone.state import GameStateUpdate, GameState


class AlphaBetaPruningAgent:
    def __init__(self, max_depth: int):
        self.max_depth = max_depth
        self.min_prunes = 0
        self.max_prunes = 0

    def AlphaBetaPruningSearch(self, game_state: GameState):
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        sorted_possible_moves = sorted(possible_moves)
        for move in sorted_possible_moves:
            successor_state = GameStateUpdate(game_state, move).resulting_state
            value = self.Min_Value(successor_state, alpha, beta, self.max_depth - 1)
            if value > alpha:
                best_move = move
                alpha = max(alpha, value)
        print(f'Max Prunes: {self.max_prunes}')
        print(f'Min Prunes: {self.min_prunes}')
        return best_move

    def Max_Value(self, game_state: GameState, alpha: float, beta: float, depth: int):
        if game_state.is_game_over() or depth == 0:
            return evaluate(game_state) * -1
        value = float('-inf')
        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        sorted_possible_moves = sorted(possible_moves)
        for move in sorted_possible_moves:
            successor_state = GameStateUpdate(game_state, move).resulting_state
            value = max(value, self.Min_Value(successor_state, alpha, beta, depth - 1))
            alpha = max(alpha, value)
            if value >= beta:
                self.max_prunes += 1
                return value

        return value

    def Min_Value(self, game_state: GameState, alpha: float, beta: float, depth: int):
        if game_state.is_game_over() or depth == 0:
            return evaluate(game_state)
        value = float('inf')
        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        sorted_possible_moves = sorted(possible_moves)
        for move in sorted_possible_moves:
            successor_state = GameStateUpdate(game_state, move).resulting_state
            value = min(value, self.Max_Value(successor_state, alpha, beta, depth - 1))
            beta = min(beta, value)
            if value <= alpha:
                self.min_prunes += 1
                return value
        return value


DEFAULT_WEIGHTS = [1000000, 10000, 10, 10, 2, 2, 1, 1]
MANHATTAN_WEIGHT_FLAT = [
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 2, 1, 1, 0,
    0, 0, 0, 1, 2, 2, 2, 2, 0,
    0, 0, 1, 2, 4, 3, 3, 2, 0,
    0, 2, 3, 4, 5, 4, 3, 2, 0,
    0, 2, 3, 3, 4, 2, 1, 0, 0,
    0, 2, 2, 2, 2, 1, 0, 0, 0,
    0, 1, 1, 2, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0
]

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

MANHATTAN_WEIGHT_CONVERTED = [
    None, None, None, None, (4, -4), (3, -4), (2, -4), (1, -4), (0, -4),
    None, None, None, (4, -3), (3, -3), (2, -3), (1, -3), (0, -3), (-1, -3),
    None, None, (4, -2), (3, -2), (2, -2), (1, -2), (0, -2), (-1, -2), (-2, -2),
    None, (4, -1), (3, -1), (2, -1), (1, -1), (0, -1), (-1, -1), (-2, -1), (-3, -1),
    (-4, 0), (-3, 0), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
    (-3, 1), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), None,
    (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), None, None,
    (-1, 3), (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), None, None, None,
    (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), None, None, None, None]


def evaluate(game_state: GameState) -> float:
    score = 0
    score += 10 * board_control(game_state, MANHATTAN_WEIGHT_CONVERTED)
    score += 1000 * piece_advantage(game_state)
    score += 10000000 * terminal_test(game_state)
    return score


def board_control(game_state, lookup_table):
    """
    A zero-sum heuristic for evaluating the board state based on the distance of the player's/opponents marbles from
    the center.
    :param game_state: The current game state
    :param lookup_table: A lookup table.
    :return: The score of the board state based on the distance of the player's/opponents marbles from the center.
    """
    player_score = 0
    opponent_score = 0

    for index, value in enumerate(game_state.board.array):
        if value in (1, 2):
            hex_coords = lookup_table[index]
            if hex_coords:
                distance = max(abs(hex_coords[0]), abs(hex_coords[1]))
                if value == game_state.turn.value:
                    player_score += distance
                else:
                    opponent_score += distance

    return player_score - opponent_score


def piece_advantage(game_state):
    """
    A heuristic for evaluating the board state based on the number of marbles the player has compared to the
    opponent.
    :param game_state: The current game state
    :return: The score of the board state based on the number of marbles the player has compared to the opponent.
    """
    return game_state.remaining_player_marbles - game_state.remaining_opponent_marbles


def terminal_test(game_state: GameState):
    """
    A heuristic for evaluating the board state based on whether the game is in a terminal state.
    :param game_state: The current game state
    :return: The score of the board state based on whether the game is in a terminal state.
    """
    if game_state.remaining_player_marbles < 9:
        return -10000
    if game_state.remaining_opponent_marbles < 9:
        return 10000
    return 0


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
        original_marbles = game_state.remaining_opponent_marbles
        original_opponent_marbles = game_state.remaining_player_marbles
        game_state = GameStateUpdate(game_state, best_move).resulting_state
        if game_state.remaining_player_marbles < original_marbles:
            print(f'marbles knocked off')
        if game_state.remaining_opponent_marbles < original_opponent_marbles:
            print(f'marbles knocked off')

        i += 1
    finish_time = time.time()
    print(finish_time - start_time)
    print(game_state.board)
    print(game_state.turn)
    print(game_state.remaining_opponent_marbles)
    print(game_state.remaining_player_marbles)


if __name__ == '__main__':
    simulate_moves(GameState(), 10)
