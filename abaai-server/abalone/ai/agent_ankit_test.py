
from abalone.ai.file_reader import FileReader
from state_space_generator import StateSpaceGenerator




GameBoard = FileReader.convert_input_file_to_game_state('Test1.input')

all_pieces = StateSpaceGenerator.get_player_piece_positions(GameBoard)
possible_moves = StateSpaceGenerator.generate_all_possible_moves(GameBoard, all_pieces)
print(len(possible_moves))