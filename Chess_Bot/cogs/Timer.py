import discord
from discord.ext import commands
from discord.ext import tasks
import time
import typing

import Chess_Bot.cogs.Utility as util
import Chess_Bot.cogs.Data as data
from Chess_Bot.cogs.CPP_IO import *

MAX_TIME_PER_MOVE = 3 * 24 * 60 * 60
LOW_TIME_WARN = 24 * 60 * 60


class Timer(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.no_time_check.start()
        self.low_time_warn.start()

    async def send_low_time_warning(self, person):
        file_in, file_out = prepare_files(person)
        prepare_input(person)

        await run_engine(file_in, file_out)

        f = open(file_out)
        out = f.readlines()
        f.close()

        game = data.data_manager.get_game(person)

        user = await self.client.fetch_user(person)

        embed = discord.Embed(
            title=f'{user}\'s game', description=f'{whiteblack[game.color].capitalize()} to move.\nYou are low on time.', color=0x5ef29c)

        file = None

        for i in range(len(out) - 1, 0, -1):
            if out[i].startswith('|'):
                get_image(person, i)

                file = discord.File(
                    f'Chess_Bot/data/image-{person}.png', filename='board.png')
                embed.set_image(url=f'attachment://board.png')

                break

        try:
            dm = user.dm_channel
            if dm == None:
                dm = await user.create_dm()

            await dm.send('You are low on time. Use `$time` to get how much time you have left.', embed=embed, file=file)
        except Exception as e:
            print('Exception in send_low_time_warning:', e)

    async def send_no_time_message(self, person):
        user = await self.client.fetch_user(person)

        data.data_manager.delete_game(person)

        old_rating = data.data_manager.get_rating(person)
        if old_rating == None:
            old_rating = 1500
            data.data_manager.change_rating(person, 1500)
        util.update_rating(person, 0)
        new_rating = data.data_manager.get_rating(person)

        try:
            dm = user.dm_channel
            if dm == None:
                dm = await user.create_dm()

            await dm.send(f'You automatically forfeited on time. Your new rating is {round(new_rating)} ({round(old_rating)} + {round(new_rating - old_rating, 2)})')
        except Exception as e:
            print('Exception in send_no_time_message:', e)

    @commands.command()
    async def time(self, ctx, *user: typing.Union[discord.User, discord.Member]):

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

        if len(user) == 1:
            await ctx.send(f'{user[0]} has {util.pretty_time(game.last_moved + MAX_TIME_PER_MOVE - time.time())} left.')
        else:
            await ctx.send(f'You have {util.pretty_time(game.last_moved + MAX_TIME_PER_MOVE - time.time())} left.')

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
