import discord
from discord.ext import commands
import typing
import chess

import Chess_Bot.util.Utility as util
import Chess_Bot.util.Data as data
import Chess_Bot.util.Images as image
from Chess_Bot.util.CPP_IO import *


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

        if game.bot in [Profile.cb1.value, Profile.cb2.value, Profile.cb3.value]:
            board = chess.Board()
            for move in game.moves:
                try:
                    board.push_uci(util.cb_to_uci(move))
                except ValueError:
                    board.push_san(util.cb_to_uci(move))
            await ctx.send(f'```{board.fen()}```')

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
