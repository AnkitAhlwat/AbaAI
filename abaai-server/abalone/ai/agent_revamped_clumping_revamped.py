import json
import os
import time

from abalone.ai.cython.cython import StateSpaceGenerator
from abalone.board import OptimizedBoard, BoardLayout
from abalone.movement import Move
from abalone.state import GameStateUpdate, GameState
from abalone.ai.game_playing_agent_revamped_iterative_deepening import AlphaBetaPruningAgentIterative
from abalone.ai.game_playing_agent_revamped_iterative_deeping_no_clumping import AlphaBetaPruningAgentIterative as AlphaBetaPruningAgentNoClumping

class alphaBetaPruningAgentClumping:
    def __init__(self, game_state, max_depth: int, max_time_sec: int = 2000, ):
        self.max_depth = max_depth
        self.max_time_sec = max_time_sec
        self.min_prunes = 0
        self.max_prunes = 0
        self.game_state = game_state
        self.MAX_PLAYER = game_state.turn.value
        self.MIN_PLAYER = 3 - game_state.turn.value
        self._table_counter = 0
        self.t_table = self.read_t_table()
        self.evaluation_t_table = {}

    def AlphaBetaPruningSearch(self):
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        start_time = time.time()
        game_state = self.game_state
        hashed_state = hash(game_state)
        if hashed_state in self.t_table:
            return self.t_table[hashed_state]
        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        sorted_possible_moves = sorted(possible_moves)

        for move in sorted_possible_moves:
            successor_state = GameStateUpdate(game_state, move).resulting_state
            value = self.Min_Value(successor_state, alpha, beta, self.max_depth - 1, start_time)
            if value > alpha:
                best_move = move
                alpha = max(alpha, value)

        print(f'Max Prunes: {self.max_prunes}')
        print(f'Min Prunes: {self.min_prunes}')

        self.t_table[hashed_state] = best_move
        return best_move

    def Max_Value(self, game_state: GameState, alpha: float, beta: float, depth: int, start_time: float):
        # check if the time to find move is up
        current_time = time.time()
        if current_time - start_time >= self.max_time_sec:
            return self.evaluate(game_state)

        if game_state.is_game_over() or depth == 0:
            return self.evaluate(game_state)

        value = float('-inf')
        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        sorted_possible_moves = sorted(possible_moves)

        for move in sorted_possible_moves:
            successor_state = GameStateUpdate(game_state, move).resulting_state
            value = max(value, self.Min_Value(successor_state, alpha, beta, depth - 1, start_time))
            alpha = max(alpha, value)
            if value >= beta:
                self.max_prunes += 1
                return value

        return value

    def Min_Value(self, game_state: GameState, alpha: float, beta: float, depth: int, start_time: float):
        # check if the time to find move is up
        current_time = time.time()
        if current_time - start_time >= self.max_time_sec:
            return self.evaluate(game_state)

        if game_state.is_game_over() or depth == 0:
            return self.evaluate(game_state)

        value = float('inf')
        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        sorted_possible_moves = sorted(possible_moves)

        for move in sorted_possible_moves:
            successor_state = GameStateUpdate(game_state, move).resulting_state
            value = min(value, self.Max_Value(successor_state, alpha, beta, depth - 1, start_time))
            beta = min(beta, value)
            if value <= alpha:
                self.min_prunes += 1
                return value
        return value

    def evaluate(self, game_state: GameState) -> float:
        hashed_state = hash(game_state)
        if hashed_state in self.evaluation_t_table:
            return self.evaluation_t_table[hashed_state]
        score = 0
        # score += 2 * self.clumping(game_state)
        score += 10 * self.board_control(game_state, MANHATTAN_WEIGHT_CONVERTED)
        score += 1000 * self.piece_advantage(game_state)
        score += 10000000 * self.terminal_test(game_state)
        self.evaluation_t_table[hashed_state] = score
        return score

    def clumping(
            self,
            game_state: GameState
    ) -> float:
        """
        Iterates through each player piece and each opponent piece separately. For each piece, it counts how many other
        pieces of the same color are adjacent to it. The function returns the difference between the number of player
        pieces clumped together and the number of opponent pieces clumped together.
        """
        board_array = game_state.board.to_matrix()
        piece_positions = StateSpaceGenerator.get_player_piece_positions(game_state)
        player_marbles = piece_positions["player_max"]
        opponent_marbles = piece_positions["player_min"]

        player_clump_value = 0
        opponent_clump_value = 0

        for player_position in player_marbles:
            player_clump_value += self.__get_clumping_value(player_position, board_array)
        for opponent_position in opponent_marbles:
            opponent_clump_value += self.__get_clumping_value(opponent_position, board_array)

        return float(opponent_clump_value - player_clump_value)

    def __get_clumping_value(self, position: tuple, board_array: list[list[int]]) -> int:
        """
        Returns the number of pieces of the same color that are adjacent to the given position.

        :param position: the position to check
        :param board_array: the current board state
        :return: the number of pieces of the same color that are adjacent to the given position
        """
        value = 0
        x, y = position[0], position[1]
        pos_marble = board_array[y][x]

        if x > 0:
            if board_array[y][x - 1] == pos_marble:
                value += 1
            if y < 8:
                if board_array[y + 1][x - 1] == pos_marble:
                    value += 1

        if x < 8:
            if board_array[y][x + 1] == pos_marble:
                value += 1
            if y > 0:
                if board_array[y - 1][x + 1] == pos_marble:
                    value += 1

        if y > 0:
            if board_array[y - 1][x] == pos_marble:
                value += 1

        if y < 8:
            if board_array[y + 1][x] == pos_marble:
                value += 1

        return value

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

    def read_t_table(self) -> dict[int, Move]:
        t_table_file_name = "no_clumping_master_t_table.json"

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
        t_table_file_name = "no_clumping_master_t_table.json"

        with open(t_table_file_name, 'w') as file:
            # Add the new records from the t_table to the master table
            serialized_t_table = {k: v.to_json() for k, v in self.t_table.items()}

            json.dump(serialized_t_table, file)


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



