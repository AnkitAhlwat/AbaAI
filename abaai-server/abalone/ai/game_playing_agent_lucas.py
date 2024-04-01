from abalone.ai.state_space_generator import StateSpaceGenerator
from abalone.movement import Position
from abalone.state import GameStateUpdate, GameState


class AlphaBetaPruningAgentLucas:
    def __init__(self, max_depth: int):
        self.max_depth = max_depth
        # self.max_player = None
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
        print(f'{game_state.turn.name}->{alpha} First')
        print(f'Max Prunes: {self.max_prunes}')
        print(f'Min Prunes: {self.min_prunes}')
        return best_move

    def Max_Value(self, game_state: GameState, alpha: float, beta: float, depth: int):
        if game_state.is_game_over() or depth == 0:
            return HeuristicFunction.evaluate(game_state) * -1
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
            return HeuristicFunction.evaluate(game_state)
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


class HeuristicFunction:
    weights = {
        "terminal_state": 100_000_000,
        "piece_count": 10_000,
        "manhattan_distance": 100,
        "clumping": 10,
    }

    @classmethod
    def evaluate(cls, game_state: GameState) -> float:
        piece_position = StateSpaceGenerator.get_player_piece_positions(game_state)
        player_marbles = piece_position["player_max"]
        opponent_marbles = piece_position["player_min"]

        score = 0

        score += cls.terminal_state(game_state) * cls.weights["terminal_state"]

        score += cls.piece_count(game_state) * cls.weights["piece_count"]

        score += cls.manhattan_distance(player_marbles, opponent_marbles) * cls.weights["manhattan_distance"]

        score += cls.clumping(game_state.board.to_matrix(), player_marbles, opponent_marbles) * cls.weights["clumping"]

        return score

    # Heuristic functions
    @staticmethod
    def terminal_state(game_state) -> float:
        """
        If the current player won return a positive value, if the opponent won return a negative value,
        if the game is not over yet, return 0.

        :param game_state: the current game state
        :return: a float representing the value of the terminal state
        """
        starting_marble_count = 14
        num_marbles_pushed_off_to_win = 6
        loser_marble_count = starting_marble_count - num_marbles_pushed_off_to_win

        # if the player wins
        if game_state.remaining_opponent_marbles <= loser_marble_count:
            return 1
        # if the opponent wins
        elif game_state.remaining_player_marbles <= loser_marble_count:
            return -1
        # if the game is not over yet
        else:
            return 0

    @staticmethod
    def piece_count(game_state) -> float:
        """
        For each player piece, add 1 point, for each opponent piece, subtract 1 point.

        :param game_state: the current game state
        :return: a float representing the value of the piece counts
        """
        return game_state.remaining_player_marbles - game_state.remaining_opponent_marbles

    @staticmethod
    def manhattan_distance(player_marbles: list[Position], opponent_marbles: list[Position]) -> float:
        player_value = 0
        opponent_value = 0
        for player_position in player_marbles:
            player_value += HeuristicFunction.__manhattan_distance_from_center(player_position)
        for opponent_position in opponent_marbles:
            opponent_value += HeuristicFunction.__manhattan_distance_from_center(opponent_position)

        return float(player_value - opponent_value)

    @staticmethod
    def clumping(
            board_array: list[list[int]],
            player_marbles: list[Position],
            opponent_marbles: list[Position]
    ) -> float:
        """
        Iterates through each player piece and each opponent piece separately. For each piece, it counts how many other
        pieces of the same color are adjacent to it. The function returns the difference between the number of player
        pieces clumped together and the number of opponent pieces clumped together.

        :param board_array: the current board state as a 2D list
        :param player_marbles: a list of player marble positions
        :param opponent_marbles: a list of opponent marble positions
        :return: the difference between the number of player pieces clumped together and the number of opponent pieces.
        This value will be negative if the opponent has better clumping than us, positive if we have better clumping.
        """

        player_clump_value = 0
        opponent_clump_value = 0

        for player_position in player_marbles:
            player_clump_value += HeuristicFunction.__get_clumping_value(player_position, board_array)
        for opponent_position in opponent_marbles:
            opponent_clump_value += HeuristicFunction.__get_clumping_value(opponent_position, board_array)

        return float(player_clump_value - opponent_clump_value)

    # Private helper methods
    @staticmethod
    def __manhattan_distance_from_center(position: Position) -> float:
        center_position_x, center_position_y = 4, 4
        return abs(position.x - center_position_x) + abs(position.y - center_position_y)

    @staticmethod
    def __get_clumping_value(position: Position, board_array: list[list[int]]) -> int:
        """
        Returns the number of pieces of the same color that are adjacent to the given position.

        :param position: the position to check
        :param board_array: the current board state
        :return: the number of pieces of the same color that are adjacent to the given position
        """
        value = 0
        x, y = position.x, position.y
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
