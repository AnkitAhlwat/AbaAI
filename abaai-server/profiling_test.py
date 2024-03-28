from abalone.game import Game


def main():
    """

    :return:
    """
    game = Game()

    selected_move = game.get_ai_move()
    print(selected_move)


if __name__ == '__main__':
    main()
