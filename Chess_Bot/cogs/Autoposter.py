import discord
from discord.ext import commands
from discord.ext import tasks

import logging
import sys

from Chess_Bot.util import Utility as util
from Chess_Bot.util import Data as data
from Chess_Bot import constants


class Autoposter(commands.Cog):

    def __init__(self, client):
        self.client = client
        if not '-beta' in sys.argv:
            self.post_stats.start()

    @tasks.loop(hours=5)
    async def post_stats(self):
        embed = discord.Embed(title="Bot Info", color=0xff0000)

        try:
            users = 0
            for guild in self.client.guilds:
                users += guild.member_count
        except Exception:
            users = 696969696969

        embed.add_field(name="Stats", value="Stats", inline=False)
        embed.add_field(name="Server Count", value=str(
            len(self.client.guilds)), inline=True)
        embed.add_field(name="Member Count", value=str(users), inline=True)
        embed.add_field(name='Games in progress', value=str(
            len(data.data_manager.get_games())), inline=True)
        embed.add_field(name='Games finished', value=str(
            data.data_manager.total_games()), inline=True)

        stats_channel = await self.client.fetch_channel(constants.STATS_CHANNEL_ID)
        await stats_channel.send(embed=embed)

    @post_stats.before_loop
    async def wait_until_ready(self):
        logging.info('Cog Autoposter: waiting for bot to get ready.')
        await self.client.wait_until_ready()


def setup(bot):
    bot.add_cog(Autoposter(bot))
