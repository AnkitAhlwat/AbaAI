from itertools import combinations
from abalone.ai.agent_ankit import LegalMoves
from abalone.movement import Position


class StateSpaceGenerator:

    @staticmethod
    def get_player_piece_positions(board) -> dict[str, list[Position]]:
        player_max_value = board.turn.value
        player_min_value = 2 if player_max_value == 1 else 1
        player_dict = {"player_max": player_max_value, "player_min": player_min_value}
        player_max_piece_positions = []
        player_min_piece_positions = []
        for y in range(9):
            for x in range(9):
                if board.board[y][x] == player_max_value:
                    player_max_piece_positions.append(Position(x, y))
                elif board.board[y][x] == player_min_value:
                    player_min_piece_positions.append(Position(x, y))
        player_dict["player_max"] = player_max_piece_positions
        player_dict["player_min"] = player_min_piece_positions
        return player_dict

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
    def generate_all_moves(board,player_piece):
        if board.turn.value == 1:
            black_positions = player_piece['player_max']
            white_positions = player_piece['player_min']
        else:
            black_positions = player_piece['player_min']
            white_positions = player_piece['player_max']
        all_moves = {
            "black": black_positions,
            "white": white_positions
        }

        result = {"black": {}, "white": {}}

        for color, positions in all_moves.items():
            for pos in positions:
                moves = LegalMoves.get_valid_moves(board.board, pos)
                if moves:
                    result[color][f'{[pos]}'] = moves

            for pos1, pos2 in combinations(positions, 2):
                moves = LegalMoves.get_valid_moves(board.board, pos1, pos2)
                if moves:
                    key = sorted([[pos1, pos2]])
                    result[color][f'{key[0]}'] = moves

            for pos1, pos2, pos3 in combinations(positions, 3):
                moves = LegalMoves.get_valid_moves(board.board, pos1, pos2, pos3)
                if moves:
                    key = sorted([[pos1, pos2, pos3]])
                    result[color][f'{key[0]}'] = moves
        if board.turn.value == 1:
            sumito = LegalMoves.generate_all_sumitos(board.board, black_positions, white_positions)
        else:
            sumito = LegalMoves.generate_all_sumitos(board.board, white_positions, black_positions)
        print(sumito)
        return result
