#Example Flask App for a hexaganal tile game
#Logic is in this python file

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Initialize a 6x7 Connect Four board (6 rows, 7 columns)
# Empty slots will be represented by 0, Player 1's chips (red) by 1, and Player 2's chips (green) by 2.
board = [[0] * 7 for _ in range(6)]

# Variable to keep track of which player's turn it is (1 for Player 1, 2 for Player 2)
current_player = 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_board', methods=['GET'])
def get_board():
    return jsonify(board=board, current_player=current_player)

@app.route('/drop_chip', methods=['POST'])

def drop_chip():
    global current_player

    # Get column index from the request
    column = request.json.get('column')

    # Check for a valid column
    if column < 0 or column >= 7:
        return jsonify(message="Invalid column"), 400

    # Find the first available row in the given column
    for row in range(5, -1, -1):
        if board[row][column] == 0:
            board[row][column] = current_player
            break
    else:
        return jsonify(message="Column is full"), 400

    # Switch the player turn (alternating between 1 and 2)
    current_player = 2 if current_player == 1 else 1

    return jsonify(board=board, current_player=current_player)

if __name__ == '__main__':
    app.run(debug=True)