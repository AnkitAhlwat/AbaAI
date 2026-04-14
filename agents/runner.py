"""
Bot runner — connects an AbaloneAgent to the game server.

Usage:
    python -m agents.runner --server http://localhost:8000 --create
    python -m agents.runner --server http://localhost:8000 --join GAME_ID
    python -m agents.runner --server http://localhost:8000 --join GAME_ID --agent random
"""

from __future__ import annotations

import argparse
import importlib
import time

import requests

from agents.base import AbaloneAgent


class RandomAgent(AbaloneAgent):
    """Picks a random legal move."""

    def select_move(self, game_state: dict) -> dict:
        import random
        idx = random.randrange(len(game_state["legal_moves"]))
        return {"move_index": idx}


BUILTIN_AGENTS = {
    "random": lambda: RandomAgent(),
    "alphabeta": lambda: importlib.import_module("agents.alphabeta.agent").AlphaBetaAgent(),
}


def load_agent(name: str) -> AbaloneAgent:
    if name in BUILTIN_AGENTS:
        return BUILTIN_AGENTS[name]()

    module_path, _, class_name = name.rpartition(".")
    if module_path:
        mod = importlib.import_module(module_path)
        cls = getattr(mod, class_name)
        return cls()

    raise ValueError(f"Unknown agent: {name}")


def run(server: str, agent: AbaloneAgent, game_id: str | None, create: bool, layout: str, poll_interval: float):
    api = server.rstrip("/") + "/api"

    if create:
        resp = requests.post(f"{api}/games", json={"layout": layout})
        resp.raise_for_status()
        data = resp.json()
        game_id = data["game_id"]
        token = data["token"]
        color = data["color"]
        print(f"Created game {game_id} as {color}")
        print(f"Share this game ID for the opponent to join: {game_id}")
    elif game_id:
        resp = requests.post(f"{api}/games/{game_id}/join")
        resp.raise_for_status()
        data = resp.json()
        token = data["token"]
        color = data["color"]
        print(f"Joined game {game_id} as {color}")
    else:
        raise ValueError("Must specify --create or --join GAME_ID")

    headers = {"X-Player-Token": token}

    print("Waiting for game to start...")
    while True:
        resp = requests.get(f"{api}/games/{game_id}/state", headers=headers)
        resp.raise_for_status()
        state = resp.json()

        if state["status"] == "game_over":
            winner = state.get("winner", "unknown")
            print(f"Game over! Winner: {winner}")
            break

        if state["status"] == "waiting":
            time.sleep(poll_interval)
            continue

        if not state["your_turn"]:
            time.sleep(poll_interval)
            continue

        move = agent.select_move(state)
        print(f"Move {state['move_number'] + 1}: {move}")

        resp = requests.post(f"{api}/games/{game_id}/move", headers=headers, json=move)
        resp.raise_for_status()


def main():
    parser = argparse.ArgumentParser(description="AbaAI Bot Runner")
    parser.add_argument("--server", default="http://localhost:8000", help="Server URL")
    parser.add_argument("--create", action="store_true", help="Create a new game")
    parser.add_argument("--join", metavar="GAME_ID", help="Join an existing game")
    parser.add_argument("--agent", default="random", help="Agent to use (random, alphabeta, or dotted.path.ClassName)")
    parser.add_argument("--layout", default="Default", help="Board layout (Default, Belgian Daisy, German Daisy)")
    parser.add_argument("--poll", type=float, default=0.5, help="Poll interval in seconds")

    args = parser.parse_args()
    agent = load_agent(args.agent)
    run(args.server, agent, args.join, args.create, args.layout, args.poll)


if __name__ == "__main__":
    main()
