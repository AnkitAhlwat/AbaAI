from copy import deepcopy

from abalone.board import BoardLayout
from abalone.state import GameState
from abalone.movement import Piece, Position, Move


class FileHandler:
    @staticmethod
    def convert_input_file_to_game_state(file_name) -> GameState:
        with open(file_name, 'r', encoding="utf-8") as file:
            turn = Piece.BLACK if file.readline().strip().upper() == 'B' else Piece.WHITE

            piece_positions = file.readline().strip().replace(' ', '').split(',')

            # Create a 9x9 board with the pieces in the correct positions, starting with empty board
            board = deepcopy(BoardLayout.EMPTY.value)
            for position_notation in piece_positions:
                y_letter, x_number, piece_letter = position_notation
                y = Position.get_y_from_letter(y_letter)
                x = Position.get_x_from_number(int(x_number))
                board[y][x] = Piece.BLACK.value if piece_letter.upper() == 'B' else Piece.WHITE.value

            return GameState(board, turn)

    @staticmethod
    def convert_moves_to_move_file(moves: list[Move], output_file_name: str):
        pass

    @staticmethod
    def convert_moves_to_board_file(moves: list[Move], output_file_name: str):
        pass
