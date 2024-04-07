import time
from itertools import combinations

from abalone.movement_optimized import Move
from abalone.state import GameState, GameStateUpdate

cdef class LegalMovesOptimized:
    possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, -1), (-1, 1)]

    @staticmethod
    cdef inline int get_flat_index(int x, int y) nogil:
        return y * 9 + x if (0 <= x < 9) and (0 <= y < 9) else -1

    @staticmethod
    cdef bint are_two_marbles_inline(tuple[int, int] pos1, tuple[int, int] pos2):
        cdef int dx = pos2[0] - pos1[0]
        cdef int dy = pos2[1] - pos1[1]
        cdef tuple direction = (dx, dy)
        return direction in [(-1, 0), (1, 0), (0, -1), (0, 1), (1, -1), (-1, 1)]

    @staticmethod
    cdef bint are_three_marbles_inline(tuple[int, int] pos1, tuple[int, int] pos2, tuple[int, int] pos3):
        cdef int dx1 = pos2[0] - pos1[0]
        cdef int dy1 = pos2[1] - pos1[1]
        cdef tuple direction1 = (dx1, dy1)

        cdef int dx2 = pos3[0] - pos2[0]
        cdef int dy2 = pos3[1] - pos2[1]
        cdef tuple direction2 = (dx2, dy2)

        return direction1 == direction2 and direction1 in [(-1, 0), (1, 0), (0, -1), (0, 1), (1, -1), (-1, 1)]

    @staticmethod
    cdef bint is_position_valid(list[int] board, position, vacating_positions=None):
        """Combined checks for board position status with static typing."""
        cdef int index = LegalMovesOptimized.get_flat_index(position[0], position[1])
        if index == -1 or board[index] == -1:
            return False

        if vacating_positions is None:
            vacating_positions = []

        return board[index] == 0 or position in vacating_positions

    @staticmethod
    def get_valid_moves(game_state: GameState, *positions: list[tuple[int, int]]):
        cdef int move_x, move_y
        cdef int pos_x, pos_y
        cdef list valid_moves = []
        cdef new_positions = []

        board = game_state.board.array

        if len(positions) == 2:
            if not LegalMovesOptimized.are_two_marbles_inline(positions[0], positions[1]):
                return []
        elif len(positions) == 3:
            if not LegalMovesOptimized.are_three_marbles_inline(positions[0], positions[1], positions[2]):
                return []

        for move_x, move_y in LegalMovesOptimized.possible_moves:
            new_positions = [(pos[0] + move_x, pos[1] + move_y) for pos in positions]
            if all(LegalMovesOptimized.is_position_valid(board, pos, positions) for pos in new_positions):
                valid_moves.append(Move(list(positions), new_positions, game_state.turn))

        return valid_moves

    @staticmethod
    cdef bint sequence_helper_function(list[int] board, tuple[int, int] position):
        cdef int index = LegalMovesOptimized.get_flat_index(position[0], position[1])
        if index == -1 or board[index] == -1 or board[index] == 0:
            return True
        return False

    @staticmethod
    cdef bint is_position_out_of_bounds(list[int]board, position):
        """Check if a position is out of bounds."""
        cdef int index = LegalMovesOptimized.get_flat_index(position[0], position[1])
        if index == -1 or board[index] == -1:
            return True

    @staticmethod
    cdef bint can_sumito_occur(dict sequence, tuple direction, list[int] board):
        cdef tuple last_opponent_pos
        cdef tuple push_target_pos
        cdef int sequence_length_player
        cdef int sequence_length_opponent

        if not sequence['opponent']:
            return False

        sequence_length_player = len(sequence['player'])
        sequence_length_opponent = len(sequence['opponent'])
        if sequence_length_player <= sequence_length_opponent:
            return False

        last_opponent_pos = sequence['opponent'][-1]
        push_target_pos = (last_opponent_pos[0] + direction[0], last_opponent_pos[1] + direction[1])
        return LegalMovesOptimized.sequence_helper_function(board, push_target_pos)

    @staticmethod
    cdef dict find_marble_sequence(list[int] board, tuple start_pos, tuple direction, list player_positions,
                                   list opponent_positions):
        cdef list player_seq = []
        cdef list opponent_seq = []
        cdef tuple current_pos = start_pos
        cdef tuple next_pos
        cdef bint sequence_found = False

        for _ in range(3):
            if current_pos in player_positions:
                player_seq.append(current_pos)
                next_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
                if next_pos in opponent_positions:
                    sequence_found = True
                    current_pos = next_pos
                    break
                elif LegalMovesOptimized.sequence_helper_function(board, next_pos):
                    break
                current_pos = next_pos
            else:
                break

        while sequence_found and current_pos in opponent_positions:
            opponent_seq.append(current_pos)
            next_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
            if LegalMovesOptimized.sequence_helper_function(board, next_pos):
                break
            current_pos = next_pos

        return {'player': player_seq, 'opponent': opponent_seq} if sequence_found else None

    @staticmethod
    def generate_all_sumitos(game_state, player_positions, opponent_positions):
        board = game_state.board.array
        sumito_move_list = []
        for start_pos in player_positions:
            for direction in LegalMovesOptimized.possible_moves:
                sequence = LegalMovesOptimized.find_marble_sequence(board, start_pos, direction, player_positions,
                                                                    opponent_positions)
                if sequence and LegalMovesOptimized.can_sumito_occur(sequence, direction, board):
                    new_positions_player = [(pos[0] + direction[0], pos[1] + direction[1]) for pos in
                                            sequence['player']]
                    new_positions_opponent = [(pos[0] + direction[0], pos[1] + direction[1]) for pos in
                                              sequence['opponent']
                                              if not LegalMovesOptimized.is_position_out_of_bounds(board, (
                        pos[0] + direction[0],
                        pos[1] + direction[1]))]

                    sumito_move_list.append(Move(
                        sequence['player'],
                        new_positions_player,
                        game_state.turn,
                        sequence['opponent'],
                        new_positions_opponent)
                    )

        return sumito_move_list

