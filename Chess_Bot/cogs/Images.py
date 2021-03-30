from PIL import Image
import os

from Chess_Bot.cogs import Data as data


def load_theme(theme):
    im = Image.open(f'Chess_Bot/data/images/{theme}.png')


def get_image(person, end):
	game_file = f'Chess_Bot/data/output-{person}.txt'
	F = open(game_file)
	game = F.readlines()
	F.close()

	color = data.data_manager.get_game(person).color

	result = Image.open('Chess_Bot/images/blank_board.png')
	result = result.resize((400, 400))

	for i in range(end - 7, end + 1):
		for j in range(1, 17, 2):
			square = 'Chess_Bot/images/'
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