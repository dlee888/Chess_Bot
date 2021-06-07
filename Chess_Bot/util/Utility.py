import discord
from PIL import Image
import asyncio


import Chess_Bot.util.Data as data
from Chess_Bot import constants

thonking = []


async def run(cmd):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    stdout = str(stdout, 'utf-8')
    stderr = str(stderr, 'utf-8')

    return stdout, stderr, f'[{cmd!r} exited with {proc.returncode}]'


async def has_roles(person, roles, client):
    support_server = await client.fetch_guild(constants.SUPPORT_SERVER_ID)
    try:
        member = await support_server.fetch_member(person)
    except discord.HTTPException:
        return False

    for role in roles:
        for member_role in member.roles:
            if member_role.name == role:
                return True

    return False


def update_rating(user, outcome, bot):
    bot_rating = data.data_manager.get_rating(bot)
    person_rating = data.data_manager.get_rating(user)

    if bot_rating == None:
        bot_rating = constants.DEFAULT_RATING
    if person_rating == None:
        person_rating = constants.DEFAULT_RATING

    E = 1 / (1 + 10 ** ((bot_rating - person_rating) / 400))

    bot_rating += 32 * (E - outcome)
    person_rating += 32 * (outcome - E)

    data.data_manager.change_rating(bot, bot_rating)
    data.data_manager.change_rating(user, person_rating)


def pretty_time(time):
    hours = time//3600
    time -= 3600 * hours
    minutes = time//60
    time -= 60 * minutes
    return f'{int(hours)} hours, {int(minutes)} minutes, {round(time, 3)} seconds'

def cb_to_uci(cb_move):
    if cb_move == 1835008:
        return "O-O"
    elif cb_move == 2883584:
        return "O-O-O"
    
    start_square = cb_move % 64
    end_square = (cb_move // 64) % 64

    start_row = start_square // 8
    start_col = start_square % 8
    end_row = end_square // 8
    end_col = end_square % 8

    rows = '87654321'
    cols = 'abcdefgh'

    res = cols[start_col] + rows[start_row] + cols[end_col] + rows[end_row]

    if cb_move // (2 ** 18) % 4 == 2:
        promote_to = 'nbrq'
        res += promote_to[cb_move // (2 ** 20)]

    return res