cdef class StateSpaceGenerator:
    cdef int width
    cdef list[int] board_array

    @staticmethod
    def get_player_piece_positions(game_state: GameState):
        cdef:
            int player_max_value = game_state.turn.value
            int player_min_value = 2 if player_max_value == 1 else 1
            dict player_dict = {"player_max": player_max_value, "player_min": player_min_value}
            list player_max_piece_positions = []
            list player_min_piece_positions = []
            int index, x, y
            int width = 9
            int array_length = len(game_state.board.array)

        for index in range(array_length):
            if game_state.board.array[index] == player_max_value:
                x = index % width
                y = index // width
                player_max_piece_positions.append((x, y))
            elif game_state.board.array[index] == player_min_value:
                x = index % width
                y = index // width
                player_min_piece_positions.append((x, y))

        player_dict["player_max"] = player_max_piece_positions
        player_dict["player_min"] = player_min_piece_positions

        return player_dict

    @staticmethod
    def generate_all_moves(game_state: GameState, dict player_piece):
        cdef:
            int turn_value = game_state.turn.value
            list possible_move_list = []
            list moves
            list positions

        if game_state.turn.value == 1:
            black_positions = player_piece['player_max']
            white_positions = player_piece['player_min']
        else:
            black_positions = player_piece['player_min']
            white_positions = player_piece['player_max']

        all_moves = {"max": black_positions if turn_value == 1 else white_positions}

        for color, positions in all_moves.items():
            for pos in positions:
                moves = LegalMovesOptimized.get_valid_moves(game_state, pos)
                if moves:
                    possible_move_list.extend(moves)
            for pos1, pos2 in combinations(positions, 2):
                moves = LegalMovesOptimized.get_valid_moves(game_state, pos1, pos2)
                if moves:
                    possible_move_list.extend(moves)

            for pos1, pos2, pos3 in combinations(positions, 3):
                moves = LegalMovesOptimized.get_valid_moves(game_state, pos1, pos2, pos3)
                if moves:
                    possible_move_list.extend(moves)

        return possible_move_list

    @staticmethod
    def generate_all_sumitos(game_state, player_pieces) -> list[Move]:
        max_positions = player_pieces["player_max"]
        min_positions = player_pieces["player_min"]
        return LegalMovesOptimized.generate_all_sumitos(game_state, max_positions, min_positions)

    @staticmethod
    def generate_all_possible_moves(game_state) -> list[Move]:
        player_pieces = StateSpaceGenerator.get_player_piece_positions(game_state)

        player_piece_moves = StateSpaceGenerator.generate_all_moves(game_state, player_pieces)
        sumito_moves = StateSpaceGenerator.generate_all_sumitos(game_state, player_pieces)

        return player_piece_moves + sumito_moves

