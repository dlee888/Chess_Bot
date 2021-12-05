import discord

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

    old_rating = person_rating

    E = 1 / (1 + 10 ** ((bot_rating - person_rating) / 400))

    bot_rating += 32 * (E - outcome)
    person_rating += 32 * (outcome - E)

    data.data_manager.change_rating(bot, bot_rating)
    data.data_manager.change_rating(user, person_rating)

    return old_rating, person_rating


def update_rating2(white, black, outcome):
    '''Outcome: 1 if white loses, 0 if black loses
    returns (white_delta, black_delta)'''
    white_rating = data.data_manager.get_rating(white)
    black_rating = data.data_manager.get_rating(black)
    if white_rating == None:
        white_rating = constants.DEFAULT_RATING
    if black_rating == None:
        black_rating = constants.DEFAULT_RATING

    old_white = white_rating
    old_black = black_rating

    E = 1 / (1 + 10 ** ((white_rating - black_rating) / 400))

    white_rating += 32 * (E - outcome)
    black_rating += 32 * (outcome - E)

    data.data_manager.change_rating(white, white_rating)
    data.data_manager.change_rating(black, black_rating)

    return white_rating - old_white, black_rating - old_black


def pretty_time(time):
    days = time // 86400
    time -= 86400 * days
    hours = time // 3600
    time -= 3600 * hours
    minutes = time // 60
    time -= 60 * minutes
    arr = []
    if days != 0:
        arr.append(f'{days} days')
    if hours != 0:
        arr.append(f'{hours} hours')
    if minutes != 0:
        arr.append(f'{minutes} minutes')
    if time != 0:
        arr.append(f'{round(time, 3)} seconds')
    return ', '.join(arr)


def change_fen(person, new_fen):
    game = data.data_manager.get_game(person)
    game.fen = new_fen
    data.data_manager.change_game(person, game)
