import discord
from discord.ext import commands

import chess
import random
import sys
import contextlib

from Chess_Bot import constants
from Chess_Bot.cogs.Profiles import Profile, get_name
import Chess_Bot.util.Data as data
from Chess_Bot.util import Images
from Chess_Bot.util import Utility as util


class DrawButton(discord.ui.Button):
    def __init__(self, client, game):
        super().__init__(label='Offer draw',
                         style=discord.ButtonStyle.grey, emoji='🤝', custom_id='draw')
        self.client = client
        self.game = game

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id not in [self.game.white, self.game.black]:
            await interaction.response.send_message('This is not your game!', ephemeral=True)
            return

        game = await data.data_manager.get_game(interaction.user.id)
        if game is None:
            await interaction.response.send_message('Game not found.', ephemeral=True)
            return

        view = discord.ui.View.from_message(interaction.message)
        for component in view.children:
            if component.custom_id == 'draw':
                component.disabled = True
        await interaction.message.edit(view=view)

        util2 = self.client.get_cog('Util')
        if interaction.user.id == self.game.white:
            if game.white_draw:
                await interaction.response.send_message('You already offered a draw.', ephemeral=True)
                return
            game.white_draw = True
            await interaction.response.send_message('Draw offer sent.', ephemeral=True)
            await util2.send_notif(game.black, 'Your opponent has offered a draw')
        else:
            if game.black_draw:
                await interaction.response.send_message('You already offered a draw.', ephemeral=True)
                return
            game.black_draw = True
            await interaction.response.send_message('Draw offer sent.', ephemeral=True)
            await util2.send_notif(game.white, 'Your opponent has offered a draw')
        await data.data_manager.change_game(game)


class AcceptDrawButton(discord.ui.Button):
    def __init__(self, client, game):
        super().__init__(label='Accept draw offer',
                         style=discord.ButtonStyle.primary, emoji='🤝')
        self.client = client
        self.game = game

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id not in [self.game.white, self.game.black]:
            await interaction.response.send_message('This is not your game!', ephemeral=True)
            return

        game = await data.data_manager.get_game(interaction.user.id)
        if game is None:
            await interaction.response.send_message('Game not found.', ephemeral=True)
            return

        view = discord.ui.View.from_message(interaction.message)
        for component in view.children:
            if issubclass(type(component), discord.ui.Button):
                component.disabled = True
        await interaction.response.edit_message(view=view)

        util2 = self.client.get_cog('Util')
        white_delta, black_delta = await util.update_rating2(
            self.game.white, self.game.black, 1 / 2)
        if interaction.user.id == self.game.white:
            await interaction.message.reply(f'Draw accepted. Your new rating is {round(await data.data_manager.get_rating(interaction.user.id), 3)} ({round(white_delta, 3)})')
            file, embed, _ = await util2.make_embed(
                self.game.black, title='Your game has ended', description=f'{interaction.user} accepted your draw offer.\nYour new rating is {round(await data.data_manager.get_rating(self.game.black), 3)} ({round(black_delta, 3)})')
            await util2.send_notif(self.game.black, file=file, embed=embed)
        else:
            await interaction.message.reply(f'Draw accepted. Your new rating is {round(await data.data_manager.get_rating(interaction.user.id), 3)} ({round(black_delta, 3)})')
            file, embed, _ = await util2.make_embed(
                self.game.white, title='Your game has ended', description=f'{interaction.user} accepted your draw offer.\nYour new rating is {round(await data.data_manager.get_rating(self.game.white), 3)} ({round(white_delta, 3)})')
            await util2.send_notif(self.game.white, file=file, embed=embed)
        await data.data_manager.delete_game(
            interaction.user.id, 69)


