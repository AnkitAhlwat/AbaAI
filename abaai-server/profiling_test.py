from abalone.game import Game
from abalone.ai.agent_test import count_threes_in_a_row

def main():
    """

    :return:
    """
    # game = Game()
    #
    # selected_move = game.get_ai_move()
    # print(selected_move)

    test_board = [
        [-1, -1, -1, -1, 0, 0, 0, 0, 0],
        [-1, -1, -1, 0, 2, 2, 2, 0, 0],
        [-1, -1, 0, 2, 2, 2, 1, 0, 0],
        [-1, 0, 0, 1, 1, 1, 2, 0, 0],
        [0, 0, 1, 2, 2, 1, 2, 0, 0],
        [0, 1, 2, 2, 1, 1, 1, 0, -1],
        [0, 2, 1, 1, 2, 0, 0, -1, -1],
        [0, 0, 1, 1, 0, 0, -1, -1, -1],
        [0, 0, 0, 0, 0, -1, -1, -1, -1],
    ]

    test_board2 = [
        [-1, -1, -1, -1, 0, 0, 0, 0, 0],
        [-1, -1, -1, 0, 0, 0, 0, 0, 0],
        [-1, -1, 0, 0, 0, 0, 0, 0, 0],
        [-1, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, -1],
        [0, 0, 0, 0, 0, 0, 0, -1, -1],
        [0, 0, 0, 0, 0, 0, -1, -1, -1],
        [0, 0, 0, 0, 0, -1, -1, -1, -1],
    ]

    print(count_threes_in_a_row(test_board, 1))
    print(count_threes_in_a_row(test_board, 2))

    print(count_threes_in_a_row(test_board2, 1))


if __name__ == '__main__':
    main()
