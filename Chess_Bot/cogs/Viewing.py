import discord
from discord.ext import commands
import typing

import Chess_Bot.cogs.Utility as util
import Chess_Bot.cogs.Data as data
import Chess_Bot.cogs.Images as image
from Chess_Bot.cogs.CPP_IO import *


class Viewing(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def view(self, ctx, *user: typing.Union[discord.User, discord.Member]):
        '''
        Views your current game
        '''
        person = -1
        if len(user) == 1:
            person = user[0].id
        else:
            person = ctx.author.id

        game = data.data_manager.get_game(person)

        if game == None:
            if len(user) == 1:
                await ctx.send(f'{user[0]} does not have a game in progress')
            else:
                await ctx.send('You do not have a game in progress')
            return

        if person in util.thonking:
            await ctx.send('Chess Bot is in the middle of thinking. Try again later.')
            return
        
        await run_engine(person, 0)
        await output_move(ctx, person)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def fen(self, ctx, *user: typing.Union[discord.User, discord.Member]):
        '''
        Sends current game in FEN format
        '''

        person = -1
        if len(user) == 1:
            person = user[0].id
        else:
            person = ctx.author.id

        game = data.data_manager.get_game(person)

        if game == None:
            if len(user) == 1:
                await ctx.send(f'{user[0]} does not have a game in progress')
            else:
                await ctx.send('You do not have a game in progress')
            return

        if person in util.thonking:
            await ctx.send('Chess Bot is in the middle of thinking. Try again later.')
            return

        file_in = f'Chess_Bot/data/input-{person}.txt'
        file_out = f'Chess_Bot/data/output-{person}.txt'

        f = open(file_in, 'w')
        f.write(f'fen\nyes2\n{str(game)}\nquit\n')
        f.close()

        await run_engine(file_in, file_out)

        f = open(file_out)
        out = f.readlines()
        f.close()

        await ctx.send(f'```{out[-2]}```')

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def theme(self, ctx, new_theme=None):
        if new_theme == None:
            cur_theme = data.data_manager.get_theme(ctx.author.id)
            await ctx.send(f'Your current theme is "{cur_theme}"\n'
                           f'Use `$theme <new theme>` to change your theme.\n'
                           'Available themes are:\n'
                           f'`{"`, `".join(image.themes_available)}`')
            return

        if not new_theme in image.themes_available:
            await ctx.send(f'That theme is not available.\n'
                           'Available themes are:\n'
                           f'`{"`, `".join(image.themes_available)}`')
            return

        data.data_manager.change_theme(ctx.author.id, new_theme)
        await ctx.send('Theme sucessfully updated')
