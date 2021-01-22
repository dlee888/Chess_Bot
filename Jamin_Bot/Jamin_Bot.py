import discord
import os
from discord.ext import commands

from cogs.Misc import *
from cogs.Beat_Jamin import *

bot = commands.Bot(command_prefix='$')

bot.add_cog(Beat_Jamin(bot))
bot.add_cog(Misc(bot))


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

TOKEN = input('Token: ')

bot.run(TOKEN)
