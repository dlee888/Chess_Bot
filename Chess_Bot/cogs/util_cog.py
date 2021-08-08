import discord
from discord.ext import commands

import logging
import random

from Chess_Bot.cogs.Profiles import Profile, get_name
import Chess_Bot.util.Data as data
from Chess_Bot.util import Images


class Util(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def get_notifchannel(self, person):
        if person < len(Profile):
            return None
        channelid = data.data_manager.get_notifchannel(person)
        if channelid is not None:
            return await self.client.fetch_channel(channelid), False
        else:
            user = await self.client.fetch_user(person)
            channel = user.dm_channel
            if channel is not None:
                return channel, True
            try:
                return await user.create_dm(), True
            except Exception:
                return None

    async def get_name(self, person):
        if person < len(Profile):
            return get_name(person)
        return str(await self.client.fetch_user(person))

    def make_embed(self, person, *, title='', description=''):
        embed = discord.Embed(color=0x5ef29c, title=title,
                              description=description)
        path = Images.get_image2(person)
        embed.set_image(url='attachment://board.png')
        return discord.File(path, filename='board.png'), embed

    async def send_notif(self, person, text='', **kwargs):
        channel, is_default = await self.get_notifchannel(person)
        if channel is not None:
            text = f'<@{person}>' + text
            if is_default and random.randint(1, 3) == 1:
                text = 'Tip: set your notification channel by using the `$notif` command!.\n' + text
            await channel.send(text, **kwargs)


def setup(bot):
    bot.add_cog(Util(bot))
