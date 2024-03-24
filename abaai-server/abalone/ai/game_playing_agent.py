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
            return HeuristicFunction.evaluate(game_state)

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
    DEFAULT_WEIGHTS = [1000000, 10000, 10, 10, 2, 2, 1]

    @classmethod
    def evaluate(cls, game_state: GameState) -> float:
        # Gets piece locations
        piece_locations = StateSpaceGenerator.get_player_piece_positions(game_state)
        player_piece_locations = piece_locations['player_max']
        opponent_piece_locations = piece_locations['opponent_max']

        # Assign weights to each criterion
        # 1. Win condition
        # 2. Value per piece
        # 3. Player distance to center
        # 4. Opponent distance to edge
        # 5. How condensed player pieces are
        # 6. How split opponent pieces are
        # 7. Number of possible sumitos
        current_weights = cls.DEFAULT_WEIGHTS

        score = 0
        score += current_weights[0] * cls.win_condition(game_state)
        score += current_weights[1] * cls.piece_value(player_piece_locations, opponent_piece_locations)

    @staticmethod
    def win_condition(game_state: GameState) -> int:
        if game_state.is_game_over():
            if game_state.remaining_player_marbles <= 8:
                return 1
            return -1
        return 0

    @staticmethod
    def piece_value(player_piece_locations: list[Position], opponent_piece_locations: list[Position]) -> int:
        player_pieces = len(player_piece_locations)
        opponent_pieces = len(opponent_piece_locations)
        return player_pieces - opponent_pieces


