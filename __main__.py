import discord
import os
from discord.ext import commands
from discord.ext.commands.errors import ExpectedClosingQuoteError

from Chess_Bot.cogs.Misc import *
from Chess_Bot.cogs.Engine import *
from Chess_Bot.cogs.Viewing import *
from Chess_Bot.cogs.Mooderation import *
from Chess_Bot.cogs.Development import *
from Chess_Bot.cogs.Help import *
from Chess_Bot.cogs.Timer import *
from Chess_Bot.cogs.Topgg import *

import Chess_Bot.cogs.Data as data
import Chess_Bot.cogs.Utility as util
import Chess_Bot.cogs.Images as image

import logging
import traceback


async def get_prefix(bot, message):
    if message.guild == None:
        return ['$', f'<@{bot.user.id}> ', f'<@!{bot.user.id}> ']
    return [data.data_manager.get_prefix(message.guild.id), f'<@{bot.user.id}> ', f'<@!{bot.user.id}> ']

bot = commands.Bot(command_prefix=get_prefix, help_command=None,
                   status='$help for commands, $botinfo for more information')


# @bot.event
# async def on_error(error, *args, **kwargs):
# 	print('error found')
# 	print(error, type(error))
# 	error_channel = bot.get_channel(799761964401819679)
# 	await error_channel.send(f'Error: {str(error)}\nArgs: {args}\nkwargs: {kwargs}')


@bot.event
async def on_command_error(ctx, exc):
    if type(exc) == commands.errors.BotMissingPermissions:
        await ctx.send(f'Chess Bot is missing permissions.\nThe missing permissions are: {" ".join(exc.missing_perms)}')
    elif type(exc) == commands.errors.MissingRequiredArgument:
        await ctx.send(f'Missing required argument.\nPlease enter a value for: {exc.param}')
    elif (type(exc) == commands.errors.ArgumentParsingError or
          type(exc) == commands.errors.ExpectedClosingQuoteError or
          type(exc) == commands.errors.BadUnionArgument or
          type(exc) == commands.errors.UserInputError):
        await ctx.send(f'There was an error parsing your argument')
    elif type(exc) == commands.errors.TooManyArguments:
        await ctx.send(f'Bruh what why are there so many arguments?')
    elif type(exc) == commands.errors.CommandOnCooldown:
        await ctx.send(f'You are on cooldown. Try again in {round(exc.retry_after, 3)} seconds')
    elif type(exc) == commands.errors.CommandNotFound:
        await ctx.send('Command not found.')
    elif type(exc) == commands.errors.MissingPermissions:
        await ctx.send(f'You are missing permissions.\nThe missing permissions are: {" ".join(exc.missing_perms)}')
    else:
        print('Command error found')

        # get data from exception
        etype = type(exc)
        trace = exc.__traceback__

        # 'traceback' is the stdlib module, `import traceback`.
        lines = traceback.format_exception(etype, exc, trace)

        # format_exception returns a list with line breaks embedded in the lines, so let's just stitch the elements together
        traceback_text = ''.join(lines)

        print(traceback_text)

        if await util.has_roles(ctx.author, ['Debugger', 'Tester', 'Mooderator'], bot):
            await ctx.send(f'Command Error:\n```\n{traceback_text}\n```')
        else:
            await ctx.send('Uh oh. Something went wrong.\n'
                           'If you feel that this is a bug, please contact the bot developers in the chess bot support server.\n'
                           'https://discord.gg/Bm4zjtNTD2')

        error_channel = bot.get_channel(799761964401819679)
        try:
            await error_channel.send('Command Error:\n'
                                     f'Author: {ctx.author} ({ctx.author.id})\n'
                                     f'Guild: {ctx.guild} ({ctx.guild.id})\n'
                                     f'```\n{traceback_text}\n```')
        except:
            with open('Chess_Bot/data/message.txt', 'w') as file:
                file.write(traceback_text)
            await error_channel.send(f'Command Error:\n', discord.File('Chess_Bot/data/message.txt'))


def setup():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(
        filename='debug.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    image.load_all_themes()


def main():
    setup()

    bot.add_cog(Engine(bot))
    bot.add_cog(Misc(bot))
    bot.add_cog(Viewing(bot))
    bot.add_cog(Mooderation(bot))
    bot.add_cog(Development(bot))
    bot.add_cog(Help(bot))
    bot.add_cog(Timer(bot))
    bot.add_cog(Topgg(bot))

    token = os.environ.get('BOT_TOKEN')
    bot.run(token)


if __name__ == '__main__':
    main()
