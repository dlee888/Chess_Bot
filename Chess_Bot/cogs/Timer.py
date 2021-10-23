import discord
from discord.ext import commands
from discord.ext import tasks

from discord_slash import cog_ext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option

import logging
import time
import typing
import sys

import Chess_Bot.util.Utility as util
import Chess_Bot.util.Data as data
from Chess_Bot.util.CPP_IO import *
from Chess_Bot import constants


class Timer(commands.Cog):

    def __init__(self, client):
        self.client = client
        if not '-beta' in sys.argv:
            self.no_time_check.start()
            self.low_time_warn.start()

    async def send_low_time_warning(self, person):
        util2 = self.client.get_cog('Util')
        await util2.send_notif(person, 'You are low on time. Use `$time` to get how much time you have left before you automatically forfeit you game.')

    async def send_no_time_message(self, person):
        game = data.data_manager.get_game(person)
        data.data_manager.delete_game(person, False)

        old_rating, new_rating = util.update_rating(person, 0, game.bot)

        util2 = self.client.get_cog('Util')
        await util2.send_notif(person, f'You automatically forfeited on time. Your new rating is {round(new_rating)} ({round(old_rating)} + {round(new_rating - old_rating, 2)})')

    @commands.command()
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

        game = data.data_manager.get_game(person.id)

        if game == None:
            await ctx.send(f'{person} does not have a game in progress')
            return

        if isinstance(game, data.Game):
            await ctx.send(f'{person} has {util.pretty_time(game.last_moved + constants.MAX_TIME_PER_MOVE - time.time())} left.')
        else:
            util2 = self.client.get_cog('Util')
            to_move = game.to_move()
            await ctx.send(f'{await util2.get_name(to_move)} to move against {await util2.get_name(game.get_person(not game.turn()))} with {util.pretty_time(game.time_left(to_move))} left.')

    @cog_ext.cog_slash(name='time', description='Shows how much time you (or someone else) has left.', options=[
        create_option(name='person', description='The person you want to get the time for.',
                      option_type=SlashCommandOptionType.USER, required=False)
    ])
    async def _time(self, ctx, person: typing.Union[discord.User, discord.Member] = None):
        if person is None:
            person = ctx.author

        game = data.data_manager.get_game(person.id)

        if game == None:
            await ctx.send(f'{person} does not have a game in progress')
            return

        if isinstance(game, data.Game):
            await ctx.send(f'{person} has {util.pretty_time(game.last_moved + constants.MAX_TIME_PER_MOVE - time.time())} left.')
        else:
            util2 = self.client.get_cog('Util')
            to_move = game.to_move()
            await ctx.send(f'{await util2.get_name(to_move)} to move against {await util2.get_name(game.get_person(not game.turn()))} with {util.pretty_time(game.time_left(to_move))} left.')

    @tasks.loop(seconds=10)
    async def low_time_warn(self):
        games = data.data_manager.get_games()

        for game in games:
            if isinstance(game, tuple):
                person = game[0]
                game = game[1]
                time_left = game.last_moved + \
                    constants.MAX_TIME_PER_MOVE - time.time()

                if time_left < constants.LOW_TIME_WARN and not game.warned:
                    await self.send_low_time_warning(person)
                    game.warned = True
                    data.data_manager.change_game(person, game)
            elif isinstance(game, data.Game2):
                if game.to_move() == chess.WHITE:
                    time_left = game.white_last_moved + constants.MAX_TIME_PER_MOVE - time.time()
                    if time_left < constants.LOW_TIME_WARN and not game.white_warned:
                        await self.send_low_time_warning(game.white)
                        game.white_warned = True
                        data.data_manager.change_game(None, game)
                else:
                    time_left = game.black_last_moved + constants.MAX_TIME_PER_MOVE - time.time()
                    if time_left < constants.LOW_TIME_WARN and not game.black_warned:
                        await self.send_low_time_warning(game.black)
                        game.black_warned = True
                        data.data_manager.change_game(None, game)

    @tasks.loop(seconds=10)
    async def no_time_check(self):
        games = data.data_manager.get_games()
        util2 = self.client.get_cog('Util')
        for game in games:
            if isinstance(game, tuple):
                person = game[0]
                game = game[1]
                time_left = game.last_moved + \
                    constants.MAX_TIME_PER_MOVE - time.time()

                if time_left < 0:
                    await self.send_no_time_message(person)
            elif isinstance(game, data.Game2):
                if game.to_move() == chess.WHITE:
                    time_left = game.time_left(game.white)
                    if time_left < 0:
                        white_delta, black_delta = util.update_rating2(
                            game.white, game.black, 1)
                        await util2.send_notif(game.white,
                                               ('You automatically forfeited on time.\n'
                                                f'Your new rating is {data.data_manager.get_rating(game.white)} ({white_delta})'))
                        await util2.send_notif(game.black,
                                               ('Your opponent automatically forfeited on time.\n'
                                                f'Your new rating is {data.data_manager.get_rating(game.black)} ({black_delta})'))
                        data.data_manager.delete_game(game.white, chess.BLACK)
                else:
                    time_left = game.time_left(game.black)
                    if time_left < 0:
                        white_delta, black_delta = util.update_rating2(
                            game.white, game.black, 0)
                        await util2.send_notif(game.white,
                                               ('Your opponent automatically forfeited on time.\n'
                                                f'Your new rating is {data.data_manager.get_rating(game.white)} ({white_delta})'))
                        await util2.send_notif(game.black,
                                               ('You automatically forfeited on time.\n'
                                                f'Your new rating is {data.data_manager.get_rating(game.black)} ({black_delta})'))
                        data.data_manager.delete_game(game.white, chess.WHITE)

    @low_time_warn.before_loop
    @no_time_check.before_loop
    async def wait_until_ready(self):
        logging.info('Cog Timer: Waiting for bot to get ready')
        await self.client.wait_until_ready()


def setup(bot):
    bot.add_cog(Timer(bot))
