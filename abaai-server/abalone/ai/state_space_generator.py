from itertools import combinations
from abalone.ai.agent_ankit import LegalMoves
from abalone.movement import Position


class StateSpaceGenerator:

    @staticmethod
    def get_max_player_piece_positions(game_state, turn) -> list[Position]:
        max_player_value = turn
        max_player_piece_positions = []
        for y in range(9):
            for x in range(9):
                if game_state.board[y][x] == max_player_value:
                    max_player_piece_positions.append(Position(x, y))

        return max_player_piece_positions

    @staticmethod
    def get_min_player_piece_positions(game_state, turn) -> list[Position]:
        min_player_value = turn
        min_player_piece_positions = []
        for y in range(9):
            for x in range(9):
                if game_state.board[y][x] == min_player_value:
                    min_player_piece_positions.append(Position(x, y))

        return min_player_piece_positions

    @staticmethod
    def generate_all_moves(board, black_positions, white_positions):
        all_moves = {
            "black": black_positions,
            "white": white_positions
        }

        result = {"black": {}, "white": {}}

        for color, positions in all_moves.items():
            for pos in positions:
                moves = LegalMoves.get_valid_moves(board.board, pos)
                if moves:
                    result[color][pos] = moves

            for pos1, pos2 in combinations(positions, 2):
                moves = LegalMoves.get_valid_moves(board.board, pos1, pos2)
                if moves:
                    result[color][(pos1, pos2)] = moves

            for pos1, pos2, pos3 in combinations(positions, 3):
                moves = LegalMoves.get_valid_moves(board.board, pos1, pos2, pos3)
                if moves:
                    result[color][(pos1, pos2, pos3)] = moves

        return result
