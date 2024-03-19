from copy import deepcopy

from abalone.board import BoardLayout
from abalone.game import GameState
from abalone.movement import Piece, Position


class FileReader:
    @staticmethod
    def convert_input_file_to_game_state(file_name) -> GameState:
        with open(file_name, 'r', encoding="utf-8") as file:
            turn = Piece.BLACK if file.readline().strip().upper() == 'B' else Piece.WHITE

            piece_positions = file.readline().strip().split(',')

            # Create a 9x9 board with the pieces in the correct positions, starting with empty board
            board = deepcopy(BoardLayout.EMPTY.value)
            for position_notation in piece_positions:
                y_letter, x_number, piece_letter = position_notation
                y = Position.get_y_from_letter(y_letter)
                x = Position.get_x_from_number(int(x_number))
                board[y][x] = Piece.BLACK.value if piece_letter.upper() == 'B' else Piece.WHITE.value

            return GameState(board, turn)