import tensorflow as tf
import numpy as np
import chess
import os
import time

pieces = {
    'p': 0,
    'n': 1,
    'b': 2,
    'r': 3,
    'q': 4,
    'k': 5
}

white_model = tf.keras.models.load_model(
    os.path.join('data/assets/nnue', 'white'))
black_model = tf.keras.models.load_model(
    os.path.join('data/assets/nnue', 'black'))

game = chess.Board()


def board_to_array(board: chess.Board):
    board_str = str(board).split('\n')
    res = np.zeros((64 * 6), np.float32)

    for row in range(8):
        squares = board_str[row].split(' ')
        for square in range(8):
            if squares[square] == '.':
                continue

            piece = pieces[squares[square].lower()]
            if squares[square].islower():
                res[64 * piece + 8 * row + square] = -1
            else:
                res[64 * piece + 8 * row + square] = 1

    return np.array([res])


def run_nnue():
    if game.turn == chess.WHITE:
        return white_model(board_to_array(game)).numpy()[0][0]
    else:
        return black_model(board_to_array(game)).numpy()[0][0]


nodes = 0


def search(depth, alpha, beta):
    global nodes
    nodes += 1
    if game.is_checkmate():
        return 0
    if game.can_claim_draw():
        return 0.5
    if depth == 0:
        return run_nnue()
    value = 0
    for move in game.generate_legal_moves():
        game.push(move)
        value = max(value, -search(depth - 1, 1 - beta, 1 - alpha))
        game.pop()
        alpha = max(alpha, value)
        if alpha >= beta:
            return alpha
    return value


def get_best_move():
    depth = 1
    while True:
        value = -1
        best_move = None
        starttime = time.time()
        for move in game.generate_legal_moves():
            game.push(move)
            x = -search(depth - 1, 0, 1)
            game.pop()
            if x > value:
                value = x
                best_move = move
        print('depth', depth)
        print('bestmove', best_move.uci())
        print('nodes', nodes, 'time', time.time() - starttime)
        depth += 1

for w in white_model.weights:
    print(w)
# print(black_model.weights)
fen = input()
game = chess.Board(fen)
get_best_move()
