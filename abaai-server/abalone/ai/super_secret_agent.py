import time


from abalone.ai.state_space_generator import StateSpaceGenerator
from abalone.state import GameStateUpdate, GameState


class AlphaBetaPruningAgent:
    def __init__(self, max_depth: int):
        self.max_depth = max_depth
        self.max_player = None
        self.min_prunes = 0
        self.max_prunes = 0

    def sort_moves(self,game_state, possible_moves):
        scored_moves = []
        for move in possible_moves:
            successor_state = GameStateUpdate(game_state, move).resulting_state
            move_score = evaluate(successor_state)
            scored_moves.append((move_score, move))
        scored_moves.sort(reverse=True)
        return [move for score, move in scored_moves]

    def AlphaBetaPruningSearch(self, game_state: GameState):
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        sorted_possible_moves = self.sort_moves(game_state, possible_moves)
        print(len(sorted_possible_moves))
        for move in sorted_possible_moves:
            successor_state = GameStateUpdate(game_state, move).resulting_state
            value = self.Min_Value(successor_state, alpha, beta, self.max_depth - 1)
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, value)
        print(f'{game_state.turn.name}->{best_value} First')
        print(f'Max Prunes: {self.max_prunes}')
        print(f'Min Prunes: {self.min_prunes}')
        return best_move

    # def AlphaBetaPruningSearch(self, game_state: GameState):
    #     best_move = None
    #     self.max_player = game_state.turn.value
    #     best_value = float('-inf') if game_state.turn.value == self.max_player else float('inf')
    #     alpha = float('-inf')
    #     beta = float('inf')
    #
    #     possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
    #     sorted_possible_moves = self.sort_moves(game_state, possible_moves)
    #
    #     for move in sorted_possible_moves:
    #         successor_state = GameStateUpdate(game_state, move).resulting_state
    #         value = self.Value(successor_state, alpha, beta, self.max_depth - 1)
    #
    #         if game_state.turn.value == self.max_player:
    #             if value > best_value:
    #                 best_value = value
    #                 best_move = move
    #             alpha = max(alpha, value)
    #         else:
    #             if value < best_value:
    #                 best_value = value
    #                 best_move = move
    #             beta = min(beta, value)
    #
    #     return best_move
    # def Value(self, game_state: GameState, alpha: float, beta: float, depth: int):
    #     if game_state.is_game_over() or depth == 0:
    #         return evaluate(game_state)
    #     value = float('-inf') if game_state.turn.value == self.max_player else float('inf')
    #
    #     possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
    #     sorted_moves = self.sort_moves(game_state, possible_moves)
    #     for move in sorted_moves:
    #         successor_state = GameStateUpdate(game_state, move).resulting_state
    #         # Since turns are updated, we keep maximizing relative to the current player
    #         successor_value = self.Value(successor_state, alpha, beta, depth - 1)
    #
    #         if game_state.turn.value == self.max_player:
    #             value = max(value, successor_value)
    #             alpha = max(alpha, value)
    #             if value >= beta:
    #                 break  # Beta cutoff
    #         else:
    #             value = min(value, successor_value)
    #             beta = min(beta, value)
    #             if value <= alpha:
    #                 break  # Alpha cutoff
    #
    #     return value

    def Max_Value(self, game_state: GameState, alpha: float, beta: float, depth: int):
        if game_state.is_game_over() or depth == 0:
            return evaluate(game_state) * -1
        value = float('-inf')
        best_value = float('-inf')
        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        sorted_possible_moves = self.sort_moves(game_state, possible_moves)
        for move in sorted_possible_moves:
            successor_state = GameStateUpdate(game_state, move).resulting_state
            value = max(value, self.Min_Value(successor_state, alpha, beta, depth - 1))
            alpha = max(alpha, value)
            if value > best_value:
                best_value = value
            if value >= beta:
                self.max_prunes += 1
                break

        return value

    def Min_Value(self, game_state: GameState, alpha: float, beta: float, depth: int):
        if game_state.is_game_over() or depth == 0:
            return evaluate(game_state)
        value = float('inf')
        best_value = float('inf')
        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        sorted_possible_moves = self.sort_moves(game_state, possible_moves)
        for move in sorted_possible_moves:
            successor_state = GameStateUpdate(game_state, move).resulting_state
            value = min(value, self.Max_Value(successor_state, alpha, beta, depth - 1))
            beta = min(beta, value)
            if value < best_value:
                best_value = value
            if value <= alpha:
                self.min_prunes += 1
                break
        return value


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
    None, None, None, None, (4, -4), (5, -4), (6, -4), (7, -4), (8, -4),
    None, None, None, (2, -3), (3, -3), (4, -3), (5, -3), (6, -3), (7, -3),
    None, None, (0, -2), (1, -2), (2, -2), (3, -2), (4, -2), (5, -2), (6, -2),
    None, (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1), (4, -1), (5, -1),
    (-4, 0), (-3, 0), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
    (-3, 1), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), None,
    (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), None, None,
    (-1, 3), (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), None, None, None,
    (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), None, None, None, None]




