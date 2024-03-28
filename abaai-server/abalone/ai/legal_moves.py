from abalone.movement import Position, Move


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
    def get_flat_index(x, y):
        """Calculate the index in the flat array for the board position (x, y)."""
        if x < 0 or y < 0:
            return -1
        return y * 9 + x

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
    def is_position_out_of_bounds(board, position):
        """Check if a position is out of bounds."""
        index = LegalMoves.get_flat_index(position.x, position.y)
        return index < 0 or index >= len(board) or board[index] == -1

    @staticmethod
    def is_position_within_board(board, position):
        """Check if the position is within the board boundaries."""
        index = LegalMoves.get_flat_index(position.x, position.y)
        return 0 <= index < len(board)

    @staticmethod
    def is_position_empty(board, position):
        """Check if a position is empty."""
        index = LegalMoves.get_flat_index(position.x, position.y)
        return index < len(board) and board[index] == 0

    @staticmethod
    def is_position_empty_or_vacating(board, position, vacating_positions=None):
        """Check if a position is empty or being vacated by the moving marbles."""
        if vacating_positions is None:
            vacating_positions = []
        index = LegalMoves.get_flat_index(position.x, position.y)
        return ((0 <= index < len(board)) and board[index] == 0) or position in vacating_positions

    @staticmethod
    def get_valid_moves(game_state, *positions):
        """Get the valid moves for the given marbles(Currently only for movement.)"""
        board = game_state.board.array
        if len(positions) > 1 and not LegalMoves.are_marbles_inline(*positions):
            return []

        valid_moves = []
        vacating_positions = list(positions)

        for move_x, move_y in LegalMoves.possible_moves:
            new_positions = [Position(pos.x + move_x, pos.y + move_y) for pos in positions]

            if all(LegalMoves.is_position_empty_or_vacating(board, new_pos, vacating_positions)
                   for new_pos in new_positions):
                move = Move(
                    vacating_positions,
                    new_positions,
                    game_state.turn
                )
                valid_moves.append(move)

        return valid_moves

    """Sumito Logic"""

    @staticmethod
    def can_sumito_occur(sequence, direction, board):
        """Determine if a Sumito move is possible based on the sequence and direction."""
        if not sequence['opponent']:
            return False

        if len(sequence['player']) <= len(sequence['opponent']):
            return False

        last_opponent_pos = sequence['opponent'][-1]
        push_target_pos = Position(last_opponent_pos.x + direction[0], last_opponent_pos.y + direction[1])

        return not LegalMoves.is_position_within_board(board, push_target_pos) \
               or LegalMoves.is_position_empty(board, push_target_pos) \
               or LegalMoves.is_position_out_of_bounds(board, push_target_pos)

    @staticmethod
    def find_marble_sequence(board, start_pos, direction, player_positions, opponent_positions):
        """Identify a sequence of player and opponent marbles in a specific direction."""
        player_seq = []
        opponent_seq = []
        current_pos = start_pos
        sequence_found = False

        for _ in range(3):
            if current_pos in player_positions:
                player_seq.append(current_pos)
                next_pos = Position(current_pos.x + direction[0], current_pos.y + direction[1])
                if next_pos in opponent_positions:
                    sequence_found = True
                    current_pos = next_pos
                    break
                elif not LegalMoves.is_position_within_board(board, next_pos) \
                        or LegalMoves.is_position_empty(board, next_pos):
                    break
                current_pos = next_pos
            else:
                break

        while sequence_found and current_pos in opponent_positions:
            opponent_seq.append(current_pos)
            next_pos = Position(current_pos.x + direction[0], current_pos.y + direction[1])
            if not LegalMoves.is_position_within_board(board, next_pos) or LegalMoves.is_position_empty(board,
                                                                                                        next_pos):
                break
            current_pos = next_pos

        if sequence_found:
            return {'player': player_seq, 'opponent': opponent_seq}
        return None

    @staticmethod
    def generate_all_sumitos(game_state, player_positions, opponent_positions):
        """Generate all possible Sumitos given the current board state."""
        board = game_state.board.array
        sumito_move_list = []
        for start_pos in player_positions:
            for direction in LegalMoves.possible_moves:
                sequence = LegalMoves.find_marble_sequence(board, start_pos, direction, player_positions,
                                                           opponent_positions)
                if sequence and LegalMoves.can_sumito_occur(sequence, direction, board):
                    new_positions_player = [Position(pos.x + direction[0], pos.y + direction[1]) for pos in
                                            sequence['player']]
                    new_positions_opponent = [Position(pos.x + direction[0], pos.y + direction[1]) for pos in
                                              sequence['opponent']
                                              if not LegalMoves.is_position_out_of_bounds
                        (board, Position(pos.x + direction[0], pos.y + direction[1]))]

                    sumito_move_list.append(Move(
                        sequence['player'],
                        new_positions_player,
                        game_state.turn,
                        sequence['opponent'],
                        new_positions_opponent)
                    )

        return sumito_move_list
