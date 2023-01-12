import discord
from discord import app_commands
from discord.ext import commands


import typing

import Chess_Bot.util.Data as data
import Chess_Bot.util.Images as image
from Chess_Bot.util.CPP_IO import *


class Viewing(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name='view', description="Views [person]'s game. If no person is specified, it will default to your own game.")
    @app_commands.describe(person='The person to view the game of.', flip='Whether to flip the board or not.')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def view(self, ctx, person: typing.Optional[typing.Union[discord.User, discord.Member]] = None, flip: bool = False):
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

        game = await data.data_manager.get_game(person.id)

        if game is None:
            await ctx.send(f'{"You do" if person == ctx.author else f"{person} does"} not have a game in progress')
            return

        util2 = self.client.get_cog('Util')
        file, embed, view = await util2.make_embed(person.id, title=f'{await util2.get_name(game.white)} vs {await util2.get_name(game.black)}',
                                       description=f'{await util2.get_name(game.to_move())} to move.', flip=flip)
        if ctx.author.id in [game.white, game.black]:
            await ctx.send(file=file, embed=embed, view=view)
        else:
            await ctx.send(file=file, embed=embed)

    @commands.hybrid_command(name='fen', description='Views the FEN of the game.')
    @app_commands.describe(person='The person to view the FEN of. If no person is specified, it will default to your own game.')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def fen(self, ctx, person: typing.Optional[typing.Union[discord.User, discord.Member]] = None):
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

        game = await data.data_manager.get_game(person.id)

        if game is None:
            await ctx.send(f'{"You do" if person == ctx.author else f"{person} does"} not have a game in progress')
            return

        await ctx.send(f'```{game.fen}```')

    @commands.hybrid_command(name='theme', description='Changes the theme of the board.')
    @app_commands.describe(new_theme='The new theme to set. If left blank, you will see your current theme')
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
            cur_theme = await data.data_manager.get_theme(ctx.author.id)
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

        await data.data_manager.change_theme(ctx.author.id, new_theme)
        await ctx.send('Theme sucessfully updated')

    @commands.hybrid_command(name='notif', description='Changes the notification settings for your game.')
    @app_commands.describe(type='Set, test, or view the channel used for notifications.')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def notif(self, ctx, type):
        """
        {
            "name": "notif",
            "description": "Sets the channel for your notifications.",
            "usage": "$notif",
            "examples": [
                "$notif"
            ],
            "cooldown": 3
        }
        """
        util2 = self.client.get_cog('Util')
        if type == 'set':
            await data.data_manager.change_settings(
                ctx.author.id, new_notif=ctx.channel.id)
            await ctx.send(f'Notification channel set to `{ctx.channel.name if ctx.guild is not None else "DM channel"}`.')
        elif type == 'test':
            await ctx.send('You should recieve a test notification. If you do not, try changing your notification channel or changing your settings.')
            await util2.send_notif(ctx.author.id, 'This is a test notification.')
        elif type == 'view':
            channel, is_default = await util2.get_notifchannel(ctx.author.id)
            if channel is None:
                await ctx.send('No notification channel found. Make sure to set a channel using the </notif:968575170547712044> `set` command to receive messages whenever your opponent moves.')
            elif is_default:
                await ctx.send(f'Your notification channel is `{"DM channel" if isinstance(channel, discord.DMChannel) else channel.name}`.\nYou can change this using the </notif:968575170547712044> `set` command.')
            else:
                await ctx.send(f'Your notification channel is `{"DM channel" if isinstance(channel, discord.DMChannel) else channel.name}`.')
        else:
            await ctx.send('Please specify either `view`, `set`, or `test`.')


async def setup(bot):
    await bot.add_cog(Viewing(bot))
