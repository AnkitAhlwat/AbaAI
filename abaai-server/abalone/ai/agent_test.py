import time

from abalone.ai.state_space_generator import StateSpaceGenerator
from abalone.board_opt import BoardLayout, OptimizedBoard, Piece
from abalone.test import GameStateUpdate, GameState


class AlphaBetaPruningAgent:
    def __init__(self, max_depth: int):
        self.max_depth = max_depth
        # self.max_player = None
        self.min_prunes = 0
        self.max_prunes = 0

    def alphabeta_pruning_search(self, game_state: GameState):
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

    def max_value(self, game_state: GameState, alpha: float, beta: float, depth: int):
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
            value = min(value, self.max_value(successor_state, alpha, beta, depth - 1))
            beta = min(beta, value)
            if value <= alpha:
                self.min_prunes += 1
                return value
        return value


SCORE_MAP = [
    -1, -1, -1, -1, 0, 1, 1, 1, 0,
    -1, -1, -1, 1, 2, 2, 2, 2, 1,
    -1, -1, 1, 2, 4, 4, 4, 2, 1,
    -1, 1, 2, 4, 8, 8, 4, 2, 1,
    0, 2, 4, 8, 16, 8, 4, 2, 0,
    1, 2, 4, 8, 8, 4, 2, 1, -1,
    1, 2, 4, 4, 4, 2, 1, -1, -1,
    1, 2, 2, 2, 2, 1, -1, -1, -1,
    0, 1, 1, 1, 0, -1, -1, -1, -1
]


def evaluate(game_state: GameState) -> float:
    score = 0
    score += 50 * distance_to_center(game_state)
    score += 20 * threes_in_a_row(game_state)
    score += 1000 * piece_advantage(game_state)
    return score


def distance_to_center(game_state: GameState):
    total_score = 0

    for index, cell in enumerate(game_state.board.array):
        if cell in (1, 2):
            total_score += SCORE_MAP[index]
    return total_score


def piece_advantage(game_state):
    return game_state.remaining_player_marbles - game_state.remaining_opponent_marbles


def terminal_test(game_state: GameState):
    if game_state.remaining_player_marbles < 9:
        return -10000
    if game_state.remaining_opponent_marbles < 9:
        return 10000
    return 0


def threes_in_a_row(game_state: GameState) -> int:
    board = game_state.board.array
    board_2d = [board[i:i + 9] for i in range(0, len(board), 9)]

    player = game_state.turn.value
    player_threes = count_threes_in_a_row(board_2d, player)
    opponent = 3 - player
    opponent_threes = count_threes_in_a_row(board_2d, opponent)
    return player_threes - opponent_threes


def count_threes_in_a_row(board_2d, player):
    count = 0
    width, height = 9, 9
    directions = [(1, 0), (0, 1), (-1, 1)]

    def is_valid_coord(x, y):
        return 0 <= x < width and 0 <= y < height and board_2d[y][x] != -1

    def check_sequence(x, y, dx, dy):
        nonlocal count
        sequence = 0
        for i in range(4):
            nx, ny = x + dx * i, y + dy * i
            if is_valid_coord(nx, ny) and board_2d[ny][nx] == player:
                if i < 3:
                    sequence += 1
                else:
                    return
            else:
                if sequence == 3:
                    count += 1
                return

    for y in range(height):
        for x in range(width):
            if board_2d[y][x] == player:
                for dx, dy in directions:
                    check_sequence(x, y, dx, dy)

    return count




