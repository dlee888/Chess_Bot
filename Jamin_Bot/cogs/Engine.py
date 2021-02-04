import discord
import os
from discord.ext import commands
import random
import asyncio

from PIL import Image

from cogs.Utility import *

thonking = []


class Engine(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['play'])
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def move(self, ctx, move):
        '''
        Plays <move> against the computer
        Please enter the move in algebraic notation
        For example, Nxe4, Nge5, c4, Ke2, etc
        More about algebraic notation here: https://www.chess.com/article/view/chess-notation#algebraic-notation
        '''
        if not ctx.author.id in games.keys():
            await ctx.send('You do not have a game in progress with Chess Bot')
            return

        if ctx.author.id in thonking:
            await ctx.send('Chess Bot is already thinking')
            return

        if len(thonking) > 3:
            await ctx.send('Resources overloaded. Please wait...')
            while len(thonking) > 3:
                await asyncio.sleep(5)

        person = ctx.author.id
        thonking.append(person)
        file_in = f'data/input-{person}.txt'
        file_out = f'data/output-{person}.txt'
        if not file_in[5:] in os.listdir('data'):
            f = open(file_in, 'x')
            f.close()
        if not file_out[5:] in os.listdir('data'):
            f = open(file_out, 'x')
            f.close()

        f = open(file_in, 'w')
        f.write('play\n')
        if len(games[ctx.author.id]) == 0:
            f.write('no\n')
        else:
            f.write('yes2\n')
            game_str = ''
            for i in range(len(games[ctx.author.id])):
                if i % 2 == 0:
                    game_str += str(i//2+1) + '. '
                game_str += str(games[ctx.author.id][i]) + ' '
            game_str += '*'
            f.write(game_str + '\n')
        f.write(f'{time_control[ctx.author.id]}\n')
        if colors[ctx.author.id] == 0:
            f.write('white\n')
        else:
            f.write('black\n')
        f.write(move + '\nquit\nquit\n')
        f.close()
        await ctx.send('Chess Bot is thinking <:thonk:517531367517454347> ...')
        await run(f'.\\a < {file_in} > {file_out}')
        f = open(file_out)
        out = f.readlines()
        f.close()

        if out[-3] == 'ILLEGAL MOVE PLAYED\n':
            await ctx.send('Illegal move played. Make sure your move is in algebraic notation.\nType "$help move" for more info')
            thonking.remove(person)
            return

        if out[-3] == 'COMPUTER RESIGNED\n':
            await ctx.send('Chess Bot resigned')
            update_rating(ctx.author.id, 1)
            await ctx.send(f'Your new rating is {get_rating(ctx.author.id)}')
            games.pop(ctx.author.id)
            push_games()
            thonking.remove(person)

            await log(person, self.client)
            return

        if out[-3] != 'GAME STILL IN PROGRESS\n':
            await log(person, self.client)
            winner = 0
            if out[-3] == 'DRAW\n':
                update_rating(ctx.author.id, 1/2)
                await ctx.send('Draw')
            else:
                if out[-3] == 'WHITE WON\n':
                    winner = 1
                elif out[-3] == 'BLACK WON\n':
                    winner = 0
                else:
                    await ctx.send('Something went wrong <:thonkery:532458240559153163>')
                    thonking.remove(person)
                    return

                if winner == colors[ctx.author.id]:
                    update_rating(ctx.author.id, 1)
                    await ctx.send('You won!')
                else:
                    update_rating(ctx.author.id, 0)
                    
                    await output_move(ctx, person, self.client)
                    await ctx.send('You lost.')

            thonking.remove(person)
            await ctx.send(f'Your new rating is {get_rating(ctx.author.id)}')
            games.pop(ctx.author.id)
            push_games()
            
            return

        await log(person, self.client)
        thonking.remove(person)
        await output_move(ctx, person, self.client)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def challenge(self, ctx, *flags):
        '''
        Challenges Chess Bot to a game
        Your color is assigned randomly.
        Flags:
            -t to set time control (in seconds)
        '''
        if ctx.author.id in games.keys():
            await ctx.send('You already have a game in progress')
            return
        person = ctx.author.id
        thonking.append(person)
        time_control[ctx.author.id] = 60

        for i in range(0, len(flags), 2):
            os.system(f'echo {flags[i]}')
            if flags[i] == '-t':
                time_control[ctx.author.id] = int(flags[i+1])

        games[ctx.author.id] = []
        colors[ctx.author.id] = random.randint(0, 1)  # 1 if white, 0 if black

        await ctx.send('Game started with Chess Bot')
        if colors[ctx.author.id] == 0:
            await ctx.send('You are black')
        else:
            await ctx.send('You are white')

        if colors[ctx.author.id] == 0:
            file_in = f'data/input-{person}.txt'
            file_out = f'data/output-{person}.txt'
            if not file_in[5:] in os.listdir('data'):
                f = open(file_in, 'x')
                f.close()
            if not file_out[5:] in os.listdir('data'):
                f = open(file_out, 'x')
                f.close()

            f = open(file_in, 'w')
            f.write(
                f'play\nno\n{time_control[ctx.author.id]}\nwhite\nquit\nquit')
            f.close()

            await run(f'.\\a < {file_in} > {file_out}')
            
            await log(person, self.client)
            await output_move(ctx, person, self.client)
        thonking.remove(person)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def resign(self, ctx):
        '''
        Resigns the game
        '''
        if not ctx.author.id in games.keys():
            await ctx.send('You do not have a game in progress')
            return

        games.pop(ctx.message.author.id)
        update_rating(ctx.author.id, 0)
        await ctx.send(f'Game resigned. Your new rating is {get_rating(ctx.author.id)}')
        push_games()

