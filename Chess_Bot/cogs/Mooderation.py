import discord
from discord.ext import commands
import typing

import Chess_Bot.util.Utility as util
import Chess_Bot.util.Data as data
from Chess_Bot import constants


class Mooderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def abort(self, ctx, user: typing.Union[discord.User, discord.Member]):
        '''
        Aborts a game
        '''

        if not await util.has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            # await ctx.send('You do not have permission to abort games')
            return

        if data.data_manager.get_game(user.id) == None:
            await ctx.send(f'{user} does not have a game in progress')
            return

        data.data_manager.delete_game(user.id, 69)
        if user.id in util.thonking:
            util.thonking.remove(user.id)

        await ctx.send('Game aborted')

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def prefix(self, ctx, *, new_prefix: str = None):
        '''
        {
            "name": "prefix",
            "description": "Sets the current server's custom prefix to [new prefix].\\nThis command requires admin permissions in the current server.\\nYou can also use just `$prefix` to see what the current prefix is.\\nNote: while the server prefix can be changed, Chess Bot will always respond to `@Chess Bot`. If you do not know what the prefix is, you can use `@Chess Bot prefix` to find out.\\nPrefixes are also case-sensitive and space-sensitive. For example, if you change the prefix to `chess`, for example, you will need to use `chessping`, to run the `ping` command.\\nTo make it so that you will be able to use `chess ping`, you must set the prefix to `chess `, with a space at the end.",
            "usage": "$prefix [new prefix]",
            "examples": [
                "$prefix",
                "$prefix chess"
            ],
            "cooldown": 3
        }
        '''
        if ctx.guild is None:
            await ctx.send('This command only works in servers!')
            return

        if new_prefix is None:
            await ctx.send(f'This server\'s prefix is "{data.data_manager.get_prefix(ctx.guild.id)}"')
            return

        if ctx.author.guild_permissions.administrator == False:
            await ctx.send(f'You do not have permission to change this server\'s custom prefix')
            return

        data.data_manager.change_prefix(ctx.guild.id, new_prefix)

        await ctx.send('Prefix successfully updated')

        bot = await ctx.guild.fetch_member(self.client.user.id)

        try:
            await bot.edit(nick=f'[{new_prefix}] - Chess Bot')
        except discord.Forbidden:
            await ctx.send(f'Changing nickname to "[{new_prefix}] - Chess Bot" failed. Missing permissions')

    @commands.command(hidden=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def gift(self, ctx, person: typing.Union[discord.User, discord.Member], amount: float):
        if not await util.has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            # await ctx.send('You do not have permission to gift rating')
            return

        if data.data_manager.get_rating(person.id) == None:
            data.data_manager.change_rating(
                person.id, constants.DEFAULT_RATING)

        data.data_manager.change_rating(
            person.id, data.data_manager.get_rating(person.id) + amount)

        await ctx.send(f'{amount} rating points gifted.')


def setup(bot):
    bot.add_cog(Mooderation(bot))
