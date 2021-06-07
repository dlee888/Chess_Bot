from Chess_Bot import constants
import discord
from discord.ext import commands

import enum

import Chess_Bot.util.Data as data
from Chess_Bot import constants


class Profile(enum.Enum):
    cb1 = 0
    cb2 = 1
    cb3 = 2


class ProfileNames(enum.Enum):
    cb1 = 'Chess Bot level 1'
    cb2 = 'Chess Bot level 2'
    cb3 = 'Chess Bot level 3'


class Profiles(commands.Cog):

    def __init__(self, client) -> None:
        super().__init__()
        self.client = client

    async def get_default_embed(self, thumbnail=constants.AVATAR_URL):
        embed = discord.Embed(title='Profiles', color=0xe3a617)

        owner = (await self.client.application_info()).owner
        embed.set_footer(text=f"Made by {owner}", icon_url=owner.avatar_url)
        embed.set_thumbnail(url=thumbnail)

        return embed

    @commands.group(invoke_without_command=True, aliases=['profiles', 'levels'])
    async def profile(self, ctx):
        embed = await self.get_default_embed()
        embed.description = 'These are the Chess Bot computers that you can challenge.\nUse `$profile <bot tag>` for more information on a bot. For example, `$profile cb1`.'
        embed.add_field(
            name='Chess Bot', value='`cb1 (Chess Bot level 1)`, `cb2 (Chess Bot level 2)`, `cb3 (Chess Bot level 3)`')
        await ctx.send(embed=embed)

    @profile.command()
    async def cb1(self, ctx):
        embed = await self.get_default_embed()
        embed.add_field(name='Chess Bot level 1',
                        value='Level 1 of the Chess Bot engine.')
        embed.add_field(name='Tag', value='`cb1`')
        embed.add_field(
            name='Stats', value='Stats about this bot.', inline=False)
        embed.add_field(name='Rating', value=str(
            round(data.data_manager.get_rating(0), 3)))
        lost, won, drew = data.data_manager.get_stats(0)
        embed.add_field(name='Games played', value=str(
            lost + won + drew), inline=False)
        embed.add_field(name='Games lost', value=str(lost)).add_field(
            name='Games won', value=str(won)).add_field(name='Games drawn', value=str(drew))
        await ctx.send(embed=embed)

    @profile.command()
    async def cb2(self, ctx):
        embed = await self.get_default_embed()
        embed.add_field(name='Chess Bot level 2',
                        value='Level 2 of the Chess Bot engine.')
        embed.add_field(name='Tag', value='`cb2`')
        embed.add_field(
            name='Stats', value='Stats about this bot.', inline=False)
        embed.add_field(name='Rating', value=str(
            round(data.data_manager.get_rating(1), 3)), inline=False)
        lost, won, drew = data.data_manager.get_stats(1)
        embed.add_field(name='Games played', value=str(
            lost + won + drew), inline=False)
        embed.add_field(name='Games lost', value=str(lost)).add_field(
            name='Games won', value=str(won)).add_field(name='Games drawn', value=str(drew))
        await ctx.send(embed=embed)

    @profile.command()
    async def cb3(self, ctx):
        embed = await self.get_default_embed()
        embed.add_field(name='Chess Bot level 3',
                        value='Level 3 of the Chess Bot engine.')
        embed.add_field(name='Tag', value='`cb3`')
        embed.add_field(
            name='Stats', value='Stats about this bot.', inline=False)
        embed.add_field(name='Rating', value=str(
            round(data.data_manager.get_rating(2), 3)), inline=False)
        lost, won, drew = data.data_manager.get_stats(2)
        embed.add_field(name='Games played', value=str(
            lost + won + drew), inline=False)
        embed.add_field(name='Games lost', value=str(lost)).add_field(
            name='Games won', value=str(won)).add_field(name='Games drawn', value=str(drew))
        await ctx.send(embed=embed)
