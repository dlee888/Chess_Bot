import discord
import os
from discord.ext import commands
from discord.ext import tasks
import sys
import time
import subprocess
import textwrap

from cogs.Utility import *

version = '1.2.5'


def get_git_history():
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd, stdout = subprocess.PIPE, env=env).communicate()[0]
        return out
    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        branch = out.strip().decode('ascii')
        out = _minimal_ext_cmd(['git', 'log', '--oneline', '-5'])
        history = out.strip().decode('ascii')
        return (
            'Branch:\n' +
            textwrap.indent(branch, '  ') +
            '\nCommits:\n' +
            textwrap.indent(history, '  ')
        )
    except OSError:
        return "Fetching git info failed"

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.start_time = time.time()
        self.cow_worshipping = False
        self.cow_worship.start()

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
    @commands.cooldown(1, 1, commands.BucketType.default)
    async def f(self, ctx):
        '''
        Sends an 'f' in the chat
        '''
        await ctx.send('f')

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def rating(self, ctx, *user : discord.Member):
        '''
        Tells you your rating
        '''
        
        if len(user) == 1:
            await ctx.send(f'{user[0]}\'s ratinng is {get_rating(user[0].id)}')
        else:
            await ctx.send(f'Your rating is {get_rating(ctx.message.author.id)}')
        
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def leaderboard(self, ctx, num = '-1'):
        '''
        Shows highest rated players
        '''
        
        number = 1
        
        if num == 'all':
            number = len(ratings.keys())
        elif num == '-1':
            number = min(10, len(ratings.keys()))
        else:
            number = int(num)
        
        #await ctx.send(number)
        
        if number > len(ratings.keys()):
            await ctx.send('There aren\'t even that many rated players lmao')
            return
        
        all_players = []
        
        for k in ratings.keys():
            all_players.append((k, ratings[k]))
        
        all_players.sort(reverse=True, key=lambda a: a[1])
        
        embed = discord.Embed(title="Leaderboard", color=0xffff69)
        for i in range(number):
            user = await self.client.fetch_user(all_players[i][0])
            embed.add_field(name= f'{i+1}: {user.name}#{user.discriminator}', value= f'{round(all_players[i][1])}', inline = True)
            
            # if i%5 == 4:
            #     embed.add_field(name='--------------', value='--------------', inline = False)
            
        
        await ctx.send(embed=embed)

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
                        inline=True)
        embed.add_field(name='Version', value=version, inline=True)
        embed.add_field(name="Info",
                        value='Chess Bot is a bot that plays chess. $help for more information', inline=False)
        users = 0
        for guild in self.client.guilds:
            users += guild.member_count
        embed.add_field(name="Stats", value="Stats", inline=False)
        embed.add_field(name="Guild Count", value=str(len(self.client.guilds)), inline=True)
        embed.add_field(name="Member Count", value=str(users), inline=True)
        embed.add_field(name="Up time", value=f'{round((time.time() - self.start_time)*1000)/1000} seconds', inline=True)
        owner = (await self.client.application_info()).owner
        embed.set_footer(text=f"Made by {owner}", icon_url=owner.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def invite(self, ctx):
        '''
        Sends invite link
        '''
        await ctx.send('https://discord.com/api/oauth2/authorize?client_id=801501916810838066&permissions=268815424&scope=bot')

    @commands.command(brief='Get git information')
    async def git_history(self, ctx):
        """Replies with git information."""
        await ctx.send('```yaml\n' + get_git_history() + '```')

    @tasks.loop(seconds=10)
    async def cow_worship(self):
        if self.cow_worshipping:
            for guild in self.client.guilds:
                for channel in guild.channels:
                    if 'cow' in channel.name.lower() and 'worship' in channel.name.lower():
                        await channel.send(':pray::cow:')
                        
    @commands.command()
    async def cow(self, ctx, onoff):
        if not await has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator'], self.client):
            await ctx.send('You do not have permission to change the status of cow')
            return
        
        if onoff == 'status':
            if self.cow_worshipping:
                await ctx.send(f'Cow worshipping is on')
            else:
                await ctx.send(f'Cow worshipping is off')
            return
        
        new_cow = False
        
        if onoff == 'on':
            new_cow = True
        elif onoff != 'off':
            await ctx.send('Please enter a valid state (on/off)')
            return
            
        if new_cow == self.cow_worshipping:
            await ctx.send(f'Cow worshipping is already {onoff}')
            return
        
        self.cow_worshipping = new_cow
        
        await ctx.send(f'Cow worshipping has been turned {onoff}')
        
    @cow_worship.before_loop
    async def wait_ready(self):
        print('waiting for bot to get ready...')
        await self.client.wait_until_ready()