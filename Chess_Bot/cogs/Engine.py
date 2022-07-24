import discord
from discord.ext import commands
from discord.ext import tasks

from discord_slash import cog_ext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option

import random
import time
from typing import Union
import asyncio
import json
import logging
import traceback
import sys

import Chess_Bot.util.Data as data
import Chess_Bot.util.Utility as util
from Chess_Bot.util.CPP_IO import *
from Chess_Bot.cogs.Profiles import Profile, ProfileNames


class Engine(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.thonking = {}
        if '-beta' not in sys.argv or '-run-engine' in sys.argv:
            self.run_engine.start()
            self.output_result.start()

    async def make_move(self, game, move):
        util2 = self.client.get_cog('Util')

        board = chess.Board(game.fen)
        board.push(move)
        game.last_moved = time.time()
        game.warned = False
        game.fen = board.fen(en_passant='fen')
        data.data_manager.change_game(game)

        if board.is_checkmate():
            white_delta, black_delta = util.update_rating2(
                game.white, game.black, 0 if board.turn == chess.BLACK else 1)

            file1, embed1 = util2.make_embed(game.white, title='Your game has ended',
                                             description=(f'{"Your opponent has" if board.turn == chess.WHITE else "You have"} moved: {move}.\n'
                                                          f'{whiteblack[not board.turn].capitalize()} won by checkmate.\n'
                                                          f'Your new rating is {round(data.data_manager.get_rating(game.white), 3)} ({round(white_delta, 3)})'))
            file2, embed2 = util2.make_embed(game.black, title='Your game has ended',
                                             description=(f'{"Your opponent has" if board.turn == chess.BLACK else "You have"} has moved: {move}.\n'
                                                          f'{whiteblack[not board.turn].capitalize()} won by checkmate.\n'
                                                          f'Your new rating is {round(data.data_manager.get_rating(game.black), 3)} ({round(black_delta, 3)})'))

            await util2.send_notif(game.white, file=file1, embed=embed1)
            await util2.send_notif(game.black, file=file2, embed=embed2)

            data.data_manager.delete_game(game.player(), not board.turn)
        elif board.can_claim_draw() or board.is_stalemate() or board.is_insufficient_material():
            white_delta, black_delta = util.update_rating2(
                game.white, game.black, 1/2)

            file1, embed1 = util2.make_embed(game.white, title='Your game has ended',
                                             description=(f'Your opponent has moved: {move}.\n'
                                                          'Draw.\n'
                                                          f'Your new rating is {round(data.data_manager.get_rating(game.white), 3)} ({round(white_delta, 3)})'))

            file2, embed2 = util2.make_embed(game.black, title='Your game has ended',
                                             description=(f'Your opponent has moved: {move}.\n'
                                                          'Draw.\n'
                                                          f'Your new rating is {round(data.data_manager.get_rating(game.black), 3)} ({round(black_delta, 3)})'))

            await util2.send_notif(game.white, file=file1, embed=embed1)
            await util2.send_notif(game.black, file=file2, embed=embed2)

            data.data_manager.delete_game(game.player(), 69)
        else:
            file, embed = util2.make_embed(game.to_move(), title=f'Your game with {await util2.get_name(game.not_to_move())}', description=f'Your opponent has moved: {move}.')
            await util2.send_notif(game.to_move(), embed=embed, file=file)

    @tasks.loop(seconds=3)
    async def run_engine(self):
        try:
            games = data.data_manager.get_games()
            for game in games:
                person = game.not_to_move()
                if game.to_move() < len(Profile) and person not in self.thonking.keys() and len(self.thonking) < 10:
                    self.thonking[person] = asyncio.create_task(
                        run_engine(person))
            print(self.thonking)
        except Exception as exc:
            etype = type(exc)
            trace = exc.__traceback__
            lines = traceback.format_exception(etype, exc, trace)
            traceback_text = ''.join(lines)
            logging.error(f'Error in run_engine:\n{traceback_text}')

    @tasks.loop(seconds=3)
    async def output_result(self):
        thonk = list(self.thonking.items())
        for person, task in thonk:
            if task.done():
                try:
                    self.thonking.pop(person)
                    game = data.data_manager.get_game(person)
                    if game is None or task.result() is None:
                        continue
                    move = task.result()
                    if move is None:
                        logging.error(
                            f'`move=None` in run_engine:\n`{game.fen}`\n{game.white} vs {game.black}')
                        continue
                    if move == 'RESIGN':
                        util2 = self.client.get_cog('Util')
                        white_delta, black_delta = util.update_rating2(game.white, game.black,
                                                                       0 if game.bot() == game.black else 1)
                        if game.bot() == game.white:
                            file, embed = util2.make_embed(
                                game.black, title='Your game has ended',
                                description=(f'It was in this position that {await util2.get_name(game.bot())} resigned the game.\n'
                                             f'Your new rating is {round(data.data_manager.get_rating(game.black), 3)} ({round(black_delta, 3)})'))
                        else:
                            file, embed = util2.make_embed(
                                game.white, title='Your game has ended',
                                description=(f'It was in this position that {await util2.get_name(game.bot())} resigned the game.\n'
                                             f'Your new rating is {round(data.data_manager.get_rating(game.white), 3)} ({round(white_delta, 3)})'))
                        await util2.send_notif(game.player(), file=file, embed=embed)
                        data.data_manager.delete_game(
                            game.player(), chess.WHITE if game.bot() == game.black else chess.BLACK)
                    else:
                        await self.make_move(game, game.parse_move(move))
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
        util2 = self.client.get_cog('Util')

        person = ctx.author.id
        game = data.data_manager.get_game(person)

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
        if data.data_manager.get_game(person) is not None:
            file, embed = util2.make_embed(person, title=f'Your game with {await util2.get_name(game.to_move())}', description='You have moved.')
            await ctx.send(file=file, embed=embed)

    @cog_ext.cog_slash(name='move', description='Make a move in your game.', options=[
        create_option(name='move', description='What move you want to make',
                      option_type=SlashCommandOptionType.STRING, required=True)
    ])
    async def _move(self, ctx, move):
        await self.move(ctx, move)

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

        game = data.Game2()
        color = random.randint(0, 1)
        if color == 0:
            game.white = botid
            game.black = person
        else:
            game.white = person
            game.black = botid
        data.data_manager.change_game(game)
        util2 = self.client.get_cog('Util')
        file, embed = util2.make_embed(ctx.author.id, title='Game started!',
                                       description=(f'White: {await util2.get_name(game.white)}\n'
                                                    f'Black: {await util2.get_name(game.black)}\n'
                                                    'Use `$view` to view the game and use `$move` to make a move.\n'))
        await ctx.send(f'Game started with {ProfileNames[bot].value}\nYou play the {whiteblack[color]} pieces.', file=file, embed=embed)
        data.data_manager.change_settings(person, new_notif=ctx.channel.id)

    @challenge.command(aliases=['person'])
    async def user(self, ctx, person: Union[discord.Member, discord.User]):
        '''
        {
            "name": "challenge user",
            "description": "Challenges another user to a game of chess.\\nReact with a check mark to accept a challenge, and react with an X mark to decline\\nThe challenge will expire in 16 minutes.",
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
            return (user.id == person.id and str(reaction.emoji) == '✅') or user.id in [person.id, ctx.author.id] and str(reaction.emoji) == '❌'

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=969.6, check=check)
        except asyncio.TimeoutError:
            try:
                await challenge_msg.reply('Challenge timed out!')
                return
            except discord.HTTPException:
                return
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
        data.data_manager.change_game(game)

        file, embed = util2.make_embed(game.white, title='Game started!',
                                       description=(f'White: {await util2.get_name(game.white)}\n'
                                                    f'Black: {await util2.get_name(game.black)}\n'
                                                    'Use `$view` to view the game and use `$move` to make a move.\n'))
        await challenge_msg.reply(f'<@{game.white}> <@{game.black}>', file=file, embed=embed)
        data.data_manager.change_settings(
            game.white, new_notif=ctx.channel.id)
        data.data_manager.change_settings(
            game.black, new_notif=ctx.channel.id)

    @cog_ext.cog_slash(name='challenge-bot', description='Starts a game of chess against a bot.', options=[
        create_option(name='bot', description='Challenge a bot', option_type=SlashCommandOptionType.STRING,
                      required=True, choices=[name for name, member in Profile.__members__.items()])
    ])
    async def _challenge_bot(self, ctx, bot):
        await self.bot(ctx, bot)

    @cog_ext.cog_slash(name='challenge-user', description='Starts a game of chess against another person.', options=[
        create_option(name='person', description='The person you want to challenge.',
                      option_type=SlashCommandOptionType.USER, required=True),
        create_option(name='time_control', description='The maximum time per move, in seconds',
                      option_type=SlashCommandOptionType.INTEGER, required=False)
    ])
    async def _challenge_user(self, ctx, person, time_control=3 * 86400):
        if data.data_manager.get_game(ctx.author.id) is not None:
            await ctx.send('You already have a game in progress.')
            return
        if data.data_manager.get_game(person.id) is not None:
            await ctx.send(f'{person} already has a game in progress.')
            return
        if ctx.author.id == person.id:
            await ctx.send(f'You cannot challenge yourself.')
            return
        if time_control < 3600 or time_control > 5 * 86400:
            await ctx.send('The time control must be between one hour and 5 days.')
            return

        util2 = self.client.get_cog('Util')
        challenge_msg = await ctx.send((f'{person.mention}, {ctx.author} has challenged you to a game of chess.\n'
                                        f'{util.pretty_time(time_control)} per move.\n'
                                        'React with :white_check_mark: to accept.\n'
                                        'React with :x: to decline or withdraw your challenge.'))
        await challenge_msg.add_reaction('✅')
        await challenge_msg.add_reaction('❌')

        def check(reaction, user):
            return (user.id == person.id and str(reaction.emoji) == '✅') or user.id in [person.id, ctx.author.id] and str(reaction.emoji) == '❌'

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=969.6, check=check)
        except asyncio.TimeoutError:
            try:
                await challenge_msg.reply('Challenge timed out!')
                return
            except discord.HTTPException:
                return
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
        game.time_control = time_control
        data.data_manager.change_game(game)

        file, embed = util2.make_embed(game.white, title='Game started!',
                                       description=(f'White: {await util2.get_name(game.white)}\n'
                                                    f'Black: {await util2.get_name(game.black)}\n'
                                                    'Use `$view` to view the game and use `$move` to make a move.\n'))
        await challenge_msg.reply(f'<@{game.white}> <@{game.black}>', file=file, embed=embed)
        data.data_manager.change_settings(
            game.white, new_notif=ctx.channel.id)
        data.data_manager.change_settings(
            game.black, new_notif=ctx.channel.id)

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

    @cog_ext.cog_slash(name='resign', description='Resigns your game.', options=[])
    async def _resign(self, ctx):
        await self.resign(ctx)


def setup(bot):
    bot.add_cog(Engine(bot))
