import os
import discord

import Chess_Bot.cogs.Utility as util


whiteblack = ['black', 'white']


def prepare_files(person):
    file_in = f'Chess_Bot/data/input-{person}.txt'
    file_out = f'Chess_Bot/data/output-{person}.txt'

    if not file_in[15:] in os.listdir('Chess_Bot/data'):
        f = open(file_in, 'x')
        f.close()
    if not file_out[15:] in os.listdir('Chess_Bot/data'):
        f = open(file_out, 'x')
        f.close()

    return file_in, file_out


def get_game_str(person):
    game_str = ''
    for i in range(len(util.games[person])):
        if i % 2 == 0:
            game_str += str(i//2+1) + '. '
        game_str += str(util.games[person][i]) + ' '
    game_str += '*'
    return game_str


def prepare_input(person, move=''):
    file_in = f'Chess_Bot/data/input-{person}.txt'

    f = open(file_in, 'w')
    f.write(
        f'play\nyes2\n{get_game_str(person)}\n{util.time_control[person]}\n{whiteblack[1 - util.colors[person]]}\n{move}\nquit\nquit\n')
    f.close()


async def run_engine(file_in, file_out):
    print('Running engine')
    out, err, status = await util.run(f'./engine < {file_in} > {file_out}')
    print(f'Stdout: {out}\nStderr: {err}\n{status}')


async def output_move(ctx, person, client):
    user = await ctx.message.guild.fetch_member(person)

    f = open(f'Chess_Bot/data/output-{person}.txt')
    out = f.readlines()
    f.close()

    embed = discord.Embed(
        title=f'{user}\'s game', description=f'{whiteblack[util.colors[user.id]].capitalize()} to move.', color=0x5ef29c)
    embed.set_footer(
        text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

    for i in range(len(out) - 1, 0, -1):
        if out[i].startswith('COMPUTER PLAYED'):
            embed.add_field(name='Computer moved', value=out[i][16:])
            break
    
    file = None
    
    for i in range(len(out) - 1, 0, -1):
        if out[i].startswith('-----'):
            util.get_image(person, i - 1)

            file = discord.File(f'Chess_Bot/data/image-{person}.png', filename = 'board.png')
            embed.set_image(url= f'attachment://board.png')

            break

    for i in range(len(out) - 1, 0, -1):
        if out[i].startswith('GAME: '):
            game_str = out[i][6:-1].split(' ')
            util.games[person].clear()
            for i in game_str:
                if i == '' or i == '\n':
                    continue
                util.games[person].append(int(i))
            break

    code = out[-3].strip()

    if code == 'DRAW':
        embed.description = 'Draw'
    elif (code == 'COMPUTER RESIGNED' and util.colors[person] == 1) or code == 'WHITE WON':
        embed.description = 'White won.'
    elif (code == 'COMPUTER RESIGNED' and util.colors[person] == 0) or code == 'BLACK WON':
        embed.description = 'Black won.'
    elif code == 'ILLEGAL MOVE PLAYED':
        embed.description = f'{whiteblack[util.colors[person]].capitalize()} to move.\nIllegal move played.'

    try:
        await ctx.message.reply(file=file, embed=embed)
    except Exception as e:
        if e == discord.Forbidden:
            await ctx.send('Something went wrong. Are you sure Chess Bot has permission to send embeds?')
        else:
            await ctx.send('Something went wrong.')
            await ctx.send(str(e))
            
    return code


async def log(person, client, ctx):
    log_channel = client.get_channel(798277701210341459)

    await log_channel.send(f'''Output for {ctx.author} (id = {ctx.author.id})
                           Request: {ctx.message.content}
                           {ctx.message}
                           Jump url: ({ctx.message.jump_url})''', files=[
        discord.File(f'Chess_Bot/data/output-{person}.txt'),
        discord.File(f'Chess_Bot/data/input-{person}.txt')])
