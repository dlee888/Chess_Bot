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
        
    @commands.command()
    async def votes(self, ctx):
        
        if not await util.has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send(f'You do not have permission to see votes')
            return
        
        voted = await self.dbl_client.get_bot_upvotes()
        print(voted)
        await ctx.send(str(voted))