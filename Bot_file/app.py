from flask import Flask, render_template, request
from Main_code import process_user_input, start_game

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    response = process_user_input(user_input)
    return response


@app.route('/play_game', methods=['POST'])
def play_game():
    game_choice = request.form['game_choice']
    game_result = start_game(game_choice)
    return game_result


if __name__ == '__main__':
    app.run(debug=True)
