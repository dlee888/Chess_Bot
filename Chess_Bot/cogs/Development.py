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

import Chess_Bot.util.Utility as util
from Chess_Bot.util.CPP_IO import *


def is_developer():
    def predicate(ctx):
        return ctx.message.author.id in [716070916550819860, 721043620060201051]
    return commands.check(predicate)


class Development(commands.Cog):

    def __init__(self, client):
        self.client = client
        self._last_result = None

    @commands.command(hidden=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    @is_developer()
    async def update(self, ctx):
        await util.run('make clear')
        out, err, status = await util.run('make')

        message = f'Updated\nCompile Message: {out}\nStderr: {err}'

        if len(message) >= 2000:
            f = open(os.path.join(constants.TEMP_DIR, 'message.txt'), 'w')
            f.write(message)
            f.close()
            await ctx.send(file=discord.File(os.path.join(constants.TEMP_DIR, 'message.txt')))
        else:
            await ctx.send(message)

        await ctx.send(status)

    @commands.command(hidden=True)
    @is_developer()
    async def shell(self, ctx, *, cmd):
        await ctx.send(f'Executing command "{cmd}"...')
        stdout, stderr, status = await util.run(cmd)

        message = f'Stdout: {stdout}\nStderr: {stderr}'

        if len(message) >= 2000:
            f = open(os.path.join(constants.TEMP_DIR, 'message.txt'), 'w')
            f.write(message)
            f.close()
            await ctx.send(file=discord.File(os.path.join(constants.TEMP_DIR, 'message.txt')))
        else:
            await ctx.send(message)

        await ctx.send(status)

    @commands.command(hidden=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    @is_developer()
    async def restart(self, ctx):
        await ctx.send(f'Restarting...')
        sys.exit()

    @commands.command(hidden=True)
    @is_developer()
    async def git_pull(self, ctx):
        await ctx.send(f'Executing command "git pull"...')

        stdout, stderr, status = await util.run(f'git pull')

        message = f'```\nStdout:\n{stdout}Stderr: {stderr}```'

        if len(message) >= 2000:
            f = open(os.path.join(constants.TEMP_DIR, 'message.txt'), 'w')
            f.write(message)
            f.close()
            await ctx.send(file=discord.File(os.path.join(constants.TEMP_DIR, 'message.txt')))
        else:
            await ctx.send(message)

        await ctx.send(status)

    @commands.command(hidden=True)
    @is_developer()
    async def debug_load(self, ctx, user: typing.Union[discord.User, discord.Member]):
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
    @is_developer()
    async def debug(self, ctx, *, body: str):
        """Evaluates a code"""

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

    @commands.command(hidden=True)
    @is_developer()
    async def gimme(self, ctx, file):
        await ctx.send(file, file=discord.File(file))

    @commands.command(hidden=True)
    @is_developer()
    async def load_db(self, ctx):
        for attachment in ctx.message.attachments:
            if attachment.filename == 'database':
                await attachment.save(os.path.join(constants.TEMP_DIR, 'database'))
                break

        games, colors, time_control, ratings, last_moved, warned, prefixes = pickle.load(
            open(os.path.join(constants.TEMP_DIR, 'database'), 'rb'))
        print(games, colors, time_control, ratings,
              last_moved, warned, prefixes)

        # await ctx.send('Loading games...')

        for k in games.keys():
            print(games[k])
            print(' '.join(str(x) for x in games[k]))
            data.data_manager.change_game(k, data.Game(
                colors[k], time_control[k], games[k], last_moved[k], warned[k]))

        # await ctx.send('Loading ratings...')
        for k in ratings.keys():
            data.data_manager.change_rating(k, ratings[k])

        # await ctx.send('Loading prefixes...')
        for k in prefixes.keys():
            data.data_manager.change_prefix(k, prefixes[k])

        await ctx.send('Loaded')


def setup(bot):
    bot.add_cog(Development(bot))
