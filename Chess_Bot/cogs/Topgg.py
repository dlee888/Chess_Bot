import dbl
import discord
from discord.ext import commands, tasks

import os

import Chess_Bot.cogs.Utility as util

class Topgg(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.dbl_token = os.environ.get('DBL_TOKEN')
        self.dbl_client = dbl.DBLClient(self.client, self.dbl_token, autopost=True)
        
    async def on_guild_post(self):
        print('Posted stats on top.gg')
        
    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        print('Vote recieved!')
        print(data)
        
        gg_channel = self.client.get_channel(819639514758643754)
        await gg_channel.send(f'data = {str(data)}')
        await gg_channel.send(f'Vote from {data.user} found!\nThank you for voting! You have recieved a gift of 10 rating points.')
        
        util.get_rating(data.user.id)
        util.ratings[data.user.id] += 10
        
    @commands.command()
    async def votes(self, ctx):
        
        if not await util.has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to see votes')
            return
        
        voted = await self.dbl_client.get_bot_upvotes()
        print(voted)
        await ctx.send(str(voted))