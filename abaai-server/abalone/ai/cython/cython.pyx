from abalone.movement_optimized import Move
from abalone.state import GameState

cdef class LegalMovesOptimized:
    possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, -1), (-1, 1)]

    @staticmethod
    cdef inline int get_flat_index(int x, int y) nogil:
        return y * 9 + x if (0 <= x < 9) and (0 <= y < 9) else -1

    @staticmethod
    def are_marbles_inline(*positions):
        """Check inline marbles with streamlined direction check."""
        cdef int num_positions = len(positions)
        cdef int dx, dy
        cdef int i
        cdef tuple direction

        if num_positions < 2:
            return False

        dx = positions[1][0] - positions[0][0]
        dy = positions[1][1] - positions[0][1]
        direction = (dx, dy)

        for i in range(1, num_positions - 1):
            if (positions[i + 1][0] - positions[i][0], positions[i + 1][1] - positions[i][1]) != direction:
                return False

        return direction in [(-1, 0), (1, 0), (0, -1), (0, 1), (1, -1), (-1, 1)]


    @staticmethod
    cdef is_position_valid(list[int] board, position, vacating_positions=None):
        """Combined checks for board position status with static typing."""
        cdef int index
        cdef int x = position[0]
        cdef int y = position[1]

        # Utilize the statically typed flat index calculation method
        index = LegalMovesOptimized.get_flat_index(x, y)
        if index == -1 or board[index] == -1:
            return False

        # Convert Python None to an empty C++ vector if needed
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

        if len(positions) > 1 and not LegalMovesOptimized.are_marbles_inline(*positions):
            return []

        for move_x, move_y in LegalMovesOptimized.possible_moves:
            new_positions = [(pos[0] + move_x, pos[1] + move_y) for pos in positions]
            if all(LegalMovesOptimized.is_position_valid(board, pos, positions) for pos in new_positions):
                valid_moves.append(Move(list(positions), new_positions, game_state.turn))

        return valid_moves