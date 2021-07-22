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
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def move(self, ctx, move):
        '''
        {
            "name": "move",
            "description": "Plays a move against the computer.\\nPlease enter the move in algebraic notation.\\nFor example, Nxe4, Nge5, c4, Ke2, etc.\\nMore about algebraic notation [here](https://www.chess.com/article/view/chess-notation#algebraic-notation).\\nYou can also enter it in UCI (universal chess interface) notation.",
            "aliases": [
                "play"
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

        person = ctx.author.id
        game = data.data_manager.get_game(person)

        if game == None:
            await ctx.send('You do not have a game in progress with Chess Bot')
            return

        if person in util.thonking:
            await ctx.send('Chess Bot is already thinking')
            return

        if 'resign' in move.lower():
            data.data_manager.delete_game(ctx.author.id, False)

            old_rating, new_rating = util.update_rating(ctx.author.id, 0, game.bot)

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
        if board.is_checkmate():                
            if board.turn == chess.WHITE and game.color == 0 or board.turn == chess.BLACK and game.color == 1:
                old_rating, new_rating = util.update_rating(ctx.author.id, 1, game.bot)
                data.data_manager.delete_game(person, True)
                await ctx.send('You won!')
            elif board.turn == chess.WHITE and game.color == 1 or board.turn == chess.BLACK and game.color == 0:
                old_rating, new_rating = util.update_rating(ctx.author.id, 0, game.bot)
                data.data_manager.delete_game(person, False)
                await ctx.send('You lost.')
                
            await ctx.send(f'Your new rating is {round(new_rating)} ({round(old_rating)} + {round(new_rating - old_rating, 2)})')
            return
        elif board.can_claim_draw():
            old_rating, new_rating = util.update_rating(ctx.author.id, 1/2, game.bot)
            await ctx.send('Draw')
            data.data_manager.delete_game(person, None)
            
            await ctx.send(f'Your new rating is {round(new_rating)} ({round(old_rating)} + {round(new_rating - old_rating, 2)})')
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
        if board.is_game_over(claim_draw=True) or move == 'RESIGN':
            if move == 'RESIGN':
                await ctx.send('Chess Bot resigned')
                old_rating, new_rating = util.update_rating(ctx.author.id, 1, game.bot)
                data.data_manager.delete_game(person, True)
            elif board.is_checkmate():
                if board.turn == chess.WHITE and game.color == 0 or board.turn == chess.BLACK and game.color == 1:
                    old_rating, new_rating = util.update_rating(ctx.author.id, 1, game.bot)
                    data.data_manager.delete_game(person, True)
                    await ctx.send('You won!')
                elif board.turn == chess.WHITE and game.color == 1 or board.turn == chess.BLACK and game.color == 0:
                    old_rating, new_rating = util.update_rating(ctx.author.id, 0, game.bot)
                    data.data_manager.delete_game(person, False)
                    await ctx.send('You lost.')
            else:
                old_rating, new_rating = util.update_rating(ctx.author.id, 1/2, game.bot)
                await ctx.send('Draw')
                data.data_manager.delete_game(person, None)

            await ctx.send(f'Your new rating is {round(new_rating)} ({round(old_rating)} + {round(new_rating - old_rating, 2)})')

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def challenge(self, ctx, bot):
        '''
        {
            "name": "challenge",
            "description": "Challenges the bot to a game of chess.\\nUse `$profiles to see which bots you can challenge.\\nYour color is assigned randomly.",
            "usage": "$challenge <bot>",
            "examples": [
                "$challenge cb1",
                "$challenge sf3"
            ],
            "cooldown": 3
        }
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
            data.data_manager.change_game(person, game)

        await output_move(ctx, person, move)
        game.last_moved = time.time()
        game.warned = False
        data.data_manager.change_game(person, game)

    @commands.command()
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

        game = data.data_manager.get_game(ctx.author.id)

        if game is None:
            await ctx.send('You do not have a game in progress')
            return

        data.data_manager.delete_game(ctx.author.id, False)
        if ctx.author.id in util.thonking:
            util.thonking.remove(ctx.author.id)

        old_rating, new_rating = util.update_rating(ctx.author.id, 0, game.bot)

        await ctx.send(f'Game resigned. Your new rating is {round(new_rating)} ({round(old_rating)} + {round(new_rating - old_rating, 2)})')


def setup(bot):
    bot.add_cog(Engine(bot))
