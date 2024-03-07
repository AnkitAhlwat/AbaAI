from flask import Flask, jsonify, request
from flask_cors import CORS

from abalone.game import Game

app = Flask(__name__)
CORS(app)

# Initialize a global game object to be used by the API
app.game = Game()


@app.route('/api/game/configure', methods=['POST'])
def configure_game():
    if request.is_json:
        data = request.get_json()
        response = app.game.set_up(data)
        return jsonify(response)

    return jsonify({"error": "Invalid JSON"}), 400


@app.route('/api/game/move', methods=['POST'])
def make_move():
    if request.is_json:
        data = request.get_json()
        game_update = app.game.make_move(data)
        return jsonify(game_update.to_json())

    return jsonify({"error": "Invalid JSON"}), 400


@app.route('/api/game/undo', methods=['POST'])
def undo_move():
    game_update = app.game.undo_move()
    return jsonify(game_update.to_json())

@app.route('/api/game/reset', methods=['POST'])
def reset_game():
    if request:
        # data = request.get_json()
        print("In da reset")
        game_update = app.game.reset_game()
        return jsonify(game_update.to_json())

    return jsonify({"error": "Invalid JSON"}), 400


if __name__ == "__main__":
    app.run()
