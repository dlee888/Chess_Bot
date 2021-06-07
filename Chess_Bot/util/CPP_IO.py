from Chess_Bot import constants
import os
import discord

import Chess_Bot.util.Data as data
import Chess_Bot.util.Utility as util
from Chess_Bot.util.Images import *
from Chess_Bot.cogs.Profiles import Profile, ProfileNames


whiteblack = ['black', 'white']


async def run_engine(person, bot, move=''):
    if bot in [Profile.cb1.value, Profile.cb2.value, Profile.cb3.value]:
        file_in = os.path.join(constants.TEMP_DIR, f'input-{person}.txt')
        file_out = os.path.join(constants.TEMP_DIR, f'output-{person}.txt')

        game = data.data_manager.get_game(person)

        f = open(file_in, 'w')
        time_control = [1, 5, 20]
        f.write(
            f'play\n{whiteblack[1 - game.color]}\nyes2\n{str(game)}\n{time_control[bot]}\n{move}\nquit\nquit\n')
        f.close()
        await util.run(f'./engine < {file_in} > {file_out}')


async def output_move(ctx, person):
    f = open(os.path.join(constants.TEMP_DIR, f'output-{person}.txt'))
    out = f.readlines()
    f.close()

    game = data.data_manager.get_game(person)

    embed = discord.Embed(
        title=f'{ctx.author}\'s game against {ProfileNames[Profile(game.bot).name].value}', description=f'{whiteblack[game.color].capitalize()} to move.', color=0x5ef29c)
    embed.set_footer(
        text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

    for i in range(len(out) - 1, 0, -1):
        if out[i].startswith('COMPUTER PLAYED'):
            embed.add_field(
                name=f'{ProfileNames[Profile(game.bot).name].value} moved', value=out[i][16:])
            break

    file = None

    for i in range(len(out) - 1, 0, -1):
        if out[i].startswith('|'):
            get_image(person, i)

            file = discord.File(
                os.path.join(constants.TEMP_DIR, f'image-{person}.txt'), filename='board.png')
            embed.set_image(url=f'attachment://board.png')

            break

    for i in range(len(out) - 1, 0, -1):
        if out[i].startswith('GAME: '):
            game_str = out[i][6:-1].split(' ')
            game.moves.clear()
            for i in game_str:
                try:
                    game.moves.append(int(i))
                except:
                    pass
            break

    code = out[-3].strip()

    if code == 'DRAW':
        embed.description = 'Draw'
    elif (code == 'COMPUTER RESIGNED' and game.color == 1) or code == 'WHITE WON':
        embed.description = 'White won.'
    elif (code == 'COMPUTER RESIGNED' and game.color == 0) or code == 'BLACK WON':
        embed.description = 'Black won.'
    elif code == 'ILLEGAL MOVE PLAYED':
        embed.description = f'{whiteblack[game.color].capitalize()} to move.\nIllegal move played.'

    await ctx.message.reply(file=file, embed=embed)

    return code, game


async def log(person, client, ctx):
    log_channel = client.get_channel(798277701210341459)

    await log_channel.send(f'Output for {ctx.author} (id = {ctx.author.id})\n'
                           f'Request: {ctx.message.content}',
                           files=[
                               discord.File(
                                   os.path.join(constants.TEMP_DIR, f'input-{person}.txt')),
                               discord.File(
                                   os.path.join(constants.TEMP_DIR, f'output-{person}.txt')),
                               discord.File(os.path.join(constants.TEMP_DIR, f'image-{person}.txt'))])
