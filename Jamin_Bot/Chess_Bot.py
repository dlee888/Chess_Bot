import discord
import os
from discord.ext import commands

from cogs.Misc import *
from cogs.Engine import *
from cogs.Viewing import *
from cogs.Mooderation import *

import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='debug.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


bot = commands.Bot(command_prefix='$')

bot.add_cog(Engine(bot))
bot.add_cog(Misc(bot))
bot.add_cog(Viewing(bot))
bot.add_cog(Mooderation(bot))

@bot.event
async def on_error(error, *args, **kwargs):
    #print('error found')
    # print(error)
    error_channel = bot.get_channel(799761964401819679)
    await error_channel.send(f'Error: {str(error)}\nArgs: {args}\nkwargs: {kwargs}')

@bot.event
async def on_command_error(ctx, exc):
    #print('command error found')
    #print(exc, type(exc))
    await ctx.send(f'Command Error: {str(exc)}')

token = open('token.txt')
TOKEN = token.readlines()[0]

bot.run(TOKEN)