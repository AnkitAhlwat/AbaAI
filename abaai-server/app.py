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
        app.game = Game(data)
        return jsonify(data)

    return jsonify({"error": "Invalid JSON"}), 400


@app.route('/api/game/move', methods=['POST'])
def make_move():
    if request.is_json:
        data = request.get_json()
        game_update = app.game.make_move(data)
        return jsonify(game_update.to_json())

    return jsonify({"error": "Invalid JSON"}), 400


if __name__ == "__main__":
    app.run()
