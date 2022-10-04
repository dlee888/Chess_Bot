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
        embed.description = ('Note: Please use slash commands instead of normal commands.\n'
                             'As some of you may know, discord has made message content a privileged intent, which stops normal commands from working.'
                             'If you still want to use the normal message commands, you have to DM the bot, or mention it as a prefix, such as <@801501916810838066> help.')
        return embed

    async def get_command(self, name):
        command_list = await self.client.tree.fetch_commands()
        for command in command_list:
            if command.name == name:
                return command

    async def make_help_embed(self, *, name, description, usage, examples=None, cooldown=None, aliases=None, subcommands=None):
        embed = self.get_default_help_embed()
        command = await self.get_command(name)
        embed.title += f' for command {command.mention}'
        # if aliases is not None:
        #     embed.add_field(name='Aliases', value=', '.join(
        #         [f'`{i}`' for i in aliases]))
        if subcommands is not None:
            embed.add_field(name='Subcommands:', value='\n'.join(
                [f'`{name} {i}`' for i in subcommands]))
        embed.add_field(name="Usage:", value=usage, inline=False)
        embed.add_field(name="Description:", value=description, inline=False)
        if examples is not None:
            embed.add_field(name="Examples:", value='\n'.join(
                examples), inline=False)
        if cooldown is not None:
            embed.add_field(name="Cooldown:", value=f'{cooldown} seconds')
        return embed

    @commands.hybrid_command(name='help', description='Lists all commands')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def help(self, ctx, *, command=None):
        '''
        {
            "name": "help",
            "description": "Sends a list of all commands.\\nUse `/help [command]` to get more information about a specific command.",
            "usage": "$help [command]",
            "examples": [
                "$help",
                "$help move"
            ],
            "cooldown": 3
        }
        '''
        if command is None:
            command_list = await self.client.tree.fetch_commands()
            command_dict = {}
            for command in command_list:
                command_dict[command.name] = command
            help_list = {'Playing': ['challenge', 'move', 'profile', 'resign'], 'Viewing': [
                'view', 'fen', 'time', 'theme'], 'Rating': ['rating', 'leaderboard', 'rank', 'stats'], 'Miscellaneous': ['ping', 'help', 'botinfo', 'invite', 'vote', 'notif']}
            embed = self.get_default_help_embed()
            embed.description = 'List of commands. Use `/help [command]` for more information about a certain command'

            for category, commands in help_list.items():
                embed.add_field(name=category, value=', '.join(
                    [command_dict[i].mention for i in commands]), inline=False)
        else:
            cmd = self.client.get_command(command)
            if cmd is None or cmd.hidden or not cmd.enabled:
                await ctx.send('That command doesn\'t exist!')
                return
            kwargs = json.loads(cmd.help.replace(f'${command}', (await self.get_command(command)).mention))
            embed = await self.make_help_embed(**kwargs)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
