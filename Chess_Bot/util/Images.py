from PIL import Image
import os

import chess

import Chess_Bot.util.Data as data
from Chess_Bot import constants

themes_available = []


# 8/8/8/8/qqkk4/QQKK4/ppnnbbrr/PPNNBBRR w - - 0 1
def load_theme(theme):
    themes_available.append(theme)

    im = Image.open(os.path.join(constants.THEMES_DIR, theme + '.png'))

    os.makedirs(os.path.join(constants.THEMES_DIR, theme), exist_ok=True)

    size = im.size
    square_len = size[0] / 8
    piece_names = ['P', 'N', 'B', 'R', 'Q', 'K']

    for piece in range(6):
        row = 6 - (piece // 4) * 2
        col = (2 * piece) % 8

        squares = [(row + 1, col), (row + 1, col + 1),
                   (row, col), (row, col + 1)]

        for square in range(4):
            if square < 2:
                name = 'W'
            else:
                name = 'B'
            name += piece_names[piece]
            if (squares[square][0] + squares[square][1]) % 2 == 0:
                name += '-light.png'
            else:
                name += '-dark.png'

            piece_img = im.crop((squares[square][1] * square_len, squares[square][0] * square_len,
                                 squares[square][1] * square_len + square_len, squares[square][0] * square_len + square_len))

            piece_img.save(os.path.join(constants.THEMES_DIR, theme, name))

    blank_light = im.crop((0, 0, square_len, square_len))
    blank_dark = im.crop((0, square_len, square_len, 2 * square_len))
    blank_light.save(os.path.join(constants.THEMES_DIR, theme, 'blank-light.png'))
    blank_dark.save(os.path.join(constants.THEMES_DIR, theme, 'blank-dark.png'))


def load_all_themes():
    print('Loading images...')
    for file in os.listdir(constants.THEMES_DIR):
        if file.endswith('.png'):
            file = file[:-4]
            load_theme(file)


def get_image(person):
    game = data.data_manager.get_game(person)
    theme = data.data_manager.get_theme(person)
    board = chess.Board(game.fen)

    result = Image.open(os.path.join(constants.ASSETS_DIR, 'blank_board.png'))
    result = result.resize((400, 400))

    for i in range(8):
        for j in range(0, 16, 2):
            square = ''
            if game[i][j] == '.':
                square += 'blank'
            elif game[i][j].islower():
                square += 'B' + game[i][j].upper()
            else:
                square += 'W' + game[i][j]

            x = i
            y = j // 2

            if (x + y) % 2 == 0:
                square += '-light.png'
            else:
                square += '-dark.png'

            square_img = Image.open(os.path.join(constants.THEMES_DIR, theme, square))
            square_img = square_img.resize((50, 50), Image.ANTIALIAS)

            x *= 50
            y *= 50

            if game.color == 1:
                result.paste(square_img, (y, x, y + 50, x + 50))
            else:
                result.paste(square_img, (350 - y, 350 - x, 400 - y, 400 - x))

    result.save(os.path.join(constants.TEMP_DIR, f'image-{person}.png'))
