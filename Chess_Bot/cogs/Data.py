import discord
from discord.ext import commands
from discord.ext import tasks

from cogs.Utility import *

class Data(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.sync_data.start()
        
    @commands.command()
    async def push_all(self, ctx):
        '''
        Sync variables with txt documents
        '''
        if not await has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to push_all')
            return

        push_games()
        push_ratings()
        await ctx.send('Sucessfully pushed')

    @commands.command()
    async def pull_all(self, ctx):
        '''
        Sync variables with txt documents
        '''
        if not await has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to pull_all')
            return

        pull_games()
        pull_ratings()
        await ctx.send('Sucessfully pulled')
        
    @tasks.loop(seconds=30)
    async def sync_data(self):
        push_games()
        push_ratings()
        
    @sync_data.before_loop
    async def wait_until_ready(self):
        print('Waiting for bot to get ready')
        await self.client.wait_until_ready()