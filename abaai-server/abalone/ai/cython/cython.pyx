from abalone.movement import Position, Move


class LegalMovesOptimized:
    possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, -1), (-1, 1)]

    @staticmethod
    def get_flat_index(x, y):
        """Simplified bounds check integrated."""
        return y * 9 + x if 0 <= x < 9 and 0 <= y < 9 else -1

    @staticmethod
    def are_marbles_inline(*positions):
        """Check inline marbles with streamlined direction check."""
        if len(positions) < 2:
            return False
        direction = (positions[1].x - positions[0].x, positions[1].y - positions[0].y)
        return all((positions[i + 1].x - positions[i].x, positions[i + 1].y - positions[i].y) == direction
                   for i in range(len(positions) - 1)) and direction in LegalMovesOptimized.possible_moves

    @staticmethod
    def is_position_valid(board, position, vacating_positions=None):
        """Combined checks for board position status."""
        index = LegalMovesOptimized.get_flat_index(position.x, position.y)
        if index == -1 or board[index] == -1:
            return False
        return board[index] == 0 or position in vacating_positions

    @staticmethod
    def get_valid_moves(game_state, *positions):
        """Optimized move validation."""
        if len(positions) > 1 and not LegalMovesOptimized.are_marbles_inline(*positions):
            return []

        board = game_state.board.array
        valid_moves = []

        for move_x, move_y in LegalMovesOptimized.possible_moves:
            new_positions = [Position(pos.x + move_x, pos.y + move_y) for pos in positions]
            if all(LegalMovesOptimized.is_position_valid(board, pos, positions) for pos in new_positions):
                valid_moves.append(Move(list(positions), new_positions, game_state.turn))

        return valid_moves
