import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks

import time
import asyncio
import logging
import traceback
import sys

import Chess_Bot.util.Data as data
import Chess_Bot.util.Utility as util
from Chess_Bot.util.CPP_IO import *
from Chess_Bot.cogs.Profiles import Profile


class Engine(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.thonking = {}
        if '-beta' not in sys.argv or '-run-engine' in sys.argv:
            self.run_engine.start()
            self.output_result.start()

    async def make_move(self, game, move):
        if move is None:
            return
        util2 = self.client.get_cog('Util')

        board = chess.Board(game.fen)
        board.push(move)
        game.last_moved = time.time()
        game.warned = False
        game.fen = board.fen(en_passant='fen')
        game.white_draw = False
        game.black_draw = False
        await data.data_manager.change_game(game)

        if board.is_checkmate():
            white_delta, black_delta = await util.update_rating2(
                game.white, game.black, 0 if board.turn == chess.BLACK else 1)

            file1, embed1, _ = await util2.make_embed(game.white, title='Your game has ended',
                                                      description=(f'{"Your opponent has" if board.turn == chess.WHITE else "You have"} moved: {move}.\n'
                                                                   f'{whiteblack[not board.turn].capitalize()} won by checkmate.\n'
                                                                   f'Your new rating is {round(await data.data_manager.get_rating(game.white), 3)} ({round(white_delta, 3)})'))
            file2, embed2, _ = await util2.make_embed(game.black, title='Your game has ended',
                                                      description=(f'{"Your opponent has" if board.turn == chess.BLACK else "You have"} has moved: {move}.\n'
                                                                   f'{whiteblack[not board.turn].capitalize()} won by checkmate.\n'
                                                                   f'Your new rating is {round(await data.data_manager.get_rating(game.black), 3)} ({round(black_delta, 3)})'))

            await util2.send_notif(game.white, file=file1, embed=embed1)
            await util2.send_notif(game.black, file=file2, embed=embed2)

            await data.data_manager.delete_game(game.player(), not board.turn)
        elif board.can_claim_draw() or board.is_stalemate() or board.is_insufficient_material():
            white_delta, black_delta = await util.update_rating2(
                game.white, game.black, 1 / 2)

            file1, embed1, _ = await util2.make_embed(game.white, title='Your game has ended',
                                                      description=(f'Your opponent has moved: {move}.\n'
                                                                   'Draw.\n'
                                                                   f'Your new rating is {round(await data.data_manager.get_rating(game.white), 3)} ({round(white_delta, 3)})'))

            file2, embed2, _ = await util2.make_embed(game.black, title='Your game has ended',
                                                      description=(f'Your opponent has moved: {move}.\n'
                                                                   'Draw.\n'
                                                                   f'Your new rating is {round(await data.data_manager.get_rating(game.black), 3)} ({round(black_delta, 3)})'))

            await util2.send_notif(game.white, file=file1, embed=embed1)
            await util2.send_notif(game.black, file=file2, embed=embed2)

            await data.data_manager.delete_game(game.player(), 69)
        else:
            file, embed, view = await util2.make_embed(game.to_move(), title=f'Your game with {await util2.get_name(game.not_to_move())}', description=f'Your opponent has moved: {move}.')
            await util2.send_notif(game.to_move(), embed=embed, file=file, view=view)

    @tasks.loop(seconds=3)
    async def run_engine(self):
        try:
            games = await data.data_manager.get_games()
            for game in games:
                person = game.not_to_move()
                if game.to_move() < len(Profile) and person not in self.thonking.keys() and len(self.thonking) < 3:
                    self.thonking[person] = asyncio.create_task(
                        run_engine(person))
        except Exception as exc:
            etype = type(exc)
            trace = exc.__traceback__
            lines = traceback.format_exception(etype, exc, trace)
            traceback_text = ''.join(lines)
            logging.error(f'Error in run_engine:\n{traceback_text}')

    async def process_task(self, person, task):
        game = await data.data_manager.get_game(person)
        if game is None or task.result() is None:
            return
        move = task.result()
        if move is None:
            logging.warning(
                f'`move=None` in run_engine:\n`{game.fen}`\n{game.white} vs {game.black}')
            return
        if move == 'RESIGN':
            util2 = self.client.get_cog('Util')
            white_delta, black_delta = await util.update_rating2(game.white, game.black,
                                                                 0 if game.bot() == game.black else 1)
            if game.bot() == game.white:
                file, embed, _ = await util2.make_embed(
                    game.black, title='Your game has ended',
                    description=(f'It was in this position that {await util2.get_name(game.bot())} resigned the game.\n'
                                 f'Your new rating is {round(await data.data_manager.get_rating(game.black), 3)} ({round(black_delta, 3)})'))
            else:
                file, embed, _ = await util2.make_embed(
                    game.white, title='Your game has ended',
                    description=(f'It was in this position that {await util2.get_name(game.bot())} resigned the game.\n'
                                 f'Your new rating is {round(await data.data_manager.get_rating(game.white), 3)} ({round(white_delta, 3)})'))
            await util2.send_notif(game.player(), file=file, embed=embed)
            await data.data_manager.delete_game(
                game.player(), chess.WHITE if game.bot() == game.black else chess.BLACK)
        else:
            await self.make_move(game, game.parse_move(move))

    @tasks.loop(seconds=3)
    async def output_result(self):
        thonk = list(self.thonking.items())
        for person, task in thonk:
            if task.done():
                try:
                    self.thonking.pop(person)
                    await self.process_task(person, task)
                except Exception as exc:
                    etype = type(exc)
                    trace = exc.__traceback__
                    lines = traceback.format_exception(etype, exc, trace)
                    traceback_text = ''.join(lines)
                    logging.error(f'Error in run_engine:\n{traceback_text}')

    @run_engine.before_loop
    @output_result.before_loop
    async def wait_until_ready(self):
        await self.client.wait_until_ready()

    @commands.hybrid_command(aliases=['play', 'm'], name='move', description='Make a move in your game.')
    @app_commands.describe(move='The move you want to make, in SAN or UCI notation.')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def move(self, ctx, move):
        '''
        {
            "name": "move",
            "description": "Plays a move against the computer.\\nPlease enter the move in algebraic notation.\\nFor example, Nxe4, Nge5, c4, Ke2, etc.\\nMore about algebraic notation [here](https://www.chess.com/article/view/chess-notation#algebraic-notation).\\nYou can also enter it in UCI (universal chess interface) notation.",
            "aliases": [
                "play",
                "m"
            ],
            "usage": "$move <move>",
            "examples": [
                "$move e4",
                "$move e7e5",
                "$move Ke2"
            ],
            "cooldown": 3
        }
        '''
        util2 = self.client.get_cog('Util')

        person = ctx.author.id
        game = await data.data_manager.get_game(person)

        if game is None:
            await ctx.send('You do not have a game in progress.')
            return
        if person != game.to_move():
            await ctx.send('It is not your turn!')
            return
        if move.lower() == 'resign':
            await self.resign(ctx)
            await ctx.send('Tip: Trying to resign? You can also use the `$resign` command.')
            return

        move = game.parse_move(move)
        if move is None:
            await ctx.send(embed=discord.Embed(title='Illegal move played.',
                                               description=('Make sure your move is in SAN (standard algebraic notation).\n'
                                                            'For example, Nxe4, Nge5, c4, Ke2, etc.\n'
                                                            'More about algebraic notation [here](https://www.chess.com/article/view/chess-notation#algebraic-notation).\n'
                                                            'You can also enter it in UCI (universal chess interface) notation.\n'
                                                            'For example, e4e5, g1f3, e1e2, etc.\n'
                                                            'For promotions, specify the piece you want to promote to.\n'
                                                            'For example, `a1=Q`, `b8=R`, `f1=Q`, etc.'),
                                               color=0xff5555))
            return

        await self.make_move(game, move)
        if await data.data_manager.get_game(person) is not None:
            file, embed, _ = await util2.make_embed(person, title=f'Your game with {await util2.get_name(game.to_move())}', description='You have moved.')
            await ctx.send(file=file, embed=embed)

    @commands.hybrid_command(name='resign', description='Resigns your current game')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def resign(self, ctx):
        '''
        {
            "name": "resign",
            "description": "Resigns your current game.",
            "usage": "$resign",
            "examples": [
                "$resign"
            ],
            "cooldown": 3
        }
        '''

        game = await data.data_manager.get_game(ctx.author.id)

        if game is None:
            await ctx.send('You do not have a game in progress')
            return

        util2 = self.client.get_cog('Util')
        white_delta, black_delta = await util.update_rating2(game.white, game.black,
                                                             0 if ctx.author.id == game.black else 1)
        if ctx.author.id == game.white:
            await ctx.send(f'Game resigned. Your new rating is {round(await data.data_manager.get_rating(ctx.author.id), 3)} ({round(white_delta, 3)})')
            file, embed, _ = await util2.make_embed(
                game.black, title='Your game has ended', description=f'It was in this position that {ctx.author} resigned the game.\nYour new rating is {round(await data.data_manager.get_rating(game.black), 3)} ({round(black_delta, 3)})')
            await util2.send_notif(game.black, file=file, embed=embed)
        else:
            await ctx.send(f'Game resigned. Your new rating is {round(await data.data_manager.get_rating(ctx.author.id), 3)} ({round(black_delta, 3)})')
            file, embed, _ = await util2.make_embed(
                game.white, title='Your game has ended', description=f'It was in this position that {ctx.author} resigned the game.\nYour new rating is {round(await data.data_manager.get_rating(game.white), 3)} ({round(white_delta, 3)})')
            await util2.send_notif(game.white, file=file, embed=embed)
        await data.data_manager.delete_game(
            ctx.author.id, chess.WHITE if ctx.author.id == game.black else chess.BLACK)


async def setup(bot):
    await bot.add_cog(Engine(bot))
