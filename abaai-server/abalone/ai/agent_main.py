from abalone.ai.game_playing_agent_lucas import MiniMaxAgent
from abalone.state import GameState


def main():
    game_state = GameState()

    depth = 1
    agent = MiniMaxAgent(depth)
    move = agent.get_best_move(game_state)
    print(move)


if __name__ == '__main__':
    main()
