from abalone.ai.state_space_generator import StateSpaceGenerator
from abalone.movement import Move, Position
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
            return self.evaluate(game_state)

        if max_turn:
            max_eval = float('-inf')
            for move in StateSpaceGenerator.generate_all_possible_moves(game_state):
                next_state = GameStateUpdate(game_state, move).resulting_state
                max_eval = max(max_eval, self.minimax(next_state, depth - 1, False, alpha, beta))
                if max_eval > beta:
                    return max_eval
                alpha = max(alpha, max_eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in StateSpaceGenerator.generate_all_possible_moves(game_state):
                next_state = GameStateUpdate(game_state, move).resulting_state
                min_eval = min(min_eval, self.minimax(next_state, depth - 1, True, alpha, beta))
                if min_eval < alpha:
                    return min_eval
                beta = min(beta, min_eval)
            return min_eval


class HeuristicFunction:
    weights = {
        "terminal_state": 100_000,
        "piece_count": 1_000,
        "pieces_near_edge": 100,
        "manhattan_distance": 10,
        "clumping": 1,
        "sumito": 1,
        "triples": 1,
        "doubles": 1
    }

    # format: (y, x) -> (row, col)
    # board_boundary_array_coords = [
    #     (-1, 4), (-1, 5), (-1, 6), (-1, 7), (-1, 8),
    #     (0, 3), (0, 9),
    #     (1, 2), (1, 9),
    #     (2, 1), (2, 9),
    #     (3, 0), (3, 9),
    #     (4, -1), (4, 9),
    #     (5, -1), (5, 8),
    #     (6, -1), (6, 7),
    #     (7, -1), (7, 6),
    #     (8, -1), (8, 5),
    #     (9, 0), (9, 1), (9, 2), (9, 3), (9, 4)
    # ]

    # the dictionary keys are the rows of the board and the values are list of out of bounds positions for that row
    board_boundary_coords = {
        0: [(-1, 4), (-1, 5), (-1, 6), (-1, 7), (-1, 8), (0, 3), (0, 9)],
        1: [(1, 2), (1, 9)],
        2: [(2, 1), (2, 9)],
        3: [(3, 0), (3, 9)],
        4: [(4, -1), (4, 9)],
        5: [(5, -1), (5, 8)],
        6: [(6, -1), (6, 7)],
        7: [(7, -1), (7, 6)],
        8: [(8, -1), (8, 5), (9, 0), (9, 1), (9, 2), (9, 3), (9, 4)],
    }

    @staticmethod
    def evaluate(game_state: GameState) -> float:
        # NOTE: Any function that is a good thing will add to value, bad things will subtract from value
        value = 0

        # 1. Terminal state: if player won large positive, if opponent won small negative, if game not over 0
        value += HeuristicFunction.terminal_state(game_state) * HeuristicFunction.weights["terminal_state"]

        # 2. Piece counts: 1 point for each player piece, -1 point for each opponent piece
        value += HeuristicFunction.piece_count(game_state) * HeuristicFunction.weights["piece_count"]

        # 3. Pieces near edge: can our pieces be pushed off soon, can we push off opponent pieces soon
        value += HeuristicFunction.pieces_near_edge(game_state) * HeuristicFunction.weights["pieces_near_edge"]

        # 4. Manhattan distance from center: +(4 - distance) player pieces, -(4 - distance) for opponent pieces
        value += HeuristicFunction.manhattan_distance(game_state) * \
                 HeuristicFunction.weights["manhattan_distance"]

        # 5. Clumping: get our pieces close together, spread out opponent pieces

        # 6. Sumito: how many sumito match ups are there, how many can we win

        # 7. Triples: number of triples we have, number of triples opponent has

        # 8. Doubles: number of doubles we have, number of doubles opponent has

        return value

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

    # TODO: This may not be necessary because having manhattan distance from center should cover this
    @staticmethod
    def pieces_near_edge(game_state) -> float:
        """
        For each player piece near the edge, add 1 point for the opponent, subtract 1 point for the player.

        :param game_state: the current game state
        :return: a float representing the value of the pieces near the edge
        """
        player_pieces = game_state.player_marble_positions
        opponent_pieces = game_state.opponent_marble_positions

        num_player_pieces_close = 0
        num_opponent_pieces_close = 0
        for player_position in player_pieces:
            num_player_pieces_close += 1 if HeuristicFunction.__is_close_to_edge(player_position) else 0
        for opponent_position in opponent_pieces:
            num_opponent_pieces_close += 1 if HeuristicFunction.__is_close_to_edge(opponent_position) else 0

        return float(num_opponent_pieces_close - num_player_pieces_close)

    @staticmethod
    def manhattan_distance(
            game_state: GameState
    ) -> float:
        player_value = 0
        opponent_value = 0
        for player_position in game_state.player_marble_positions:
            player_value += HeuristicFunction.__manhattan_distance_from_center(player_position)
        for opponent_position in game_state.opponent_marble_positions:
            opponent_value += HeuristicFunction.__manhattan_distance_from_center(opponent_position)

        # the smaller value the better
        # e.g. player distance = 2, opponent distance = 4, the value should be +2 because player is closer to the center
        return float(opponent_value - player_value)

    # Private helper functions
    @staticmethod
    def __is_close_to_edge(position: Position) -> bool:
        """
        If the position is within 2 spaces of the edge, return true, otherwise false.

        :param position: the position to check
        :return: True if the position is close to the edge, False otherwise
        """
        boundaries_in_this_row = HeuristicFunction.board_boundary_coords[position.y]
        min_distance_from_edge = min(
            [abs(position.x - boundary_x) for boundary_y, boundary_x in boundaries_in_this_row]
        )
        number_of_spaces_considered_close_to_edge = 2

        return min_distance_from_edge <= number_of_spaces_considered_close_to_edge

    @staticmethod
    def __manhattan_distance_from_center(position: Position) -> float:
        center_position_x, center_position_y = 4, 4
        return abs(position.x - center_position_x) + abs(position.y - center_position_y)
