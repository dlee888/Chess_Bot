import chess
from Chess_Bot import constants
import os
import discord

import Chess_Bot.util.Data as data
import Chess_Bot.util.Utility as util
from Chess_Bot.util.Images import *
from Chess_Bot.cogs.Profiles import Profile, ProfileNames


whiteblack = ['black', 'white']


async def run_engine(person):
    game = data.data_manager.get_game(person)
    
    if game.bot in [Profile.cb1.value, Profile.cb2.value, Profile.cb3.value]:
        file_in = os.path.join(constants.TEMP_DIR, f'input-{person}.txt')
        file_out = os.path.join(constants.TEMP_DIR, f'output-{person}.txt')

        game = data.data_manager.get_game(person)

        f = open(file_in, 'w')
        time_control = [1, 5, 20]
        max_depth = [5, 10, 69]
        f.write(
            f'setoption time_limit {time_control[game.bot]}\nsetoption depth_limit {max_depth[game.bot]}\ngo {game.fen}\nquit')
        f.close()
        await util.run(f'./engine < {file_in} > {file_out}')
        
        f = open(file_out)
        out = f.readlines()
        f.close()
        move = None
        for i in range(len(out) - 1, 0, -1):
            if out[i].startswith('COMPUTER PLAYED'):
                move = out[i][16:].strip()
                break
        for i in range(len(out) - 1, 0, -1):
            if out[i].startswith('GAME: '):
                game.fen = out[i][6:].strip()
                break
        return move, game

async def output_move(ctx, person, move):
    game = data.data_manager.get_game(person)

    embed = discord.Embed(
        title=f'{ctx.author}\'s game against {ProfileNames[Profile(game.bot).name].value}', description=f'{whiteblack[game.color].capitalize()} to move.', color=0x5ef29c)
    embed.set_footer(
        text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

    if move is not None:
        embed.add_field(
            name=f'{ProfileNames[Profile(game.bot).name].value} moved', value=move)

    get_image(person)

    file = discord.File(
        os.path.join(constants.TEMP_DIR, f'image-{person}.png'), filename='board.png')
    embed.set_image(url=f'attachment://board.png')

    await ctx.message.reply(file=file, embed=embed)


async def log(person, client, ctx):
    log_channel = client.get_channel(constants.LOG_CHANNEL_ID)

    await log_channel.send(f'Output for {ctx.author} (id = {ctx.author.id})\n'
                           f'Request: {ctx.message.content}',
                           files=[
                               discord.File(
                                   os.path.join(constants.TEMP_DIR, f'input-{person}.txt')),
                               discord.File(
                                   os.path.join(constants.TEMP_DIR, f'output-{person}.txt')),
                               discord.File(os.path.join(constants.TEMP_DIR, f'image-{person}.png'))])
