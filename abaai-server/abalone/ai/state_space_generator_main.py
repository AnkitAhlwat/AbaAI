from abalone.ai.file_handler import FileHandler
from state_space_generator import StateSpaceGenerator


def main():
    input_file = '../../state_space_test_files/Test1.input'
    game_state = FileHandler.convert_input_file_to_game_state(input_file)
    possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
    print(len(possible_moves))


if __name__ == "__main__":
    main()
