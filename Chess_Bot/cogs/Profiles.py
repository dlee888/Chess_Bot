import discord
from discord.ext import commands


import enum


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

    async def get_default_embed(self):
        embed = discord.Embed(title='Profiles', color=0xe3a617)

        owner = (await self.client.application_info()).owner
        embed.set_footer(text=f"Made by {owner}", icon_url=owner.avatar_url)
        embed.set_thumbnail(url='https://i.imgur.com/n1jak68.png')

        return embed

    @commands.group(invoke_without_command=True, alias=['profiles', 'levels'])
    async def profile(self, ctx):
        embed = await self.get_default_embed()
        embed.description = 'These are the Chess Bot computers that you can challenge.\nUse `$profile <bot tag> for more information on a bot. For example, `$profile cb1`.'
        embed.add_field(
            name='Chess Bot', value='`cb1 (Chess Bot level 1)`, `cb2 (Chess Bot level 2)`, `cb3 (Chess Bot level 3)`')
        await ctx.send(embed=embed)

    @profile.command()
    async def cb1(self, ctx):
        embed = await self.get_default_embed()
        embed.add_field(name='Chess Bot level 1',
                        value='Level 1 of the Chess Bot engine.')
        embed.add_field(name='Tag', value='cb1')
        await ctx.send(embed=embed)

    @profile.command()
    async def cb2(self, ctx):
        embed = await self.get_default_embed()
        embed.add_field(name='Chess Bot level 2',
                        value='Level 2 of the Chess Bot engine.')
        embed.add_field(name='Tag', value='cb2')
        await ctx.send(embed=embed)

    @profile.command()
    async def cb3(self, ctx):
        embed = await self.get_default_embed()
        embed.add_field(name='Chess Bot level 3s',
                        value='Level 3 of the Chess Bot engine.')
        embed.add_field(name='Tag', value='cb3')
        await ctx.send(embed=embed)
