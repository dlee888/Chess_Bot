import sys
import typing

import discord
from discord import app_commands
from discord.ext import commands, tasks

import Chess_Bot.util.Data as data
import Chess_Bot.util.Utility as util
from Chess_Bot.util.CPP_IO import *


class Timer(commands.Cog):

    def __init__(self, client):
        self.client = client
        if '-beta' not in sys.argv:
            self.no_time_check.start()
            self.low_time_warn.start()

    @commands.hybrid_command(name='time', description='Shows how much time you (or someone else) has left.')
    @app_commands.describe(person='The person to view the time of. If no person is specified, it will default to your own game.')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def time(self, ctx, person: typing.Union[discord.User, discord.Member] = None):
        '''
        {
            "name": "time",
            "description": "Sends how much time [person] has before automatically resigning.\\nIf nobody is specified, it will default to your time left.",
            "usage": "$time [person]",
            "examples": [
                "$time",
                "$time @person"
            ],
            "cooldown": 3
        }
        '''
        if person is None:
            person = ctx.author

        game = await data.data_manager.get_game(person.id)

        if game is None:
            await ctx.send(f'{"You do" if person == ctx.author else f"{person} does"} not have a game in progress')
            return

        util2 = self.client.get_cog('Util')
        to_move = game.to_move()
        await ctx.send(f'{await util2.get_name(to_move)} to move against {await util2.get_name(game.get_person(not game.turn()))} with {util.pretty_time(game.time_left())} left.')

    @tasks.loop(seconds=10)
    async def low_time_warn(self):
        games = await data.data_manager.get_games()

        for game in games:
            if game.time_left() * 3 < game.time_control and not game.warned:
                util2 = self.client.get_cog('Util')
                file, embed, view = await util2.make_embed(game.to_move(),
                                                           title=f'{await util2.get_name(game.white)} vs {await util2.get_name(game.black)}',
                                                           description=f'{util.pretty_time(game.time_left())} left')
                await util2.send_notif(game.to_move(), ('You are low on time.\n'
                                                        'Use </time:968575170958749699> to get how much time you have left '
                                                        'before you automatically forfeit your game.'), file=file, embed=embed, view=view)
                game.warned = True
                await data.data_manager.change_game(game)

    @ tasks.loop(seconds=10)
    async def no_time_check(self):
        games = await data.data_manager.get_games()
        util2 = self.client.get_cog('Util')
        for game in games:
            if game.time_left() < 0:
                white_file, white_embed, _ = await util2.make_embed(game.white, title=f'{await util2.get_name(game.white)} vs {await util2.get_name(game.black)}')
                black_file, black_embed, _ = await util2.make_embed(game.black, title=f'{await util2.get_name(game.white)} vs {await util2.get_name(game.black)}')
                if game.turn() == chess.WHITE:
                    white_embed.description = f'{await util2.get_name(game.black)} won on time'
                    black_embed.description = f'{await util2.get_name(game.black)} won on time'
                    white_delta, black_delta = await util.update_rating2(
                        game.white, game.black, 1)
                    await util2.send_notif(game.white,
                                           ('You automatically forfeited on time.\n'
                                            f'Your new rating is {await data.data_manager.get_rating(game.white)} ({white_delta})'),
                                           file=white_file, embed=white_embed)
                    await util2.send_notif(game.black,
                                           ('Your opponent automatically forfeited on time.\n'
                                            f'Your new rating is {await data.data_manager.get_rating(game.black)} ({black_delta})'),
                                           file=black_file, embed=black_embed)
                    await data.data_manager.delete_game(game.player(), chess.BLACK)
                else:
                    white_embed.description = f'{await util2.get_name(game.white)} won on time'
                    black_embed.description = f'{await util2.get_name(game.white)} won on time'
                    white_delta, black_delta = await util.update_rating2(
                        game.white, game.black, 0)
                    await util2.send_notif(game.white,
                                           ('Your opponent automatically forfeited on time.\n'
                                            f'Your new rating is {await data.data_manager.get_rating(game.white)} ({white_delta})'),
                                           file=white_file, embed=white_embed)
                    await util2.send_notif(game.black,
                                           ('You automatically forfeited on time.\n'
                                            f'Your new rating is {await data.data_manager.get_rating(game.black)} ({black_delta})'),
                                           file=black_file, embed=black_embed)
                    await data.data_manager.delete_game(game.player(), chess.WHITE)

    @ low_time_warn.before_loop
    @ no_time_check.before_loop
    async def wait_until_ready(self):
        await self.client.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Timer(bot))
