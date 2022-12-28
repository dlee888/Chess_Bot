import discord
from discord.ext import commands

import Chess_Bot.util.Data as data
import Chess_Bot.util.Images as image

from Chess_Bot import constants

import asyncio
import os
import logging
from logging.handlers import TimedRotatingFileHandler
import traceback
from pathlib import Path
import sys


async def get_prefix(bot, message):
    if message.guild is None:
        return ['$', f'<@{bot.user.id}> ', f'<@!{bot.user.id}> ']
    return [await data.data_manager.get_prefix(message.guild.id), f'<@{bot.user.id}> ', f'<@!{bot.user.id}> ']

intents = discord.Intents.none()
intents.messages = True
intents.reactions = True

total = os.getenv('TOTAL_SHARDS')
start = os.getenv('SHARD_START')
end = os.getenv('SHARD_END')
if total is not None and start is not None and end is not None:
    bot = commands.AutoShardedBot(command_prefix=get_prefix, shard_count=int(
        total), shard_ids=list(range(int(start), int(end))), help_command=None,
        status='$help for commands, $botinfo for more information', max_messages=None, intents=intents)
else:
    bot = commands.AutoShardedBot(command_prefix=get_prefix, help_command=None,
                                  status='$help for commands, $botinfo for more information', max_messages=None, intents=intents)


@bot.event
async def on_command_error(ctx, exc):
    try:
        if type(exc) == commands.errors.BotMissingPermissions:
            await ctx.send(f'Chess Bot is missing permissions.\nThe missing permissions are: `{" ".join(exc.missing_perms)}`')
            return
        elif isinstance(exc, discord.Forbidden) or str(exc).startswith('Command raised an exception: Forbidden'):
            await ctx.send('Chess Bot is missing permissions.')
            return
        elif type(exc) == commands.errors.MissingRequiredArgument:
            await ctx.send(f'Missing required argument.\nPlease enter a value for: `{exc.param}`.\nUse `$help <command name>` to get more information about a command.')
            return
        elif issubclass(type(exc), commands.errors.UserInputError):
            await ctx.send('There was an error parsing your argument')
            return
        elif type(exc) == commands.errors.TooManyArguments:
            await ctx.send('Bruh what why are there so many arguments?')
            return
        elif type(exc) == commands.errors.CommandOnCooldown:
            await ctx.send(f'You are on cooldown. Try again in {round(exc.retry_after, 3)} seconds')
            return
        elif type(exc) in [commands.errors.CommandNotFound, commands.errors.CheckFailure]:
            # await ctx.send('Command not found.')
            return
        elif type(exc) == commands.errors.MissingPermissions:
            await ctx.send(f'You are missing permissions.\nThe missing permissions are: {" ".join(exc.missing_perms)}')
            return
    except Exception as e:
        if not isinstance(e, discord.errors.Forbidden):
            print('Exception in on_command_error:\n', e)

    print('Command error found')

    # get data from exception
    etype = type(exc)
    trace = exc.__traceback__

    lines = traceback.format_exception(etype, exc, trace)
    traceback_text = ''.join(lines)

    if ctx.guild is not None:
        msg = ('Command Error:\n'
               f'Author: {ctx.author} ({ctx.author.id})\n'
               f'Guild: {ctx.guild} ({ctx.guild.id})\n'
               f'Channel: {ctx.channel} ({ctx.channel.id})\n'
               f'Request: {ctx.message.content}\n'
               f'{exc}, {type(exc)}\n'
               f'```\n{traceback_text}```\n')
    else:
        msg = ('Command Error:\n'
               f'Author: {ctx.author} ({ctx.author.id})\n'
               'Guild: None\n'
               f'Request: {ctx.message.content}\n'
               f'{exc}, {type(exc)}\n'
               f'```\n{traceback_text}```\n')
    logging.error(msg)

    if ctx.author.id in constants.DEVELOPERS:
        try:
            await ctx.send(msg)
        except discord.errors.HTTPException:
            msg_txt_path = os.path.join(constants.TEMP_DIR, 'message.txt')
            with open(msg_txt_path, 'w') as file:
                file.write(msg)
            await ctx.send('Command Error:\\n', file=discord.File(msg_txt_path))
    else:
        await ctx.send('Uh oh. Something went wrong.\n'
                       'If you feel that this is a bug, please contact the bot developers in the chess bot support server.\n'
                       'https://discord.gg/Bm4zjtNTD2')

    error_channel = bot.get_channel(constants.ERROR_CHANNEL_ID)
    if len(msg) < 2000:
        await error_channel.send(msg)
    else:
        msg_txt_path = os.path.join(constants.TEMP_DIR, 'message.txt')
        with open(msg_txt_path, 'w') as file:
            file.write(msg)
        await error_channel.send('Command Error:\\n', file=discord.File(msg_txt_path))


def setup():
    for path in constants.ALL_DIRS:
        os.makedirs(path, exist_ok=True)

    logging.basicConfig(format='{asctime}:{levelname}:{name}:{message}', style='{',
                        datefmt='%d-%m-%Y %H:%M:%S', level=logging.INFO,
                        handlers=[logging.StreamHandler(),
                                  TimedRotatingFileHandler(constants.LOG_FILE_PATH, when='D',
                                                           backupCount=3, utc=True)])

    image.load_all_themes()


async def main():
    setup()

    token = os.getenv(
        'BOT_TOKEN') if '-beta-bot' not in sys.argv else os.getenv('TEST_TOKEN')
    if token is None:
        token = input('Token? ')
    await bot.login(token)

    cogs = [file.stem for file in Path('Chess_Bot', 'cogs').glob('*.py')]
    for extension in cogs:
        await bot.load_extension(f'Chess_Bot.cogs.{extension}')
    logging.info(f'Cogs loaded: {", ".join(bot.cogs)}')

    if '-beta' in sys.argv:
        bot.add_check(lambda ctx: ctx.channel.id in constants.BETA_CHANNELS)
    else:
        bot.add_check(
            lambda ctx: ctx.channel.id not in constants.BETA_CHANNELS)

    await bot.tree.sync()
    logging.info('Done syncing')
    await bot.start(token, reconnect=True)


if __name__ == '__main__':
    asyncio.run(main())
