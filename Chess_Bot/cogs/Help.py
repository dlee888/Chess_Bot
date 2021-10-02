import discord
from discord.ext import commands

import json

from Chess_Bot import constants


class Help(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    def get_default_help_embed(self):
        embed = discord.Embed(title='Help', color=0x02b022)

        embed.set_footer(
            text="Usage syntax: <required argument>, [optional argument]")
        embed.set_thumbnail(url=constants.AVATAR_URL)

        return embed

    def make_help_embed(self, *, name, description, usage, examples=None, cooldown=None, aliases=None, subcommands=None):
        embed = self.get_default_help_embed()
        embed.title += f' for command "${name}"'
        if aliases is not None:
            embed.add_field(name='Aliases', value=', '.join([f'`{i}`' for i in aliases]))
        if subcommands is not None:
            embed.add_field(name='Subcommands:', value='\n'.join([f'`{name} {i}`' for i in subcommands]))
        embed.add_field(name="Usage:", value=f'`{usage}`', inline=False)
        embed.add_field(name="Description:", value=description, inline=False)
        if examples is not None:
            embed.add_field(name="Examples:", value='\n'.join([f'`{i}`' for i in examples]), inline=False)
        if cooldown is not None:
            embed.add_field(name="Cooldown:", value=f'{cooldown} seconds')
        return embed

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def help(self, ctx, *, command=None):
        '''
        {
            "name": "help",
            "description": "Sends a list of all commands.\\nUse `$help [command]` to get more information about a specific command.",
            "usage": "$help [command]",
            "examples": [
                "$help",
                "$help move"
            ],
            "cooldown": 3
        }
        '''
        if command is None:
            embed = self.get_default_help_embed()
            embed.description = 'List of commands. Type `$help [command]` for more information about a certain command'

            embed.add_field(
                name='Playing', value='`challenge`, `move`, `profiles`, `resign`', inline=False)
            embed.add_field(
                name='Viewing', value= '`view`, `fen`, `time`, `theme`', inline=False)
            embed.add_field(
                name='Rating', value='`rating`, `leaderboard`, `rank`, `stats`', inline=False)
            embed.add_field(
                name='Other', value='`ping`, `help`, `botinfo`, `invite`, `prefix`, `vote`, `notif`')

            await ctx.send(embed=embed)
        else:
            cmd = self.client.get_command(command)
            if cmd is None or cmd.hidden or not cmd.enabled:
                await ctx.send('That command doesn\'t exist!')
                return

            kwargs = json.loads(cmd.help)
            embed = self.make_help_embed(**kwargs)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
