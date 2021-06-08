import discord
from discord.ext import commands
import typing
import chess

import Chess_Bot.util.Utility as util
import Chess_Bot.util.Data as data
import Chess_Bot.util.Images as image
from Chess_Bot.util.CPP_IO import *


class Viewing(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def view(self, ctx, person: typing.Union[discord.User, discord.Member] = None):
        '''
        Views your current game
        '''
        
        if person is None:
            person = ctx.author

        game = data.data_manager.get_game(person.id)

        if game == None:
            await ctx.send(f'{person} does not have a game in progress')
            return
        
        get_image(person.id)
        embed = discord.Embed(
            title=f'{ctx.author}\'s game against {ProfileNames[Profile(game.bot).name].value}', description=f'{whiteblack[game.color].capitalize()} to move.', color=0x5ef29c)
        if person.id in util.thonking:
            embed.description = f'{ProfileNames[Profile(game.bot).name].value} is thinking...'
        embed.set_footer(
            text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        file = discord.File(
                os.path.join(constants.TEMP_DIR, f'image-{person}.png'), filename='board.png')
        embed.set_image(url=f'attachment://board.png')
        await ctx.message.reply(embed=embed, file=file)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def fen(self, ctx, person: typing.Union[discord.User, discord.Member] = None):
        '''
        Sends current game in FEN format
        '''

        if person is None:
	        person = ctx.author

        game = data.data_manager.get_game(person.id)

        if game == None:
            await ctx.send(f'{person} does not have a game in progress')
            return

        await ctx.send(f'```{game.fen}```')

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def theme(self, ctx, new_theme=None):
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


def setup(bot):
    bot.add_cog(Viewing(bot))
