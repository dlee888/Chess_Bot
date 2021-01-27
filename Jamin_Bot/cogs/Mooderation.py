import discord
from discord.ext import commands

from cogs.Utility import *

class Mooderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    @commands.has_any_role('Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger')
    async def abort(self, ctx, user):
        '''
        Aborts a game
        '''

        person = int(user[3:-1])

        if not person in games.keys():
            await ctx.send('You do not have a game in progress')
            return

        games.pop(person)
        await ctx.send('Game aborted')
        push_games()

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    @commands.has_any_role('Admin', 'Mooderator', 'Moderator', 'Chess-Admin')
    async def adminify(self, ctx, user : discord.Member):
        await ctx.send(f'Adminifying {user.name}')
        role = discord.utils.get(user.guild.roles, name='Chess-Admin')
        if role == None:
            await ctx.send('Role "Chess-Admin" not found. Creating role...')
            role = await user.guild.create_role(name='Chess-Admin', color='0x69ff69')
        
        await user.add_roles(role)
        await ctx.send(f'Done adminifying {user.name}')