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
            name='Playing', value='`challenge`, `profiles`, `move`, `resign`, `view`, `fen`, `time`', inline=False)
        embed.add_field(
            name='Rating', value='`rating`, `leaderboard`, `rank`', inline=False)
        embed.add_field(
            name='Other', value='`ping`, `help`, `botinfo`, `invite`, `prefix`, `theme`, `vote`')

        await ctx.send(embed=embed)

    @help.command()
    async def challenge(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$challenge <bot>`
                              Challenges Chess bot to a game. Color is assigned randomly.'''

        await ctx.send(embed=embed)
        
    @help.command()
    async def profiles(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = 'Sends a list of the Chess Bot computers that you can challenge.\nUse `$profile <bot tag> for more information on a bot. For example, `$profile cb1`.'

        await ctx.send(embed=embed)

    @help.command(aliases=['play'])
    async def move(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$move <move>` or `$play <move>`
                                Plays <move> against the computer
                                Please enter the move in algebraic notation
                                For example, `$move Ke2`
                                More about algebraic notation in [this chess.com article](https://www.chess.com/article/view/chess-notation#algebraic-notation).'''

        await ctx.send(embed=embed)

    @help.command()
    async def resign(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$resign`
                                Resigns your game.'''

        await ctx.send(embed=embed)

    @help.command()
    async def view(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$view`
                                Views your current game.
                                `$view <person>` to view <person>'s game.'''

        await ctx.send(embed=embed)

    @help.command()
    async def fen(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$fen`
                                Sends your current game in [fen notation](https://en.wikipedia.org/wiki/Forsyth%e2%80%93Edwards_Notation).
                                `$fen <person>` to get <person>'s game.'''

        await ctx.send(embed=embed)

    @help.command()
    async def rating(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$rating`
                                Sends your rating.
                                `$rating <person>` to get <person>'s rating.'''

        await ctx.send(embed=embed)

    @help.command()
    async def leaderboard(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$leaderboard`
                                Shows top rated players.
                                By default, shows 10 players.
                                Use `$leaderboard <number>` to get the top <number> players. For example, `$leaderboard 13` will give the top 13 instead of the top 10.
                                Use `$leaderboard all` to get all players.
                                Note: Leaderboard can not hold over 25 people. If there are more than 25 players, not all of them will be shown.'''

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
                                Sends basic info and stats about the bot.'''

        await ctx.send(embed=embed)

    @help.command()
    async def invite(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$invite`
                                Sends a invite link.'''

        await ctx.send(embed=embed)

    @help.command()
    async def time(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$time`
                                Sends how much time you have left before you will automatically resign.'''

        await ctx.send(embed=embed)

    @help.command()
    async def rank(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$rank`
                                Tells you what rank you are out of all rated players.'''

        await ctx.send(embed=embed)

    @help.command()
    async def prefix(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$prefix <new prefix>`
                                Sets a custom bot prefix for the server. You must have admin permission to change the prefix.
                                If you want to figure out what the prefix is, use `$prefix`.
                                Note: while the prefix can be changed, the bot will always to respond to `@Chess Bot`.
                                If you are unsure of what the prefix is, you should use `@Chess Bot prefix`'''

        await ctx.send(embed=embed)

    @help.command()
    async def theme(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$theme`
                                Sets a theme.
                                Use `$theme` to see your current theme and use `$theme <new theme>` to change your theme.'''

        await ctx.send(embed=embed)

    @help.command()
    async def vote(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''`$vote`
                                Gifts you 5 rating points after voting for Chess Bot on top.gg
                                Note: `$vote` will only give you rating points if you have voted within the last 12 hours. If not, then vote and then use the command again.'''

        await ctx.send(embed=embed)
