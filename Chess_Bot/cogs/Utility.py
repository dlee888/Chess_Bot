import discord
from PIL import Image
import asyncio


from Chess_Bot.cogs import Data as data


thonking = []


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


def update_rating(user, outcome):
    bot_rating = data.data_manager.get_rating(801501916810838066)
    person_rating = data.data_manager.get_rating(user)

    if bot_rating == None:
        bot_rating = 1500
    if person_rating == None:
        person_rating = 1500

    E = 1 / (1 + 10 ** ((bot_rating - person_rating) / 400))

    bot_rating += 32 * (E - outcome)
    person_rating += 32 * (outcome - E)

    data.data_manager.change_rating(801501916810838066, bot_rating)
    data.data_manager.change_rating(user, person_rating)


def pretty_time(time):
    hours = time//3600
    time -= 3600 * hours
    minutes = time//60
    time -= 60 * minutes
    return f'{int(hours)} hours, {int(minutes)} minutes, {round(time)} seconds'
