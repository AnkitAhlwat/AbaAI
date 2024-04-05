from abalone.movement_optimized import Move


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
        direction = (positions[1][0] - positions[0][0], positions[1][1] - positions[0][1])
        return all((positions[i + 1][0] - positions[i][0], positions[i + 1][1] - positions[i][1]) == direction
                   for i in range(len(positions) - 1)) and direction in LegalMovesOptimized.possible_moves

    @staticmethod
    def is_position_valid(board, position, vacating_positions=None):
        """Combined checks for board position status."""
        index = LegalMovesOptimized.get_flat_index(position[0], position[1])
        if index == -1 or board[index] == -1:
            return False
        if vacating_positions is None:
            vacating_positions = []
        return board[index] == 0 or position in vacating_positions

    @staticmethod
    def get_valid_moves(game_state, *positions):
        """Optimized move validation."""
        if len(positions) > 1 and not LegalMovesOptimized.are_marbles_inline(*positions):
            return []

        board = game_state.board.array
        valid_moves = []

        for move_x, move_y in LegalMovesOptimized.possible_moves:
            new_positions = [(pos[0] + move_x, pos[1] + move_y) for pos in positions]
            if all(LegalMovesOptimized.is_position_valid(board, pos, positions) for pos in new_positions):
                valid_moves.append(Move(list(positions), new_positions, game_state.turn))

        return valid_moves

    @staticmethod
    def can_sumito_occur(sequence, direction, board):
        """Determine if a Sumito move is possible based on the sequence and direction."""
        if not sequence['opponent']:
            return False

        if len(sequence['player']) <= len(sequence['opponent']):
            return False

        last_opponent_pos = sequence['opponent'][-1]
        push_target_pos = (last_opponent_pos[0] + direction[0], last_opponent_pos[1] + direction[1])

        return not LegalMovesOptimized.is_position_valid(board, push_target_pos)


    @staticmethod
    def sequence_helper_function(board,position):
        index = LegalMovesOptimized.get_flat_index(position[0], position[1])
        if index == -1 or board[index] == -1:
            return True
        if board[index] == 0:
            return True

        return False


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
                next_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
                if next_pos in opponent_positions:
                    sequence_found = True
                    current_pos = next_pos
                    break
                elif LegalMovesOptimized.sequence_helper_function(board,next_pos):
                    break
                current_pos = next_pos
            else:
                break

        while sequence_found and current_pos in opponent_positions:
            opponent_seq.append(current_pos)
            next_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
            if LegalMovesOptimized.sequence_helper_function(board,next_pos):
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
            for direction in LegalMovesOptimized.possible_moves:
                sequence = LegalMovesOptimized.find_marble_sequence(board, start_pos, direction, player_positions,
                                                                    opponent_positions)
                if sequence and LegalMovesOptimized.can_sumito_occur(sequence, direction, board):
                    new_positions_player = [(pos.x + direction[0], pos.y + direction[1]) for pos in
                                            sequence['player']]
                    new_positions_opponent = [(pos.x + direction[0], pos.y + direction[1]) for pos in
                                              sequence['opponent']
                                              if not LegalMovesOptimized.is_position_valid(board,(pos[0] + direction[0],
                                                                                                   pos[1] + direction[1]))]

                    sumito_move_list.append(Move(
                        sequence['player'],
                        new_positions_player,
                        game_state.turn,
                        sequence['opponent'],
                        new_positions_opponent)
                    )

        return sumito_move_list
