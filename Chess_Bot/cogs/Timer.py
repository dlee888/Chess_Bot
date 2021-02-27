import discord
from discord.ext import commands
from discord.ext import tasks
import time

from Chess_Bot.cogs.Utility import *
from Chess_Bot.cogs.CPP_IO import *

MAX_TIME_PER_MOVE = 3 * 24 * 60 * 60
LOW_TIME_WARN = 24 * 60 * 60

class Timer(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def reset(self, ctx):
        
        if not await has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to reset')
            return
        
        last_moved.clear()
        
        for k in games.keys():
            last_moved[k] = time.time()
        
        await ctx.send('Times reset')
            
    async def send_low_time_warning(self, person):
        file_in, file_out = prepare_files(person)
        prepare_input(person)
        
        await run_engine(file_in, file_out)
        
        f = open(file_out)
        out = f.readlines()
        f.close()
        
        user = self.client.fetch_user(person)
        
        embed = discord.Embed(
            title=f'{user}\'s game', description=f'{whiteblack[colors[user.id]].capitalize()} to move.\nYou are low on time.', color=0x5ef29c)
        
        for i in range(len(out) - 1, 0, -1):
            if out[i].startswith('-----'):
                get_image(person, i - 1)

                temp_channel = self.client.get_channel(806967405414187019)
                image_msg = await temp_channel.send(file=discord.File(f'Chess_Bot/data/image-{person}.png'))

                image_url = image_msg.attachments[0].url

                embed.set_image(url=image_url)

                break
        
        dm = user.dm_channel
        if dm == None:
            dm = await user.create_dm()
            
        await dm.send('You are low on time. Use `$time` to get how much time you have left.', embed=embed)
        
    async def send_no_time_message(self, person): 
        user = self.client.fetch_user(person)
               
        games.pop(person)
        update_rating(person, 0)
        
        dm = user.dm_channel
        if dm == None:
            dm = await user.create_dm()
        
        await dm.send(f'Your game was automatically forfeited on time. Your new rating is {get_rating(person)}')
        
    @commands.command()
    async def time(self, ctx, *user : discord.Member):
        
        person = -1
        if len(user) == 1:
            person = user[0].id
        else:
            person = ctx.author.id
            
        if not person in games.keys():
            if len(user) == 1:
                await ctx.send(f'{user[0]} does not have a game in progress')
            else:
                await ctx.send('You do not have a game in progress')
            return
    
        if len(user) == 1:
            await ctx.send(f'{user[0]} has {pretty_time(time.time() - last_moved[person])} left.')
        else:
            await ctx.send(f'You have {pretty_time(time.time() - last_moved[person])} left.')
            
    @tasks.loop(seconds=10)
    async def low_time_warn(self):
        for k in last_moved.keys():
            time_left = last_moved[k] + MAX_TIME_PER_MOVE - time.time()
            
            if time_left < LOW_TIME_WARN:
                await self.send_low_time_warning(k)
                
    @tasks.loop(seconds=10)
    async def no_time_check(self):
        for k in last_moved.keys():
            time_left = last_moved[k] + MAX_TIME_PER_MOVE - time.time()
            
            if time_left < 0:
                await self.send_no_time_message(k)
        
    @low_time_warn.before_loop
    @no_time_check.before_loop
    async def wait_until_ready(self):
        print('Waiting for bot to get ready')
        await self.client.wait_until_ready()