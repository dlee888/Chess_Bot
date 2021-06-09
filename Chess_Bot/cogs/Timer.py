import discord
from discord.ext import commands
from discord.ext import tasks
import time
import typing

import Chess_Bot.util.Utility as util
import Chess_Bot.util.Data as data
from Chess_Bot.util.CPP_IO import *
from Chess_Bot import constants

MAX_TIME_PER_MOVE = 3 * 24 * 60 * 60
LOW_TIME_WARN = 24 * 60 * 60


class Timer(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.no_time_check.start()
        self.low_time_warn.start()

    async def send_low_time_warning(self, person):
        user = await self.client.fetch_user(person)

        try:
            dm = user.dm_channel
            if dm == None:
                dm = await user.create_dm()

            await dm.send('You are low on time. Use `$time` to get how much time you have left before you automatically forfeit you game.')
        except Exception as e:
            print('Exception in send_low_time_warning:', e)

    async def send_no_time_message(self, person):
        user = await self.client.fetch_user(person)
        game = data.data_manager.get_game(person)
        data.data_manager.delete_game(person, False)

        old_rating = data.data_manager.get_rating(person)
        if old_rating == None:
            old_rating = constants.DEFAULT_RATING
            data.data_manager.change_rating(person, constants.DEFAULT_RATING)
        util.update_rating(person, 0, game.bot)
        new_rating = data.data_manager.get_rating(person)

        try:
            dm = user.dm_channel
            if dm == None:
                dm = await user.create_dm()

            await dm.send(f'You automatically forfeited on time. Your new rating is {round(new_rating)} ({round(old_rating)} + {round(new_rating - old_rating, 2)})')
        except Exception as e:
            print('Exception in send_no_time_message:', e)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def time(self, ctx, person: typing.Union[discord.User, discord.Member] = None):

        if person is None:
            person = ctx.author

        game = data.data_manager.get_game(person.id)

        if game == None:
            await ctx.send(f'{person} does not have a game in progress')
            return

        await ctx.send(f'{person} has {util.pretty_time(game.last_moved + MAX_TIME_PER_MOVE - time.time())} left.')

    @tasks.loop(seconds=10)
    async def low_time_warn(self):
        games = data.data_manager.get_games()

        for person in games.keys():
            time_left = games[person].last_moved + \
                MAX_TIME_PER_MOVE - time.time()

            if time_left < LOW_TIME_WARN and not games[person].warned:
                await self.send_low_time_warning(person)
                games[person].warned = True
                data.data_manager.change_game(person, games[person])

    @tasks.loop(seconds=10)
    async def no_time_check(self):
        games = data.data_manager.get_games()

        for person in games.keys():
            time_left = games[person].last_moved + \
                MAX_TIME_PER_MOVE - time.time()

            if time_left < 0:
                await self.send_no_time_message(person)

    @low_time_warn.before_loop
    @no_time_check.before_loop
    async def wait_until_ready(self):
        print('Waiting for bot to get ready')
        await self.client.wait_until_ready()


def setup(bot):
    bot.add_cog(Timer(bot))
