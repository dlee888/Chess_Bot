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

        if game is None:
            await ctx.send(f'{"You do" if person == ctx.author else f"{person} does"} not have a game in progress')
            return

        util2 = self.client.get_cog('Util')
        file, embed = util2.make_embed(person.id, title=f'{await util2.get_name(game.white)} vs {await util2.get_name(game.black)}',
                                       description=f'{await util2.get_name(game.to_move())} to move.')
        await ctx.send(file=file, embed=embed)

    @cog_ext.cog_slash(name='view', description='View a person\'s game.', options=[
        create_option(name='person', description='The person whose game you want to see.',
                      option_type=SlashCommandOptionType.USER, required=False),
        create_option(name='flip', description='Flip the board',
                      option_type=SlashCommandOptionType.BOOLEAN, required=False)
    ])
    async def _view(self, ctx: SlashContext, person: typing.Union[discord.User, discord.Member] = None, flip: bool = False):
        if person is None:
            person = ctx.author

        game = data.data_manager.get_game(person.id)

        if game is None:
            await ctx.send(f'{"You do" if person == ctx.author else f"{person} does"} not have a game in progress')
            return

        util2 = self.client.get_cog('Util')
        file, embed = util2.make_embed(person.id, title=f'{await util2.get_name(game.white)} vs {await util2.get_name(game.black)}',
                                       description=f'{await util2.get_name(game.to_move())} to move.', flip=flip)
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

        if game is None:
            await ctx.send(f'{"You do" if person == ctx.author else f"{person} does"} not have a game in progress')
            return

        await ctx.send(f'```{game.fen}```')

    @cog_ext.cog_slash(name='fen', description='Sends a game in fen format.', options=[
        create_option(name='person', description='The person whose game you want to see.',
                      option_type=SlashCommandOptionType.USER, required=False)
    ])
    async def _fen(self, ctx: SlashContext, person: typing.Union[discord.User, discord.Member] = None):
        await self.fen(ctx, person)

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
        if new_theme is None:
            cur_theme = data.data_manager.get_theme(ctx.author.id)
            await ctx.send(f'Your current theme is "{cur_theme}"\n'
                           f'Use `$theme <new theme>` to change your theme.\n'
                           'Available themes are:\n'
                           f'`{"`, `".join(image.themes_available)}`')
            return

        if new_theme not in image.themes_available:
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
    async def _theme(self, ctx: SlashContext, new_theme=None):
        await self.theme(ctx, new_theme)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def notif(self, ctx, type='view'):
        '''
        {
            "name": "notif",
            "description": "Sets the channel for your notifications.",
            "usage": "$notif",
            "examples": [
                "$notif"
            ],
            "cooldown": 3
        }
        '''
        util2 = self.client.get_cog('Util')
        if type == 'view':
            channel, is_default = await util2.get_notifchannel(ctx.author.id)
            if channel is None:
                await ctx.send('No notification channel found. Make sure to specify a channel using the `$notif set` command to receive messages whenever your opponent moves.')
            elif is_default:
                await ctx.send(f'Your notification channel is `{"DM channel" if isinstance(channel, discord.DMChannel) else channel.name}`.\nYou can change this using the `$notif set` command.')
            else:
                await ctx.send(f'Your notification channel is `{"DM channel" if isinstance(channel, discord.DMChannel) else channel.name}`.')
        elif type == 'set':
            data.data_manager.change_settings(
                ctx.author.id, new_notif=ctx.channel.id)
            await ctx.send(f'Notification channel set to `{ctx.channel.name if ctx.guild is not None else "DM channel"}`.')
        elif type == 'test':
            await ctx.send('You should recieve a test notification. If you do not, try changing your notification channel or changing your settings.')
            await util2.send_notif(ctx.author.id, 'This is a test notification.')
        else:
            await ctx.send('Please specify either `view`, `set`, or `test`.')

    @cog_ext.cog_slash(name='notif', description='Sets your default channel for recieving notifications.', options=[
        create_option(name='type', description='View your notification channel, Test a notification, or Set your default channel.',
                      option_type=SlashCommandOptionType.STRING, required=True, choices=['view', 'test', 'set'])
    ])
    async def _notif(self, ctx, type):
        await self.notif(ctx, type)


def setup(bot):
    bot.add_cog(Viewing(bot))
