"""Heuristic evaluation functions for Abalone."""

from server.engine.movement import DIRECTIONS

MANHATTAN_WEIGHT = [
    None, None, None, None, 8, 7, 6, 5, 4,
    None, None, None, 7, 6, 5, 4, 3, 4,
    None, None, 6, 5, 4, 3, 2, 3, 4,
    None, 5, 4, 3, 2, 1, 2, 3, 4,
    4, 3, 2, 1, 0, 1, 2, 3, 4,
    4, 3, 2, 1, 2, 3, 4, 5, None,
    4, 3, 2, 3, 4, 5, 6, None, None,
    4, 3, 4, 5, 6, 7, None, None, None,
    4, 5, 6, 7, 8, None, None, None, None,
]

def board_control(board_array: list[int], max_player: int) -> float:
    player_score = 0
    opponent_score = 0
    for index, value in enumerate(board_array):
        if value in (1, 2):
            weight = MANHATTAN_WEIGHT[index]
            if weight is None:
                continue
            if value == max_player:
                player_score += weight
            else:
                opponent_score += weight
    return float(opponent_score - player_score)


def piece_advantage(
    remaining_player: int,
    remaining_opponent: int,
) -> float:
    return float(remaining_player - remaining_opponent)


def terminal_score(
    remaining_player: int,
    remaining_opponent: int,
) -> float:
    if remaining_player < 9:
        return -10000.0
    if remaining_opponent < 9:
        return 10000.0
    return 0.0


def clumping(board_array: list[int], max_player: int) -> float:
    player_clump = 0
    opponent_clump = 0
    for index, value in enumerate(board_array):
        if value not in (1, 2):
            continue
        x = index % 9
        y = index // 9
        adj = 0
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 9 and 0 <= ny < 9 and board_array[ny * 9 + nx] == value:
                adj += 1
        if value == max_player:
            player_clump += adj
        else:
            opponent_clump += adj
    return float(player_clump - opponent_clump)
