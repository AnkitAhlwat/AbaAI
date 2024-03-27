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


@app.route('/api/game/start', methods=['POST'])
def start_game():
    game_status = app.game.start_game()
    return jsonify(game_status), 200


@app.route('/api/game', methods=['GET'])
def get_game_status():
    game_status = app.game.get_game_status()
    return jsonify(game_status)


@app.route('/api/game/move', methods=['POST'])
def make_move():
    if request.is_json:
        data = request.get_json()
        game_status = app.game.make_move(data)
        return jsonify(game_status)

    return jsonify({"error": "Invalid JSON"}), 400


@app.route('/api/game/aiMove', methods=['GET'])
def ai_move():
    selected_move = app.game.get_ai_move()
    return jsonify(selected_move)


@app.route('/api/game/undo', methods=['POST'])
def undo_move():
    game_status = app.game.undo_move()
    return jsonify(game_status)


@app.route('/api/game/reset', methods=['POST'])
def reset_game():
    if request:
        # data = request.get_json()
        print("In da reset")
        game_status = app.game.reset_game()
        return jsonify(game_status)

    return jsonify({"error": "Invalid JSON"}), 400


@app.route('/api/game/possibleMoves', methods=['GET'])
def possible_moves():
    moves = app.game.get_possible_moves()
    return jsonify(moves)


if __name__ == "__main__":
    app.run()
