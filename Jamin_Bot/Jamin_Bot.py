import discord
import os
from discord.ext import commands

from cogs.Misc import *
from cogs.Beat_Jamin import *

bot = commands.Bot(command_prefix = '!')

bot.add_cog(Beat_Jamin(bot))
bot.add_cog(Misc(bot))

TOKEN = input('Token: ')

bot.run(TOKEN)
