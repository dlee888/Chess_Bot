import topgg
import discord
from discord.ext import commands, tasks

import os
import logging

import Chess_Bot.util.Data as data
from Chess_Bot import constants


class Topgg(commands.Cog):

    def __init__(self, client, dbl_client):
        self.client = client
        self.dbl_client = dbl_client
        if self.dbl_client is not None:
            self.reset_votes.start()

    async def on_guild_post(self):
        logging.info('Posted stats on top.gg')

    @commands.hybrid_command(name='vote', description='Vote for Chess Bot on top.gg to get 5 free rating points.')
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
        try:
            voted = await self.dbl_client.get_user_vote(ctx.author.id)
        except Exception:
            await ctx.send('An error occurred. Most likely top.gg is down.')
            return

        if not voted:
            await ctx.send('You have not voted!\nPlease vote for Chess Bot at https://top.gg/bot/801501916810838066/vote')
            return

        if await data.data_manager.has_claimed(ctx.author.id):
            await ctx.send('You have already claimed your rating points. Vote again to claim more.')
            return

        rating = await data.data_manager.get_rating(ctx.author.id)
        if rating is None:
            rating = constants.DEFAULT_RATING
        rating += 5
        await data.data_manager.change_rating(ctx.author.id, rating)
        await data.data_manager.add_vote(ctx.author.id)

        await ctx.send('Thank you for voting for Chess Bot! You have been gifted 5 rating points.')

    @tasks.loop(seconds=3)
    async def reset_votes(self):
        votes = await data.data_manager.get_claimed()
        for row in votes:
            status = await self.dbl_client.get_user_vote(row)
            if status == False:
                await data.data_manager.remove_vote(row)

    @reset_votes.before_loop
    async def wait_until_ready(self):
        await self.client.wait_until_ready()


async def setup(bot):
    dbl_token = os.environ.get('DBL_TOKEN')
    if dbl_token is not None:
        dbl_client = topgg.DBLClient(
            bot, dbl_token, autopost=True, post_shard_count=True)
    else:
        dbl_client = None
    await bot.add_cog(Topgg(bot, dbl_client))
