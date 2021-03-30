import os
import discord
from PIL import Image
import time

import Chess_Bot.cogs.Data as data
import Chess_Bot.cogs.Utility as util

whiteblack = ['black', 'white']


def prepare_files(person):
	file_in = f'Chess_Bot/data/input-{person}.txt'
	file_out = f'Chess_Bot/data/output-{person}.txt'

	if not file_in[15:] in os.listdir('Chess_Bot/data'):
		f = open(file_in, 'x')
		f.close()
	if not file_out[15:] in os.listdir('Chess_Bot/data'):
		f = open(file_out, 'x')
		f.close()

	return file_in, file_out



def prepare_input(person, move=''):
	file_in = f'Chess_Bot/data/input-{person}.txt'

	game = data.data_manager.get_game(person)

	f = open(file_in, 'w')
	f.write(
		f'play\nyes2\n{str(game)}\n{game.time_control}\n{whiteblack[1 - game.color]}\n{move}\nquit\nquit\n')
	f.close()


async def run_engine(file_in, file_out):
	# print('Running engine')
	out, err, status = await util.run(f'./engine < {file_in} > {file_out}')
	# print(f'Stdout: {out}\nStderr: {err}\n{status}')


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
	
	
async def output_move(ctx, person):
	f = open(f'Chess_Bot/data/output-{person}.txt')
	out = f.readlines()
	f.close()

	game = data.data_manager.get_game(person)

	embed = discord.Embed(
		title=f'{ctx.author}\'s game', description=f'{whiteblack[game.color].capitalize()} to move.', color=0x5ef29c)
	embed.set_footer(
		text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

	for i in range(len(out) - 1, 0, -1):
		if out[i].startswith('COMPUTER PLAYED'):
			embed.add_field(name='Computer moved', value=out[i][16:])
			break
	
	file = None
	
	for i in range(len(out) - 1, 0, -1):
		if out[i].startswith('|'):
			get_image(person, i)

			file = discord.File(f'Chess_Bot/data/image-{person}.png', filename = 'board.png')
			embed.set_image(url= f'attachment://board.png')

			break

	for i in range(len(out) - 1, 0, -1):
		if out[i].startswith('GAME: '):
			game_str = out[i][6:-1].split(' ')
			game.moves.clear()

			for i in game_str:
				try:
					game.moves.append(int(i))
				except:
					pass

			break

	code = out[-3].strip()

	if code == 'DRAW':
		embed.description = 'Draw'
	elif (code == 'COMPUTER RESIGNED' and game.color == 1) or code == 'WHITE WON':
		embed.description = 'White won.'
	elif (code == 'COMPUTER RESIGNED' and game.color == 0) or code == 'BLACK WON':
		embed.description = 'Black won.'
	elif code == 'ILLEGAL MOVE PLAYED':
		embed.description = f'{whiteblack[game.color].capitalize()} to move.\nIllegal move played.'

	try:
		await ctx.message.reply(file=file, embed=embed)
	except Exception as e:
		if e == discord.Forbidden:
			await ctx.send('Something went wrong. Are you sure Chess Bot has permission to send embeds?')
		else:
			await ctx.send('Something went wrong.')
			await ctx.send(str(e))
			
	return code, game


async def log(person, client, ctx):
	log_channel = client.get_channel(798277701210341459)

	await log_channel.send(f'''Output for {ctx.author} (id = {ctx.author.id})
Request: {ctx.message.content}
{ctx.message}
Jump url: ({ctx.message.jump_url})''', files=[
		discord.File(f'Chess_Bot/data/output-{person}.txt'),
		discord.File(f'Chess_Bot/data/input-{person}.txt')])
