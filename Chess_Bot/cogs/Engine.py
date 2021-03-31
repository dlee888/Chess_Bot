from discord.ext import commands
import random
import time

import Chess_Bot.cogs.Data as data
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

		person = ctx.author.id
		game = data.data_manager.get_game(person)
  
		if game == None:
			await ctx.send('You do not have a game in progress with Chess Bot')
			return

		if person in util.thonking:
			await ctx.send('Chess Bot is already thinking')
			return

		
		thonk = self.client.get_emoji(814285875265536001)
		await ctx.message.add_reaction(thonk)
		util.thonking.append(person)
		
		file_in, file_out = prepare_files(person)
		prepare_input(person, move)

		await run_engine(file_in, file_out)

		await log(person, self.client, ctx)
	
		code, game = await output_move(ctx, person)
		util.thonking.remove(person)
		
		if code == 'GAME STILL IN PROGRESS':
			game.last_moved = time.time()
			game.warned = False
			data.data_manager.change_game(person, game)
			return
		
		if code == 'ILLEGAL MOVE PLAYED':
			await ctx.send('Illegal move played. Make sure your move is in algebraic notation.\nType "$help move" for more info')
			return

		old_rating = data.data_manager.get_rating(person)
		if old_rating == None:
			old_rating = 1500
		
		if code == 'COMPUTER RESIGNED':
			await ctx.send('Chess Bot resigned')
			util.update_rating(ctx.author.id, 1)        
		elif code == 'DRAW':
			util.update_rating(ctx.author.id, 1/2)
			await ctx.send('Draw')
		elif code[:5].lower() == whiteblack[game.color]:
			util.update_rating(ctx.author.id, 1)
			await ctx.send('You won!')
		elif code[:5].lower() == whiteblack[1 - game.color]:
			util.update_rating(ctx.author.id, 0)
			await ctx.send('You lost.')
		else:
			await ctx.send('Something went wrong. <:thonkery:532458240559153163>')
			return

		new_rating = data.data_manager.get_rating(person)
		await ctx.send(f'Your new rating is {round(new_rating)} ({round(old_rating)} + {round(new_rating - old_rating, 2)})')
		
		data.data_manager.delete_game(person)


	@commands.command()
	@commands.cooldown(1, 3, commands.BucketType.default)
	async def challenge(self, ctx, *flags):
		'''
		Challenges Chess Bot to a game
		Your color is assigned randomly.
		Flags:
			-t to set time control (in seconds)
		'''
  
		person = ctx.author.id
  
		game = data.data_manager.get_game(person)
		if game != None:
			await ctx.send('You already have a game in progress')
			return

		game = data.Game(random.randint(0, 1), 30)
		
		for i in range(0, len(flags), 2):
			if flags[i] == '-t':
				try:
					game.time_control = int(flags[i + 1])
				except ValueError:
					await ctx.send('Bruh that isn\'t even an integer.')
					return

				if game.time_control < 1 or game.time_control > 120:
					await ctx.send('Please enter an integer between 1 and 120')
					return

		data.data_manager.change_game(person, game)
  
		await ctx.send(f'Game started with Chess Bot\nYou play the {whiteblack[game.color]} pieces.')

		thonk = self.client.get_emoji(814285875265536001)
		await ctx.message.add_reaction(thonk)
		util.thonking.append(person)
		
		file_in, file_out = prepare_files(person)
		prepare_input(person)

		await run_engine(file_in, file_out)
		
		await log(person, self.client, ctx)
		code, game = await output_move(ctx, person)
		util.thonking.remove(person)
  
		game.last_moved = time.time()
		game.warned = False
		data.data_manager.change_game(person, game)


	@commands.command()
	@commands.cooldown(1, 3, commands.BucketType.default)
	async def resign(self, ctx):
		'''
		Resigns the game
		'''
  
		game = data.data_manager.get_game(ctx.author.id)
  
		if game == None:
			await ctx.send('You do not have a game in progress')
			return

		data.data_manager.delete_game(ctx.author.id)
		
		old_rating = data.data_manager.get_rating(ctx.author.id)
  
		if old_rating == None:
			data.data_manager.change_rating(ctx.author.id, 1500)
			old_rating = 1500
		
		util.update_rating(ctx.author.id, 0)
		
		new_rating = data.data_manager.get_rating(ctx.author.id)
  
		await ctx.send(f'Game resigned. Your new rating is {round(new_rating)} ({round(old_rating)} + {round(new_rating - old_rating, 2)})')
