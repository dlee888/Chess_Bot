import discord
from discord.ext import commands
import typing

import Chess_Bot.util.Utility as util
import Chess_Bot.util.Data as data
from Chess_Bot import constants
from Chess_Bot.cogs.Development import is_developer


class Mooderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @is_developer()
    async def abort(self, ctx, user: typing.Union[discord.User, discord.Member]):
        '''
        Aborts a game
        '''

        if data.data_manager.get_game(user.id) is None:
            await ctx.send(f'{user} does not have a game in progress')
            return

        data.data_manager.delete_game(user.id, None)

        await ctx.send('Game aborted')

    @commands.hybrid_command(name='prefix', description='Set a custom prefix for your server.')
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
            await ctx.send((f'This server\'s prefix is `{data.data_manager.get_prefix(ctx.guild.id)}`\nNote:\nPlease use slash commands instead of normal commands.\n'
                            'As some of you may know, discord has made message content a privileged intent, which means that bots cannot access the contents of messages you send. This stops the normal commands from working. Instead, users are expected to interact with bots using slash commands.\n'
                            'If you still want to use the normal message commands, there are ways, though. You can still use commands by DMing the bot, or mentioning the bot instead of using a prefix, such as <@801501916810838066> help.\n'))
            return

        # Disabled due to disabling guild intents
        # if ctx.author.guild_permissions.administrator == False:
        #     await ctx.send("You do not have permission to change this server\'s custom prefix")
        #     return

        data.data_manager.change_prefix(ctx.guild.id, new_prefix)

        await ctx.send('Prefix successfully updated')

        bot = await ctx.guild.fetch_member(self.client.user.id)

        try:
            await bot.edit(nick=f'[{new_prefix}] - Chess Bot')
        except Exception:
            pass

    @commands.command(hidden=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @is_developer()
    async def gift(self, ctx, person: typing.Union[discord.User, discord.Member], amount: float):
        if data.data_manager.get_rating(person.id) is None:
            data.data_manager.change_rating(
                person.id, constants.DEFAULT_RATING)

        data.data_manager.change_rating(
            person.id, data.data_manager.get_rating(person.id) + amount)

        await ctx.send(f'{amount} rating points gifted.')


async def setup(bot):
    await bot.add_cog(Mooderation(bot))