def evaluate(game_state: GameState) -> float:
    score = 0
    score += 10 * manhattan_distance(game_state, MANHATTAN_WEIGHT_CONVERTED)
    score += 10000 * marbles_knocked_off(game_state)
    score += 10000000 * terminal_test(game_state)
    return score


def flat_index_to_hex(index):
    row = index // 9
    column = index % 9

    row_offset = max(0, 4 - abs(4 - row))
    q = column - row_offset
    r = row - 4

    return q, r


# def hex_distance(hex_a, hex_b):
#     x1, y1, z1 = qr_to_cube(hex_a)
#     x2, y2, z2 = qr_to_cube(hex_b)
#     return (abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)) // 2


# def qr_to_cube(hex):
#     q, r = hex
#     x = q
#     z = r
#     y = -x - z
#     return x, y, z

def cube_distance(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))


def manhattan_distance(game_state, hex_lookup_table):
    player_score = 0
    opponent_score = 0
    center_cube_coords = (0, 0, 0)

    for index, value in enumerate(game_state.board.array):
        if value in (game_state.turn.value, 2 if game_state.turn.value == 1 else 1):
            hex_coords = hex_lookup_table[index]
            if hex_coords:
                cube_coords = (hex_coords[0], -hex_coords[0] - hex_coords[1], hex_coords[1])
                distance = cube_distance(cube_coords, center_cube_coords)
                if value == game_state.turn.value:
                    player_score += distance
                else:
                    opponent_score += distance

    return player_score - opponent_score

def marbles_knocked_off(game_state):
    return game_state.remaining_player_marbles - game_state.remaining_opponent_marbles
def terminal_test(game_state: GameState):

    if game_state.remaining_player_marbles < 9:
        return -10000
    if game_state.remaining_opponent_marbles < 9:
        return 10000
    return 0
def simulate_moves(game_state: GameState, max_moves: int):
    agent = AlphaBetaPruningAgent(max_depth=3)
    print("Initial Board")
    print(game_state.board)
    game_state = game_state
    i = 0
    start_time = time.time()
    while i < max_moves:
        best_move = agent.AlphaBetaPruningSearch(game_state)
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


#
#
# def generate_hex_lookup_table():
#     lookup_table = []
#     for row in range(9):
#         for column in range(9):
#             # Calculate row offset for hexagonal layout
#             row_offset = max(0, 4 - abs(4 - row))
#             # Adjust for hexagonal grid coordinates
#             q = column - row_offset
#             r = row - 4
#             # Append the calculated hex coordinates to the lookup table
#             # Only include valid positions (not out of bounds)
#             if not (row < 4 and column < 4 - row) and not (row > 4 and column > 13 - row):
#                 lookup_table.append((q, r))
#             else:
#                 lookup_table.append(None)  # Mark out-of-bounds positions as None
#     return lookup_table


# print(generate_hex_lookup_table())
# simulate_moves(GameState(), 50)
agent = AlphaBetaPruningAgent(max_depth=3)
current_time = time.time()
best_move = agent.AlphaBetaPruningSearch(GameState())
finish_time = time.time()
print(finish_time - current_time)
print(best_move)