cdef class alphaBetaPruningAgent:
    cdef public int max_depth, max_time_sec
    cdef public int min_prunes, max_prunes
    cdef public int MAX_PLAYER, MIN_PLAYER
    cdef public game_state
    def __init__(self, game_state, int max_depth, int max_time_sec=50):
        self.max_depth = max_depth
        self.max_time_sec = max_time_sec
        self.game_state = game_state
        self.MAX_PLAYER = game_state.turn.value
        self.MIN_PLAYER = 3 - game_state.turn.value

    def AlphaBetaPruningSearch(self):
        cdef float alpha = float('-inf')
        cdef float beta = float('inf')
        cdef float value
        cdef list possible_moves
        cdef float start_time

        best_move = None

        start_time = time.time()
        game_state = self.game_state
        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        sorted_possible_moves = sorted(possible_moves)

        for move in sorted_possible_moves:
            successor_state = GameStateUpdate(game_state, move).resulting_state
            value = self.Min_Value(successor_state, alpha, beta, self.max_depth - 1, start_time)
            if value > alpha:
                best_move = move
                alpha = max(alpha, value)

        return best_move

    def Max_Value(self, game_state, alpha: float, beta: float, depth: int, start_time: float):
        cdef float current_time = time.time()
        cdef float value = float('-inf')
        cdef list possible_moves
        if current_time - start_time >= self.max_time_sec:
            return self.evaluate(game_state)

        if game_state.is_game_over() or depth == 0:
            return self.evaluate(game_state)

        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        sorted_possible_moves = sorted(possible_moves)

        for move in sorted_possible_moves:
            successor_state = GameStateUpdate(game_state, move).resulting_state
            value = max(value, self.Min_Value(successor_state, alpha, beta, depth - 1, start_time))
            alpha = max(alpha, value)
            if value >= beta:
                return value

        return value

    def Min_Value(self, game_state, alpha: float, beta: float, depth: int, start_time: float):
        cdef float current_time = time.time()
        cdef float value = float('inf')
        cdef list possible_moves
        if current_time - start_time >= self.max_time_sec:
            return self.evaluate(game_state)

        if game_state.is_game_over() or depth == 0:
            return self.evaluate(game_state)

        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        sorted_possible_moves = sorted(possible_moves)

        for move in sorted_possible_moves:
            successor_state = GameStateUpdate(game_state, move).resulting_state
            value = min(value, self.Max_Value(successor_state, alpha, beta, depth - 1, start_time))
            beta = min(beta, value)
            if value <= alpha:
                return value
        return value

    cdef double evaluate(self, game_state: GameState):
        cdef double score = 0
        score += 10 * self.board_control(game_state, MANHATTAN_WEIGHT_CONVERTED)
        score += 1000 * self.piece_advantage(game_state)
        score += 10000000 * self.terminal_test(game_state)
        return score

    cdef int board_control(self, game_state: GameState, list[tuple[int, int]] lookup_table):
        cdef int player_score = 0
        cdef int opponent_score = 0
        cdef int index
        cdef int value
        cdef tuple hex_coords
        cdef int distance

        for index in range(len(game_state.board.array)):
            value = game_state.board.array[index]
            if value == 1 or value == 2:
                hex_coords = lookup_table[index]
                if hex_coords is not None:
                    distance = abs(hex_coords[0]) + abs(hex_coords[1])
                    if value == self.MAX_PLAYER:
                        player_score += distance
                    else:
                        opponent_score += distance

        return opponent_score - player_score

    cdef piece_advantage(self, game_state):
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

    cpdef int terminal_test(self, game_state: GameState):
        if game_state.turn.value == self.MAX_PLAYER:
            if game_state.remaining_player_marbles < 9:
                return -10000
            if game_state.remaining_opponent_marbles < 9:
                return 10000
        else:
            if game_state.remaining_opponent_marbles < 9:
                return -10000
            if game_state.remaining_player_marbles < 9:
                return 10000
        return 0  #
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
