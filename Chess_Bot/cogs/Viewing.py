import discord
from discord.ext import commands

import Chess_Bot.cogs.Utility as util
import Chess_Bot.cogs.Data as data
import Chess_Bot.cogs.Images as image
from Chess_Bot.cogs.CPP_IO import *

class Viewing(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command()
	@commands.cooldown(1, 10, commands.BucketType.default)
	async def view(self, ctx, *user : discord.Member):
		'''
		Views your current game
		'''
		person = -1
		if len(user) == 1:
			person = user[0].id
		else:
			person = ctx.author.id
			
		game = data.data_manager.get_game(person)

		if game == None:
			if len(user) == 1:
				await ctx.send(f'{user[0]} does not have a game in progress')
			else:
				await ctx.send('You do not have a game in progress')
			return
		
		if person in util.thonking:
			await ctx.send('Chess Bot is in the middle of thinking. Try again later.')
			return

		file_in, file_out = prepare_files(person)
		prepare_input(person)
		
		await run_engine(file_in, file_out)
		
		await output_move(ctx, person)

	@commands.command()
	@commands.cooldown(1, 10, commands.BucketType.default)
	async def fen(self, ctx, *user : discord.Member):
		'''
		Sends current game in FEN format
		'''

		person = -1
		if len(user) == 1:
			person = user[0].id
		else:
			person = ctx.author.id
			
		game = data.data_manager.get_game(person)

		if game == None:
			if len(user) == 1:
				await ctx.send(f'{user[0]} does not have a game in progress')
			else:
				await ctx.send('You do not have a game in progress')
			return
		
		if person in util.thonking:
			await ctx.send('Chess Bot is in the middle of thinking. Try again later.')
			return

		file_in, file_out = prepare_files(person)

		f = open(file_in, 'w')
		f.write(f'fen\nyes2\n{str(game)}\nquit\n')
		f.close()
		
		await run_engine(file_in, file_out)
		
		f = open(file_out)
		out = f.readlines()
		f.close()

		await ctx.send(f'```{out[-2]}```')
		
	@commands.command()
	async def theme(self, ctx, new_theme = None):
		if new_theme == None:
			cur_theme = data.data_manager.get_theme(ctx.author.id)
			await ctx.send(f'''Your current theme is "{cur_theme}"
Use `$theme <new theme>` to change your theme.
Available themes are:
`{"`, `".join(image.themes_available)}`''')
			return
		
		if not new_theme in image.themes_available:
			await ctx.send(f'''That theme is not available
Available themes are:
`{"`, `".join(image.themes_available)}`''')  
   
		data.data_manager.change_theme(ctx.author.id, new_theme)
		await ctx.send('Theme sucessfully updated')
