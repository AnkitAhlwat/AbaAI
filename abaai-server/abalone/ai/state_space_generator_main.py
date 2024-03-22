from abalone.ai.file_handler import FileHandler
from abalone.state import GameStateUpdate
from abalone.ai.state_space_generator import StateSpaceGenerator
import os


def main():

    input_dir = 'input_files'
    output_dir = 'output_files'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.input'):

            input_file_path = os.path.join(input_dir, filename)
            output_file_base = os.path.join(output_dir, filename.split('.input')[0])

            game_state = FileHandler.convert_input_file_to_game_state(input_file_path)

            possible_moves = StateSpaceGenerator.generate_all_possible_moves(game_state)
            game_state_updates = GameStateUpdate.convert_moves_to_game_state_updates(game_state, possible_moves)

            FileHandler.convert_game_state_updates_to_output_files(game_state_updates, output_file_base)


if __name__ == "__main__":
    main()
