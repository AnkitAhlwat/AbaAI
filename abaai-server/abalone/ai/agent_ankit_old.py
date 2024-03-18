# from abalone.movement import Position
#
#
# class LegalMoves:
#     possible_moves = [
#         (-1, 0),  # Move left
#         (1, 0),  # Move right
#         (0, -1),  # Move down
#         (0, 1),  # Move up
#         (1, -1),  # Move up-right
#         (-1, 1)  # Move down-left
#     ]
#
#     # Conditions / Helpers
#     @staticmethod
#     def are_marbles_inline(*positions):
#         """Check if the given marbles (positions) are in-line. Works for 2 or 3 marbles."""
#         if len(positions) < 2:
#             return False
#         initial_direction = (positions[1].x - positions[0].x, positions[1].y - positions[0].y)
#
#         for i in range(1, len(positions) - 1):
#             direction = (positions[i + 1].x - positions[i].x, positions[i + 1].y - positions[i].y)
#             if direction != initial_direction:
#                 return False
#
#         return initial_direction in LegalMoves.possible_moves
#
#     @staticmethod
#     def is_position_within_board(board, position):
#         """Check if the position is within the board boundaries."""
#         return 0 <= position.y < len(board) and 0 <= position.x < len(board[position.y])
#
#     @staticmethod
#     def is_position_empty(board, position):
#         """Check if a position is empty."""
#         if LegalMoves.is_position_within_board(board, position):
#             return board[position.y][position.x] == 0
#         return False
#
#     @staticmethod
#     def is_position_empty_or_vacating(board, position, vacating_positions=None):
#         """Check if a position is empty or being vacated by the moving marbles."""
#         if vacating_positions is None:
#             vacating_positions = []
#         if LegalMoves.is_position_within_board(board, position):
#             return board[position.y][position.x] == 0 or position in vacating_positions
#
#     @staticmethod
#     def get_valid_moves(board, *positions):
#         num_marbles = len(positions)
#         if num_marbles == 1:
#             return LegalMoves.get_valid_moves_one_marble(board, positions[0])
#         elif num_marbles == 2:
#             return LegalMoves.get_valid_moves_two_marbles(board, positions[0], positions[1])
#         elif num_marbles == 3:
#             return LegalMoves.get_valid_moves_three_marbles(board, positions[0], positions[1], positions[2])
#         else:
#             return []
#
#     @staticmethod
#     def get_valid_moves_one_marble(board, pos):
#         valid_moves = []
#
#         for move_x, move_y in LegalMoves.possible_moves:
#             new_pos = Position(pos.x + move_x, pos.y + move_y)
#             if LegalMoves.is_position_empty(board, new_pos):
#                 valid_moves.append(new_pos)
#
#         return valid_moves
#
#     @staticmethod
#     def get_valid_moves_two_marbles(board, pos1, pos2):
#         if not LegalMoves.are_marbles_inline(pos1, pos2):
#             return []
#
#         valid_moves = []
#         vacating_positions = [pos1, pos2]
#         for move_x, move_y in LegalMoves.possible_moves:
#             new_pos1 = Position(pos1.x + move_x, pos1.y + move_y)
#             new_pos2 = Position(pos2.x + move_x, pos2.y + move_y)
#
#             if LegalMoves.is_position_empty_or_vacating(board, new_pos1, vacating_positions) and \
#                     LegalMoves.is_position_empty_or_vacating(board, new_pos2, vacating_positions):
#                 valid_moves.append((new_pos1, new_pos2))
#         return valid_moves
#
#     @staticmethod
#     def get_valid_moves_three_marbles(board, pos1, pos2, pos3):
#         if not LegalMoves.are_marbles_inline(pos1, pos2, pos3):
#             return []
#
#         valid_moves = []
#         vacating_positions = [pos1, pos2, pos3]
#
#         for move_x, move_y in LegalMoves.possible_moves:
#             new_pos1 = Position(pos1.x + move_x, pos1.y + move_y)
#             new_pos2 = Position(pos2.x + move_x, pos2.y + move_y)
#             new_pos3 = Position(pos3.x + move_x, pos3.y + move_y)
#
#             if all(LegalMoves.is_position_empty_or_vacating(board, p, vacating_positions)
#                    for p in [new_pos1, new_pos2, new_pos3]):
#                 valid_moves.append((new_pos1, new_pos2, new_pos3))
#
#         return valid_moves
