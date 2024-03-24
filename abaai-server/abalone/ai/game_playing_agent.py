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

    def evaluate(self, game_state: GameState) -> float:
        # NOTE: Any function that is a good thing will add to value, bad things will subtract from value
        value = 0

        # Get the positions of the min and max player pieces
        player_piece_positions = StateSpaceGenerator.get_player_piece_positions(game_state)
        max_player_piece_positions = player_piece_positions["player_max"]
        min_player_piece_positions = player_piece_positions["player_min"]

        # 1. Terminal state: if player won large positive, if opponent won small negative, if game not over 0
        value += MiniMaxAgent.terminal_state(game_state)

        # 2. Piece counts: 1 point for each player piece, -1 point for each opponent piece
        value += MiniMaxAgent.piece_counts(game_state)

        # 3. Pieces near edge: can our pieces be pushed off soon, can we push off opponent pieces soon

        # 4. Manhattan distance from center: +(4 - distance) player pieces, -(4 - distance) for opponent pieces
        value += MiniMaxAgent.manhattan_distance(max_player_piece_positions, min_player_piece_positions)

        # 5. Clumping: get our pieces close together, spread out opponent pieces

        # 6. Sumito: how many sumito match ups are there, how many can we win

        # 7. Triples: number of triples we have, number of triples opponent has

        # 8. Doubles: number of doubles we have, number of doubles opponent has

        return value

    # Heuristic functions
    @staticmethod
    def terminal_state(game_state):
        """
        If the current player won return a large positive value, if the opponent won return a small negative value,
        if the game is not over yet, return 0.

        :param game_state: the current game state
        :return: a float representing the value of the terminal state
        """
        starting_marble_count = 14
        num_marbles_pushed_off_to_win = 6
        loser_marble_count = starting_marble_count - num_marbles_pushed_off_to_win

        # if the player wins
        if game_state.remaining_opponent_marbles <= loser_marble_count:
            return 100_000
        # if the opponent wins
        elif game_state.remaining_player_marbles <= loser_marble_count:
            return -100_000
        # if the game is not over yet
        else:
            return 0

    @staticmethod
    def piece_counts(game_state):
        """
        For each player piece, add 1 point, for each opponent piece, subtract 1 point.

        :param game_state: the current game state
        :return: a float representing the value of the piece counts
        """
        return game_state.remaining_player_marbles - game_state.remaining_opponent_marbles

    @staticmethod
    def manhattan_distance(
            player_piece_positions: list[Position],
            opponent_piece_positions: list[Position]
    ) -> float:
        player_value = 0
        opponent_value = 0
        for player_position in player_piece_positions:
            player_value += MiniMaxAgent.__manhattan_distance_from_center(player_position)
        for opponent_position in opponent_piece_positions:
            opponent_value += MiniMaxAgent.__manhattan_distance_from_center(opponent_position)

        # the smaller value the better
        # e.g. player distance = 2, opponent distance = 4, the value should be +2 because player is closer to the center
        return float(opponent_value - player_value)

    # Private helper functions
    @staticmethod
    def __manhattan_distance_from_center(position: Position):
        center_position_x, center_position_y = 4, 4
        return abs(position.x - center_position_x) + abs(position.y - center_position_y)
