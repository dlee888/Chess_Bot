import discord
from discord.ext import commands
from discord.ext import tasks
import pickle

import Chess_Bot.cogs.Utility as util

class Data(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game(name='$help or $botinfo for more info'))
        print('Getting data...')
        
        await self.download_data()
        
        # pull_games()
        # pull_ratings()
        
        self.pull_data()  
         
        self.sync_data.start()
        
        print('Bot is ready') 
    
    def pull_data(self):
        util.games, util.colors, util.time_control, util.ratings, util.last_moved, util.warned = pickle.load(open('Chess_Bot/data/database', 'rb'))
        
    def push_data(self):
        pickle.dump([util.games, util.colors, util.time_control, util.ratings, util.last_moved, util.warned], open('Chess_Bot/data/database', 'wb'))
    
    # @commands.command()
    # async def push_all(self, ctx):
    #     '''
    #     Sync variables with txt documents
    #     '''
    #     if not await has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
    #         await ctx.send(f'You do not have permission to push_all')
    #         return

    #     push_games()
    #     push_ratings()
    #     await ctx.send('Sucessfully pushed')

    # @commands.command()
    # async def pull_all(self, ctx):
    #     '''
    #     Sync variables with txt documents
    #     '''
    #     if not await has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
    #         await ctx.send(f'You do not have permission to pull_all')
    #         return

    #     pull_games()
    #     pull_ratings()
    #     await ctx.send('Sucessfully pulled')
        
    @tasks.loop(hours=1)
    async def sync_data(self):
        # push_games()
        # push_ratings()
        
        self.push_data()
        
        await self.upload_data()
        
    @sync_data.before_loop
    async def wait_until_ready(self):
        print('Waiting for bot to get ready')
        await self.client.wait_until_ready()
        
    async def upload_data(self):
        data_channel = await self.client.fetch_channel(814962871532257310)
        
        await data_channel.send(file=discord.File('Chess_Bot/data/database'))
        
    async def download_data(self):
        data_channel = await self.client.fetch_channel(814962871532257310)
        log_channel = await self.client.fetch_channel(798277701210341459)
        await log_channel.send('Downloading data...')
        
        async for message in data_channel.history(limit=25):
            for attachment in message.attachments:
                if attachment.filename == 'database':
                    await log_channel.send(str(await attachment.save('Chess_Bot/data/database')))
                    return True
        
        return False
        
    @commands.command()
    async def upload(self, ctx):
        if not await util.has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to upload')
            return
        
        await self.upload_data()
        
        await ctx.send('Finished uploading data')
        
    @commands.command()
    async def download(self, ctx):
        if not await util.has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to download')
            return
        
        status = await self.download_data()
        
        if status:
            await ctx.send('Finished downloading data')
        else:
            await ctx.send('"database" not found in #data')