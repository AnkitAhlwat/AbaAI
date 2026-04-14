"""
Alpha-beta pruning agent with iterative deepening.

Ported from the original AlphaBetaPruningAgentAnkit.
Uses the server engine internally for move generation during search.
"""

from __future__ import annotations

import sys
import os
import time

# Add project root to path so we can import the engine
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from server.engine import Board, Piece, GameState, GameStateUpdate, generate_all_legal_moves
from agents.base import AbaloneAgent
from .heuristics import board_control, piece_advantage, terminal_score, clumping


class AlphaBetaAgent(AbaloneAgent):
    def __init__(self, max_depth: int = 4, max_time_sec: float = 10.0):
        self.max_depth = max_depth
        self.max_time_sec = max_time_sec
        self._max_player: int = 1
        self._eval_cache: dict[int, float] = {}

    def select_move(self, game_state: dict) -> dict:
        board_grid = game_state["board"]
        turn = Piece.BLACK if game_state["turn"] == "black" else Piece.WHITE
        self._max_player = turn.value

        board = Board(board_grid)
        state = GameState(
            board,
            turn,
            board.count(Piece.BLACK.value),
            board.count(Piece.WHITE.value),
        )

        move = self._iterative_deepening(state)
        if move is None:
            return {"move_index": 0}
        return move.to_notation()

    def _iterative_deepening(self, state: GameState):
        start = time.time()
        best_move = None

        for depth in range(1, self.max_depth + 1):
            move, _ = self._alpha_beta_root(state, depth, start)
            if time.time() - start >= self.max_time_sec:
                break
            if move is not None:
                best_move = move

        return best_move

    def _alpha_beta_root(self, state: GameState, max_depth: int, start: float):
        alpha = float("-inf")
        beta = float("inf")
        best_move = None

        moves = sorted(generate_all_legal_moves(state))
        for move in moves:
            child = GameStateUpdate(state, move).resulting_state
            value = self._min_value(child, alpha, beta, max_depth - 1, start)
            if value > alpha:
                best_move = move
                alpha = value

        return best_move, alpha

    def _max_value(self, state: GameState, alpha: float, beta: float, depth: int, start: float) -> float:
        if time.time() - start >= self.max_time_sec:
            return self._evaluate(state)
        if state.is_game_over() or depth == 0:
            return self._evaluate(state)

        value = float("-inf")
        for move in sorted(generate_all_legal_moves(state)):
            child = GameStateUpdate(state, move).resulting_state
            value = max(value, self._min_value(child, alpha, beta, depth - 1, start))
            alpha = max(alpha, value)
            if value >= beta:
                return value
        return value

    def _min_value(self, state: GameState, alpha: float, beta: float, depth: int, start: float) -> float:
        if time.time() - start >= self.max_time_sec:
            return self._evaluate(state)
        if state.is_game_over() or depth == 0:
            return self._evaluate(state)

        value = float("inf")
        for move in sorted(generate_all_legal_moves(state)):
            child = GameStateUpdate(state, move).resulting_state
            value = min(value, self._max_value(child, alpha, beta, depth - 1, start))
            beta = min(beta, value)
            if value <= alpha:
                return value
        return value

    def _evaluate(self, state: GameState) -> float:
        h = hash(state)
        if h in self._eval_cache:
            return self._eval_cache[h]

        mp = self._max_player
        if state.turn.value == mp:
            rem_player = state.remaining_player_marbles
            rem_opp = state.remaining_opponent_marbles
        else:
            rem_player = state.remaining_opponent_marbles
            rem_opp = state.remaining_player_marbles

        score = (
            clumping(state.board.array, mp)
            + 10 * board_control(state.board.array, mp)
            + 10000 * piece_advantage(rem_player, rem_opp)
            + 10000000 * terminal_score(rem_player, rem_opp)
        )

        self._eval_cache[h] = score
        return score
