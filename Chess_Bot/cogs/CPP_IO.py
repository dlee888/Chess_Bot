import os
import discord

from Chess_Bot.cogs.Utility import *


whiteblack = ['black', 'white']


def prepare_files(person):
    file_in = f'Chess_Bot/data/input-{person}.txt'
    file_out = f'Chess_Bot/data/output-{person}.txt'

    if not file_in[5:] in os.listdir('Chess_Bot/data'):
        f = open(file_in, 'x')
        f.close()
    if not file_out[5:] in os.listdir('Chess_Bot/data'):
        f = open(file_out, 'x')
        f.close()

    return file_in, file_out


def get_game_str(person):
    game_str = ''
    for i in range(len(games[person])):
        if i % 2 == 0:
            game_str += str(i//2+1) + '. '
        game_str += str(games[person][i]) + ' '
    game_str += '*'
    return game_str


def prepare_input(person, move=''):
    file_in = f'Chess_Bot/data/input-{person}.txt'

    f = open(file_in, 'w')
    f.write(f'play\nyes2\n{get_game_str(person)}\n{time_control[person]}\n{whiteblack[1 - colors[person]]}\n{move}\nquit\nquit\n')
    f.close()

async def run_engine(file_in, file_out):
    print('Running engine')
    out, err, status = await run(f'./"Chess_Bot/a" < {file_in} > {file_out}')
    print(f'Stdout: {out}\nStderr: {err}\n{status}')

async def output_move(ctx, person, client):
    user = await ctx.message.guild.fetch_member(person)

    f = open(f'Chess_Bot/data/output-{person}.txt')
    out = f.readlines()
    f.close()

    embed = discord.Embed(
        title=f'{user}\'s game', description=f'{whiteblack[colors[user.id]].capitalize()} to move.', color=0x5ef29c)
    embed.set_footer(
        text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

    for i in range(len(out) - 1, 0, -1):
        if out[i].startswith('COMPUTER PLAYED'):
            embed.add_field(name='Computer moved', value=out[i][16:])
            break

    for i in range(len(out) - 1, 0, -1):
        if out[i].startswith('-----'):
            get_image(person, i - 1)

            temp_channel = client.get_channel(806967405414187019)
            image_msg = await temp_channel.send(file=discord.File(f'Chess_Bot/data/image-{person}.png'))

            image_url = image_msg.attachments[0].url

            embed.set_image(url=image_url)

            break

    for i in range(len(out) - 1, 0, -1):
        if out[i].startswith('GAME: '):
            game_str = out[i][6:-1].split(' ')
            games[person].clear()
            for i in game_str:
                if i == '' or i == '\n':
                    continue
                games[person].append(int(i))
            push_games()
            break
    
    code = out[-3].strip()
    
    if code == 'DRAW':
        embed.description = 'Draw'
    elif (code == 'RESIGN' and colors[person] == 1) or code == 'WHITE WON':
        embed.description = 'White won.'
    elif (code == 'RESIGN' and colors[person] == 0) or code == 'BLACK WON':
        embed.description = 'Black won.'
    elif code == 'ILLEGAL MOVE PLAYED':
        embed.description = f'{whiteblack[colors[person]].capitalize()} to move.\nIllegal move played.'
        
    await ctx.message.reply(embed=embed)
    return code


async def log(person, client):
    f = open(f'Chess_Bot/data/output-{person}.txt')
    out = f.readlines()
    f.close()
    log_channel = client.get_channel(798277701210341459)
    msg = f'<{person}>\n```\n'
    for i in range(len(out)):
        msg += out[i] + '\n'
        if i % 10 == 0:
            msg += '```'
            await log_channel.send(msg)
            msg = '```'
    msg += '```'
    await log_channel.send(msg)
