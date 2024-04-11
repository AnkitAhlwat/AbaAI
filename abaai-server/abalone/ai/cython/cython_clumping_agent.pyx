import json
import os
import time
from abalone.ai.cython.cython import StateSpaceGenerator
from abalone.movement_optimized import Move
from abalone.state import GameStateUpdate, GameState


cdef class AlphaBetaPruningAgentAnkit:
    cdef public int max_depth
    cdef public double max_time_sec
    cdef public int MAX_PLAYER
    cdef public int MIN_PLAYER
    cdef public game_state

    cdef public int _table_counter
    cdef public dict t_table
    cdef public dict evaluation_t_table
    def __init__(self, max_depth: int, max_time_sec: float = 2000):
        self.max_depth = max_depth
        self.max_time_sec = max_time_sec
        self._table_counter = 0
        self.t_table = self.read_t_table()
        self.evaluation_t_table = {}

    def iterative_deepening_search(self, game_state):
        start_time = time.time()
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
            move, move_value = self.alpha_beta_pruning_search(depth, start_time)

            current_time = time.time()
            if current_time - start_time >= self.max_time_sec:
                break

            current_best_move = move
            depth += 1

        self.t_table[hashed_state] = current_best_move
        return current_best_move

    def alpha_beta_pruning_search(self, max_depth: int, start_time: float):
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        game_state = self.game_state
        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        sorted_possible_moves = sorted(possible_moves)

        for move in sorted_possible_moves:
            successor_state = GameStateUpdate(game_state, move).resulting_state

            value = self.min_value(successor_state, alpha, beta, max_depth - 1, start_time)
            if value > alpha:
                best_move = move
                alpha = max(alpha, value)

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
        score += 2* self.clumping(game_state)
        score +=  self.board_control_flat(game_state, MANHATTAN_WEIGHT_CONVERTED_FLAT)
        score += 10 * self.edge(game_state, EDGE)
        score += 10000 * self.piece_advantage(game_state)
        score += 10000000 * self.terminal_test(game_state)

        self.evaluation_t_table[hashed_state] = score
        return score

    def board_control_flat(self, game_state, lookup_table):
        cdef int player_score = 0
        cdef int opponent_score = 0
        cdef int index
        cdef int value
        cdef int board_len = len(game_state.board.array)
        cdef int distance

        for index, value in enumerate(game_state.board.array):
            if value in (1, 2):
                distance = lookup_table[index]
                if value == self.MAX_PLAYER:
                    player_score += distance
                else:
                    opponent_score += distance

        return opponent_score - player_score

    def edge(self, game_state, lookup_table):
        """
        A zero-sum heuristic for evaluating the board state based on the distance of the player's/opponents marbles from
        the center.
        :param game_state: The current game state
        :param lookup_table: A lookup table.
        :return: The score of the board state based on the distance of the player's/opponents marbles from the center.
        """
        cdef int player_score = 0
        cdef int opponent_score = 0
        cdef int index
        cdef int value
        cdef int distance

        for index, value in enumerate(game_state.board.array):
            if value in (1, 2):
                distance = lookup_table[index]
                if value == self.MAX_PLAYER:
                    player_score += distance
                else:
                    opponent_score += distance

        return player_score - opponent_score
    def piece_advantage(self, game_state):
        if game_state.turn.value == self.MAX_PLAYER:
            return game_state.remaining_player_marbles - game_state.remaining_opponent_marbles
        else:
            return game_state.remaining_opponent_marbles - game_state.remaining_player_marbles

    def terminal_test(self, game_state: GameState):
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
                return +10000
            return 0

    def clumping(
            self,
            game_state: GameState
    ) -> float:
        cdef int player_clump_value = 0
        cdef int opponent_clump_value = 0
        cdef int index
        cdef int value
        cdef int board_len = len(game_state.board.array)

        for index, value in enumerate(game_state.board.array):
            if value in (1, 2):
                if value == self.MAX_PLAYER:
                    player_clump_value += self.__get_clumping_value(index, game_state.board.array, value)
                else:
                    opponent_clump_value += self.__get_clumping_value(index, game_state.board.array, value)

        return float(player_clump_value - opponent_clump_value)

    cdef int __get_clumping_value(self, int position, list[int] board_array, int player_value):
        cdef int value = 0
        cdef list[int] dxs = [-1, 1, 0, 0, 1, -1]
        cdef list[int] dys = [0, 0, -1, 1, -1, 1]
        cdef int i
        cdef int new_x, new_y
        cdef int new_position

        for i in range(6):
            new_x = position % 9 + dxs[i]
            new_y = position // 9 + dys[i]
            new_position = new_y * 9 + new_x
            if 0 <= new_x < 9 and 0 <= new_y < 9 and board_array[new_position] == player_value:
                value += 1

        return value

    def read_t_table(self) -> dict[int, Move]:
        t_table_file_name = "look_up_tables/agent_ankit.json"

        if os.path.exists(t_table_file_name):
            with open(t_table_file_name, 'r') as file:
                t_table_json: dict = json.load(file)
                deserialized_t_table = {
                    int(state_hash): Move.from_json(move_json)
                    for state_hash, move_json
                    in t_table_json.items()
                }
                return deserialized_t_table
        else:
            return {}

    def write_t_table(self):
        t_table_file_name = "look_up_tables/agent_ankit.json"

        with open(t_table_file_name, 'w') as file:
            # Add the new records from the t_table to the master table
            serialized_t_table = {k: v.to_json() for k, v in self.t_table.items()}

            json.dump(serialized_t_table, file)


MANHATTAN_WEIGHT_CONVERTED_FLAT = [
    None, None, None, None, 8, 7, 6, 5, 4,
    None, None, None, 7, 6, 5, 4, 3, 4,
    None, None, 6, 5, 4, 3, 2, 3, 4,
    None, 5, 4, 3, 2, 1, 2, 3, 4,
    4, 3, 2, 1, 0, 1, 2, 3, 4,
    4, 3, 2, 1, 2, 3, 4, 5, None,
    4, 3, 2, 3, 4, 5, 6, None, None,
    4, 3, 4, 5, 6, 7, None, None, None,
    4, 5, 6, 7, 8, None, None, None, None]

EDGE =[-999, -999, -999, -999, -5, -5, -5, -5, -5,
       -999, -999, -999, -5, -2.5, -2.5, -2.5, -2.5, -5,
       -999, -999, -5, -2.5, 0, 0, 0, -2.5, -5,
       -999, -5, -2.5, 0, 0, 0, 0, -2.5, -5,
       -5, -2.5, 0, 0, 0, 0, 0, -2.5, -5,
       -5, -2.5, 0, 0, 0, 0, -2.5, -5, -999,
       -5, -2.5, 0, 0, 0, -2.5, -5, -999, -999,
       -5, -2.5, -2.5, -2.5, -2.5, -5, -999, -999, -999,
       -5, -5, -5, -5, -5, -999, -999, -999, -999]
