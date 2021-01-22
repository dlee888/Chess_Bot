import discord
import os
from discord.ext import commands

from cogs.Utility import *

version = '1.0.0'


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        pull_ratings()
        pull_games()

        await self.client.change_presence(activity=discord.Game(name='$help or $botinfo for more info'))

        print('Bot is ready')

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def ping(self, ctx):
        '''
        Sends "Pong!"
        '''
        await ctx.send('Pong!')

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.default)
    async def update(self, ctx):
        '''
        Compiles the latest version of Chess Bot
        Compile message of 1 means that there were compile errors
        Compiler: g++
        '''
        #os.system('echo hi')
        compile_cmd = 'g++ '
        for filename in os.listdir('engine'):
            #os.system(f'echo {filename}')
            #print(filename, filename[-4:], filename[-2:])
            if filename[-4:] == '.cpp' or filename[-2:] == '.h':
                compile_cmd += f'engine/{filename} '
        
        print(compile_cmd)

        out = os.system(compile_cmd)

        await ctx.send(f'Updated\nCompile Message: {out}')

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def rating(self, ctx):
        '''
        Tells you your rating
        '''
        await ctx.send(f'Your rating is {get_rating(ctx.message.author.id)}')

    @commands.command(aliases = ['info'])
    @commands.cooldown(1, 4, commands.BucketType.default)
    async def botinfo(self, ctx):
        embed = discord.Embed(title="Bot Info", color=0xff0000)
        embed.add_field(name="Links",
                        value="[Github](https://github.com/jeffarjeffar/Chess_Bot) | [Invite](https://discord.com/api/oauth2/authorize?client_id=801501916810838066&permissions=2113928439&scope=bot)",
                        inline=False)
        embed.add_field(name="Info",
                        value='Chess Bot is a bot that plays chess. $help for more information', inline=True)
        embed.add_field(name='Version', value=version, inline=True)
        embed.set_footer(text="Made by Farmer John#3907")
        await ctx.send(embed=embed)
