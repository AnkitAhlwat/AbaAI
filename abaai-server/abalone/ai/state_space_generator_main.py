from abalone.ai.file_handler import FileHandler
from abalone.state import GameStateUpdate
from state_space_generator import StateSpaceGenerator


def main():
    input_files = ["Test4", "Test5", "Test6", "Test7", "Test8", "Test9", "Test10"]

    for input_file in input_files:
        input_file = '../../state_space_test_files/' + input_file + '.input'

        game_state = FileHandler.convert_input_file_to_game_state(input_file)

        possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
        game_state_updates = GameStateUpdate.convert_moves_to_game_state_updates(game_state, possible_moves)

        FileHandler.convert_game_state_updates_to_output_files(game_state_updates, input_file)


if __name__ == "__main__":
    main()
