import discord
from discord.ext import commands
from discord.ext import tasks
import time

import Chess_Bot.cogs.Utility as util
from Chess_Bot.cogs.CPP_IO import *

MAX_TIME_PER_MOVE = 3 * 24 * 60 * 60
LOW_TIME_WARN = 24 * 60 * 60

class Timer(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.no_time_check.start()
        self.low_time_warn.start()
        
    @commands.command()
    async def reset(self, ctx):
        
        if not await util.has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to reset')
            return
        
        util.last_moved.clear()
        util.warned.clear()
        
        for k in util.games.keys():
            util.last_moved[k] = time.time()
            util.warned[k] = False
        
        await ctx.send('Times reset')
            
    async def send_low_time_warning(self, person):
        file_in, file_out = prepare_files(person)
        prepare_input(person)
        
        await run_engine(file_in, file_out)
        
        f = open(file_out)
        out = f.readlines()
        f.close()
        
        user = await self.client.fetch_user(person)
        
        embed = discord.Embed(
            title=f'{user}\'s game', description=f'{whiteblack[util.colors[user.id]].capitalize()} to move.\nYou are low on time.', color=0x5ef29c)
        
        for i in range(len(out) - 1, 0, -1):
            if out[i].startswith('-----'):
                util.get_image(person, i - 1)

                temp_channel = self.client.get_channel(806967405414187019)
                image_msg = await temp_channel.send(file=discord.File(f'Chess_Bot/data/image-{person}.png'))

                image_url = image_msg.attachments[0].url

                embed.set_image(url=image_url)

                break
        
        try:
            dm = user.dm_channel
            if dm == None:
                dm = await user.create_dm()
                
            await dm.send('You are low on time. Use `$time` to get how much time you have left.', embed=embed)
        except Exception as e:
            print('Exception in send_low_time_warning:', e)
        
    async def send_no_time_message(self, person): 
        user = await self.client.fetch_user(person)
               
        util.games.pop(person)
        util.warned.pop(person)
        util.last_moved.pop(person)
        
        old_rating = util.get_rating(person)
        util.update_rating(person, 0)
        
        try:
            dm = user.dm_channel
            if dm == None:
                dm = await user.create_dm()
            
            await dm.send(f'Your game was automatically forfeited on time. Your new rating is {util.get_rating(person)} ({old_rating} + {util.get_rating(person) - old_rating}')
        except Exception as e:
            print('Exception in send_no_time_message:', e)
        
    @commands.command()
    async def time(self, ctx, *user : discord.Member):
        
        person = -1
        if len(user) == 1:
            person = user[0].id
        else:
            person = ctx.author.id
            
        if not person in util.games.keys():
            if len(user) == 1:
                await ctx.send(f'{user[0]} does not have a game in progress')
            else:
                await ctx.send('You do not have a game in progress')
            return
    
        if len(user) == 1:
            await ctx.send(f'{user[0]} has {util.pretty_time(util.last_moved[person] + MAX_TIME_PER_MOVE - time.time())} left.')
        else:
            await ctx.send(f'You have {util.pretty_time(util.last_moved[person] + MAX_TIME_PER_MOVE - time.time())} left.')
            
    @tasks.loop(seconds=10)
    async def low_time_warn(self):
        for k in util.last_moved.keys():
            time_left = util.last_moved[k] + MAX_TIME_PER_MOVE - time.time()
            
            if time_left < LOW_TIME_WARN and not util.warned[k]:
                await self.send_low_time_warning(k)
                util.warned[k] = True
                
    @tasks.loop(seconds=10)
    async def no_time_check(self):
        for k in util.last_moved.keys():
            time_left = util.last_moved[k] + MAX_TIME_PER_MOVE - time.time()
            
            if time_left < 0:
                await self.send_no_time_message(k)
        
    @low_time_warn.before_loop
    @no_time_check.before_loop
    async def wait_until_ready(self):
        print('Waiting for bot to get ready')
        await self.client.wait_until_ready()