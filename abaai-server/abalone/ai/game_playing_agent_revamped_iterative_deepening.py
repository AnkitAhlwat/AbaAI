import time

from abalone.ai.cython.cython import StateSpaceGenerator
from abalone.state import GameStateUpdate, GameState


class AlphaBetaPruningAgentIterative:
    def __init__(self, max_depth: int, max_time_sec: int = 50):
        self.max_depth = max_depth
        self.max_time_sec = max_time_sec
        self.game_state = None
        self.MAX_PLAYER = None
        self.MIN_PLAYER = None

        self._table_counter = 0
        self.t_table = {}
        self.evaluation_t_table = {}

    def iterative_deepening_search(self, game_state):
        self.game_state = game_state
        self.MAX_PLAYER = game_state.turn.value
        self.MIN_PLAYER = 3 - game_state.turn.value

        depth = 1
        current_best_move = None
        current_best_move_value = float('-inf')

        hashed_state = hash(game_state)
        if hashed_state in self.t_table:
            return self.t_table[hashed_state]

        while depth <= self.max_depth:
            move, move_value = self.alpha_beta_pruning_search(depth)
            if move_value >= current_best_move_value:
                current_best_move = move
                current_best_move_value = move_value
            depth += 1

        self.t_table[hashed_state] = current_best_move
        return current_best_move

    def alpha_beta_pruning_search(self, max_depth: int):
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        start_time = time.time()
        game_state = self.game_state
        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        sorted_possible_moves = sorted(possible_moves)

        for move in sorted_possible_moves:
            successor_state = GameStateUpdate(game_state, move).resulting_state

            value = self.min_value(successor_state, alpha, beta, max_depth, start_time)
            if value > alpha:
                best_move = move
                alpha = max(alpha, value)

        # print(f'Max Prunes: {self.max_prunes}')
        # print(f'Min Prunes: {self.min_prunes}')

        return best_move, alpha

    def max_value(self, game_state: GameState, alpha: float, beta: float, depth: int, start_time: float):
        # check if the time to find move is up
        current_time = time.time()
        if current_time - start_time >= self.max_time_sec:
            value = self.evaluate(game_state)
            return value

        if game_state.is_game_over() or depth == 0:
            value = self.evaluate(game_state)
            return value

        value = float('-inf')
        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        sorted_possible_moves = sorted(possible_moves)

        for move in sorted_possible_moves:
            successor_state = GameStateUpdate(game_state, move).resulting_state
            value = max(value, self.min_value(successor_state, alpha, beta, depth - 1, start_time))
            alpha = max(alpha, value)
            if value >= beta:
                # self.max_prunes += 1
                return value

        return value

    def min_value(self, game_state: GameState, alpha: float, beta: float, depth: int, start_time: float):
        # check if the time to find move is up
        current_time = time.time()
        if current_time - start_time >= self.max_time_sec:
            value = self.evaluate(game_state)
            return value

        if game_state.is_game_over() or depth == 0:
            value = self.evaluate(game_state)
            return value

        value = float('inf')
        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        sorted_possible_moves = sorted(possible_moves)

        for move in sorted_possible_moves:
            successor_state = GameStateUpdate(game_state, move).resulting_state
            value = min(value, self.max_value(successor_state, alpha, beta, depth - 1, start_time))
            beta = min(beta, value)
            if value <= alpha:
                # self.min_prunes += 1
                return value

        return value

    def evaluate(self, game_state: GameState) -> float:
        hashed_state = hash(game_state)
        if hashed_state in self.evaluation_t_table:
            return self.evaluation_t_table[hashed_state]

        score = 0
        score += 10 * self.board_control(game_state, MANHATTAN_WEIGHT_CONVERTED)
        score += 1000 * self.piece_advantage(game_state)
        score += 10000000 * self.terminal_test(game_state)

        self.evaluation_t_table[hashed_state] = score
        return score

    def board_control(self, game_state, lookup_table):
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
                    distance = abs(hex_coords[0]) + abs(hex_coords[1])
                    if value == self.MAX_PLAYER:
                        player_score += distance
                    else:
                        opponent_score += distance

        return opponent_score - player_score

    def piece_advantage(self, game_state):
        """
        A heuristic for evaluating the board state based on the number of marbles the player has compared to the
        opponent.
        :param game_state: The current game state
        :return: The score of the board state based on the number of marbles the player has compared to the opponent.
        """
        if game_state.turn.value == self.MAX_PLAYER:
            return game_state.remaining_player_marbles - game_state.remaining_opponent_marbles
        else:
            return game_state.remaining_opponent_marbles - game_state.remaining_player_marbles

    def terminal_test(self, game_state: GameState):
        """
        A heuristic for evaluating the board state based on whether the game is in a terminal state.
        :param game_state: The current game state
        :return: The score of the board state based on whether the game is in a terminal state.
        """
        if game_state.turn.value == self.MAX_PLAYER:
            if game_state.remaining_player_marbles < 9:
                return -10000
            if game_state.remaining_opponent_marbles < 9:
                return 10000
            return 0
        else:
            if game_state.remaining_opponent_marbles < 9:
                return -10000
            if game_state.remaining_player_marbles < 9:
                return 10000
            return 0


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
