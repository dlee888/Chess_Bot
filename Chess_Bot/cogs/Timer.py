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

        util2 = self.client.get_cog('Util')
        to_move = game.to_move()
        await ctx.send(f'{await util2.get_name(to_move)} to move against {await util2.get_name(game.get_person(not game.turn()))} with {util.pretty_time(game.time_left())} left.')

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

        util2 = self.client.get_cog('Util')
        to_move = game.to_move()
        await ctx.send(f'{await util2.get_name(to_move)} to move against {await util2.get_name(game.get_person(not game.turn()))} with {util.pretty_time(game.time_left())} left.')

    @tasks.loop(seconds=10)
    async def low_time_warn(self):
        games = data.data_manager.get_games()

        for game in games:
            if game.time_left() * 3 < game.time_control and not game.warned:
                util2 = self.client.get_cog('Util')
                await util2.send_notif(game.to_move(), 'You are low on time. Use `$time` to get how much time you have left before you automatically forfeit you game.')
                game.warned = True
                data.data_manager.change_game(game)

    @tasks.loop(seconds=10)
    async def no_time_check(self):
        games = data.data_manager.get_games()
        util2 = self.client.get_cog('Util')
        for game in games:
            if game.time_left() < 0:
                if game.to_move() == chess.WHITE:
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
        await self.client.wait_until_ready()


def setup(bot):
    bot.add_cog(Timer(bot))
