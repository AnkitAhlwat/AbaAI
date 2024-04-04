from copy import deepcopy

from abalone.board import OptimizedBoard, BoardLayout
from abalone.state import GameState, GameStateUpdate
from abalone.movement import Piece, Position


class FileHandler:
    @staticmethod
    def convert_input_file_to_game_state(file_name) -> GameState:
        with open(file_name, 'r', encoding="utf-8") as file:
            turn = Piece.BLACK if file.readline().strip().upper() == 'B' else Piece.WHITE

            piece_positions = file.readline().strip().replace(' ', '').split(',')

            # Create a 9x9 board with the pieces in the correct positions, starting with empty board
            board_array = deepcopy(BoardLayout.EMPTY.value)
            for position_notation in piece_positions:
                y_letter, x_number, piece_letter = position_notation
                y = Position.get_y_from_letter(y_letter)
                x = Position.get_x_from_number(int(x_number))
                board_array[y][x] = Piece.BLACK.value if piece_letter.upper() == 'B' else Piece.WHITE.value

            # Convert the board array to a Board object and return the GameState
            return GameState(OptimizedBoard(board_array), turn)

    @staticmethod
    def convert_game_state_updates_to_output_files(state_updates: list[GameStateUpdate], output_file_base: str):
        move_file_name = f"{output_file_base}.move"
        board_file_name = f"{output_file_base}.board"

        with open(move_file_name, 'w', encoding="utf-8") as move_file, \
                open(board_file_name, 'w', encoding="utf-8") as board_file:
            for state_update in state_updates:
                move_file.write(str(state_update.move) + '\n')
                board_file.write(
                    FileHandler.__convert_board_object_to_board_notation(state_update.resulting_state.board) + '\n')

        print(f'Output files created: {move_file_name} and {board_file_name}')

    # Private helpers
    @staticmethod
    def __convert_board_object_to_board_notation(board: OptimizedBoard) -> str:
        black_piece_positions = []
        white_piece_positions = []

        def index_to_coordinates(index):
            return divmod(index, 9)

        # Iterate through from bottom to top
        for index in range(board.array.__len__()):
            y, x = index_to_coordinates(index)
            if board.array[index] == Piece.BLACK.value:
                position_notation = Position.to_notation_generic(x, y) + 'b'
                black_piece_positions.insert(0, position_notation)
            elif board.array[index] == Piece.WHITE.value:
                position_notation = Position.to_notation_generic(x, y) + 'w'
                white_piece_positions.insert(0, position_notation)

        return ','.join(sorted(black_piece_positions) + sorted(white_piece_positions))

    @staticmethod
    def test_output_files(first_file, second_file):
        new_set = set()
        with open(f'{first_file}', 'r') as file:
            for line in file:
                new_set.add(line)
            print(len(new_set))
        with open(f'{second_file}', 'r') as file:
            for line in file:
                new_set.add(line)
            print(len(new_set))
