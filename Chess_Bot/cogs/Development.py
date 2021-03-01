import discord
import os
from discord.ext import commands
import sys
import time

from Chess_Bot.cogs.Utility import *
from Chess_Bot.cogs.CPP_IO import *

class Development(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def get_gcc(self):
        out, err, status = await run('apt-get install g++')
        print(f'stdout: {out}\nstderr: {err}\n{status}')

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.default)
    async def update(self, ctx, flags = ''):
        '''
        Compiles the latest version of Chess Bot
        Compiler: g++
        (Bot developers only)
        '''

        if not await has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to update')
            return
        
        compile_cmd = 'g++ '
        for filename in os.listdir('engine'):
            if filename[-4:] == '.cpp' or filename[-2:] == '.h':
                compile_cmd += f'engine/{filename} '
        compile_cmd += flags
        
        await ctx.send(compile_cmd)

        out, err, status = await run(compile_cmd)

        message = f'Updated\nCompile Message: {out}\nStderr: {err}'
        
        if len(message) >= 2000:
            f = open('Chess_Bot/data/message.txt', 'w')
            f.write(message)
            f.close()
            await ctx.send(file=discord.File('Chess_Bot/data/message.txt'))
        else:
            await ctx.send(message)
        
        await ctx.send(status)

    
    @commands.command()
    async def shell(self, ctx, cmd):
        '''
        Executes shell commands
        (Bot developers only)
        '''
        await ctx.send(f'Executing command "{cmd}"...')

        if ctx.author.id != 716070916550819860:
            await ctx.send('Geniosity limit exceeded. Try again later')
            return

        stdout, stderr, status = await run(cmd)
        
        message = f'Stdout: {stdout}\nStderr: {stderr}'
        
        if len(message) >= 2000:
            f = open('Chess_Bot/data/message.txt', 'w')
            f.write(message)
            f.close()
            await ctx.send(file=discord.File('Chess_Bot/data/message.txt'))
        else:
            await ctx.send(message)
            
        await ctx.send(status)

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.default)
    async def restart(self, ctx):
        '''
        Restarts the bot
        (Bot developers only)
        '''

        if not await has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to restart')
            return

        await ctx.send(f'Restarting...')
        
        push_games()
        push_ratings()
        
        data_channel = await self.client.fetch_channel(814962871532257310)
        
        await data_channel.send(file=discord.File('Chess_Bot/data/games.txt'))
        await data_channel.send(file=discord.File('Chess_Bot/data/times.txt'))
        await data_channel.send(file=discord.File('Chess_Bot/data/colors.txt'))
        await data_channel.send(file=discord.File('Chess_Bot/data/ratings.txt'))

        sys.exit()

    @commands.command()
    @commands.has_any_role('Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger')
    async def git_pull(self, ctx):
        '''
        Pulls from the github repository
        (Bot developers only)
        '''
        await ctx.send(f'Executing command "git pull"...')

        if not await has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to git_pull')
            return

        stdout, stderr, status = await run(f'git pull')

        message = f'Stdout: {stdout}\nStderr: {stderr}'
        
        if len(message) >= 2000:
            f = open('Chess_Bot/data/message.txt', 'w')
            f.write(message)
            f.close()
            await ctx.send(file=discord.File('Chess_Bot/data/message.txt'))
        else:
            await ctx.send(message)
            
        await ctx.send(status)
        
       
    @commands.command()
    async def debug_load(self, ctx, user : discord.Member):
        '''
        Loads <user>'s game to your game
        (Bot developers only)
        '''

        if not await has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to debug_load')
            return

        if not user.id in games.keys():
            await ctx.send(f'<@{user.id}> does not have a game in progress')
            return
        
        games[ctx.author.id] = games[user.id]
        colors[ctx.author.id] = colors[user.id]
        
        await ctx.send(f'Succesfully loaded game')

    @commands.command()
    async def debug(self, ctx, *, code):
        '''
        Runs python code
        '''
        if not await has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to debug')
            return
        
        await ctx.send(eval(code))

    @commands.command()
    async def execute(self, ctx, *, code):
        '''
        Runs python code
        '''
        if ctx.author.id != 716070916550819860:
            await ctx.send('Geniosity limit exceeded. Try again later')
            return
        
        exec(code)

        await ctx.send('Code done executing')
        
    @commands.command()
    async def gimme(self, ctx, file):
        '''
        Sends files
        '''
        if '..' in file and ctx.author.id != 716070916550819860:
            await ctx.send('Geniosity limit exceeded. Try again later')
            return
            
        if not await has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to get files')
            return
        
        await ctx.send(file, file=discord.File(file))