import discord
from discord.ext import commands
import time

import Chess_Bot.cogs.Utility as util

version = '1.2.8'


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.start_time = time.time()

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def ping(self, ctx):
        '''
        Sends "Pong!"
        '''
        await ctx.send(f'Pong!\nLatency: {round(self.client.latency*1000000)/1000}ms')

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def rating(self, ctx, *user : discord.Member):
        '''
        Tells you your rating
        '''
        
        person = ctx.author
        if len(user) == 1:
            person = user[0]
        
        result = util.get_rating(person.id)
        
        if result == None:
            await ctx.send(f'{person} is unrated.')
        else:
            await ctx.send(f'{person}\'s rating is {result}')
        
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def leaderboard(self, ctx, num = '-1'):
        '''
        Shows highest rated players
        '''
        
        number = 1
        
        if num == 'all':
            number = len(util.ratings.keys())
        elif num == '-1':
            number = min(10, len(util.ratings.keys()))
        else:
            try:
                number = int(num)
            except ValueError:
                await ctx.send('That isn\'t even an integer lol')
                return
        
        if number > len(util.ratings.keys()):
            await ctx.send('There aren\'t even that many rated players lmao')
            return

        number = min(number, 25)

        all_players = []
        
        for k in util.ratings.keys():
            all_players.append((k, util.ratings[k]))
        
        all_players.sort(reverse=True, key=lambda a: a[1])
        
        embed = discord.Embed(title="Leaderboard", color=0xffff69)
        
        for i in range(number):
            user = await self.client.fetch_user(all_players[i][0])
            embed.add_field(name= f'{i+1}: {user}', value= f'{round(all_players[i][1])}', inline = True)
        
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def rank(self, ctx):
        '''
        Shows highest rated players
        '''

        all_players = []
        
        for k in util.ratings.keys():
            all_players.append((k, util.ratings[k]))
        
        all_players.sort(reverse=True, key=lambda a: a[1])
        
        rank = None
        for i in range(len(all_players)):
            if all_players[i][0] == ctx.author.id:
                rank = i + 1
                break
        
        await ctx.send(f'Your rating is {util.get_rating(ctx.author.id)}. You are ranked {rank} out of {len(all_players)} players.')

    @commands.command(aliases=['info'])
    @commands.cooldown(1, 4, commands.BucketType.default)
    async def botinfo(self, ctx):
        '''
        Basic info about Chess Bot
        Use $help for commands
        '''
        embed = discord.Embed(title="Bot Info", color=0xff0000)
        embed.add_field(name="Links",
                        value="[Github](https://github.com/jeffarjeffar/Chess_Bot) | [Invite](https://discord.com/api/oauth2/authorize?client_id=801501916810838066&permissions=268815424&scope=bot) | [Join the discord server](https://discord.gg/Bm4zjtNTD2) | [Top.gg](https://top.gg/bot/801501916810838066/vote)",
                        inline=False)
        embed.add_field(name='Version', value=version, inline=True)
        embed.add_field(name="Info",
                        value='Chess Bot is a bot that plays chess. $help for a list of commands.', inline=False)
        
        users = 0
        for guild in self.client.guilds:
            users += guild.member_count
        
        embed.add_field(name="Stats", value="Stats", inline=False)
        embed.add_field(name="Server Count", value=str(len(self.client.guilds)), inline=True)
        embed.add_field(name="Member Count", value=str(users), inline=True)
        embed.add_field(name="Up time", value=f'{util.pretty_time(time.time() - self.start_time)}', inline=False)
        
        owner = (await self.client.application_info()).owner
        embed.set_footer(text=f"Made by {owner}", icon_url=owner.avatar_url)
        
        embed.set_thumbnail(url='https://i.imgur.com/n1jak68.png')
        
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def invite(self, ctx):
        '''
        Sends invite link
        '''
        await ctx.send('https://discord.com/api/oauth2/authorize?client_id=801501916810838066&permissions=268815424&scope=bot')
        