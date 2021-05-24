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
        self.password = os.environ.get('DBL_PASSWORD')
        self.dbl_client = dbl.DBLClient(
            self.client, self.dbl_token, autopost=True, webhook_path='/dblwebhook', webhook_auth=self.password, webhook_port=5000)
        self.reset_votes.start()

    async def on_guild_post(self):
        print('Posted stats on top.gg')

    @commands.command()
    async def vote(self, ctx):
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
            rating = 1500
        rating += 5
        data.data_manager.change_rating(ctx.author.id, rating)
        data.data_manager.add_vote(ctx.author.id)

        await ctx.send('Thank you for voting for Chess Bot! You have been gifted 5 rating points.')
        
    @tasks.loop(seconds=3)
    async def reset_votes(self):
        votes = data.data_manager.get_claimed()
        for row in votes:
            status = await self.dbl_client.get_user_vote(row[0])
            if status == False:
                data.data_manager.remove_vote(row[0])

    @reset_votes.before_loop()
    async def wait_until_ready(self):
        await self.client.wait_until_ready()

    @commands.Cog.listener()
    async def on_dbl_vote(data):
        """An event that is called whenever someone votes for the bot on top.gg."""
        print(f"Received an upvote:\n{data}")

    @commands.Cog.listener()
    async def on_dbl_test(data):
        """An event that is called whenever someone tests the webhook system for your bot on top.gg."""
        print(f"Received a test upvote:\n{data}")