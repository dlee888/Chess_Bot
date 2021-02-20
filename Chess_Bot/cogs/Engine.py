import discord
import os
from discord.ext import commands
import random
import asyncio

from cogs.Utility import *
from cogs.CPP_IO import *

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
        
        file_in, file_out = prepare_files(person)
        prepare_input(person, move)

        await ctx.send('Chess Bot is thinking <:thonk:517531367517454347> ...')
        await run(f'.\\a < {file_in} > {file_out}')
        f = open(file_out)
        out = f.readlines()
        f.close()

        await log(person, self.client)
        thonking.remove(person)
        await output_move(ctx, person, self.client)
        
        if out[-3] == 'GAME STILL IN PROGRESS\n':
            return
        
        if out[-3] == 'ILLEGAL MOVE PLAYED\n':
            await ctx.send('Illegal move played. Make sure your move is in algebraic notation.\nType "$help move" for more info')
            return

        if out[-3] == 'COMPUTER RESIGNED\n':
            await ctx.send('Chess Bot resigned')
            update_rating(ctx.author.id, 1)
            await ctx.send(f'Your new rating is {get_rating(ctx.author.id)}')
            games.pop(ctx.author.id)
            return
        
        if out[-3] == 'DRAW\n':
            update_rating(ctx.author.id, 1/2)
            await ctx.send('Draw')
        elif out[-3][:5].lower() == whiteblack[colors[ctx.author.id]]:
            update_rating(ctx.author.id, 1)
            await ctx.send('You won!')
        elif out[-3][:5].lower() == whiteblack[1 - colors[ctx.author.id]]:
            update_rating(ctx.author.id, 0)
            await ctx.send('You lost.')
        else:
            await ctx.send('Something went wrong. <:thonkery:532458240559153163>')

        await ctx.send(f'Your new rating is {get_rating(ctx.author.id)}')
        games.pop(ctx.author.id)


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
        
        time_control[person] = 60

        for i in range(0, len(flags), 2):
            if flags[i] == '-t':
                time_control[person] = int(flags[i+1])

        games[person] = []
        colors[person] = random.randint(0, 1)  # 1 if white, 0 if black

        await ctx.send(f'Game started with Chess Bot\nYou are {whiteblack[colors[person]]}')

        file_in, file_out = prepare_files(person)
        prepare_input(person)

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

