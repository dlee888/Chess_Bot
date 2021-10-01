import discord
from discord.ext import commands

from discord_slash import SlashContext
from discord_slash import cog_ext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option

import enum

import Chess_Bot.util.Data as data
from Chess_Bot import constants


class Profile(enum.Enum):
    cb1 = 0
    cb2 = 1
    cb3 = 2
    cb4 = 3
    cb5 = 4
    sf1 = 5
    sf2 = 6
    sf3 = 7
    sfmax = 8


class ProfileNames(enum.Enum):
    cb1 = 'Chess Bot level 1'
    cb2 = 'Chess Bot level 2'
    cb3 = 'Chess Bot level 3'
    cb4 = 'Chess Bot level 4'
    cb5 = 'Chess Bot level 5'
    sf1 = 'Stockfish level 1'
    sf2 = 'Stockfish level 2'
    sf3 = 'Stockfish level 3'
    sfmax = 'Stockfish max strength'


def get_name(bot_id : int):
    return ProfileNames[Profile(bot_id).name].value
def get_description(bot_name : str):
    descriptions = {
        'cb1': 'Level 1 of the Chess Bot engine',
        'cb2': 'Level 2 of the Chess Bot engine',
        'cb3': 'Level 3 of the Chess Bot engine',
        'cb4': 'Level 4 of the Chess Bot engine',
        'cb5': 'Level 5 of the Chess Bot engine',
        'sf1': 'Stockfish with the UCI option `Skill level` set to 1.',
        'sf2': 'Stockfish with the UCI option `Skill level` set to 4.',
        'sf3': 'Stockfish with the UCI option `Skill level` set to 8.',
        'sfmax': 'Stockfish with the UCI option `Skill level` set to 20 (the maximum possible).',
    }
    return descriptions[bot_name]

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
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def profile(self, ctx):
        '''
        {
            "name": "profile",
            "description": "Shows a list of the Chess Bot computers that you can challenge.",
            "aliases": [
                "profiles",
                "levels"
            ],
            "usage": "$profile",
            "examples": [
                "$profiles",
                "$profile view cb1"
            ],
            "cooldown": 3,
            "subcommands": [
                "view"
            ]
        }
        '''
        embed = await self.get_default_embed()
        embed.description = ('These are the Chess Bot computers that you can challenge.\n'
        'Use the command `$profile view <bot tag>` for more information on a bot.\n'
        'For example, `$profile view cb1` to get info about Chess Bot level 1.')
        all_cb = [
            f'`{bot.name}` ({get_name(bot.value)})' for bot in Profile if bot.name.startswith('cb')]
        all_sf = [
            f'`{bot.name}` ({get_name(bot.value)})' for bot in Profile if bot.name.startswith('sf')]
        embed.add_field(
            name='Chess Bot', value='\n'.join(all_cb))
        embed.add_field(
            name='Stockfish', value='\n'.join(all_sf))
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name='profiles', description="Shows a list of the Chess Bot computers that you can challenge.")
    async def _profiles(self, ctx: SlashContext):
        embed = await self.get_default_embed()
        embed.description = ('These are the Chess Bot computers that you can challenge.\n'
        'Use the command `$profile view <bot tag>` for more information on a bot.\n'
        'For example, `$profile view cb1` to get info about Chess Bot level 1.')
        all_cb = [
            f'`{bot.name}` ({get_name(bot.value)})' for bot in Profile if bot.name.startswith('cb')]
        all_sf = [
            f'`{bot.name}` ({get_name(bot.value)})' for bot in Profile if bot.name.startswith('sf')]
        embed.add_field(
            name='Chess Bot', value='\n'.join(all_cb))
        embed.add_field(
            name='Stockfish', value='\n'.join(all_sf))
        await ctx.send(embed=embed)

    @profile.command(aliases=['info'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def view(self, ctx, tag):
        '''
        {
            "name": "profile view",
            "description": "Views information about a specific Chess Bot profile that you can challenge.",
            "aliases": [
                "profile info"
            ],
            "usage": "$profile view <tag>",
            "examples": [
                "$profile view cb1"
            ],
            "cooldown": 3
        }
        '''
        try:
            bot = Profile[tag]
        except KeyError:
            await ctx.send('That isn\'t a valid bot. Use `$profiles` to see which bots you can challenge.')
            return

        embed = await self.get_default_embed()
        if bot.name.startswith('sf'):
            embed.set_thumbnail(url='https://stockfishchess.org/images/logo/icon_512x512@2x.png')
        
        embed.add_field(name=get_name(bot.value),
                        value=get_description(bot.name))
        embed.add_field(name='Tag', value=f'`{bot.name}`')

        id = bot.value
        embed.add_field(
            name='Stats', value='Stats about this bot.', inline=False)
        embed.add_field(name='Rating', value=str(
            round(data.data_manager.get_rating(id), 3)), inline=False)

        lost, won, drew = data.data_manager.get_stats(id)
        embed.add_field(name='Games played', value=str(
            lost + won + drew), inline=False)
        embed.add_field(name='Games lost', value=str(lost)).add_field(
            name='Games won', value=str(won)).add_field(name='Games drawn', value=str(drew))
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name='profile view', description="Views information about a specific Chess Bot profile that you can challenge.", option=[
        create_option(name='tag', description='The tag of the bot. For example, `cb1`.', option_type=SlashCommandOptionType.STRING, required=True)
    ])
    async def _view(self, ctx: SlashContext, tag):
        try:
            bot = Profile[tag]
        except KeyError:
            await ctx.send('That isn\'t a valid bot. Use `$profiles` to see which bots you can challenge.')
            return

        embed = await self.get_default_embed()
        if bot.name.startswith('sf'):
            embed.set_thumbnail(url='https://stockfishchess.org/images/logo/icon_512x512@2x.png')
        
        embed.add_field(name=get_name(bot.value),
                        value=get_description(bot.name))
        embed.add_field(name='Tag', value=f'`{bot.name}`')

        id = bot.value
        embed.add_field(
            name='Stats', value='Stats about this bot.', inline=False)
        embed.add_field(name='Rating', value=str(
            round(data.data_manager.get_rating(id), 3)), inline=False)

        lost, won, drew = data.data_manager.get_stats(id)
        embed.add_field(name='Games played', value=str(
            lost + won + drew), inline=False)
        embed.add_field(name='Games lost', value=str(lost)).add_field(
            name='Games won', value=str(won)).add_field(name='Games drawn', value=str(drew))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Profiles(bot))
