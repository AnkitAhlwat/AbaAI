from state_space_generator import StateSpaceGenerator
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
    def are_marbles_inline(pos1, pos2):
        """Check if the marbles are in-line."""
        return any((pos1.x - pos2.x, pos1.y - pos2.y) == move for move in LegalMoves.possible_moves)

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

    # Put all the methods to get valid moves here
    @staticmethod
    def get_valid_moves_one_marble(board, x, y):
        valid_moves = []

        for move_x, move_y in LegalMoves.possible_moves:
            new_x, new_y = x + move_x, y + move_y
            if LegalMoves.is_position_empty(board, Position(new_x, new_y)):
                valid_moves.append(Position(new_x, new_y))

        return valid_moves

    @staticmethod
    def get_valid_moves_two_marbles(board, pos1, pos2):
        if not LegalMoves.are_marbles_inline(pos1, pos2):
            return []

        valid_moves = []
        vacating_positions = [pos1, pos2]
        for move_x, move_y in LegalMoves.possible_moves:
            new_pos1 = Position(pos1.x + move_x, pos1.y + move_y)
            new_pos2 = Position(pos2.x + move_x, pos2.y + move_y)

            if LegalMoves.is_position_empty_or_vacating(board, new_pos1, vacating_positions) and \
                    LegalMoves.is_position_empty_or_vacating(board, new_pos2, vacating_positions):
                valid_moves.append((new_pos1, new_pos2))
        return valid_moves


GameBoard = StateSpaceGenerator.convert_input_file_to_game_state('Ankit.input')
# print(GameBoard.board)
maxPlayer = StateSpaceGenerator.get_max_player_piece_positions(GameBoard)
# minPlayer = StateSpaceGenerator.get_min_player_piece_positions(GameBoard)
print(f'All possible max moves : {maxPlayer}')
for i in maxPlayer:
    # get all possible moves from left, right, up, down, up-right, down-left
    # print(i)
    # print(LegalMoves.get_valid_moves_one_marble(GameBoard.board, i.x, i.y))
    print(i, (i.x - 1, i.y))
    print(LegalMoves.get_valid_moves_two_marbles(GameBoard.board, i, Position(i.x - 1, i.y)))
    print("---------------------------------------------------")
    print(i, (i.x + 1, i.y))
    print(LegalMoves.get_valid_moves_two_marbles(GameBoard.board, i, Position(i.x + 1, i.y)))
    print("---------------------------------------------------")
    print(i, (i.x, i.y - 1))
    print(LegalMoves.get_valid_moves_two_marbles(GameBoard.board, i, Position(i.x, i.y - 1)))
    print("---------------------------------------------------")
    print(i, (i.x, i.y + 1))
    print(LegalMoves.get_valid_moves_two_marbles(GameBoard.board, i, Position(i.x, i.y + 1)))
    print("---------------------------------------------------")
    print(i, (i.x - 1, i.y + 1))
    print(LegalMoves.get_valid_moves_two_marbles(GameBoard.board, i, Position(i.x - 1, i.y + 1)))
    print("---------------------------------------------------")
    print(i, (i.x + 1, i.y - 1))
    print(LegalMoves.get_valid_moves_two_marbles(GameBoard.board, i, Position(i.x + 1, i.y - 1)))
    print("---------------------------------------------------")