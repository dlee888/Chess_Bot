import discord
from discord import app_commands
from discord.ext import commands

import time
import typing
import logging
import textwrap

import Chess_Bot.util.Utility as util
import Chess_Bot.util.Data as data
from Chess_Bot.cogs import Profiles as profiles
from Chess_Bot import constants

version = '4.1.0'


class CachedUsernames:

    def __init__(self, client):
        self.client = client
        self.cache = {}

    async def get_username(self, id):
        if id < len(profiles.Profile):
            return profiles.get_name(id)
        if id in self.cache.keys() and self.cache[id][1] >= time.time():
            return self.cache[id][0]
        name = str(await self.client.fetch_user(id))
        name = textwrap.shorten(name, 30, placeholder='...')
        self.cache[id] = (name, time.time() + constants.CACHE_REFRESH_TIME)
        return name


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.start_time = time.time()
        self.cache = CachedUsernames(client)

    @commands.Cog.listener()
    async def on_ready(self):
        game = discord.Game("chess")
        await self.client.change_presence(activity=game)

        logging.info(f'Bot is ready. Logged in as {self.client.user}')

    @commands.hybrid_command(name='ping', description='Is the bot online?')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ping(self, ctx):
        '''
        {
            "name": "ping",
            "description": "Sends the bot's latency.\\nAccording to the discord.py docs:\\nMeasures latency between a `HEARTBEAT` and a `HEARTBEAT_ACK` in seconds.\\nThis could be referred to as the Discord WebSocket protocol latency.",
            "usage": "$ping",
            "examples": [
                "$ping"
            ],
            "cooldown": 3
        }
        '''
        await ctx.send(f'Pong!\nLatency: {round(self.client.latency * 1000, 3)}ms')

    @commands.hybrid_command(name='rating', description='Get your rating.')
    @app_commands.describe(person='The person to view the rating of. If no person is specified, it will default to your own rating.')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def rating(self, ctx, person: typing.Union[discord.User, discord.Member] = None):
        '''
        {
            "name": "rating",
            "description": "Tells you a person's rating.\\nIf no person is specified, it defaults to your rating.",
            "usage": "$rating [user]",
            "examples": [
                "$rating",
                "$rating @person"
            ],
            "cooldown": 3
        }
        '''

        if person is None:
            person = ctx.author

        result = await data.data_manager.get_rating(person.id)

        if result is None:
            person_str = 'You are' if person == ctx.author else f'{person} is'
            await ctx.send(f'{person_str} unrated.')
        else:
            person_str = 'Your' if person == ctx.author else f'{person}\''
            await ctx.send(f'{person_str} rating is {round(result, 2)}')

    @commands.hybrid_command(name='leaderboard', description='Sends a list of highest rated players.', aliases=['top'])
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def leaderboard(self, ctx, num='-1'):
        '''
        {
            "name": "leaderboard",
            "description": "Sends a list of [number] highest rated players.\\nIf a number is not specified, it will default to 10.\\nYou can also enter \\"all\\" for all rated players, or \\"bots\\" for all bots.\\nRight now, the leaderboard can hold a maximum of 40 people.",
            "aliases": [
                "top"
            ],
            "usage": "$leaderboard [number]",
            "examples": [
                "$leaderboard",
                "$leaderboard 13",
                "$leaderboard all",
                "$leaderboard bots"
            ],
            "cooldown": 7
        }
        '''

        msg = await ctx.send('Fetching leaderboard (may take time)...')

        embed = discord.Embed(title="Leaderboard", color=0xffb521)

        ratings = await data.data_manager.get_ratings()
        all_players = list(ratings.items())

        if num in ['bots', 'bot']:
            all_players = [(bot.value, ratings[bot.value])
                           for bot in profiles.Profile]
            all_players.sort(reverse=True, key=lambda a: a[1])
            embed.set_footer(text='Top rated bots')
        else:
            number = constants.DEFAULT_LEADERBOARD_SIZE
            if num in ['all', 'max']:
                number = min(constants.MAX_LEADERBOARD_SIZE,
                             len(ratings.keys()))
            elif num == '-1':
                number = min(constants.DEFAULT_LEADERBOARD_SIZE,
                             len(ratings.keys()))
            else:
                try:
                    number = int(num)
                    assert(1 <= number <= constants.MAX_LEADERBOARD_SIZE)
                except (ValueError, AssertionError):
                    await ctx.send(f'Please enter an integer from 1 to {constants.MAX_LEADERBOARD_SIZE}.')
                    return

            if number > len(ratings.keys()):
                await ctx.send('There aren\'t even that many rated players.')
                return
            if number > constants.MAX_LEADERBOARD_SIZE:
                await ctx.send(f'The leaderboard can hold a max of {constants.MAX_LEADERBOARD_SIZE} people.')
                return

            embed.set_footer(text=f'Top {number} rated players')

            all_players.sort(reverse=True, key=lambda a: a[1])
            all_players = all_players[:number]

        rows = [f"{str(i + 1).rjust(2)}: {(await self.cache.get_username(person[0])).rjust(30)} ({f'{round(person[1], 2):.2f}'.rjust(7)})" for i, person in enumerate(all_players)]
        body = '\n'.join(rows)
        embed.description = f'```\n{body}\n```'
        embed.set_thumbnail(url=constants.AVATAR_URL)
        await msg.reply(embed=embed)

    @commands.hybrid_command(name='rank', description='Get your rank.')
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def rank(self, ctx):
        '''
        {
            "name": "rank",
            "description": "Tells you your rank among all rated players.",
            "usage": "$rank",
            "examples": [
                "$rank"
            ],
            "cooldown": 7
        }
        '''

        if await data.data_manager.get_rating(ctx.author.id) is None:
            await ctx.send('You are unrated.')
            return

        msg = await ctx.send('Fetching ratings...')

        ratings = await data.data_manager.get_ratings()

        all_players = [(k, ratings[k]) for k in ratings.keys()]

        all_players.sort(reverse=True, key=lambda a: a[1])

        rank = next((i + 1 for i in range(len(all_players))
                    if all_players[i][0] == ctx.author.id), None)

        await msg.reply(f'Your rating is {round(await data.data_manager.get_rating(ctx.author.id), 2)}. You are ranked {rank} out of {len(all_players)} players.')

    @commands.hybrid_command(aliases=['info', 'about'], name='botinfo', description='Sends information about the bot.')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def botinfo(self, ctx):
        '''
        {
            "name": "botinfo",
            "description": "Sends some info and stats about the bot.\\nUse `$help` for a list of commands.",
            "aliases": [
                "info"
            ],
            "usage": "$botinfo",
            "examples": [
                "$botinfo"
            ],
            "cooldown": 3
        }
        '''

        msg = await ctx.send('Getting info...')

        embed = discord.Embed(title="Bot Info", color=0xff0000)
        embed.add_field(name="Links",
                        value=f"[Github]({constants.GITHUB_LINK}) | [Invite]({constants.INVITE_LINK}) | [Join the discord server]({constants.SUPPORT_SERVER_INVITE}) | [Top.gg]({constants.TOPGG_LINK})",
                        inline=False)
        embed.add_field(name='Version', value=version, inline=True)
        embed.add_field(name="Info",
                        value='Chess Bot is a bot that plays chess. Use `$help` for a list of commands.', inline=False)

        embed.add_field(name="Stats", value="Stats", inline=False)
        embed.add_field(name="Server Count", value=str(
            len(self.client.guilds)), inline=True)
        embed.add_field(name="Total rated users", value=str(await data.data_manager.rated_users()), inline=True)
        embed.add_field(
            name="Up time", value=f'{util.pretty_time(time.time() - self.start_time)}', inline=True)
        embed.add_field(name='Games in progress', value=str(
            await data.data_manager.current_games()), inline=True)
        embed.add_field(name='Games finished', value=str(
            await data.data_manager.total_games()), inline=True)
        owner = (await self.client.application_info()).owner
        embed.set_footer(text=f"Made by {owner}")

        embed.set_thumbnail(url=constants.AVATAR_URL)

        await msg.edit(embed=embed)

    @commands.hybrid_command(name='invite', description='Sends an invite link for the bot.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def invite(self, ctx):
        '''
        {
            "name": "invite",
            "description": "Sends an invite link for adding the bot to a server.",
            "usage": "$invite",
            "examples": [
                "$invite"
            ],
            "cooldown": 1
        }
        '''
        await ctx.send(constants.INVITE_LINK)

    @commands.hybrid_command(name='stats', description='Sends some stats about some person.')
    @app_commands.describe(person='The person to get stats about. Defaults to you.')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def stats(self, ctx, person: typing.Union[discord.Member, discord.User] = None):
        """
        {
            "name": "stats",
            "description": "Sends stats about the person.",
            "usage": "$stats [person]",
            "examples": [
                "$stats",
                "$stats @person"
            ],
            "cooldown": 3
        }
        """

        if person is None:
            person = ctx.author
        lost, won, drew = await data.data_manager.get_stats(person.id)
        embed = discord.Embed(title=f'{person}\'s stats', color=0xf9ff82)
        embed.add_field(name='Rating', value=str(
            await data.data_manager.get_rating(person.id)), inline=False)
        embed.add_field(name='Games Played', value=str(
            lost+won+drew), inline=False)
        embed.add_field(name='Lost', value=str(lost))
        embed.add_field(name='Won', value=str(won))
        embed.add_field(name='Drawn', value=str(drew))
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Misc(bot))
