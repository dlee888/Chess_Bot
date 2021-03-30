from PIL import Image
import os

import Chess_Bot.cogs.Data as data


themes_available = []


def load_theme(theme):
	themes_available.append(theme)
	
	im = Image.open(f'Chess_Bot/images/{theme}.png')

	os.makedirs(f'Chess_Bot/images/{theme}', exist_ok=True)

	size = im.size
	square_len = size[0] / 8
	piece_names = ['P', 'N', 'B', 'R', 'Q', 'K']

	for piece in range(6):
		row = 6 - (piece // 4) * 2
		col = (2 * piece) % 8

		# print(piece, row, col)

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

			piece_img.save(f'Chess_Bot/images/{theme}/{name}')

	blank_light = im.crop((0, 0, square_len, square_len))
	blank_dark = im.crop((0, square_len, square_len, 2 * square_len))
	blank_light.save(f'Chess_Bot/images/{theme}/blank-light.png')
	blank_dark.save(f'Chess_Bot/images/{theme}/blank-dark.png')


def load_all_themes():
	print('Loading images...')
	for file in os.listdir('Chess_Bot/images'):
		if file.endswith('.png') and file != 'blank_board.png':
			file = file.strip('.png')
			print(f'Loading theme {file}')
			load_theme(file)


def get_image(person, end):
	game_file = f'Chess_Bot/data/output-{person}.txt'
	F = open(game_file)
	game = F.readlines()
	F.close()

	color = data.data_manager.get_game(person).color
	theme = data.data_manager.get_theme(person)

	result = Image.open('Chess_Bot/images/blank_board.png')
	result = result.resize((400, 400))

	for i in range(end - 7, end + 1):
		for j in range(1, 17, 2):
			square = f'Chess_Bot/images/{theme}/'
			if game[i][j] == ' ':
				square += 'blank'
			elif game[i][j].islower():
				square += 'B' + game[i][j].upper()
			else:
				square += 'W' + game[i][j]

			x = i + 7 - end
			y = (j - 1)//2

			if (x + y) % 2 == 0:
				square += '-light.png'
			else:
				square += '-dark.png'

			square_img = Image.open(square)
			square_img = square_img.resize((50, 50), Image.ANTIALIAS)

			x *= 50
			y *= 50

			if color == 1:
				result.paste(square_img, (y, x, y + 50, x + 50))
			else:
				result.paste(square_img, (350 - y, 350 - x, 400 - y, 400 - x))

	result.save(f'Chess_Bot/data/image-{person}.png')


# for testing
if __name__ == '__main__':
	load_all_themes()
