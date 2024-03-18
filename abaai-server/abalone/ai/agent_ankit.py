from copy import deepcopy

from abalone.board import BoardLayout
from abalone.game import GameState
from abalone.movement import Piece, Position, Move


class StateSpaceGenerator:

    @staticmethod
    def get_max_player_piece_positions(game_state: GameState) -> list[Position]:
        max_player_value = game_state.turn.value

        max_player_piece_positions = []
        for y in range(9):
            for x in range(9):
                if game_state.board[y][x] == max_player_value:
                    max_player_piece_positions.append(Position(x, y))

        return max_player_piece_positions

    @staticmethod
    def get_min_player_piece_positions(game_state: GameState) -> list[Position]:
        min_player_value = Piece.BLACK.value if game_state.turn == Piece.WHITE else Piece.WHITE.value

        min_player_piece_positions = []
        for y in range(9):
            for x in range(9):
                if game_state.board[y][x] == min_player_value:
                    min_player_piece_positions.append(Position(x, y))

        return min_player_piece_positions

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



class LegalMoves:
    def is_empty(self, position: Position) -> bool:
        pass

    def is_out_of_bounds(self, position: Position) -> bool:
        pass

    def move_one_marble(self, position: Position, direction: Position) -> Move:
        pass

    def move_two_marbles(self, position1: Position, position2: Position, direction: Position) -> Move:
        pass

    def move_three_marbles(self, position1: Position, position2: Position, position3: Position,
                           direction: Position) -> Move:
        pass

    def two_sumito_one(self):
        pass

    def three_sumito_one(self):
        pass

    def three_sumito_two(self):
        pass


GameBoard = StateSpaceGenerator.convert_input_file_to_game_state('Test1.input')
print(GameBoard.board)
maxPlayer = StateSpaceGenerator.get_max_player_piece_positions(GameBoard)
minPlayer = StateSpaceGenerator.get_min_player_piece_positions(GameBoard)