import discord
from discord.ext import commands

from discord_slash import SlashCommand

import Chess_Bot.util.Data as data
import Chess_Bot.util.Utility as util
import Chess_Bot.util.Images as image

from Chess_Bot import constants

import os
import logging
from logging.handlers import TimedRotatingFileHandler
import traceback
from pathlib import Path
import sys


async def get_prefix(bot, message):
    if message.guild == None:
        return ['$', f'<@{bot.user.id}> ', f'<@!{bot.user.id}> ']
    return [data.data_manager.get_prefix(message.guild.id), f'<@{bot.user.id}> ', f'<@!{bot.user.id}> ']

bot = commands.Bot(command_prefix=get_prefix, help_command=None,
                   status='$help for commands, $botinfo for more information')
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_command_error(ctx, exc):
    try:
        if type(exc) == commands.errors.BotMissingPermissions:
            await ctx.send(f'Chess Bot is missing permissions.\nThe missing permissions are: `{" ".join(exc.missing_perms)}`')
            return
        elif isinstance(exc, discord.Forbidden) or str(exc).startswith('Command raised an exception: Forbidden'):
            await ctx.send(f'Chess Bot is missing permissions.')
            return
        elif type(exc) == commands.errors.MissingRequiredArgument:
            await ctx.send(f'Missing required argument.\nPlease enter a value for: `{exc.param}`.\nUse `$help <command name>` to get more information about a command.')
            return
        elif issubclass(type(exc), commands.errors.UserInputError):
            await ctx.send(f'There was an error parsing your argument')
            return
        elif type(exc) == commands.errors.TooManyArguments:
            await ctx.send(f'Bruh what why are there so many arguments?')
            return
        elif type(exc) == commands.errors.CommandOnCooldown:
            await ctx.send(f'You are on cooldown. Try again in {round(exc.retry_after, 3)} seconds')
            return
        elif type(exc) == commands.errors.CommandNotFound or type(exc) == commands.errors.CheckFailure:
            # await ctx.send('Command not found.')
            return
        elif type(exc) == commands.errors.MissingPermissions:
            await ctx.send(f'You are missing permissions.\nThe missing permissions are: {" ".join(exc.missing_perms)}')
            return
    except Exception as e:
        if not isinstance(e, discord.exceptions.Forbidden):
            print('Exception in on_command_error:\n', e)

    print('Command error found')

    # get data from exception
    etype = type(exc)
    trace = exc.__traceback__

    lines = traceback.format_exception(etype, exc, trace)
    traceback_text = ''.join(lines)

    if ctx.guild.id is not None:
        msg = ('Command Error:\n'
               f'Author: {ctx.author} ({ctx.author.id})\n'
               f'Guild: {ctx.guild} ({ctx.guild.id})\n'
               f'Request: {ctx.message.content}\n'
               f'{exc}, {type(exc)}'
               f'```\n{traceback_text}\n```')
    else:
        msg = ('Command Error:\n'
               f'Author: {ctx.author} ({ctx.author.id})\n'
               'Guild: None\n'
               f'Request: {ctx.message.content}\n'
               f'{exc}, {type(exc)}'
               f'```\n{traceback_text}\n```')
    print(msg)

    if await util.has_roles(ctx.author.id, ['Debugger', 'Tester', 'Mooderator'], bot):
        try:
            await ctx.send(msg)
        except discord.errors.HTTPException:
            msg_txt_path = os.path.join(constants.TEMP_DIR, 'message.txt')
            with open(msg_txt_path, 'w') as file:
                file.write(msg)
            await ctx.send(f'Command Error:\n', file=discord.File(msg_txt_path))
    else:
        await ctx.send('Uh oh. Something went wrong.\n'
                       'If you feel that this is a bug, please contact the bot developers in the chess bot support server.\n'
                       'https://discord.gg/Bm4zjtNTD2')

    error_channel = bot.get_channel(constants.ERROR_CHANNEL_ID)
    try:
        await error_channel.send(msg)
    except discord.errors.HTTPException:
        msg_txt_path = os.path.join(constants.TEMP_DIR, 'message.txt')
        with open(msg_txt_path, 'w') as file:
            file.write(msg)
        await error_channel.send(f'Command Error:\n', file=discord.File(msg_txt_path))


def setup():
    for path in constants.ALL_DIRS:
        os.makedirs(path, exist_ok=True)

    logging.basicConfig(format='{asctime}:{levelname}:{name}:{message}', style='{',
                        datefmt='%d-%m-%Y %H:%M:%S', level=logging.INFO,
                        handlers=[logging.StreamHandler(),
                                  TimedRotatingFileHandler(constants.LOG_FILE_PATH, when='D',
                                                           backupCount=3, utc=True)])

    image.load_all_themes()


def main():
    setup()

    cogs = [file.stem for file in Path('Chess_Bot', 'cogs').glob('*.py')]
    for extension in cogs:
        bot.load_extension(f'Chess_Bot.cogs.{extension}')
    logging.info(f'Cogs loaded: {", ".join(bot.cogs)}')

    if '-beta' in sys.argv:
        bot.add_check(lambda ctx: ctx.channel.id in constants.BETA_CHANNELS)
    else:
        bot.add_check(
            lambda ctx: not ctx.channel.id in constants.BETA_CHANNELS)

    token = os.getenv('BOT_TOKEN')
    if token is None:
        token = input('Token? ')
    bot.run(token)


if __name__ == '__main__':
    main()
