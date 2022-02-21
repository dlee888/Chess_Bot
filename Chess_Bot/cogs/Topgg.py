import dbl
import discord
from discord.ext import commands, tasks

from discord_slash import SlashContext
from discord_slash import cog_ext

import os
import logging

import Chess_Bot.util.Data as data
from Chess_Bot import constants


class Topgg(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.dbl_token = os.environ.get('DBL_TOKEN')
        if self.dbl_token is not None:
            self.dbl_client = dbl.DBLClient(
                self.client, self.dbl_token, autopost=True)
            self.reset_votes.start()
        else:
            self.dbl_client = None

    async def on_guild_post(self):
        logging.info('Posted stats on top.gg')

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def vote(self, ctx):
        '''
        {
            "name": "vote",
            "description": "Claims 5 free rating points for voting for Chess bot on [top.gg](https://top.gg/bot/801501916810838066)",
            "usage": "$vote",
            "examples": [
                "$vote"
            ],
            "cooldown": 3
        }
        '''
        if self.dbl_client is None:
            return

        voted = await self.dbl_client.get_user_vote(ctx.author.id)

        if not voted:
            await ctx.send('You have not voted!\nPlease vote for Chess Bot at https://top.gg/bot/801501916810838066/vote')
            return

        claimed = data.data_manager.has_claimed(ctx.author.id)
        if claimed:
            await ctx.send('You have already claimed your rating points. Vote again to claim more.')
            return

        rating = data.data_manager.get_rating(ctx.author.id)
        if rating == None:
            rating = constants.DEFAULT_RATING
        rating += 5
        data.data_manager.change_rating(ctx.author.id, rating)
        data.data_manager.add_vote(ctx.author.id)

        await ctx.send('Thank you for voting for Chess Bot! You have been gifted 5 rating points.')

    @cog_ext.cog_slash(name='vote', description='Claim 5 free rating points for voting for Chess Bot on top.gg')
    async def _vote(self, ctx: SlashContext):
        voted = await self.dbl_client.get_user_vote(ctx.author.id)

        if not voted:
            await ctx.send('You have not voted!\nPlease vote for Chess Bot at https://top.gg/bot/801501916810838066/vote')
            return

        claimed = data.data_manager.has_claimed(ctx.author.id)
        if claimed:
            await ctx.send('You have already claimed your rating points. Vote again to claim more.')
            return

        rating = data.data_manager.get_rating(ctx.author.id)
        if rating == None:
            rating = constants.DEFAULT_RATING
        rating += 5
        data.data_manager.change_rating(ctx.author.id, rating)
        data.data_manager.add_vote(ctx.author.id)

        await ctx.send('Thank you for voting for Chess Bot! You have been gifted 5 rating points.')

    @tasks.loop(seconds=3)
    async def reset_votes(self):
        votes = data.data_manager.get_claimed()
        for row in votes:
            status = await self.dbl_client.get_user_vote(row)
            if status == False:
                data.data_manager.remove_vote(row)

    @reset_votes.before_loop
    async def wait_until_ready(self):
        await self.client.wait_until_ready()


def setup(bot):
    bot.add_cog(Topgg(bot))
