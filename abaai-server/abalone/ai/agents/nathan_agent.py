from abalone.movement import Position
import time
from abalone.ai.state_space_generator import StateSpaceGenerator
from abalone.state import GameStateUpdate, GameState

class HeuristicFunction:
    DEFAULT_WEIGHTS = [-10000000, -100000, -20, -20, 2, 2]

    CENTER_WEIGHTS = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 2, 2, 2, 1, 0],
        [0, 0, 1, 2, 3, 3, 2, 1, 0],
        [0, 1, 2, 3, 4, 3, 2, 1, 0],
        [0, 1, 2, 3, 3, 2, 1, 0, 0],
        [0, 1, 2, 2, 2, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    @classmethod
    def evaluate(cls, game_state: GameState) -> float:
        # Gets piece locations
        piece_locations = StateSpaceGenerator.get_player_piece_positions(game_state)
        player_piece_locations = piece_locations['player_max']
        opponent_piece_locations = piece_locations['player_min']

        # Assign weights to each criterion
        # 1. Win condition
        # 2. Value per piece
        # 3. Player distance to center
        # 4. Opponent distance to center
        # 5. How condensed player pieces are
        # 6. How condensed opponent pieces are
        current_weights = cls.DEFAULT_WEIGHTS

        score = 0
        score += current_weights[0] * cls.win_condition(game_state)
        score += current_weights[1] * cls.piece_value(player_piece_locations, opponent_piece_locations)

        center_score = cls.center_distance(player_piece_locations, opponent_piece_locations)
        score += current_weights[2] * center_score[0]
        score -= current_weights[3] * center_score[1]

        condensed_score = cls.piece_condensed(player_piece_locations, opponent_piece_locations)
        score += current_weights[4] * condensed_score[0]
        score -= current_weights[5] * condensed_score[1]

        return score

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

    @classmethod
    def center_distance(cls, player_piece_locations: list[Position], opponent_piece_locations: list[Position]) -> list:
        player_sum = 0
        opp_sum = 0
        for location in player_piece_locations:
            player_sum += cls.CENTER_WEIGHTS[location.y][location.x]
        for location in opponent_piece_locations:
            opp_sum += cls.CENTER_WEIGHTS[location.y][location.x]
        return [player_sum, opp_sum]

    @staticmethod
    def piece_condensed(player_piece_locations: list[Position], opponent_piece_locations: list[Position]) -> list:
        player_sum = 0
        opp_sum = 0
        player_set = set((location.x, location.y) for location in player_piece_locations)
        opp_set = set((location.x, location.y) for location in opponent_piece_locations)

        for position in player_piece_locations:
            x, y = position.x, position.y
            for coordinate in [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (-1, -1)]:
                if (x + coordinate[0], y + coordinate[1]) in player_set:
                    player_sum += 1

        for position in opponent_piece_locations:
            x, y = position.x, position.y
            for coordinate in [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (-1, -1)]:
                if (x + coordinate[0], y + coordinate[1]) in opp_set:
                    opp_sum += 1

        return [player_sum, opp_sum]




class MiniMaxAgent:
    def __init__(self, max_depth: int):
        self.max_depth = max_depth

    def minimax_search(self, game_state: GameState):
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for move in sorted(StateSpaceGenerator.generate_all_possible_moves(game_state)):
            successor_state = GameStateUpdate(game_state, move).resulting_state
            value = self.min_value(successor_state, alpha, beta, self.max_depth - 1)
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, value)

        return best_move

    def max_value(self, game_state: GameState, alpha: float, beta: float, depth: int):
        if game_state.is_game_over() or depth == 0:
            return HeuristicFunction.evaluate(game_state)

        value = float('-inf')
        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        for move in sorted(possible_moves):
            successor_state = GameStateUpdate(game_state, move).resulting_state
            value = max(value, self.min_value(successor_state, alpha, beta, depth - 1))
            alpha = max(alpha, value)
            if value >= beta:
                break
        return value

    def min_value(self, game_state: GameState, alpha: float, beta: float, depth: int):
        if game_state.is_game_over() or depth == 0:
            return HeuristicFunction.evaluate(game_state)

        value = float('inf')
        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        for move in sorted(possible_moves):
            successor_state = GameStateUpdate(game_state, move).resulting_state
            value = min(value, self.max_value(successor_state, alpha, beta, depth - 1))
            beta = min(beta, value)
            if value <= alpha:
                break
        return value


def simulate_moves(game_state: GameState, max_moves: int):
    agent = MiniMaxAgent(max_depth=3)
    print("Initial Board")
    print(game_state.board)
    game_state = game_state
    i = 0
    start_time = time.time()
    while i < max_moves:
        best_move = agent.minimax_search(game_state)
        print(f"{game_state.turn.name}->({best_move})")
        game_state = GameStateUpdate(game_state, best_move).resulting_state
        i += 1
    finish_time = time.time()
    print(finish_time - start_time)
    print(game_state.board)
    print(game_state.remaining_player_marbles)
    print(game_state.remaining_opponent_marbles)
