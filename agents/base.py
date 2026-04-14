"""Base class for Abalone agents."""

from abc import ABC, abstractmethod


class AbaloneAgent(ABC):
    @abstractmethod
    def select_move(self, game_state: dict) -> dict:
        """
        Receive the full state from GET /api/games/{id}/state.

        game_state contains:
            board        - 9x9 integer grid (0=empty, 1=black, 2=white, -1=void)
            turn         - "black" or "white"
            your_turn    - bool
            captures     - {"black": int, "white": int}
            legal_moves  - list of {"from": [...], "to": [...], "pushed"?: [...]}
            move_number  - int
            status       - "waiting" | "in_progress" | "game_over"

        Return either:
            {"move_index": int}               - pick from the legal_moves list
            {"from": [...], "to": [...]}      - explicit move in algebraic notation
        """
        ...
