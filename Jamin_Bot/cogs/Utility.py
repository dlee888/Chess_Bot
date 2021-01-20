import discord
import os
from discord.ext import commands


def is_mooderator(person):
    for role in person.roles:
        if role.name == 'Mooderator':
            return True
    return False


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
