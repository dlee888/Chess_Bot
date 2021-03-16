import discord
from discord.ext import commands

import Chess_Bot.cogs.Utility as util


class Mooderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def abort(self, ctx, user: discord.Member):
        '''
        Aborts a game
        '''

        if not await util.has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send('You do not have permission to abort games')
            return

        if not user.id in util.games.keys():
            await ctx.send(f'{user} does not have a game in progress')
            return

        util.games.pop(user.id)
        util.last_moved.pop(user.id)

        await ctx.send('Game aborted')

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def refund(self, ctx, user: discord.Member, points: float):
        '''
        Refunds rating points to a user
        '''

        if not await util.has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Chess-Admin'], self.client):
            await ctx.send('You do not have permission to refund rating')
            return

        util.ratings[user.id] += points
        util.ratings[self.client.user.id] -= points

        await ctx.send(f'{points} points refunded')

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, new_prefix: str):
        util.prefixes[ctx.guild.id] = new_prefix

        await ctx.send('Prefix successfully updated')

        bot = await ctx.guild.fetch_member(self.client.user.id)

        try:
            await bot.edit(nick=f'[{new_prefix}] - Chess Bot')
        except discord.Forbidden:
            await ctx.send(f'Changing nickname to "[{new_prefix}] - Chess Bot" failed. Missing permissions')
