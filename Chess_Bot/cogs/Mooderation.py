import discord
from discord.ext import commands
import typing

import Chess_Bot.cogs.Utility as util
import Chess_Bot.cogs.Data as data


class Mooderation(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command()
	@commands.cooldown(1, 3, commands.BucketType.default)
	async def abort(self, ctx, user : typing.Union[discord.User, discord.Member]):
		'''
		Aborts a game
		'''

		if not await util.has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
			await ctx.send('You do not have permission to abort games')
			return

		if data.data_manager.get_game(user.id) == None:
			await ctx.send(f'{user} does not have a game in progress')
			return

		data.data_manager.delete_game(user.id)

		await ctx.send('Game aborted')

	@commands.command()
	@commands.cooldown(1, 3, commands.BucketType.default)
	async def refund(self, ctx, person: typing.Union[discord.User, discord.Member], amount: float):
		'''
		Refunds rating points to a user
		'''

		if not await util.has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Chess-Admin'], self.client):
			await ctx.send('You do not have permission to refund rating')
			return

		if data.data_manager.get_rating(person.id) == None:
			data.data_manager.change_rating(person.id, 1500)
		if data.data_manager.get_rating(801501916810838066) == None:
			data.data_manager.change_rating(801501916810838066, 1500)

		data.data_manager.change_rating(person.id, data.data_manager.get_rating(person.id) + amount)
		data.data_manager.change_rating(801501916810838066, data.data_manager.get_rating(801501916810838066) + amount)

		await ctx.send(f'{amount} points refunded')

	@commands.command()
	@commands.cooldown(1, 3, commands.BucketType.default)
	@commands.has_permissions(administrator=True)
	async def prefix(self, ctx, new_prefix: str):
		data.data_manager.change_prefix(ctx.guild.id, new_prefix)

		await ctx.send('Prefix successfully updated')

		bot = await ctx.guild.fetch_member(self.client.user.id)

		try:
			await bot.edit(nick=f'[{new_prefix}] - Chess Bot')
		except discord.Forbidden:
			await ctx.send(f'Changing nickname to "[{new_prefix}] - Chess Bot" failed. Missing permissions')
			
	@commands.command()
	@commands.cooldown(1, 3, commands.BucketType.default)
	async def gift(self, ctx, person : typing.Union[discord.User, discord.Member], amount : float):
		if not await util.has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
			await ctx.send('You do not have permission to gift rating')
			return
		
		if data.data_manager.get_rating(person.id) == None:
			data.data_manager.change_rating(person.id, 1500)
   
		data.data_manager.change_rating(person.id, data.data_manager.get_rating(person.id) + amount)
		
		await ctx.send(f'{amount} rating points gifted.')