from abalone.movement import Position


class LegalMoves:
    possible_moves = [
        (-1, 0),  # Move left
        (1, 0),  # Move right
        (0, -1),  # Move down
        (0, 1),  # Move up
        (1, -1),  # Move up-right
        (-1, 1)  # Move down-left
    ]

    # Conditions / Helpers
    @staticmethod
    def are_marbles_inline(*positions):
        """Check if the given marbles (positions) are in-line. Works for 2 or 3 marbles."""
        if len(positions) < 2:
            return False
        initial_direction = (positions[1].x - positions[0].x, positions[1].y - positions[0].y)

        for i in range(1, len(positions) - 1):
            direction = (positions[i + 1].x - positions[i].x, positions[i + 1].y - positions[i].y)
            if direction != initial_direction:
                return False

        return initial_direction in LegalMoves.possible_moves

    @staticmethod
    def is_position_within_board(board, position):
        """Check if the position is within the board boundaries."""
        return 0 <= position.y < len(board) and 0 <= position.x < len(board[position.y])

    @staticmethod
    def is_position_empty(board, position):
        """Check if a position is empty."""
        if LegalMoves.is_position_within_board(board, position):
            return board[position.y][position.x] == 0
        return False

    @staticmethod
    def is_position_empty_or_vacating(board, position, vacating_positions=None):
        """Check if a position is empty or being vacated by the moving marbles."""
        if vacating_positions is None:
            vacating_positions = []
        if LegalMoves.is_position_within_board(board, position):
            return board[position.y][position.x] == 0 or position in vacating_positions

    @staticmethod
    def get_valid_moves(board, *positions):
        """Get the valid moves for the given marbles(Currently only for movement.)"""
        if len(positions) > 1 and not LegalMoves.are_marbles_inline(*positions):
            return []

        valid_moves = []
        vacating_positions = list(positions)

        for move_x, move_y in LegalMoves.possible_moves:
            new_positions = [Position(pos.x + move_x, pos.y + move_y) for pos in positions]

            if all(LegalMoves.is_position_within_board(board, new_pos) for new_pos in new_positions) and \
                    all(LegalMoves.is_position_empty_or_vacating(board, new_pos, vacating_positions)
                        for new_pos in new_positions):
                valid_moves.append(new_positions[0] if len(new_positions) == 1 else tuple(new_positions))

        return valid_moves
