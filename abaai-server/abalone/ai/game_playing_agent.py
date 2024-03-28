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
    DEFAULT_WEIGHTS = [1000000, 10000, 10, 10, 2, 2, 1,1]

    @classmethod
    def evaluate(cls, game_state: GameState) -> float:
        # Gets piece locations
        piece_locations = StateSpaceGenerator.get_player_piece_positions(game_state)
        player_piece_locations = piece_locations['player_max']
        opponent_piece_locations = piece_locations['player_min']
        board = game_state.board.array

        player_center_control = cls.number_near_center(board, game_state.turn.value)
        opp_value = 1
        if game_state.turn.value == 1:
            opp_value = 2
        opponent_center_control = cls.number_near_center(board, opp_value)

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
        score += current_weights[4] * cls.compactness(player_piece_locations)
        score += current_weights[4] * (player_center_control - opponent_center_control)


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

    @staticmethod
    def compactness(piece_locations: list[Position]) -> int:
        compactness_score = 0
        n = len(piece_locations)
        for i in range(n):
            for j in range(i + 1, n):
                piece1 = piece_locations[i]
                piece2 = piece_locations[j]
                distance = HeuristicFunction.hex_distance(piece1, piece2)
                compactness_score += distance
        return compactness_score

    @staticmethod
    def hex_distance(pos1: Position, pos2: Position) -> int:
        x1, y1, z1 = pos1.x, pos1.y, -pos1.x-pos1.y
        x2, y2, z2 = pos2.x, pos2.y, -pos2.x-pos2.y
        return (abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)) // 2

    @staticmethod
    def number_near_center(board: list[list[int]], player_num: int) -> int:
        center_row, center_col = len(board) // 2, len(board[0]) // 2
        count = 0
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == player_num:
                    if abs(row - center_row) <= 2 and abs(col - center_col) <= 2:
                        count += 1
        return count


def simulate_moves(game_state: GameState, max_moves: int):
    agent = MiniMaxAgent(max_depth=2)
    print("Initial Board")
    print_board(game_state.board)
    for i in range(max_moves):
        best_move = agent.get_best_move(game_state)
        print(f"{game_state.turn.name}->({best_move})")

        game_state = GameStateUpdate(game_state,best_move)

        print_board(game_state.resulting_state.board)


def print_board(board):

    for row in board.array:
        print(' '.join(str(cell) for cell in row))
    print()


simulate_moves(GameState(), 2)