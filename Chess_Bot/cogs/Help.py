import discord
from discord.ext import commands


import Chess_Bot.cogs.Utility as util


class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def get_default_help_embed(self):
        embed = discord.Embed(title='Help', color=0x02b022)

        owner = (await self.client.application_info()).owner
        embed.set_footer(text=f"Made by {owner}", icon_url=owner.avatar_url)
        embed.set_thumbnail(url='https://i.imgur.com/n1jak68.png')

        return embed

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = 'List of commands. Type "$help [command]" for more information about a certain command'

        embed.add_field(
            name='Playing', value='`challenge`, `move`, `resign`, `view`, `fen`, `time`', inline=False)
        embed.add_field(
            name='Rating', value='`rating`, `leaderboard`, `rank`', inline=False)
        embed.add_field(
            name='Other', value='`ping`, `help`, `botinfo`, `invite`')
        
        if await util.has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            embed.add_field(
                name='Development', value='Note: some developer commands do not work on heroku: `git_pull` and `update`\n`debug`, `debug_load`, `gimme`, `git_pull`, `restart`, `update`', inline=False
            )
            embed.add_field(
                name='Moderation', value='`abort`, `refund`'
            )

        await ctx.send(embed=embed)

    @help.command()
    async def challenge(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$challenge <flags>`
                              Challenges Chess bot to a game. Color is assigned randomly.
                              Flags:
                                `-t` to set the time control (in seconds). 
                                For example, `$challenge -t 5` to indicate that you want the computer to think for about 5 seconds
                                If no time is specified, the default time is 60 seconds'''

        await ctx.send(embed=embed)

    @help.command(aliases=['play'])
    async def move(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$move <move>` / `$play <move>`
                                Plays <move> against the computer
                                Please enter the move in algebraic notation
                                For example, `$move Ke2`
                                More about algebraic notation in [this chess.com article](https://www.chess.com/article/view/chess-notation#algebraic-notation)'''

        await ctx.send(embed=embed)

    @help.command()
    async def resign(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$resign`
                                Resigns your game'''

        await ctx.send(embed=embed)

    @help.command()
    async def view(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$view`
                                Views your current game.
                                `$view <person>` to view <person>'s game'''

        await ctx.send(embed=embed)

    @help.command()
    async def fen(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$fen`
                                Sends your current game in [fen notation](https://en.wikipedia.org/wiki/Forsyth%e2%80%93Edwards_Notation).
                                `$fen <person>` to get <person>'s game'''

        await ctx.send(embed=embed)


    @help.command()
    async def rating(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$rating`
                                Sends your rating.
                                `$rating <person>` to get <person>'s rating'''

        await ctx.send(embed=embed)
        
    @help.command()
    async def leaderboard(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$leaderboard`
                                Shows top rated players.
                                By default, shows 10 players.
                                Use `$leaderboard <number>` to get the top <number> players
                                Use `$leaderboard all` to get all players.
                                Note: Leaderboard is really laggy with more than about 15 people, and can not hold over 25 people'''

        await ctx.send(embed=embed)
        
    @help.command()
    async def ping(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$ping`
                                Sends "pong" and tells you the latency'''

        await ctx.send(embed=embed)
        
    @help.command()
    async def botinfo(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$botinfo`
                                Sends basic info and stats about the bot'''

        await ctx.send(embed=embed)
        
    @help.command()
    async def invite(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$invite`
                                Sends a invite link'''

        await ctx.send(embed=embed)
        
    @help.command()
    async def time(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$time`
                                Sends how much time you have left'''

        await ctx.send(embed=embed)
        
    @help.command()
    async def rank(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$rank`
                                Tells you what rank you are'''

        await ctx.send(embed=embed)
        