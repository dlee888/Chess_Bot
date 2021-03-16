from discord.ext import commands
import random
import time

import Chess_Bot.cogs.Utility as util
from Chess_Bot.cogs.CPP_IO import *

class Engine(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command(aliases=['play'])
	@commands.cooldown(1, 5, commands.BucketType.default)
	async def move(self, ctx, move):
		'''
		Plays <move> against the computer
		Please enter the move in algebraic notation
		For example, Nxe4, Nge5, c4, Ke2, etc
		More about algebraic notation here: https://www.chess.com/article/view/chess-notation#algebraic-notation
		'''
		if not ctx.author.id in util.games.keys():
			await ctx.send('You do not have a game in progress with Chess Bot')
			return

		if ctx.author.id in util.thonking:
			await ctx.send('Chess Bot is already thinking')
			return

		person = ctx.author.id
		
		thonk = self.client.get_emoji(814285875265536001)
		await ctx.message.add_reaction(thonk)
		util.thonking.append(person)
		
		file_in, file_out = prepare_files(person)
		prepare_input(person, move)

		await run_engine(file_in, file_out)

		await log(person, self.client, ctx)
	
		code = await output_move(ctx, person, self.client)
		
		if code == 'GAME STILL IN PROGRESS':
			util.last_moved[person] = time.time()
			util.warned[person] = False
			return
		
		if code == 'ILLEGAL MOVE PLAYED':
			await ctx.send('Illegal move played. Make sure your move is in algebraic notation.\nType "$help move" for more info')
			return

		old_rating = util.get_rating(ctx.author.id)
		
		if code == 'COMPUTER RESIGNED':
			await ctx.send('Chess Bot resigned')
			util.update_rating(ctx.author.id, 1)        
		elif code == 'DRAW':
			util.update_rating(ctx.author.id, 1/2)
			await ctx.send('Draw')
		elif code[:5].lower() == whiteblack[util.colors[ctx.author.id]]:
			util.update_rating(ctx.author.id, 1)
			await ctx.send('You won!')
		elif code[:5].lower() == whiteblack[1 - util.colors[ctx.author.id]]:
			util.update_rating(ctx.author.id, 0)
			await ctx.send('You lost.')
		else:
			await ctx.send('Something went wrong. <:thonkery:532458240559153163>')
			return

		await ctx.send(f'Your new rating is {round(util.get_rating(ctx.author.id))} ({round(old_rating)} + {round(util.get_rating(person) - old_rating)})')
		
		util.games.pop(ctx.author.id)
		util.last_moved.pop(person)
		util.warned.pop(person)


	@commands.command()
	@commands.cooldown(1, 3, commands.BucketType.default)
	async def challenge(self, ctx, *flags):
		'''
		Challenges Chess Bot to a game
		Your color is assigned randomly.
		Flags:
			-t to set time control (in seconds)
		'''
		if ctx.author.id in util.games.keys():
			await ctx.send('You already have a game in progress')
			return
		
		person = ctx.author.id
		

		util.games[person] = []
		util.colors[person] = random.randint(0, 1)  # 1 if white, 0 if black
		
		util.time_control[person] = 30
		util.last_moved[person] = time.time()
		util.warned[person] = False
		
		for i in range(0, len(flags), 2):
			if flags[i] == '-t':
				try:
					time_control = int(flags[i + 1])
				except ValueError:
					await ctx.send('That isn\'t even an integer lol')
					return

				if time_control < 1 or time_control > 120:
					await ctx.send('Please enter an integer between 1 and 120')
					return

				util.time_control[person] = time_control

		await ctx.send(f'Game started with Chess Bot\nYou are {whiteblack[util.colors[person]]}')

		thonk = self.client.get_emoji(814285875265536001)
		await ctx.message.add_reaction(thonk)
		util.thonking.append(person)
		
		file_in, file_out = prepare_files(person)
		prepare_input(person)

		await run_engine(file_in, file_out)
		
		await log(person, self.client, ctx)
		await output_move(ctx, person, self.client)
		util.thonking.remove(person)


	@commands.command()
	@commands.cooldown(1, 3, commands.BucketType.default)
	async def resign(self, ctx):
		'''
		Resigns the game
		'''
		if not ctx.author.id in util.games.keys():
			await ctx.send('You do not have a game in progress')
			return

		util.games.pop(ctx.author.id)
		util.last_moved.pop(ctx.author.id)
		util.warned.pop(ctx.author.id)
		
		old_rating = util.get_rating(ctx.author.id)
		
		util.update_rating(ctx.author.id, 0)
		
		await ctx.send(f'Game resigned. Your new rating is {round(util.get_rating(ctx.author.id))} ({round(old_rating)} + {round(util.get_rating(ctx.author.id) - old_rating)})')
