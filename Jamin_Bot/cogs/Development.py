import discord
import os
from discord.ext import commands
import sys

class Development(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.default)
    @commands.has_any_role('Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger')
    async def update(self, ctx, flags = ''):
        '''
        Compiles the latest version of Chess Bot
        Compile message of 1 means that there were compile errors
        Compiler: g++
        '''

        if ctx.message.guild.id != 733762995372425337:
            await ctx.send(f'This command can only be used in the Chess Bot Support server')
            return

        compile_cmd = 'g++ '
        for filename in os.listdir('engine'):
            if filename[-4:] == '.cpp' or filename[-2:] == '.h':
                compile_cmd += f'engine/{filename} '
        compile_cmd += flags
        
        await ctx.send(compile_cmd)

        out, err, status = await run(compile_cmd)

        await ctx.send(f'Updated\nCompile Message: ```{out}```\nStderr: ```{err}```')
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
        await ctx.send(f'stdout: {stdout}\nstderr: {stderr}\n{status}')

    @commands.command()
    @commands.has_any_role('Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger')
    @commands.cooldown(1, 15, commands.BucketType.default)
    async def restart(self, ctx):
        '''
        Restarts the bot
        (Bot developers only)
        '''

        if ctx.message.guild.id != 733762995372425337:
            await ctx.send(f'This command can only be used in the Chess Bot Support server')
            return

        await ctx.send(f'Restarting...')

        sys.exit()

    @commands.command()
    @commands.has_any_role('Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger')
    async def git_pull(self, ctx):
        '''
        Pulls from the github repository
        (Bot developers only)
        '''
        await ctx.send(f'Executing command "git pull"...')

        if ctx.message.guild.id != 733762995372425337:
            await ctx.send(f'This command can only be used in the Chess Bot Support server')
            return

        stdout, stderr, status = await run(f'git pull')

        await ctx.send(f'stdout: {stdout}\nstderr: {stderr}')
        await ctx.send(status)