import discord
import os
from discord.ext import commands

from Chess_Bot.cogs.Misc import *
from Chess_Bot.cogs.Engine import *
from Chess_Bot.cogs.Viewing import *
from Chess_Bot.cogs.Mooderation import *
from Chess_Bot.cogs.Development import *
from Chess_Bot.cogs.Data import *
from Chess_Bot.cogs.Help import *
from Chess_Bot.cogs.Timer import *
from Chess_Bot.cogs.Topgg import *

import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='debug.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'), help_command=None)

bot.add_cog(Engine(bot))
bot.add_cog(Misc(bot))
bot.add_cog(Viewing(bot))
bot.add_cog(Mooderation(bot))
bot.add_cog(Development(bot))
bot.add_cog(Data(bot))
bot.add_cog(Help(bot))
bot.add_cog(Timer(bot))
bot.add_cog(Topgg(bot))

@bot.event
async def on_error(error, *args, **kwargs):
    print('error found')
    print(error, type(error))
    error_channel = bot.get_channel(799761964401819679)
    await error_channel.send(f'Error: {str(error)}\nArgs: {args}\nkwargs: {kwargs}')

@bot.event
async def on_command_error(ctx, exc):
    print('command error found')
    print(exc, type(exc))
    await ctx.send(f'Command Error: {str(exc)}')

token = os.environ.get('BOT_TOKEN')

bot.run(token)
