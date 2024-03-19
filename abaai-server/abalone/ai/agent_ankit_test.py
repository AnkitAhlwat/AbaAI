
from abalone.ai.file_reader import FileReader
from agent_ankit import LegalMoves
from state_space_generator import StateSpaceGenerator




GameBoard = FileReader.convert_input_file_to_game_state('Test1.input')
maxPlayer = StateSpaceGenerator.get_max_player_piece_positions(GameBoard,1)
minPlayer = StateSpaceGenerator.get_min_player_piece_positions(GameBoard,2)
all_moves = StateSpaceGenerator.generate_all_moves(GameBoard, maxPlayer, minPlayer)
print(all_moves)
sumitos = LegalMoves.generate_all_sumitos(GameBoard.board, maxPlayer, minPlayer)
print(sumitos)
sumitos2 = LegalMoves.generate_all_sumitos(GameBoard.board, minPlayer, maxPlayer)
print(sumitos2)
"""Testing Ignore below"""

# GameBoard = StateSpaceGenerator.convert_input_file_to_game_state('Ankit.input')
# print(GameBoard.board)
# # minPlayer = StateSpaceGenerator.get_min_player_piece_positions(GameBoard)
# moves = generate_all_black_moves(GameBoard, maxPlayer)
# print(moves)

# # Test for are_marbles_inline
# # Should be true
# pos1 = Position(2, 6)
# pos2 = Position(1, 7)
# pos3 = Position(0, 8)
# print(LegalMoves.are_marbles_inline(pos1, pos2, pos3))
# # Should be true
# pos1 = Position(2, 6)
# pos2 = Position(2, 7)
# pos3 = Position(2, 8)
# print(LegalMoves.are_marbles_inline(pos1, pos2, pos3))
# # Should be True
# pos1 = Position(2, 6)
# pos2 = Position(3, 6)
# pos3 = Position(4, 6)
# print(LegalMoves.are_marbles_inline(pos1, pos2, pos3))
# # Should be False
# pos1 = Position(2, 6)
# pos2 = Position(3, 6)
# pos3 = Position(3, 7)
# print(LegalMoves.are_marbles_inline(pos1, pos2, pos3))


# print(f'All possible max moves : {maxPlayer}')
# for i in maxPlayer:
#     pos1 = Position(i.x, i.y)
#     pos2 = Position(i.x + 1, i.y)
#     pos3 = Position(i.x + 2, i.y)
#     print(f'For position ({pos1},{pos2},{pos3}) : '
#           f'{LegalMoves.get_valid_moves_three_marbles(GameBoard.board, pos1, pos2, pos3)}')
# for i in maxPlayer:
#     # get all possible moves from left, right, up, down, up-right, down-left
#     # print(i)
#     # print(LegalMoves.get_valid_moves_one_marble(GameBoard.board, i.x, i.y))
#     print(i, (i.x - 1, i.y))
#     print(LegalMoves.get_valid_moves_two_marbles(GameBoard.board, i, Position(i.x - 1, i.y)))
#     print("---------------------------------------------------")
#     print(i, (i.x + 1, i.y))
#     print(LegalMoves.get_valid_moves_two_marbles(GameBoard.board, i, Position(i.x + 1, i.y)))
#     print("---------------------------------------------------")
#     print(i, (i.x, i.y - 1))
#     print(LegalMoves.get_valid_moves_two_marbles(GameBoard.board, i, Position(i.x, i.y - 1)))
#     print("---------------------------------------------------")
#     print(i, (i.x, i.y + 1))
#     print(LegalMoves.get_valid_moves_two_marbles(GameBoard.board, i, Position(i.x, i.y + 1)))
#     print("---------------------------------------------------")
#     print(i, (i.x - 1, i.y + 1))
#     print(LegalMoves.get_valid_moves_two_marbles(GameBoard.board, i, Position(i.x - 1, i.y + 1)))
#     print("---------------------------------------------------")
#     print(i, (i.x + 1, i.y - 1))
#     print(LegalMoves.get_valid_moves_two_marbles(GameBoard.board, i, Position(i.x + 1, i.y - 1)))
#     print("---------------------------------------------------")
