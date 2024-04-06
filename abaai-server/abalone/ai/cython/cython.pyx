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
    cdef is_position_valid(list[int] board, position, vacating_positions=None):
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