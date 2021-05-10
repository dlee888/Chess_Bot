import dbl
import discord
from discord.ext import commands, tasks

import os

import Chess_Bot.cogs.Utility as util
import Chess_Bot.cogs.Data as data


class Topgg(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.dbl_token = os.environ.get('DBL_TOKEN')
        self.dbl_client = dbl.DBLClient(
            self.client, self.dbl_token, autopost=True)

    async def on_guild_post(self):
        print('Posted stats on top.gg')

    @commands.command()
    async def votes(self, ctx):

        if not await util.has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to see votes')
            return

        voted = await self.dbl_client.get_bot_upvotes()
        print(voted)
        await ctx.send(str(voted))

    @commands.command()
    @commands.cooldown(1, 12 * 3600, commands.BucketType.default)
    async def vote(self, ctx):
        voted = await self.dbl_client.get_user_vote(ctx.author.id)

        if not voted:
            await ctx.send('You have not voted!\nPlease vote for Chess Bot at https://top.gg/bot/801501916810838066/vote')
            ctx.command.reset_cooldown(ctx)
            return

        rating = data.data_manager.get_rating(ctx.author.id)
        if rating == None:
            rating = 1500

        rating += 5
        data.data_manager.change_rating(ctx.author.id, rating)

        await ctx.send('Thank you for voting for Chess Bot! You have been gifted 5 rating points.')
