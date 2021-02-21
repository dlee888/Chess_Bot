import discord
from discord.ext import commands

class Help(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    
    async def get_default_help_embed(self):
        embed = discord.Embed(title='Help', color=0x02b022)
        
        owner = (await self.client.application_info()).owner
        embed.set_footer(text=f"Made by {owner}", icon_url=owner.avatar_url)
        embed.set_thumbnail(url='https://i.imgur.com/n1jak68.png')
        
        return embed
    
        
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = 'List of commands. Type "$help [command]" for more information about a certain command'
        
        embed.add_field(name='Playing', value='`challenge`, `move`, `resign`, `view`, `fen`', inline=False)
        embed.add_field(name='Rating', value='`rating`, `leaderboard`', inline=False)
        embed.add_field(name='Other', value='`ping`, `help`, `botinfo`, `invite`, `git_history`')
        
        await ctx.send(embed=embed)
    
    @help.command()
    async def challenge(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description='''`$challenge <flags>`
                              Challenges Chess bot to a game. Color is assigned randomly.
                              Flags:
                              `-t` to set the time control (in seconds). 
                              For example, `$challenge -t 5` to indicate that you want the computer to think for about 5 seconds'''
                              
        await ctx.send(embed=embed)
        
    @help.command(aliases=['play'])
    async def move(self, ctx):
        embed = await self.get_default_help_embed()
        embed.description = '''$move <move> / $play <move>
Plays <move> against the computer
Please enter the move in algebraic notation
For example, `$move Ke2`
More about algebraic notation in [this chess.com article](https://www.chess.com/article/view/chess-notation#algebraic-notation)'''

        await ctx.send(embed=embed)