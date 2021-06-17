import logging
import discord
from discord.ext import commands
from discord.ext import tasks

from Chess_Bot.util import Utility as util
from Chess_Bot.util import Data as data
from Chess_Bot import constants


class Autoposter(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.post_stats.start()

    @tasks.loop(hours=3)
    async def post_stats(self):
        embed = discord.Embed(title="Bot Info", color=0xff0000)

        users = 0
        for guild in self.client.guilds:
            users += guild.member_count

        embed.add_field(name="Stats", value="Stats", inline=False)
        embed.add_field(name="Server Count", value=str(
            len(self.client.guilds)), inline=True)
        embed.add_field(name="Member Count", value=str(users), inline=True)
        embed.add_field(name='Games in progress', value=str(
            len(data.data_manager.get_games())), inline=True)
        embed.add_field(name='Games finished', value=str(
            data.data_manager.total_games()), inline=True)
        owner = (await self.client.application_info()).owner
        embed.set_footer(text=f"Made by {owner}", icon_url=owner.avatar_url)

        embed.set_thumbnail(url=constants.AVATAR_URL)

        guild = await self.client.fetch_guild(constants.SUPPORT_SERVER_ID)
        stats_channel = guild.get_channel(constants.STATS_CHANNEL_ID)
        await stats_channel.send(embed=embed)

    @post_stats.before_loop
    async def wait_until_ready(self):
        logging.info('Cog Autoposter: waiting for bot to get ready.')
        await self.client.wait_until_ready()


def setup(bot):
    bot.add_cog(Autoposter(bot))
