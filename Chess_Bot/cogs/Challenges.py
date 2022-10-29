import discord
from discord import app_commands
from discord.ext import commands

import random
from typing import Union
import asyncio
import json

import Chess_Bot.util.Data as data
from Chess_Bot.util.CPP_IO import *
from Chess_Bot.cogs.Profiles import Profile, ProfileNames


class AcceptButton(discord.ui.Button):
    def __init__(self, client, challenger, challengee):
        super().__init__(label='Accept', style=discord.ButtonStyle.green)
        self.client = client
        self.challenger = challenger
        self.challengee = challengee

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.challengee:
            await interaction.response.send_message('You are not the challengee!', ephemeral=True)
            return

        view = discord.ui.View.from_message(interaction.message)
        for component in view.children:
            if issubclass(type(component), discord.ui.Button):
                component.disabled = True

        util2 = self.client.get_cog('Util')
        if await data.data_manager.get_game(self.challenger) is not None or await data.data_manager.get_game(self.challengee) is not None:
            await interaction.message.reply('Challenge failed. One of the people already has a game in progress.')
            return

        game = data.Game2()
        if random.randint(0, 1) == 0:
            game.white = self.challengee
            game.black = self.challenger
        else:
            game.white = self.challenger
            game.black = self.challengee
        await data.data_manager.change_game(game)
        file, embed, view = await util2.make_embed(game.white, title='Game started!', description=f'White: {await util2.get_name(game.white)}\nBlack: {await util2.get_name(game.black)}\nUse `$view` to view the game and use `$move` to make a move.\n')

        await interaction.message.reply(f'<@{game.white}> <@{game.black}>\nYour game has started!', file=file, embed=embed, view=view)

        await data.data_manager.change_settings(
            game.white, new_notif=interaction.message.channel.id)
        await data.data_manager.change_settings(
            game.black, new_notif=interaction.message.channel.id)

        await interaction.response.edit_message(view=view)


class DeclineButton(discord.ui.Button):
    def __init__(self, client, challenger, challengee):
        super().__init__(label='Decline', style=discord.ButtonStyle.red)
        self.client = client
        self.challenger = challenger
        self.challengee = challengee

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id not in [self.challengee, self.challenger]:
            await interaction.response.send_message('You are not the challengee or challenger!', ephemeral=True)
            return

        view = discord.ui.View.from_message(interaction.message)
        for component in view.children:
            if issubclass(type(component), discord.ui.Button):
                component.disabled = True

        await interaction.message.reply('Challenge declined / withdrawn.')
        await interaction.response.edit_message(view=view)


class ChallengeView(discord.ui.View):
    def __init__(self, client, challenger, challenged):
        super().__init__()
        self.add_item(AcceptButton(client, challenger, challenged))
        self.add_item(DeclineButton(client, challenger, challenged))


class Challenges(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.hybrid_group(invoke_without_command=True, name='challenge', description='Challenges a user or bot to a game of chess.')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def challenge(self, ctx):
        '''
        {
            "name": "challenge",
            "description": "Challenges somebody to a game of chess. Use </challenge bot:1005187298817736714> to challenge a bot, or </challenge user:1005187298817736714> to challenge another person.",
            "usage": "$challenge <bot/user> <person>",
            "examples": [
                "$challenge bot cb1",
                "$challenge bot sf3",
                "$challenge user <@person>"
            ],
            "cooldown": 3,
            "subcommands": [
                "bot",
                "user"
            ]
        }
        '''
        helpcog = self.client.get_cog('Help')
        docstr = self.client.get_command('challenge').help
        kwargs = json.loads(docstr)
        await ctx.send(embed=await helpcog.make_help_embed(**kwargs))

    @challenge.command(name='bot', description='Challenges a bot to a game of chess.')
    @app_commands.describe(bot='The bot you want to challenge.')
    async def bot(self, ctx, bot: str):
        '''
        {
            "name": "challenge bot",
            "description": "Challenges the bot to a game of chess.\\nUse `$profiles to see which bots you can challenge.\\nYour color is assigned randomly.",
            "usage": "$challenge bot <bot>",
            "examples": [
                "$challenge bot cb1",
                "$challenge bot sf3"
            ],
            "cooldown": 3
        }
        '''
        try:
            bot = Profile[bot]
        except KeyError:
            await ctx.send('That isn\'t a valid bot. Use </profile list:1005187298817736715> to see which bots you can challenge.')
            return

        person = ctx.author.id

        game = await data.data_manager.get_game(person)
        if game is not None:
            await ctx.send('You already have a game in progress')
            return

        game = data.Game2()
        color = random.randint(0, 1)
        if color == 0:
            game.white = bot.value
            game.black = person
        else:
            game.white = person
            game.black = bot.value
        await data.data_manager.change_game(game)
        util2 = self.client.get_cog('Util')
        file, embed, view = await util2.make_embed(ctx.author.id, title='Game started!',
                                             description=(f'White: {await util2.get_name(game.white)}\n'
                                                          f'Black: {await util2.get_name(game.black)}\n'
                                                          'Use </view:968575170958749698> to view the game and use </move:968575170958749704> to make a move.\n'))
        await ctx.send(f'Game started with {ProfileNames[bot.name].value}\nYou play the {whiteblack[color]} pieces.', file=file, embed=embed, view=view)
        await data.data_manager.change_settings(person, new_notif=ctx.channel.id)

    @challenge.command(aliases=['person'], name='user', description='Challenges another person to a game of chess.')
    @app_commands.describe(person='The person you want to challenge.')
    async def user(self, ctx, person: Union[discord.Member, discord.User]):
        """
        {
            "name": "challenge user",
            "description": "Challenges another user to a game of chess.\\\\nReact with a check mark to accept a challenge, and react with an X mark to decline\\\\nThe challenge will expire in 16 minutes.",
            "usage": "$challenge user <user>",
            "examples": [
                "$challenge user <@person>"
            ],
            "cooldown": 3,
            "aliases": [
                "person"
            ]
        }
        """
        if await data.data_manager.get_game(ctx.author.id) is not None:
            await ctx.send('You already have a game in progress.')
            return
        if await data.data_manager.get_game(person.id) is not None:
            await ctx.send(f'{person} already has a game in progress.')
            return
        if ctx.author.id == person.id:
            await ctx.send('You cannot challenge yourself.')
            return

        await ctx.send(f'{person.mention}, {ctx.author} has challenged you to a game of chess.\nNote: the challenge will time out if you wait too long to accept', view=ChallengeView(self.client, ctx.author.id, person.id))


async def setup(bot):
    await bot.add_cog(Challenges(bot))
