from discord.ext import commands
import random
import time

import Chess_Bot.util.Data as data
import Chess_Bot.util.Utility as util
from Chess_Bot.util.CPP_IO import *
from Chess_Bot.cogs.Profiles import Profile, ProfileNames
from Chess_Bot import constants


class Engine(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['play'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def move(self, ctx, move):
        '''
        Plays <move> against the computer
        Please enter the move in algebraic notation
        For example, Nxe4, Nge5, c4, Ke2, etc
        More about algebraic notation here: https://www.chess.com/article/view/chess-notation#algebraic-notation
        '''

        person = ctx.author.id
        game = data.data_manager.get_game(person)

        if game == None:
            await ctx.send('You do not have a game in progress with Chess Bot')
            return

        if person in util.thonking:
            await ctx.send('Chess Bot is already thinking')
            return

        if 'resign' in move.lower():
            data.data_manager.delete_game(ctx.author.id)
            if ctx.author.id in util.thonking:
                util.thonking.remove(ctx.author.id)

            old_rating = data.data_manager.get_rating(ctx.author.id)
            if old_rating == None:
                data.data_manager.change_rating(
                    ctx.author.id, constants.DEFAULT_RATING)
                old_rating = constants.DEFAULT_RATING

            util.update_rating(ctx.author.id, 0, game.bot)
            new_rating = data.data_manager.delete_game(person, False)

            await ctx.send(f'Game resigned. Your new rating is {round(new_rating)} ({round(old_rating)} + {round(new_rating - old_rating, 2)}).\n'
                           'Tip: Trying to resign? You can also use the `$resign` command.')
            return

        board = chess.Board(game.fen)
        try:
            board.push_san(move)
        except ValueError:
            try:
                board.push_uci(move)
            except ValueError:
                await ctx.send('Illegal move played. Make sure your move is in SAN or UCI notation.\nUse `$help move` for more info.')
                return
        game.fen = board.fen()
        data.data_manager.change_game(person, game)

        thonk = self.client.get_emoji(constants.THONK_EMOJI_ID)
        await ctx.message.add_reaction(thonk)
        util.thonking.append(person)

        move, game = await run_engine(person)
        game.last_moved = time.time()
        game.warned = False
        data.data_manager.change_game(person, game)

        await output_move(ctx, person, move)
        await log(person, self.client, ctx)
        util.thonking.remove(person)

        board = chess.Board(game.fen)
        if board.is_game_over(claim_draw=True):
            old_rating = data.data_manager.get_rating(person)
            if old_rating == None:
                old_rating = constants.DEFAULT_RATING

            if move == 'RESIGN':
                await ctx.send('Chess Bot resigned')
                util.update_rating(ctx.author.id, 1, game.bot)
                data.data_manager.delete_game(person, True)
            elif board.is_checkmate():
                if board.turn == chess.WHITE and game.color == 0 or board.turn == chess.BLACK and game.color == 1:
                    util.update_rating(ctx.author.id, 1, game.bot)
                    data.data_manager.delete_game(person, True)
                    await ctx.send('You won!')
                elif board.turn == chess.WHITE and game.color == 1 or board.turn == chess.BLACK and game.color == 0:
                    util.update_rating(ctx.author.id, 0, game.bot)
                    data.data_manager.delete_game(person, False)
                    await ctx.send('You lost.')
            else:
                util.update_rating(ctx.author.id, 1/2, game.bot)
                await ctx.send('Draw')
                data.data_manager.delete_game(person, None)

            new_rating = data.data_manager.get_rating(person)
            await ctx.send(f'Your new rating is {round(new_rating)} ({round(old_rating)} + {round(new_rating - old_rating, 2)})')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def challenge(self, ctx, bot):
        '''
        Challenges Chess Bot to a game
        Your color is assigned randomly.
        '''

        person = ctx.author.id

        game = data.data_manager.get_game(person)
        if game != None:
            await ctx.send('You already have a game in progress')
            return

        try:
            botid = Profile[bot].value
        except KeyError:
            await ctx.send(f'"{bot}" is not the valid tag of a bot. Use `$profiles` to see which bots you can challenge.')
            return

        game = data.Game()
        game.color = random.randint(0, 1)
        game.bot = botid

        data.data_manager.change_game(person, game)

        await ctx.send(f'Game started with {ProfileNames[bot].value}\nYou play the {whiteblack[game.color]} pieces.')

        move = None
        if game.color == 0:
            thonk = self.client.get_emoji(constants.THONK_EMOJI_ID)
            await ctx.message.add_reaction(thonk)
            util.thonking.append(person)

            move, game = await run_engine(person)
            await log(person, self.client, ctx)
            util.thonking.remove(person)

        await output_move(ctx, person, move)
        game.last_moved = time.time()
        game.warned = False
        data.data_manager.change_game(person, game)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def resign(self, ctx):
        '''
        Resigns the game
        '''

        game = data.data_manager.get_game(ctx.author.id)

        if game == None:
            await ctx.send('You do not have a game in progress')
            return

        data.data_manager.delete_game(ctx.author.id, False)
        if ctx.author.id in util.thonking:
            util.thonking.remove(ctx.author.id)

        old_rating = data.data_manager.get_rating(ctx.author.id)
        if old_rating == None:
            data.data_manager.change_rating(
                ctx.author.id, constants.DEFAULT_RATING)
            old_rating = constants.DEFAULT_RATING

        util.update_rating(ctx.author.id, 0, game.bot)
        new_rating = data.data_manager.get_rating(ctx.author.id)

        await ctx.send(f'Game resigned. Your new rating is {round(new_rating)} ({round(old_rating)} + {round(new_rating - old_rating, 2)})')


def setup(bot):
    bot.add_cog(Engine(bot))
