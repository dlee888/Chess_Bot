from Chess_Bot.util.CPP_IO import log
import discord
from discord.ext import commands
from discord.ext import tasks

import time
import typing
import logging
import sys

import Chess_Bot.util.Utility as util
import Chess_Bot.util.Data as data
from Chess_Bot.cogs.Profiles import Profile, ProfileNames
from Chess_Bot import constants

version = '2.1.1'


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.start_time = time.time()

    @commands.Cog.listener()
    async def on_ready(self):
        game = discord.Game("chess")
        await self.client.change_presence(status=discord.Status.dnd, activity=game)

        status_channel = await self.client.fetch_channel(constants.STATUS_CHANNEL_ID)
        
        if not '-beta' in sys.argv:
            await status_channel.send('Chess Bot has just restarted.')
        else:
            logging.info('Using beta version.')

        logging.info(f'Bot is ready. Logged in as {self.client.user}')

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ping(self, ctx):
        '''
        Sends "Pong!"
        '''
        await ctx.send(f'Pong!\nLatency: {round(self.client.latency*1000000)/1000}ms')

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def rating(self, ctx, person: typing.Union[discord.User, discord.Member] = None):
        '''
        Tells you your rating
        '''

        if person is None:
            person = ctx.author

        result = data.data_manager.get_rating(person.id)

        if result == None:
            await ctx.send(f'{person} is unrated.')
        else:
            await ctx.send(f'{person}\'s rating is {round(result, 2)}')

    @commands.command()
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def leaderboard(self, ctx, num='-1'):
        '''
        Shows highest rated players
        '''

        number = 1

        ratings = data.data_manager.get_ratings()

        if num == 'all':
            number = min(25, len(ratings.keys()))
        elif num == '-1':
            number = min(10, len(ratings.keys()))
        else:
            try:
                number = int(num)
            except ValueError:
                await ctx.send('That isn\'t even an integer lol')
                return

        if number > len(ratings.keys()):
            await ctx.send('There aren\'t even that many rated players lmao')
            return
        if number > 25:
            await ctx.send('The leaderboard can hold a max of 25 people.')
            return

        all_players = []

        for k in ratings.keys():
            if k in constants.LEADERBOARD_IGNORE:
                continue
            all_players.append((k, ratings[k]))

        all_players.sort(reverse=True, key=lambda a: a[1])

        embed = discord.Embed(title="Leaderboard", color=0xffff69)

        for i in range(number):
            if all_players[i][0] < 10:
                embed.add_field(
                    name=f'{i+1}: {ProfileNames[Profile(all_players[i][0]).name].value}', value=f'{round(all_players[i][1], 2)}', inline=True)
            else:
                user = await self.client.fetch_user(all_players[i][0])
                embed.add_field(
                    name=f'{i+1}: {user}', value=f'{round(all_players[i][1], 2)}', inline=True)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def rank(self, ctx):
        '''
        Shows highest rated players
        '''

        if data.data_manager.get_rating(ctx.author.id) is None:
            await ctx.send('You are unrated.')
            return

        ratings = data.data_manager.get_ratings()

        all_players = []

        for k in ratings.keys():
            if k in constants.LEADERBOARD_IGNORE:
                continue
            all_players.append((k, ratings[k]))

        all_players.sort(reverse=True, key=lambda a: a[1])

        rank = None
        for i in range(len(all_players)):
            if all_players[i][0] == ctx.author.id:
                rank = i + 1
                break

        await ctx.send(f'Your rating is {round(data.data_manager.get_rating(ctx.author.id), 2)}. You are ranked {rank} out of {len(all_players)} players.')

    @commands.command(aliases=['info'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def botinfo(self, ctx):
        '''
        Basic info about Chess Bot
        Use $help for commands
        '''
        embed = discord.Embed(title="Bot Info", color=0xff0000)
        embed.add_field(name="Links",
                        value=f"[Github]({constants.GITHUB_LINK}) | [Invite]({constants.INVITE_LINK}) | [Join the discord server]({constants.SUPPORT_SERVER_INVITE}) | [Top.gg]({constants.TOPGG_LINK})",
                        inline=False)
        embed.add_field(name='Version', value=version, inline=True)
        embed.add_field(name="Info",
                        value='Chess Bot is a bot that plays chess. Use `$help` for a list of commands.', inline=False)

        users = 0
        for guild in self.client.guilds:
            users += guild.member_count

        embed.add_field(name="Stats", value="Stats", inline=False)
        embed.add_field(name="Server Count", value=str(
            len(self.client.guilds)), inline=True)
        embed.add_field(name="Member Count", value=str(users), inline=True)
        embed.add_field(
            name="Up time", value=f'{util.pretty_time(time.time() - self.start_time)}', inline=True)
        embed.add_field(name='Games in progress', value=str(
            len(data.data_manager.get_games())), inline=True)
        embed.add_field(name='Games finished', value=str(
            data.data_manager.total_games()), inline=True)
        owner = (await self.client.application_info()).owner
        embed.set_footer(text=f"Made by {owner}", icon_url=owner.avatar_url)

        embed.set_thumbnail(url=constants.AVATAR_URL)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def invite(self, ctx):
        '''
        Sends invite link
        '''
        await ctx.send(constants.INVITE_LINK)

    @commands.command()
    async def stats(self, ctx, person: typing.Union[discord.Member, discord.User] = None):
        if person is None:
            person = ctx.author
        lost, won, drew = data.data_manager.get_stats(person.id)
        embed = discord.Embed(title=f'{person}\'s stats', color=0xfc26e0)
        embed.add_field(name='Rating', value=str(
            data.data_manager.get_rating(person.id)), inline=False)
        embed.add_field(name='Games Played', value=str(
            lost+won+drew), inline=False)
        embed.add_field(name='Lost', value=str(lost))
        embed.add_field(name='Won', value=str(won))
        embed.add_field(name='Drawn', value=str(drew))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))
