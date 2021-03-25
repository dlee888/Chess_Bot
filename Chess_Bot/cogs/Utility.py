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

prefixes = {}

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    stdout = str(stdout, 'utf-8')
    stderr = str(stderr, 'utf-8')

    return stdout, stderr, f'[{cmd!r} exited with {proc.returncode}]'


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
    return None


def update_rating(user, outcome):
    bot_rating = get_rating(801501916810838066)
    
    if bot_rating == None:
        ratings[801501916810838066] = 1500
        bot_rating = 1500

    if not user in ratings.keys():
        ratings[user] = 1500
    
    E = 1 / (1 + 10 ** ((bot_rating - get_rating(user)) / 400))
    
    if outcome == 1:
        bot_rating -= 32 * E
        ratings[user] += 32 * E
    elif outcome == 0:
        bot_rating += 32 * E
        ratings[user] -= 32 * E
    else:
        bot_rating += 32 * (E - 0.5)
        ratings[user] += 32 * (0.5 - E)

    ratings[801501916810838066] = bot_rating


def pretty_time(time):
    hours = time//3600
    time -= 3600 * hours
    minutes = time//60
    time -= 60 * minutes
    return f'{int(hours)} hours, {int(minutes)} minutes, {round(time)} seconds'
