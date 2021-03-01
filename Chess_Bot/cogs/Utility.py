import discord
from PIL import Image
import asyncio


thonking = []

games = {}
colors = {}
time_control = {}

ratings = {}

last_moved = {}
warned = {}

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    stdout = str(stdout, 'utf-8')
    stderr = str(stderr, 'utf-8')

    return stdout, stderr, f'[{cmd!r} exited with {proc.returncode}]'


def get_image(person, end):
    game_file = f'Chess_Bot/data/output-{person}.txt'
    F = open(game_file)
    game = F.readlines()
    F.close()

    result = Image.open('Chess_Bot/images/blank_board.png')
    result = result.resize((400, 400))

    for i in range(end - 14, end + 2, 2):
        for j in range(1, 25, 3):
            square = 'Chess_Bot/images/'
            if game[i][j:j+2] == '  ':
                square += 'blank'
            else:
                square += game[i][j:j+2]
            x = (i + 14 - end)//2
            y = (j - 1)//3
            if (x + y) % 2 == 0:
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

    result.save(f'Chess_Bot/data/image-{person}.png')


async def has_roles(person, roles, client):
    support_server = await client.fetch_guild(733762995372425337)
    try:
        member = await support_server.fetch_member(person)
    except discord.HTTPException:
        return False

    for role in roles:
        for member_role in member.roles:
            if member_role.name == role:
                return True

    return False


def get_rating(user):
    if user in ratings.keys():
        return ratings[user]
    ratings[user] = 1500
    return 1500


def update_rating(user, outcome):
    jamin_rating = get_rating(801501916810838066)

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

    ratings[801501916810838066] = jamin_rating


# def push_ratings():
#     f = open('Chess_Bot/data/ratings.txt', 'w')

#     for k in ratings.keys():
#         f.write(f'{k} ----- {ratings[k]}\n')

#     f.close()


# def pull_ratings():
#     f = open('Chess_Bot/data/ratings.txt')
#     pulled = f.readlines()

#     ratings.clear()
#     for i in range(0, len(pulled)):
#         p = pulled[i].split(' ----- ')
#         ratings[int(p[0])] = float(p[1])

#     f.close()


# def push_games():
#     #os.system('echo "pushing games"')
#     f = open('Chess_Bot/data/games.txt', 'w')

#     for k in games.keys():
#         f.write(f'{k} ----- ')
#         for move in games[k]:
#             f.write(f'{move} ')
#         f.write('\n')
#     f.close()

#     f2 = open('Chess_Bot/data/colors.txt', 'w')
#     for k in colors.keys():
#         f2.write(f'{k} ----- {colors[k]}\n')
#     f2.close()

#     f3 = open('Chess_Bot/data/times.txt', 'w')
#     for k in time_control.keys():
#         f3.write(f'{k} ----- {time_control[k]}\n')
#     f3.close()
    
#     f4 = open('Chess_Bot/data/timer.txt', 'w')
#     for k in last_moved.keys():
#         f4.write(f'{k} ----- {last_moved[k]}')
#     f4.close()


# def pull_games():
#     f = open('Chess_Bot/data/games.txt')

#     g = f.readlines()
#     games.clear()
#     for i in g:
#         p = i.split(' ----- ')
#         games[int(p[0])] = []
#         g2 = p[1].strip().split(' ')
#         for i2 in g2:
#             if i2 == '' or i2 == '\n':
#                 continue
#             games[int(p[0])].append(int(i2))
#     f.close()

#     f2 = open('Chess_Bot/data/colors.txt')
#     g2 = f2.readlines()
#     colors.clear()
#     for i in g2:
#         p = i.split(' ----- ')
#         colors[int(p[0])] = int(p[1])
#     f2.close()

#     f3 = open('Chess_Bot/data/times.txt')
#     g3 = f3.readlines()
#     time_control.clear()
#     for i in g3:
#         p = i.split(' ----- ')
#         time_control[int(p[0])] = int(p[1])
#     f3.close()
    
#     f4 = open('Chess_Bot/data/timer.txt')
#     g4 = f4.readlines()
#     last_moved.clear()
#     for i in g4:
#         p = i.split(' ----- ')
#         last_moved[int(p[0])] = float(p[1])
#     f4.close()


def pretty_time(time):
    hours = time//3600
    time -= 3600 * hours
    minutes = time//60
    time -= 60 * minutes
    return f'{hours} hours, {minutes} minutes, {time} seconds'