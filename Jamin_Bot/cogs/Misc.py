import discord
import os
from discord.ext import commands
import sys

from cogs.Utility import *

version = '1.2.4'


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        pull_ratings()
        pull_games()

        await self.client.change_presence(activity=discord.Game(name='$help or $botinfo for more info'))

        print('Bot is ready')

        await status_check()

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def ping(self, ctx):
        '''
        Sends "Pong!"
        '''
        await ctx.send(f'Pong!\nLatency: {round(self.client.latency*1000000)/1000}ms')

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def rating(self, ctx):
        '''
        Tells you your rating
        '''
        await ctx.send(f'Your rating is {get_rating(ctx.message.author.id)}')

    @commands.command(aliases=['info'])
    @commands.cooldown(1, 4, commands.BucketType.default)
    async def botinfo(self, ctx):
        '''
        Basic info about Chess Bot
        Use $help for commands
        '''
        embed = discord.Embed(title="Bot Info", color=0xff0000)
        embed.add_field(name="Links",
                        value="[Github](https://github.com/jeffarjeffar/Chess_Bot) | [Invite](https://discord.com/api/oauth2/authorize?client_id=801501916810838066&permissions=1544023120&scope=bot) | [Join the discord server](https://discord.gg/Bm4zjtNTD2)",
                        inline=True)
        embed.add_field(name='Version', value=version, inline=True)
        embed.add_field(name="Info",
                        value='Chess Bot is a bot that plays chess. $help for more information', inline=False)
        embed.set_footer(text="Made by Farmer John#3907")
        await ctx.send(embed=embed)