class ResignButton(discord.ui.Button):
    def __init__(self, client, game):
        super().__init__(label='Resign', style=discord.ButtonStyle.grey, emoji='🏳️')
        self.client = client
        self.game = game

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id not in [self.game.white, self.game.black]:
            await interaction.response.send_message('This is not your game!', ephemeral=True)
            return

        game = await data.data_manager.get_game(interaction.user.id)
        if game is None:
            await interaction.response.send_message('Game not found.', ephemeral=True)
            return

        view = discord.ui.View.from_message(interaction.message)
        for component in view.children:
            if issubclass(type(component), discord.ui.Button):
                component.disabled = True
        await interaction.response.edit_message(view=view)

        util2 = self.client.get_cog('Util')
        white_delta, black_delta = await util.update_rating2(self.game.white, self.game.black,
                                                       0 if interaction.user.id == self.game.black else 1)
        if interaction.user.id == self.game.white:
            await interaction.message.reply(f'Game resigned. Your new rating is {round(await data.data_manager.get_rating(interaction.user.id), 3)} ({round(white_delta, 3)})')
            file, embed, _ = await util2.make_embed(
                self.game.black, title='Your game has ended', description=f'It was in this position that {interaction.user} resigned the game.\nYour new rating is {round(await data.data_manager.get_rating(self.game.black), 3)} ({round(black_delta, 3)})')
            await util2.send_notif(self.game.black, file=file, embed=embed)
        else:
            await interaction.message.reply(f'Game resigned. Your new rating is {round(await data.data_manager.get_rating(interaction.user.id), 3)} ({round(black_delta, 3)})')
            file, embed, _ = await util2.make_embed(
                self.game.white, title='Your game has ended', description=f'It was in this position that {interaction.user} resigned the game.\nYour new rating is {round(await data.data_manager.get_rating(self.game.white), 3)} ({round(white_delta, 3)})')
            await util2.send_notif(self.game.white, file=file, embed=embed)
        await data.data_manager.delete_game(
            interaction.user.id, chess.WHITE if interaction.user.id == self.game.black else chess.BLACK)


class GameView(discord.ui.View):
    def __init__(self, client, game):
        super().__init__()
        self.add_item(DrawButton(client, game))
        self.add_item(ResignButton(client, game))


class GameViewDraw(discord.ui.View):
    def __init__(self, client, game):
        super().__init__()
        self.add_item(AcceptDrawButton(client, game))
        self.add_item(ResignButton(client, game))


class Util(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def get_notifchannel(self, person):
        if person < len(Profile):
            return None, None
        channelid = await data.data_manager.get_notifchannel(person)
        if channelid is not None:
            try:
                return await self.client.fetch_channel(channelid), False
            except Exception:
                return None, None
        else:
            user = await self.client.fetch_user(person)
            channel = user.dm_channel
            if channel is not None:
                return channel, True
            try:
                return await user.create_dm(), True
            except Exception:
                return None, None

    async def get_name(self, person):
        if person < len(Profile):
            return get_name(person)
        return str(await self.client.fetch_user(person))

    async def make_embed(self, person, *, title='', description='', flip=False):
        embed = discord.Embed(color=0x5ef29c, title=title,
                              description=description)
        game = await data.data_manager.get_game(person)
        path = await Images.get_image2(person, game.get_color(person) ^ flip)
        embed.set_image(url='attachment://board.png')
        if person not in [game.white, game.black]:
            return discord.File(path, filename='board.png'), embed, None
        elif game.turn() == chess.WHITE:
            embed.set_footer(text='White to move')
            if game.black_draw and person == game.white:
                embed.set_footer(
                    text='White to move. Black has offered a draw')
                return discord.File(path, filename='board.png'), embed, GameViewDraw(self.client, game)
            else:
                return discord.File(path, filename='board.png'), embed, GameView(self.client, game)
        else:
            embed.set_footer(text='Black to move')
            if game.white_draw and person == game.black:
                embed.set_footer(
                    text='Black to move. White has offered a draw')
                return discord.File(path, filename='board.png'), embed, GameViewDraw(self.client, game)
            else:
                return discord.File(path, filename='board.png'), embed, GameView(self.client, game)

    async def send_notif(self, person, text='', **kwargs):
        if '-beta' in sys.argv and person not in constants.DEVELOPERS:
            return
        channel, is_default = await self.get_notifchannel(person)
        if channel is not None:
            text = f'<@{person}> {text}'
            if is_default and random.randint(1, 3) == 1:
                text = 'Tip: change your default notification channel by using the `$notif set` command!.\n' + text
            with contextlib.suppress(Exception):
                await channel.send(text, **kwargs)


async def setup(bot):
    await bot.add_cog(Util(bot))
