from itertools import combinations

from abalone.ai.legal_moves_optimized import LegalMovesOptimized
from abalone.ai.cython.cython import LegalMovesOptimized as CythonLegalMovesOptimized
from abalone.movement import Move


class StateSpaceGenerator:

    @staticmethod
    def get_player_piece_positions(game_state) -> dict[str, list]:
        player_max_value = game_state.turn.value
        player_min_value = 2 if player_max_value == 1 else 1
        player_dict = {"player_max": player_max_value, "player_min": player_min_value}
        player_max_piece_positions = []
        player_min_piece_positions = []
        for index in range(game_state.board.array.__len__()):
            if game_state.board.array[index] == player_max_value:
                x = index % game_state.board.width
                y = index // game_state.board.width
                player_max_piece_positions.append((x, y))
            elif game_state.board.array[index] == player_min_value:
                x = index % game_state.board.width
                y = index // game_state.board.width
                player_min_piece_positions.append((x, y))
        player_dict["player_max"] = player_max_piece_positions
        player_dict["player_min"] = player_min_piece_positions
        return player_dict

    @staticmethod
    def generate_all_moves(game_state, player_piece) -> list[Move]:
        if game_state.turn.value == 1:
            black_positions = player_piece['player_max']
            white_positions = player_piece['player_min']
        else:
            black_positions = player_piece['player_min']
            white_positions = player_piece['player_max']
        all_moves = {
            "max": black_positions} if game_state.turn.value == 1 else {"max": white_positions}

        possible_move_list = []
        for color, positions in all_moves.items():
            for pos in positions:
                moves = CythonLegalMovesOptimized.get_valid_moves(game_state, pos)
                if moves:
                    possible_move_list.extend(moves)
            for pos1, pos2 in combinations(positions, 2):
                moves = CythonLegalMovesOptimized.get_valid_moves(game_state, pos1, pos2)
                if moves:
                    possible_move_list.extend(moves)

            for pos1, pos2, pos3 in combinations(positions, 3):
                moves = CythonLegalMovesOptimized.get_valid_moves(game_state, pos1, pos2, pos3)
                if moves:
                    possible_move_list.extend(moves)

        return possible_move_list

    @staticmethod
    def generate_all_sumitos(game_state, player_pieces) -> list[Move]:
        max_positions = player_pieces["player_max"]
        min_positions = player_pieces["player_min"]
        return LegalMovesOptimized.generate_all_sumitos(game_state, max_positions, min_positions)

    @staticmethod
    def generate_all_possible_moves(game_state) -> list[Move]:
        player_pieces = StateSpaceGenerator.get_player_piece_positions(game_state)

        player_piece_moves = StateSpaceGenerator.generate_all_moves(game_state, player_pieces)
        sumito_moves = StateSpaceGenerator.generate_all_sumitos(game_state, player_pieces)

        return player_piece_moves + sumito_moves
