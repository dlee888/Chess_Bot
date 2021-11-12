from discord.ext import commands
from discord.ext import tasks

import random
import time
from typing import Union
import asyncio
import json

import Chess_Bot.util.Data as data
import Chess_Bot.util.Utility as util
from Chess_Bot.util.CPP_IO import *
from Chess_Bot.cogs.Profiles import Profile, ProfileNames
from Chess_Bot import constants


class Engine(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.thonking = {}
        self.run_engine.start()
        self.output_result.start()

    @tasks.loop(seconds=3)
    async def run_engine(self):
        games = data.data_manager.get_games2()
        for game in games:
            person = game.not_to_move()
            if game.to_move() < len(Profile) and not person in self.thonking.keys():
                self.thonking[person] = asyncio.create_task(run_engine(person))

    @tasks.loop(seconds=3)
    async def output_result(self):
        thonk = list(self.thonking.items())
        for person, task in thonk:
            if task.done():
                move, game = task.result()
                util2 = self.client.get_cog('Util')
                self.thonking.pop(person)
                board = chess.Board(game.fen)
                if person == game.white:
                    bot = game.black
                else:
                    bot = game.white
                if board.is_game_over(claim_draw=True) or move == 'RESIGN':
                    if move == 'RESIGN':
                        old_rating, new_rating = util.update_rating(
                            person, 1, bot)
                        file, embed = util2.make_embed(person, title='Game over', description=f'It was in this position that {await util2.get_name(bot)} resigned the game.')
                        await util2.send_notif(person, f'Chess Bot resigned.\nYour new rating is {round(new_rating)} ({round(new_rating - old_rating, 2)})', file=file, embed=embed)
                        data.data_manager.delete_game(person, not game.turn())
                    elif board.is_checkmate():
                        old_rating, new_rating = util.update_rating(
                            person, 0, bot)
                        data.data_manager.delete_game(person, not game.turn())
                        await util2.send_notif(person, f'You lost.\nYour new rating is {round(new_rating)} ({round(new_rating - old_rating, 2)})')
                    else:
                        old_rating, new_rating = util.update_rating(
                            person, 1/2, bot)
                        await util2.send_notif(person, f'Draw.\nYour new rating is {round(new_rating)} ({round(new_rating - old_rating, 2)})')
                        data.data_manager.delete_game(person, 69)
                    continue
                if person == game.white:
                    game.last_moved = time.time()
                    game.white_warned = False
                else:
                    game.last_moved = time.time()
                    game.black_warned = False
                data.data_manager.change_game(None, game)
                file, embed = util2.make_embed(person, title=f'Your game with {await util2.get_name(game.not_to_move())}', description=f'The bot has moved\n{move}')
                await util2.send_notif(person, 'The bot has moved', file=file, embed=embed)

    @run_engine.before_loop
    @output_result.before_loop
    async def wait_until_ready(self):
        await self.client.wait_until_ready()

    @commands.command(aliases=['play', 'm'])
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

        person = ctx.author.id
        game = data.data_manager.get_game(person)

        if game == None:
            await ctx.send('You do not have a game in progress.')
            return
        if 'resign' == move.lower():
            await self.resign(ctx)
            await ctx.send('Tip: Trying to resign? You can also use the `$resign` command.')
            return

        if isinstance(game, data.Game):
            if person in util.thonking:
                await ctx.send('Chess Bot is already thinking')
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
                    old_rating, new_rating = util.update_rating(
                        ctx.author.id, 1, game.bot)
                    data.data_manager.delete_game(person, True)
                    await ctx.send('You won!')
                elif board.turn == chess.WHITE and game.color == 1 or board.turn == chess.BLACK and game.color == 0:
                    old_rating, new_rating = util.update_rating(
                        ctx.author.id, 0, game.bot)
                    data.data_manager.delete_game(person, False)
                    await ctx.send('You lost.')

                await ctx.send(f'Your new rating is {round(new_rating)} ({round(old_rating)} + {round(new_rating - old_rating, 2)})')
                return
            elif board.can_claim_draw():
                old_rating, new_rating = util.update_rating(
                    ctx.author.id, 1/2, game.bot)
                await ctx.send('Draw')
                data.data_manager.delete_game(person, None)

                await ctx.send(f'Your new rating is {round(new_rating)} ({round(old_rating)} + {round(new_rating - old_rating, 2)})')
                return

            game.fen = board.fen(en_passant='fen')
            data.data_manager.change_game(person, game)

            thonk = self.client.get_emoji(constants.THONK_EMOJI_ID)
            await ctx.message.add_reaction(thonk)
            util.thonking.append(person)

            move, game = await run_engine(person)
            # If person resigned while bot was thinking
            if data.data_manager.get_game(person) is None:
                return
            game.last_moved = time.time()
            game.warned = False
            data.data_manager.change_game(person, game)

            await output_move(ctx, person, move)
            await log(person, self.client, ctx)
            if person in util.thonking:
                util.thonking.remove(person)

            board = chess.Board(game.fen)
            if board.is_game_over(claim_draw=True) or move == 'RESIGN':
                if move == 'RESIGN':
                    await ctx.send('Chess Bot resigned')
                    old_rating, new_rating = util.update_rating(
                        ctx.author.id, 1, game.bot)
                    data.data_manager.delete_game(person, True)
                elif board.is_checkmate():
                    if board.turn == chess.WHITE and game.color == 0 or board.turn == chess.BLACK and game.color == 1:
                        old_rating, new_rating = util.update_rating(
                            ctx.author.id, 1, game.bot)
                        data.data_manager.delete_game(person, True)
                        await ctx.send('You won!')
                    elif board.turn == chess.WHITE and game.color == 1 or board.turn == chess.BLACK and game.color == 0:
                        old_rating, new_rating = util.update_rating(
                            ctx.author.id, 0, game.bot)
                        data.data_manager.delete_game(person, False)
                        await ctx.send('You lost.')
                else:
                    old_rating, new_rating = util.update_rating(
                        ctx.author.id, 1/2, game.bot)
                    await ctx.send('Draw')
                    data.data_manager.delete_game(person, None)

                await ctx.send(f'Your new rating is {round(new_rating)} ({round(old_rating)} + {round(new_rating - old_rating, 2)})')
        elif isinstance(game, data.Game2):
            board = chess.Board(game.fen)
            color = chess.WHITE if person == game.white else chess.BLACK
            util2 = self.client.get_cog('Util')

            if board.turn != color:
                await ctx.send(f'It is not your turn!')
                return
            try:
                board.push_san(move)
            except ValueError:
                try:
                    board.push_uci(move)
                except ValueError:
                    await ctx.send('Illegal move played. Make sure your move is in SAN or UCI notation.\nUse `$help move` for more info.')
                    return
            if color == chess.WHITE:
                game.last_moved = time.time()
                game.white_warned = False
            else:
                game.last_moved = time.time()
                game.black_warned = False
            game.fen = board.fen(en_passant='fen')
            data.data_manager.change_game(person, game)
            if board.is_checkmate():
                white_delta, black_delta = util.update_rating2(
                    game.white, game.black, 0 if board.turn == chess.BLACK else 1)
                embed = discord.Embed(
                    title=f'{ctx.author}\'s game', description=f'{whiteblack[not board.turn].capitalize()} won by checkmate.')
                path = get_image2(person, color)
                file = discord.File(path, filename='board.png')
                embed.set_image(url='attachment://board.png')
                await ctx.send(embed=embed, file=file)

                file1, embed1 = util2.make_embed(
                    game.white, title='Your game has ended', description=f'{whiteblack[not board.turn].capitalize()} won by checkmate.\nYour new rating is {round(data.data_manager.get_rating(game.white))} ({white_delta})')
                file2, embed2 = util2.make_embed(
                    game.black, title='Your game has ended', description=f'{whiteblack[not board.turn].capitalize()} won by checkmate.\nYour new rating is {round(data.data_manager.get_rating(game.black))} ({black_delta})')

                await util2.send_notif(game.white, file=file1, embed=embed1)
                await util2.send_notif(game.black, file=file2, embed=embed2)

                data.data_manager.delete_game(game.white, not board.turn)
                return
            elif board.can_claim_draw():
                white_delta, black_delta = util.update_rating2(
                    game.white, game.black, 1/2)
                embed = discord.Embed(
                    title=f'{ctx.author}\'s game', description=f'Draw.')
                path = get_image2(person, color)
                file = discord.File(path, filename='board.png')
                embed.set_image(url='attachment://board.png')
                await ctx.send(embed=embed, file=file)

                file1, embed1 = util2.make_embed(
                    title=f'Your game has ended', description=f'Draw.\nYour new rating is {round(data.data_manager.get_rating(game.white))} ({white_delta})')
                file2, embed2 = util2.make_embed(
                    title=f'Your game has ended', description=f'Draw.\nYour new rating is {round(data.data_manager.get_rating(game.black))} ({black_delta})')
                await util2.send_notif(game.white, file=file1, embed=embed1)
                await util2.send_notif(game.black, file=file2, embed=embed2)

                data.data_manager.delete_game(game.white, 69)
                return

            game.fen = board.fen(en_passant='fen')
            if color == chess.WHITE:
                game.last_moved = time.time()
                game.white_warned = False
                data.data_manager.change_game(person, game)
                file, embed = util2.make_embed(game.white, title=f'Your game with {await util2.get_name(game.black)}', description='You have moved.')
                await ctx.message.reply(file=file, embed=embed)

                file, embed = util2.make_embed(game.black, title=f'Your game with {await util2.get_name(game.white)}', description='It is your turn')
                await util2.send_notif(game.black, embed=embed, file=file)
            else:
                game.last_moved = time.time()
                game.black_warned = False
                data.data_manager.change_game(person, game)

                file, embed = util2.make_embed(game.black, title=f'Your game with {await util2.get_name(game.white)}', description='You have moved.')
                await ctx.message.reply(file=file, embed=embed)

                file, embed = util2.make_embed(game.white, title=f'Your game with {await util2.get_name(game.black)}', description='It is your turn')
                await util2.send_notif(game.white, embed=embed, file=file)

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def challenge(self, ctx):
        '''
        {
            "name": "challenge",
            "description": "Challenges somebody to a game of chess. Use `$challenge bot` to challenge a bot, or `$challenge user` to challenge another person.",
            "usage": "$challenge <bot/user> <person>",
            "examples": [
                "$challenge bot cb1",
                "$challenge bot sf3",
                "$challenge user <@person>"
            ],
            "cooldown": 3,
            "subcommands": [
                "bot",
                "user"
            ]
        }
        '''
        helpcog = self.client.get_cog('Help')
        docstr = self.client.get_command('challenge').help
        kwargs = json.loads(docstr)
        await ctx.send(embed=helpcog.make_help_embed(**kwargs))

    @challenge.command()
    async def bot(self, ctx, bot):
        '''
        {
            "name": "challenge bot",
            "description": "Challenges the bot to a game of chess.\\nUse `$profiles to see which bots you can challenge.\\nYour color is assigned randomly.",
            "usage": "$challenge bot <bot>",
            "examples": [
                "$challenge bot cb1",
                "$challenge bot sf3"                
            ],
            "cooldown": 3
        }
        '''
        person = ctx.author.id

        game = data.data_manager.get_game(person)
        if game is not None:
            await ctx.send('You already have a game in progress')
            return

        try:
            botid = Profile[bot].value
        except KeyError:
            await ctx.send(f'"{bot}" is not the valid tag of a bot. Use `$profiles` to see which bots you can challenge.')
            return

        if True:
            # EXPERIMENTAL
            game = data.Game2()
            color = random.randint(0, 1)
            if color == 0:
                game.white = botid
                game.black = person
            else:
                game.white = person
                game.black = botid
            data.data_manager.change_game(None, game)
            await ctx.send(f'Game started with {ProfileNames[bot].value}\nYou play the {whiteblack[color]} pieces.')
            data.data_manager.change_settings(person, new_notif=ctx.channel.id)
        else:
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
                if person in util.thonking:
                    util.thonking.remove(person)
                data.data_manager.change_game(person, game)

            await output_move(ctx, person, move)
            game.last_moved = time.time()
            game.warned = False
            data.data_manager.change_game(person, game)

    @challenge.command(aliases=['person'])
    async def user(self, ctx, person: Union[discord.Member, discord.User]):
        '''
        {
            "name": "challenge user",
            "description": "Challenges another user to a game of chess.\\nReact with a check mark to accept a challenge, and react with an X mark to decline\\nThe challenge will expire in 10 minutes.",
            "usage": "$challenge user <user>",
            "examples": [
                "$challenge user <@person>"             
            ],
            "cooldown": 3,
            "aliases": [
                "person"
            ]
        }
        '''

        if data.data_manager.get_game(ctx.author.id) is not None:
            await ctx.send('You already have a game in progress.')
            return
        if data.data_manager.get_game(person.id) is not None:
            await ctx.send(f'{person} already has a game in progress.')
            return
        if ctx.author.id == person.id:
            await ctx.send(f'You cannot challenge yourself.')
            return

        util2 = self.client.get_cog('Util')

        challenge_msg = await ctx.send((f'{person.mention}, {ctx.author} has challenged you to a game of chess.\n'
                                        'React with :white_check_mark: to accept.\n'
                                        'React with :x: to decline or withdraw your challenge.'))
        await challenge_msg.add_reaction('✅')
        await challenge_msg.add_reaction('❌')

        def check(reaction, user):
            return ((user.id == person.id and str(reaction.emoji) == '✅') or
                    ((user.id == person.id or user.id == ctx.author.id) and str(reaction.emoji) == '❌'))

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=600.0, check=check)
        except asyncio.TimeoutError:
            await challenge_msg.reply('Challenge timed out!')
        else:
            if str(reaction.emoji) == '❌':
                await challenge_msg.reply('Challenge declined / withdrawn')
                return

            if data.data_manager.get_game(ctx.author.id) is not None or data.data_manager.get_game(person.id) is not None:
                await challenge_msg.reply('Challenge failed. One of the people already has a game in progress.')

            game = data.Game2()
            if random.randint(0, 1) == 0:
                game.white = ctx.author.id
                game.black = person.id
            else:
                game.white = person.id
                game.black = ctx.author.id
            data.data_manager.change_game(None, game)
            path = get_image2(ctx.author.id)
            file = discord.File(path, filename='board.png')
            embed = discord.Embed(
                title='Game started!', description=f'White: {await util2.get_name(game.white)}\nBlack: {await util2.get_name(game.black)}')
            embed.set_image(url='attachment://board.png')
            await challenge_msg.reply(f'<@{game.white}> <@{game.black}>', file=file, embed=embed)
            data.data_manager.change_settings(game.white, new_notif=ctx.channel.id)
            data.data_manager.change_settings(game.black, new_notif=ctx.channel.id)

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

        if isinstance(game, data.Game):
            data.data_manager.delete_game(ctx.author.id, False)
            if ctx.author.id in util.thonking:
                util.thonking.remove(ctx.author.id)

            old_rating, new_rating = util.update_rating(
                ctx.author.id, 0, game.bot)

            await ctx.send(f'Game resigned. Your new rating is {round(new_rating)} ({round(old_rating)} + {round(new_rating - old_rating, 2)})')
        elif isinstance(game, data.Game2):
            util2 = self.client.get_cog('Util')
            white_delta, black_delta = util.update_rating2(game.white, game.black,
                                                           0 if ctx.author.id == game.black else 1)
            if ctx.author.id == game.white:
                await ctx.send(f'Game resigned. Your new rating is {round(data.data_manager.get_rating(ctx.author.id), 3)} ({round(white_delta, 3)})')
                file, embed = util2.make_embed(
                    game.black, title='Your game has ended', description=f'It was in this position that {ctx.author} resigned the game.\nYour new rating is {round(data.data_manager.get_rating(game.black), 3)} ({round(black_delta, 3)})')
                await util2.send_notif(game.black, file=file, embed=embed)
            else:
                await ctx.send(f'Game resigned. Your new rating is {round(data.data_manager.get_rating(ctx.author.id), 3)} ({round(black_delta, 3)})')
                file, embed = util2.make_embed(
                    game.white, title='Your game has ended', description=f'It was in this position that {ctx.author} resigned the game.\nYour new rating is {round(data.data_manager.get_rating(game.white), 3)} ({round(white_delta, 3)})')
                await util2.send_notif(game.white, file=file, embed=embed)
            data.data_manager.delete_game(
                ctx.author.id, chess.WHITE if ctx.author.id == game.black else chess.BLACK)


def setup(bot):
    bot.add_cog(Engine(bot))
