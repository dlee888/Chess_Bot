import discord
import os
from discord.ext import commands
import sys
import time
import pickle
import typing
import io
import textwrap
import traceback
from contextlib import redirect_stdout

import Chess_Bot.cogs.Utility as util
from Chess_Bot.cogs.CPP_IO import *


class Development(commands.Cog):

    def __init__(self, client):
        self.client = client
        self._last_result = None

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.default)
    async def update(self, ctx, flags=''):
        '''
        Compiles the latest version of Chess Bot
        Compiler: g++
        (Bot developers only)
        '''

        if not await util.has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to update')
            return

        await util.run('make clear')
        out, err, status = await util.run('make')

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

        stdout, stderr, status = await util.run(cmd)

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

        if not await util.has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to restart')
            return

        await ctx.send(f'Restarting...')

        data_channel = await self.client.fetch_channel(814962871532257310)

        await data_channel.send(file=discord.File('Chess_Bot/data/database'))

        sys.exit()

    @commands.command()
    @commands.has_any_role('Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger')
    async def git_pull(self, ctx):
        '''
        Pulls from the github repository
        (Bot developers only)
        '''

        if not await util.has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to run "git pull"')
            return

        await ctx.send(f'Executing command "git pull"...')

        stdout, stderr, status = await util.run(f'git pull')

        message = f'```\nStdout:\n{stdout}Stderr: {stderr}```'

        if len(message) >= 2000:
            f = open('Chess_Bot/data/message.txt', 'w')
            f.write(message)
            f.close()
            await ctx.send(file=discord.File('Chess_Bot/data/message.txt'))
        else:
            await ctx.send(message)

        await ctx.send(status)

    @commands.command()
    async def debug_load(self, ctx, user: typing.Union[discord.User, discord.Member]):
        '''
        Loads <user>'s game to your game
        (Bot developers only)
        '''

        if not await util.has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to debug_load')
            return

        game = data.data_manager.get_game(user.id)

        if game == None:
            await ctx.send(f'{user} does not have a game in progress')
            return

        data.data_manager.change_game(ctx.author.id, game)

        await ctx.send(f'Succesfully loaded game')

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    @commands.command(pass_context=True, hidden=True)
    async def debug(self, ctx, *, body: str):
        """Evaluates a code"""

        if not await util.has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            return

        env = {
            'bot': self.client,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.command()
    async def gimme(self, ctx, file):
        '''
        Sends files
        '''
        if '..' in file and ctx.author.id != 716070916550819860:
            await ctx.send('Geniosity limit exceeded. Try again later')
            return

        if not await util.has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to get files')
            return

        await ctx.send(file, file=discord.File(file))

    @commands.command()
    async def load_db(self, ctx):
        for attachment in ctx.message.attachments:
            if attachment.filename == 'database':
                await attachment.save('Chess_Bot/data/database')
                break

        games, colors, time_control, ratings, last_moved, warned, prefixes = pickle.load(
            open('Chess_Bot/data/database', 'rb'))
        print(games, colors, time_control, ratings,
              last_moved, warned, prefixes)

        await ctx.send('Loading games...')

        for k in games.keys():
            print(games[k])
            print(' '.join(str(x) for x in games[k]))
            data.data_manager.change_game(k, data.Game(
                colors[k], time_control[k], games[k], last_moved[k], warned[k]))

        await ctx.send('Loading ratings...')
        for k in ratings.keys():
            data.data_manager.change_rating(k, ratings[k])

        await ctx.send('Loading prefixes...')
        for k in prefixes.keys():
            data.data_manager.change_prefix(k, prefixes[k])

        await ctx.send('Loaded')

    @commands.command()
    async def troll_change(self, ctx, guild: int, new_prefix):
        if not await util.has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            return

        data.data_manager.change_prefix(guild, new_prefix)

        await ctx.send('Prefix successfully updated')

        bot = await (await self.client.fetch_guild(guild)).fetch_member(801501916810838066)

        try:
            await bot.edit(nick=f'[{new_prefix}] - Chess Bot')
        except discord.Forbidden:
            await ctx.send(f'Changing nickname to "[{new_prefix}] - Chess Bot" failed. Missing permissions')
