import discord
from discord.ext import commands
from discord.ext import tasks

from cogs.Utility import *

class Data(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.sync_data.start()
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Getting data...')
        
        self.download_data()
        
        pull_games()
        pull_ratings()    
    
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
        
    async def upload_data(self):
        data_channel = self.client.fetch_channel(814962871532257310)
        
        await data_channel.send(file=discord.File('data/games.txt'))
        await data_channel.send(file=discord.File('data/times.txt'))
        await data_channel.send(file=discord.File('data/colors.txt'))
        await data_channel.send(file=discord.File('data/ratings.txt'))
        
    async def download_data(self):
        data_channel = self.client.fetch_channel(814962871532257310)
        
        games_found = False
        times_found = False
        colors_found = False
        ratings_found = False
        
        async for message in data_channel.history():
            for attachment in message.attachments:
                if not games_found and attachment.filename == 'games.txt':
                    games_found = True
                    await attachment.save('data/games.txt')
                if not times_found and attachment.filename == 'times.txt':
                    times_found = True
                    await attachment.save('data/times.txt')
                if not colors_found and attachment.filename == 'colors.txt':
                    colors_found = True
                    await attachment.save('data/colors.txt')
                if not ratings_found and attachment.filename == 'ratings.txt':
                    ratings_found = True
                    await attachment.save('data/ratings.txt')
                    
        return games_found, times_found, colors_found, ratings_found
        
    @commands.command()
    async def upload(self, ctx):
        if not await has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to upload')
            return
        
        await self.upload_data()
        
    @commands.command()
    async def download(self, ctx):
        if not await has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to download')
            return
        
        status = await self.download_data()
        filenames = ['games.txt', 'times.txt', 'colors.txt', 'ratings.txt']
        for i in range(4):
            if not status[i]:
                await ctx.send(f'File {filenames[i]} not found in the last 100 message')