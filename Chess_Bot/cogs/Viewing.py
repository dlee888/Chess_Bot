import discord
from discord.ext import commands

from Chess_Bot.cogs.Utility import *
from Chess_Bot.cogs.CPP_IO import *

class Viewing(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.default)
    async def view(self, ctx, *user : discord.Member):
        '''
        Views your current game
        '''
        
        person = -1
        if len(user) == 1:
            person = user.id
        else:
            person = ctx.author.id

        if not person in games.keys():
            if len(user) == 1:
                await ctx.send(f'{user[0]} does not have a game in progress')
            else:
                await ctx.send('You do not have a game in progress')
            return
        
        if person in thonking:
            await ctx.send('Chess Bot is in the middle of thinking. Try again later.')
            return

        file_in, file_out = prepare_files(person)
        prepare_input(person)
        
        await run_engine(file_in, file_out)
        
        await output_move(ctx, person, self.client)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.default)
    async def fen(self, ctx, *user : discord.Member):
        '''
        Sends current game in FEN format
        '''

        person = -1
        if len(user) == 1:
            person = user[0].id
        else:
            person = ctx.author.id

        if not person in games.keys():
            if len(user) == 1:
                await ctx.send(f'{user[0]} does not have a game in progress')
            else:
                await ctx.send('You do not have a game in progress')
            return
        
        if person in thonking:
            await ctx.send('Chess Bot is in the middle of thinking. Try again later.')
            return

        file_in, file_out = prepare_files(person)

        f = open(file_in, 'w')
        f.write(f'fen\nyes2\n{get_game_str(person)}\nquit\n')
        f.close()
        
        await run_engine(file_in, file_out)
        
        f = open(file_out)
        out = f.readlines()
        f.close()

        await ctx.send(out[-2])
