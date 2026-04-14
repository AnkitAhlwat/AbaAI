"""
Legal move generation for Abalone.

Consolidated from the original legal_moves_optimized.py and state_space_optimized.py.
Pure Python — no Cython dependency.
"""

from __future__ import annotations

from itertools import combinations

from .board import WIDTH, Piece
from .movement import DIRECTIONS, Move
from .state import GameState


def _flat_index(x: int, y: int) -> int:
    if 0 <= x < WIDTH and 0 <= y < WIDTH:
        return y * WIDTH + x
    return -1


def _is_cell_free(board_array: list[int], x: int, y: int) -> bool:
    idx = _flat_index(x, y)
    if idx == -1:
        return False
    val = board_array[idx]
    return val == 0


def _is_off_board(board_array: list[int], x: int, y: int) -> bool:
    idx = _flat_index(x, y)
    return idx == -1 or board_array[idx] == -1


def _are_inline(*positions: tuple[int, int]) -> bool:
    if len(positions) < 2:
        return False
    direction = (positions[1][0] - positions[0][0], positions[1][1] - positions[0][1])
    if direction not in DIRECTIONS:
        return False
    for i in range(len(positions) - 1):
        d = (positions[i + 1][0] - positions[i][0], positions[i + 1][1] - positions[i][1])
        if d != direction:
            return False
    return True


def _get_valid_moves(game_state: GameState, *positions: tuple[int, int]) -> list[Move]:
    """Non-sumito moves for a group of 1-3 marbles."""
    if len(positions) > 1 and not _are_inline(*positions):
        return []

    board = game_state.board.array
    valid = []
    vacating = set(positions)

    for dx, dy in DIRECTIONS:
        new_positions = [(p[0] + dx, p[1] + dy) for p in positions]
        ok = True
        for nx, ny in new_positions:
            idx = _flat_index(nx, ny)
            if idx == -1 or board[idx] == -1:
                ok = False
                break
            if board[idx] != 0 and (nx, ny) not in vacating:
                ok = False
                break
        if ok:
            valid.append(Move(list(positions), new_positions, game_state.turn))

    return valid


def _find_marble_sequence(
    board_array: list[int],
    start: tuple[int, int],
    direction: tuple[int, int],
    player_set: set[tuple[int, int]],
    opponent_set: set[tuple[int, int]],
) -> dict | None:
    """Walk along a direction to find a player-then-opponent marble chain."""
    player_seq = []
    opponent_seq = []
    pos = start

    for _ in range(3):
        if pos not in player_set:
            break
        player_seq.append(pos)
        nxt = (pos[0] + direction[0], pos[1] + direction[1])
        if nxt in opponent_set:
            pos = nxt
            # Start collecting opponent marbles
            while pos in opponent_set:
                opponent_seq.append(pos)
                nxt2 = (pos[0] + direction[0], pos[1] + direction[1])
                idx = _flat_index(nxt2[0], nxt2[1])
                if idx == -1 or board_array[idx] == -1 or board_array[idx] == 0:
                    break
                pos = nxt2
            if opponent_seq:
                return {"player": player_seq, "opponent": opponent_seq}
            return None
        elif _is_off_board(board_array, nxt[0], nxt[1]) or _is_cell_free(board_array, nxt[0], nxt[1]):
            break
        pos = nxt

    return None


def _can_sumito(
    sequence: dict,
    direction: tuple[int, int],
    board_array: list[int],
) -> bool:
    if not sequence["opponent"]:
        return False
    if len(sequence["player"]) <= len(sequence["opponent"]):
        return False
    last_opp = sequence["opponent"][-1]
    push_target = (last_opp[0] + direction[0], last_opp[1] + direction[1])
    idx = _flat_index(push_target[0], push_target[1])
    return idx == -1 or board_array[idx] == -1 or board_array[idx] == 0


def _generate_sumitos(game_state: GameState, player_positions: list, opponent_positions: list) -> list[Move]:
    board = game_state.board.array
    player_set = set(player_positions)
    opponent_set = set(opponent_positions)
    sumitos = []

    for start in player_positions:
        for direction in DIRECTIONS:
            seq = _find_marble_sequence(board, start, direction, player_set, opponent_set)
            if seq and _can_sumito(seq, direction, board):
                new_player = [(p[0] + direction[0], p[1] + direction[1]) for p in seq["player"]]
                new_opponent = []
                for p in seq["opponent"]:
                    nx, ny = p[0] + direction[0], p[1] + direction[1]
                    idx = _flat_index(nx, ny)
                    if idx != -1 and board[idx] != -1:
                        new_opponent.append((nx, ny))
                sumitos.append(Move(
                    seq["player"],
                    new_player,
                    game_state.turn,
                    seq["opponent"],
                    new_opponent,
                ))

    return sumitos


def generate_all_legal_moves(game_state: GameState) -> list[Move]:
    """Generate every legal move for the current player."""
    player_positions = game_state.piece_positions(game_state.turn)
    opponent_positions = game_state.piece_positions(game_state.turn.opponent)

    moves = []

    # Single marble moves
    for pos in player_positions:
        moves.extend(_get_valid_moves(game_state, pos))

    # Two marble moves
    for p1, p2 in combinations(player_positions, 2):
        moves.extend(_get_valid_moves(game_state, p1, p2))

    # Three marble moves
    for p1, p2, p3 in combinations(player_positions, 3):
        moves.extend(_get_valid_moves(game_state, p1, p2, p3))

    # Sumito moves
    moves.extend(_generate_sumitos(game_state, player_positions, opponent_positions))

    return moves
