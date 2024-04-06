from abalone.movement_optimized import Move
from abalone.state import GameState

cdef class LegalMovesOptimized:
    possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, -1), (-1, 1)]

    @staticmethod
    cdef inline int get_flat_index(int x, int y) nogil:
        return y * 9 + x if (0 <= x < 9) and (0 <= y < 9) else -1

    @staticmethod
    cdef bint are_two_marbles_inline(tuple[int,int] pos1, tuple[int,int] pos2):
        cdef int dx = pos2[0] - pos1[0]
        cdef int dy = pos2[1] - pos1[1]
        cdef tuple direction = (dx, dy)
        return direction in [(-1, 0), (1, 0), (0, -1), (0, 1), (1, -1), (-1, 1)]

    @staticmethod
    cdef bint are_three_marbles_inline(tuple[int,int] pos1, tuple[int,int] pos2, tuple[int,int] pos3):
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
    def get_valid_moves(game_state:GameState, *positions:list[tuple[int, int]]):
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
    cdef bint sequence_helper_function(int[:] board, tuple[int,int] position) nogil:
        cdef int index = LegalMovesOptimized.get_flat_index(position[0], position[1])
        if index == -1 or board[index] == -1 or board[index] == 0:
            return True
        return False

    @staticmethod
    cdef bint can_sumito_occur(dict sequence, tuple direction, int[:] board):
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

        # Determine the position to push onto and check its validity
        last_opponent_pos = sequence['opponent'][-1]
        push_target_pos = (last_opponent_pos[0] + direction[0], last_opponent_pos[1] + direction[1])
        return LegalMovesOptimized.sequence_helper_function(board, push_target_pos)

    @staticmethod
    cdef dict find_marble_sequence(int[:] board, tuple start_pos, tuple direction, list player_positions, list opponent_positions):
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

        # Return the sequences if found, else None
        return {'player': player_seq, 'opponent': opponent_seq} if sequence_found else None

    @staticmethod
    def generate_all_sumitos(game_state, player_positions, opponent_positions):
        """Generate all possible Sumitos given the current board state."""
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
                                              if LegalMovesOptimized.is_position_valid(board,(pos[0] + direction[0],
                                                                                                   pos[1] + direction[1]))]

                    sumito_move_list.append(Move(
                        sequence['player'],
                        new_positions_player,
                        game_state.turn,
                        sequence['opponent'],
                        new_positions_opponent)
                    )

        return sumito_move_list