def simulate_agents(game_state: GameState, max_moves: int):
    game_state = game_state
    agent1 = AlphaBetaPruningAgentIterative(max_depth=4)
    agent2 = AlphaBetaPruningAgentNoClumping(max_depth=4)

    for i in range(max_moves):
        if game_state.turn.value == 2:
            original_marbles = game_state.remaining_opponent_marbles
            original_opponent_marbles = game_state.remaining_player_marbles
            best_move = agent1.iterative_deepening_search(game_state)
            game_state = GameStateUpdate(game_state, best_move).resulting_state
            print(f'white move {best_move}')
            if game_state.remaining_player_marbles < original_marbles:
                print(f'marbles knocked off')
            if game_state.remaining_opponent_marbles < original_opponent_marbles:
                print(f'marbles knocked off')
        else:
            # agent2 = alphaBetaPruningAgentClumping(game_state, max_depth=4)
            # move = agent2.AlphaBetaPruningSearch()
            original_marbles = game_state.remaining_opponent_marbles
            original_opponent_marbles = game_state.remaining_player_marbles
            move = agent2.iterative_deepening_search(game_state)
            game_state = GameStateUpdate(game_state, move).resulting_state
            print(f'black move {move}')
            if game_state.remaining_player_marbles < original_marbles:
                print(f'marbles knocked off')
            if game_state.remaining_opponent_marbles < original_opponent_marbles:
                print(f'marbles knocked off')

    print(game_state.turn)
    print(game_state.remaining_player_marbles)
    print(game_state.remaining_opponent_marbles)
    agent1.write_t_table()
    agent2.write_t_table()



def simulate_moves(game_state: GameState, max_moves: int):
    # print("Initial Board")
    # print(game_state.board)
    i = 0
    start_time = time.time()
    agent = AlphaBetaPruningAgentIterative(max_depth=4)
    while i < max_moves:
        # agent = alphaBetaPruningAgentClumping(max_depth=4, game_state=game_state)
        # best_move = agent.AlphaBetaPruningSearch()
        best_move = agent.iterative_deepening_search(game_state)
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
    agent.write_t_table()


if __name__ == '__main__':
    # simulate_moves(GameState(), 10)
    # simulate_moves(GameState(OptimizedBoard(BoardLayout.GERMAN_DAISY.value)), 1)
    simulate_agents(GameState(),80)
    # simulate_moves(GameState(), 150)
