import discord
from discord.ext import commands

import os
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
        return ctx.message.author.id in constants.DEVELOPERS
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
            if len(f'```py\n{value}{traceback.format_exc()}\n```') < 4000:
                await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
            else:
                with open('data/temp/message2.txt', 'w') as f:
                    f.write(f'{value}\n-----------\n{traceback.format_exc()}')
                await ctx.send(file=discord.File('data/temp/message2.txt'))
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    try:
                        await ctx.send(f'```py\n{value}\n```')
                    except:
                        with open('data/temp/message.txt', 'w') as f:
                            f.write(value)
                        await ctx.send(file=discord.File('data/temp/message.txt'))
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.command(hidden=True)
    @is_developer()
    async def gimme(self, ctx, file):
        await ctx.send(file, file=discord.File(file))


def setup(bot):
    bot.add_cog(Development(bot))
