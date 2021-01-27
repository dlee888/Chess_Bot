import discord
import os
from discord.ext import commands
from PIL import Image
import asyncio

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    stdout = str(stdout, 'utf-8')
    stderr = str(stderr, 'utf-8')

    return stdout, stderr, f'[{cmd!r} exited with {proc.returncode}]'

def get_image(person, end):
    game_file = f'data/output-{person}.txt'
    F = open(game_file)
    game = F.readlines()
    F.close()

    result = Image.open('images/blank_board.png')
    result = result.resize((400, 400))

    for i in range(end - 14, end + 2, 2):
        for j in range(1, 25, 3):
            square = 'images/'
            if game[i][j:j+2] == '  ':
                square += 'blank'
            else:
                square += game[i][j:j+2]
            x = (i + 14 - end)//2
            y = (j - 1)//3
            if (x + y) % 2:
                square += '-light.png'
            else:
                square += '-dark.png'
            
            square_img = Image.open(square)
            square_img = square_img.resize((50, 50), Image.ANTIALIAS)

            x *= 50
            y *= 50
            
            if colors[person] == 1:
                result.paste(square_img, (y, x, y + 50, x + 50))
            else:
                result.paste(square_img, (350 - y, 350 - x, 400 - y, 400 - x))
    
    result.save(f'data/image-{person}.png')

async def output_move(ctx, person, ping = -1):
    if ping == -1:
        ping = person
    f = open(f'data/output-{person}.txt')
    out = f.readlines()
    f.close()
    await ctx.send(f'<@{ping}>')
    for i in range(len(out) - 1, 0, -1):
        if out[i].startswith('COMPUTER PLAYED'):
            await ctx.send(out[i])
            break
    for i in range(len(out) - 1, 0, -1):
        if out[i].startswith('-----'):
            #print('Found board at', i)
            get_image(person, i - 1)
            await ctx.send(file=discord.File(f'data/image-{person}.png'))
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
            return

async def log(person, client):
    f = open(f'data/output-{person}.txt')
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

games = {}
colors = {}
time_control = {}

ratings = {}
jamin_rating = 1500


def get_rating(user):
    if user in ratings.keys():
        return ratings[user]
    ratings[user] = 1500
    return 1500


def update_rating(user, outcome):
    global jamin_rating

    E = 1 / (1 + 10 ** ((jamin_rating - get_rating(user)) / 400))
    if outcome == 1:
        jamin_rating -= 32 * E
        ratings[user] += 32 * E
    elif outcome == 0:
        jamin_rating += 32 * E
        ratings[user] -= 32 * E
    else:
        jamin_rating += 32 * (E - 0.5)
        ratings[user] += 32 * (0.5 - E)
    push_ratings()


def push_ratings():
    f = open('data/ratings.txt', 'w')
    f.write(str(jamin_rating)+'\n')
    for k in ratings.keys():
        f.write(f'{k} ----- {ratings[k]}\n')

    f.close()


def pull_ratings():
    global jamin_rating

    f = open('data/ratings.txt')
    pulled = f.readlines()
    jamin_rating = float(pulled[0])

    for i in range(1, len(pulled)):
        p = pulled[i].split(' ----- ')
        ratings[int(p[0])] = float(p[1])

    f.close()


def push_games():
    #os.system('echo "pushing games"')
    f = open('data/games.txt', 'w')
    for k in games.keys():
        f.write(f'{k} -----')
        for move in games[k]:
            f.write(f' {move}')
        f.write('\n')
    f.close()
    f = open('data/colors.txt', 'w')
    for k in colors.keys():
        f.write(f'{k} ----- {colors[k]}\n')
    f = open('data/times.txt', 'w')
    for k in time_control.keys():
        f.write(f'{k} ----- {time_control[k]}\n')


def pull_games():
    f = open('data/games.txt')

    g = f.readlines()
    for i in g:
        p = i.split(' ----- ')
        games[int(p[0])] = []
        g2 = p[1].split(' ')
        for i2 in g2:
            games[int(p[0])].append(int(i2))
    f.close()

    f = open('data/colors.txt')
    g = f.readlines()
    for i in g:
        p = i.split(' ----- ')
        colors[int(p[0])] = int(p[1])

    f = open('data/times.txt')
    g = f.readlines()
    for i in g:
        p = i.split(' ----- ')
        time_control[int(p[0])] = int(p[1])

async def status_check():
    while True:
        f = open('status.txt', 'w')
        f.write('RUNNING\n')
        f.close()
        await asyncio.sleep(5)