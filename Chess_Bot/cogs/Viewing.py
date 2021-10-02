import discord
from discord.ext import commands

from discord_slash import SlashContext
from discord_slash import cog_ext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option

import typing

import Chess_Bot.util.Utility as util
import Chess_Bot.util.Data as data
import Chess_Bot.util.Images as image
from Chess_Bot.util.CPP_IO import *


class Viewing(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def view(self, ctx, person: typing.Union[discord.User, discord.Member] = None):
        '''
        {
            "name": "view",
            "description": "Views [person]'s game. If no person is specified, it will default to your own game.",
            "usage": "$view [person]",
            "examples": [
                "$view",
                "$view @person"
            ],
            "cooldown": 5
        }
        '''

        if person is None:
            person = ctx.author

        game = data.data_manager.get_game(person.id)

        if game == None:
            await ctx.send(f'{person} does not have a game in progress')
            return
        if isinstance(game, data.Game):
            get_image(person.id)
            embed = discord.Embed(
                title=f'{ctx.author}\'s game against {ProfileNames[Profile(game.bot).name].value}', description=f'{whiteblack[game.color].capitalize()} to move.', color=0x5ef29c)
            if person.id in util.thonking:
                embed.description = f'{ProfileNames[Profile(game.bot).name].value} is thinking...'
            embed.set_footer(
                text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            file = discord.File(
                os.path.join(constants.TEMP_DIR, f'image-{person.id}.png'), filename='board.png')
            embed.set_image(url=f'attachment://board.png')
            await ctx.message.reply(embed=embed, file=file)
        elif isinstance(game, data.Game2):
            util2 = self.client.get_cog('Util')
            file, embed = util2.make_embed(person.id, title=f'Your game with {await util2.get_name(game.white if game.black == person.id else game.black)}', description=f'{await util2.get_name(game.to_move())} to move.')
            await ctx.send(file=file, embed=embed)

    @cog_ext.cog_slash(name='view', description='View a person\'s game.', options=[
        create_option(name='person', description='The person whose game you want to see.',
                      option_type=SlashCommandOptionType.USER, required=False)
    ])
    async def _view(self, ctx: SlashContext, person: typing.Union[discord.User, discord.Member] = None):
        if person is None:
            person = ctx.author

        game = data.data_manager.get_game(person.id)

        if game == None:
            await ctx.send(f'{person} does not have a game in progress')
            return
        if isinstance(game, data.Game):
            get_image(person.id)
            embed = discord.Embed(
                title=f'{ctx.author}\'s game against {ProfileNames[Profile(game.bot).name].value}', description=f'{whiteblack[game.color].capitalize()} to move.', color=0x5ef29c)
            if person.id in util.thonking:
                embed.description = f'{ProfileNames[Profile(game.bot).name].value} is thinking...'
            embed.set_footer(
                text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            file = discord.File(
                os.path.join(constants.TEMP_DIR, f'image-{person.id}.png'), filename='board.png')
            embed.set_image(url=f'attachment://board.png')
            await ctx.message.reply(embed=embed, file=file)
        elif isinstance(game, data.Game2):
            util2 = self.client.get_cog('Util')
            file, embed = util2.make_embed(person.id, title=f'Your game with {await util2.get_name(game.white if game.black == person.id else game.black)}', description=f'{await util2.get_name(game.to_move())} to move.')
            await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def fen(self, ctx, person: typing.Union[discord.User, discord.Member] = None):
        '''
        {
            "name": "fen",
            "description": "Sends [person]'s game if [FEN format](https://www.chess.com/terms/fen-chess).\\nIf no person is specified, it will default to your own game.",
            "usage": "$fen [person]",
            "examples": [
                "$fen",
                "$fen @person"
            ],
            "cooldown": 3
        }
        '''

        if person is None:
            person = ctx.author

        game = data.data_manager.get_game(person.id)

        if game == None:
            await ctx.send(f'{person} does not have a game in progress')
            return

        await ctx.send(f'```{game.fen}```')

    @cog_ext.cog_slash(name='fen', description='Sends a game in fen format.', options=[
        create_option(name='person', description='The person whose game you want to see.',
                      option_type=SlashCommandOptionType.USER, required=False)
    ])
    async def _fen(self, ctx: SlashContext, person: typing.Union[discord.User, discord.Member] = None):
        if person is None:
            person = ctx.author

        game = data.data_manager.get_game(person.id)

        if game == None:
            await ctx.send(f'{person} does not have a game in progress')
            return

        await ctx.send(f'```{game.fen}```')

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def theme(self, ctx, new_theme=None):
        '''
        {
            "name": "theme",
            "description": "Customize your board theme.\\nYou can also use `$theme` without a new theme specified to see your current theme and a list of all available themes.",
            "usage": "$theme [new theme]",
            "examples": [
                "$theme",
                "$theme orange"
            ],
            "cooldown": 3
        }
        '''
        if new_theme == None:
            cur_theme = data.data_manager.get_theme(ctx.author.id)
            await ctx.send(f'Your current theme is "{cur_theme}"\n'
                           f'Use `$theme <new theme>` to change your theme.\n'
                           'Available themes are:\n'
                           f'`{"`, `".join(image.themes_available)}`')
            return

        if not new_theme in image.themes_available:
            await ctx.send(f'That theme is not available.\n'
                           'Available themes are:\n'
                           f'`{"`, `".join(image.themes_available)}`')
            return

        data.data_manager.change_theme(ctx.author.id, new_theme)
        await ctx.send('Theme sucessfully updated')

    @cog_ext.cog_slash(name='theme', description='Customize your board theme.', options=[
        create_option(name='new_theme', description='The new theme, if you want to change your theme.',
                      option_type=SlashCommandOptionType.STRING, required=False)
    ])
    async def _fen(self, ctx: SlashContext, new_theme=None):
        if new_theme == None:
            cur_theme = data.data_manager.get_theme(ctx.author.id)
            await ctx.send(f'Your current theme is `{cur_theme}`\n'
                           f'Use `/theme <new theme>` to change your theme.\n'
                           'Available themes are:\n'
                           f'`{"`, `".join(image.themes_available)}`')
            return

        if not new_theme in image.themes_available:
            await ctx.send(f'That theme is not available.\n'
                           'Available themes are:\n'
                           f'`{"`, `".join(image.themes_available)}`')
            return

        data.data_manager.change_theme(ctx.author.id, new_theme)
        await ctx.send('Theme sucessfully updated')


def setup(bot):
    bot.add_cog(Viewing(bot))
