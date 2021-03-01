import discord
from discord.ext import commands

from Chess_Bot.cogs.Utility import *

class Mooderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def abort(self, ctx, user : discord.Member):
        '''
        Aborts a game
        '''
        
        if not await has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send('You do not have permission to abort games')
            return

        if not user.id in games.keys():
            await ctx.send(f'{user} does not have a game in progress')
            return

        games.pop(user.id)
        last_moved.pop(user.id)
        
        await ctx.send('Game aborted')
        
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def refund(self, ctx, user : discord.Member, points : float):
        '''
        Refunds rating points to a user
        '''
        
        if not await has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Chess-Admin'], self.client):
            await ctx.send('You do not have permission to refund rating')
            return

        ratings[user.id] += points
        ratings[801501916810838066] -= points
        
        await ctx.send(f'{points} points refunded')