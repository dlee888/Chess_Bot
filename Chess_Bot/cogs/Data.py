import discord
from discord.ext import commands
from discord.ext import tasks

from Chess_Bot.cogs.Utility import *

class Data(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game(name='$help or $botinfo for more info'))
        print('Getting data...')
        
        await self.download_data()
        
        pull_games()
        pull_ratings()  
         
        self.sync_data.start()
        
        print('Bot is ready') 
    
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
        
    @tasks.loop(hours=1)
    async def sync_data(self):
        push_games()
        push_ratings()
        
        data_channel = await self.client.fetch_channel(814962871532257310)
        
        await data_channel.send(file=discord.File('Chess_Bot/data/games.txt'))
        await data_channel.send(file=discord.File('Chess_Bot/data/times.txt'))
        await data_channel.send(file=discord.File('Chess_Bot/data/colors.txt'))
        await data_channel.send(file=discord.File('Chess_Bot/data/ratings.txt'))
        await data_channel.send(file=discord.File('Chess_Bot/data/timer.txt'))
        
    @sync_data.before_loop
    async def wait_until_ready(self):
        print('Waiting for bot to get ready')
        await self.client.wait_until_ready()
        
    async def upload_data(self):
        data_channel = await self.client.fetch_channel(814962871532257310)
        
        await data_channel.send(file=discord.File('Chess_Bot/data/games.txt'))
        await data_channel.send(file=discord.File('Chess_Bot/data/times.txt'))
        await data_channel.send(file=discord.File('Chess_Bot/data/colors.txt'))
        await data_channel.send(file=discord.File('Chess_Bot/data/ratings.txt'))
        await data_channel.send(file=discord.File('Chess_Bot/data/timer.txt'))
        
    async def download_data(self):
        data_channel = await self.client.fetch_channel(814962871532257310)
        log_channel = await self.client.fetch_channel(798277701210341459)
        await log_channel.send('Downloading data...')
        
        games_found = False
        times_found = False
        colors_found = False
        ratings_found = False
        timer_found = False
        
        async for message in data_channel.history(limit=25):
            # await log_channel.send(f'Processing message {message.jump_url}')
            for attachment in message.attachments:
                if not games_found and attachment.filename == 'games.txt':
                    games_found = True
                    await log_channel.send(str(await attachment.save('Chess_Bot/data/games.txt')))
                if not times_found and attachment.filename == 'times.txt':
                    times_found = True
                    await log_channel.send(str(await attachment.save('Chess_Bot/data/times.txt')))
                if not timer_found and attachment.filename == 'timer.txt':
                    timer_found = True
                    await log_channel.send(str(await attachment.save('Chess_Bot/data/timer.txt')))
                if not colors_found and attachment.filename == 'colors.txt':
                    colors_found = True
                    await log_channel.send(str(await attachment.save('Chess_Bot/data/colors.txt')))
                if not ratings_found and attachment.filename == 'ratings.txt':
                    ratings_found = True
                    await log_channel.send(str(await attachment.save('Chess_Bot/data/ratings.txt')))
                    
        return games_found, times_found, colors_found, ratings_found, timer_found
        
    @commands.command()
    async def upload(self, ctx):
        if not await has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to upload')
            return
        
        await self.upload_data()
        
        await ctx.send('Finished uploading data')
        
    @commands.command()
    async def download(self, ctx):
        if not await has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to download')
            return
        
        status = await self.download_data()
        filenames = ['games.txt', 'times.txt', 'colors.txt', 'ratings.txt', 'timer.txt']
        for i in range(4):
            if not status[i]:
                await ctx.send(f'File {filenames[i]} not found in the last 25 message')
                
        await ctx.send('Finished downloading data')