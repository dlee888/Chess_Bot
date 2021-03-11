import dbl
import discord
from discord.ext import commands, tasks

import os

class Topgg(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.dbl_token = os.environ.get('BOT_TOKEN')
        self.dbl_client = dbl.DBLClient(self.client, self.dbl_token, autopost=True)
        
    async def on_guild_post(self):
        print('Posted stats on top.gg')
        
    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        print(data)
        
    @commands.command()
    async def votes(self, ctx):
        voted = await self.dbl_client.get_bot_upvotes()
        print(voted)
        await ctx.send(str(voted))