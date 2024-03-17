from abalone.board import BoardLayout
from abalone.game import GameState
from abalone.movement import Piece, Position, Move
from copy import deepcopy


class StateSpaceGenerator:

    @staticmethod
    def generate_legal_moves(game_state: GameState) -> list[Move]:
        """
        Generate all the legal moves for the current game state. It will only generate the moves for the MAX player
        who is the color which turn it is.

        :param game_state: the state of the game
        :return: a list of legal moves
        """
        max_player_piece_positions = StateSpaceGenerator.get_max_player_piece_positions(game_state)
        min_player_piece_positions = StateSpaceGenerator.get_min_player_piece_positions(game_state)
        legal_moves = []

        # Generate all possible one piece moves
        for position in max_player_piece_positions:
            x, y = position.x, position.y
            legal_moves.extend(LegalMovesGeneratorLucas.generate_legal_one_piece_moves(game_state, x, y))

        # Generate all possible two piece moves

        # Generate all possible three piece moves

        # Generate all possible 2-1 sumitos

        # Generate all possible 3-1 sumitos

        # Generate all possible 3-2 sumitos

        return legal_moves

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
    def get_max_player_two_piece_adjacent_positions(max_player_piece_positions: list[Position]) -> list[tuple[Position,
    Position]]:
        pass

    @staticmethod
    def are_positions_adjacent_and_in_line(positions: list[Position]) -> bool:
        # Check if the positions are in a straight line on the x, y or z (diagonal) axis
        if not (
                (positions[0].x == positions[1].x == positions[2].x) or
                (positions[0].y == positions[1].y == positions[2].y) or
                (positions[0].x - positions[0].y == positions[1].x - positions[1].y == positions[2].x - positions[2].y)
        ):
            return False

        # Check if the positions are adjacent
        if not (
                (abs(positions[0].x - positions[1].x) <= 1 and abs(positions[0].y - positions[1].y) <= 1) or
                (abs(positions[0].x - positions[2].x) <= 1 and abs(positions[0].y - positions[2].y) <= 1) or
                (abs(positions[1].x - positions[2].x) <= 1 and abs(positions[1].y - positions[2].y) <= 1)
        ):
            return False

        return True

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


class LegalMovesGeneratorLucas:
    @staticmethod
    def generate_legal_one_piece_moves(game_state: GameState, x: int, y: int):
        possible_positions = PossibleMovesGenerator.get_possible_one_piece_new_positions(x, y)
        legal_moves = []

        for new_x, new_y in possible_positions:
            previous_positions = [(x, y)]
            new_positions = [(new_x, new_y)]

            if LegalMovesGeneratorLucas.__is_available_position(game_state, previous_positions, new_positions):
                previous_positions = [Position(x, y)]
                new_positions = [Position(new_x, new_y)]
                legal_move = Move(previous_positions, new_positions, game_state.turn)
                legal_moves.append(legal_move)

        return legal_moves

    @staticmethod
    def generate_legal_two_piece_moves(game_state: GameState, x1: int, y1: int, x2: int, y2):
        possible_positions = PossibleMovesGenerator.get_possible_two_piece_new_positions(x1, y1, x2, y2)
        legal_moves = []

        for (new_x1, new_y1), (new_x2, new_y2) in possible_positions:
            previous_positions = [(x1, y1), (x2, y2)]
            new_positions = [(new_x1, new_y1), (new_x2, new_y2)]

            if LegalMovesGeneratorLucas.__is_available_position(game_state, previous_positions, new_positions):
                previous_positions = [Position(x1, y1), Position(x2, y2)]
                new_positions = [Position(new_x1, new_y1), Position(new_x2, new_y2)]
                legal_move = Move(previous_positions, new_positions, game_state.turn)
                legal_moves.append(legal_move)

        return legal_moves

    @staticmethod
    def __is_available_position(
            game_state: GameState,
            previous_positions: list[tuple[int, int]],
            new_positions: list[tuple[int, int]]
    ) -> bool:
        for x, y in new_positions:
            if (
                    not LegalMovesGeneratorLucas.__is_position_inside_board(game_state, x, y) or
                    not LegalMovesGeneratorLucas.__is_space_empty(game_state, previous_positions, new_positions)
            ):
                return False

        return True

    @staticmethod
    def __is_space_empty(
            game_state: GameState,
            previous_positions: list[tuple[int, int]],
            new_positions: list[tuple[int, int]]
    ) -> bool:
        for x, y in new_positions:
            # It can't move to a position that is already occupied and not going to be moved
            if game_state.board[y][x] != 0 and (x, y) not in previous_positions:
                return False

        return True

    @staticmethod
    def __is_position_inside_board(game_state: GameState, x: int, y: int):
        # Check if the position is in the bounds of the board indices
        if x < 0 or y < 0 or x > 8 or y > 8:
            return False
        # Check if the position is beyond the edge of the playable board
        if game_state.board[y][x] == -1:
            return False

        return True


class PossibleMovesGenerator:
    @staticmethod
    def get_possible_one_piece_new_positions(x, y) -> list[tuple[int, int]]:
        possible_moves = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
            (x + 1, y - 1),
            (x - 1, y + 1)
        ]

        return possible_moves

    @staticmethod
    def get_possible_two_piece_new_positions(x1, y1, x2, y2):
        possible_moves_1 = PossibleMovesGenerator.get_possible_one_piece_new_positions(x1, y1)
        possible_moves_2 = PossibleMovesGenerator.get_possible_one_piece_new_positions(x2, y2)

        possible_moves = list(zip(possible_moves_1, possible_moves_2))

        return possible_moves

    @staticmethod
    def get_possible_three_piece_new_positions(x1, y1, x2, y2, x3, y3):
        possible_moves_1 = PossibleMovesGenerator.get_possible_one_piece_new_positions(x1, y1)
        possible_moves_2 = PossibleMovesGenerator.get_possible_one_piece_new_positions(x2, y2)
        possible_moves_3 = PossibleMovesGenerator.get_possible_one_piece_new_positions(x3, y3)

        possible_moves = list(zip(possible_moves_1, possible_moves_2, possible_moves_3))

        return possible_moves


def main():
    file_name = "Test1.input"
    game_state = StateSpaceGenerator.convert_input_file_to_game_state(file_name)
    legal_moves = StateSpaceGenerator.generate_legal_moves(game_state)
    for move in legal_moves:
        print(move.to_json())


if __name__ == "__main__":
    main()
