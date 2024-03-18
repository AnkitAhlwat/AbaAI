from copy import deepcopy

from abalone.board import BoardLayout
from abalone.game import GameState
from abalone.movement import Piece, Position, Move


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
            legal_moves.extend(LegalMovesGeneratorLucas.generate_legal_one_piece_moves(game_state, position))

        # Generate all possible two piece moves
        max_player_adjacent_pairs = StateSpaceGenerator.get_max_player_two_piece_adjacent_positions(
            max_player_piece_positions)
        for position1, position2 in max_player_adjacent_pairs:
            legal_moves.extend(
                LegalMovesGeneratorLucas.generate_legal_two_piece_moves(game_state, position1, position2))

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
        adjacent_positions = []
        for i in range(len(max_player_piece_positions)):
            for j in range(i + 1, len(max_player_piece_positions)):
                if Position.are_positions_adjacent(max_player_piece_positions[i], max_player_piece_positions[j]):
                    adjacent_positions.append((max_player_piece_positions[i], max_player_piece_positions[j]))

        return adjacent_positions

    # @staticmethod
    # def are_positions_adjacent_and_in_line(positions: list[Position]) -> bool:
    #     # Check if the positions are in a straight line on the x, y or z (diagonal) axis
    #     if not (
    #             (positions[0].x == positions[1].x == positions[2].x) or
    #             (positions[0].y == positions[1].y == positions[2].y) or
    #             (positions[0].x - positions[0].y == positions[1].x - positions[1].y == positions[2].x - positions[2].y)
    #     ):
    #         return False
    #
    #     # Check if the positions are adjacent
    #     if not (
    #             (abs(positions[0].x - positions[1].x) <= 1 and abs(positions[0].y - positions[1].y) <= 1) or
    #             (abs(positions[0].x - positions[2].x) <= 1 and abs(positions[0].y - positions[2].y) <= 1) or
    #             (abs(positions[1].x - positions[2].x) <= 1 and abs(positions[1].y - positions[2].y) <= 1)
    #     ):
    #         return False
    #
    #     return True

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
    def generate_legal_one_piece_moves(game_state: GameState, position: Position) -> list[Move]:
        possible_positions = PossibleMovesGenerator.get_possible_one_piece_new_positions(position)
        legal_moves = []

        for new_position in possible_positions:
            previous_positions = [position]
            new_positions = [new_position]

            if LegalMovesGeneratorLucas.__is_available_position(game_state, previous_positions, new_positions):
                legal_move = Move(previous_positions, new_positions, game_state.turn)
                legal_moves.append(legal_move)

        return legal_moves

    @staticmethod
    def generate_legal_two_piece_moves(game_state: GameState, position1: Position, position2: Position):
        possible_positions = PossibleMovesGenerator.get_possible_two_piece_new_positions(position1, position2)
        legal_moves = []

        for new_position1, new_position2 in possible_positions:
            previous_positions = [position1, position2]
            new_positions = [new_position1, new_position2]

            if LegalMovesGeneratorLucas.__is_available_position(game_state, previous_positions, new_positions):
                legal_move = Move(previous_positions, new_positions, game_state.turn)
                legal_moves.append(legal_move)

        return legal_moves

    @staticmethod
    def __is_available_position(
            game_state: GameState,
            previous_positions: list[Position],
            new_positions: list[Position]
    ) -> bool:
        for position in new_positions:
            if (
                    not LegalMovesGeneratorLucas.__is_position_inside_board(game_state, position) or
                    not LegalMovesGeneratorLucas.__is_space_empty(game_state, previous_positions, new_positions)
            ):
                return False

        return True

    @staticmethod
    def __is_space_empty(
            game_state: GameState,
            previous_positions: list[Position],
            new_positions: list[Position]
    ) -> bool:
        for position in new_positions:
            x, y = position.x, position.y
            # It can't move to a position that is already occupied and not going to be moved
            if game_state.board[y][x] != 0 and position not in previous_positions:
                return False

        return True

    @staticmethod
    def __is_position_inside_board(game_state: GameState, position: Position) -> bool:
        x, y = position.x, position.y
        # Check if the position is in the bounds of the board indices
        if x < 0 or y < 0 or x > 8 or y > 8:
            return False
        # Check if the position is beyond the edge of the playable board
        if game_state.board[y][x] == -1:
            return False

        return True


class PossibleMovesGenerator:
    @staticmethod
    def get_possible_one_piece_new_positions(position: Position) -> list[Position]:
        return Position.get_adjacent_positions(position)

    @staticmethod
    def get_possible_two_piece_new_positions(
            position1: Position, position2: Position
    ) -> list[tuple[Position, Position]]:
        possible_moves_1 = PossibleMovesGenerator.get_possible_one_piece_new_positions(position1)
        possible_moves_2 = PossibleMovesGenerator.get_possible_one_piece_new_positions(position2)

        possible_moves = list(zip(possible_moves_1, possible_moves_2))

        return possible_moves

    @staticmethod
    def get_possible_three_piece_new_positions(
            position1: Position, position2: Position, position3: Position
    ) -> list[tuple[Position, Position, Position]]:
        possible_moves_1 = PossibleMovesGenerator.get_possible_one_piece_new_positions(position1)
        possible_moves_2 = PossibleMovesGenerator.get_possible_one_piece_new_positions(position2)
        possible_moves_3 = PossibleMovesGenerator.get_possible_one_piece_new_positions(position3)

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
