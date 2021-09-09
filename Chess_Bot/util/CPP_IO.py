import chess
import chess.engine
import os
import discord

import Chess_Bot.util.Data as data
import Chess_Bot.util.Utility as util
from Chess_Bot.util.Images import *
from Chess_Bot.cogs.Profiles import Profile, ProfileNames
from Chess_Bot import constants


whiteblack = ['black', 'white']


async def run_engine(person):
    game = data.data_manager.get_game(person)

    all_cb = [bot.value for bot in Profile if bot.name.startswith('cb')]
    all_sf = [bot.value for bot in Profile if bot.name.startswith('sf')]

    if game.bot in all_cb:
        file_in = os.path.join(constants.TEMP_DIR, f'input-{person}.txt')
        file_out = os.path.join(constants.TEMP_DIR, f'output-{person}.txt')

        game = data.data_manager.get_game(person)

        f = open(file_in, 'w')
        time_control = [969, 1264, 3696, 9696, 30000]
        max_depth = [3, 5, 7, 13, 69]
        mcts_probs = [1000000000, 200000000, 100000000, 100000000, 100000000]
        mcts_depth = [10, 10, 5, 4, 4]
        f.write(
            f'setoption time_limit {time_control[game.bot]}\n'
            f'setoption depth_limit {max_depth[game.bot]}\n'
            f'setoption mcts_prob {mcts_probs[game.bot]}\n'
            f'setoption mcts_max_depth {mcts_depth[game.bot]}\n'
            f'go {game.fen}\nquit')
        f.close()
        await util.run(f'./engine < {file_in} > {file_out}')

        f = open(file_out)
        out = f.readlines()
        f.close()
        move = None
        for i in range(len(out) - 1, 0, -1):
            if out[i].startswith('COMPUTER PLAYED'):
                move = out[i][16:].strip()
                break
        for i in range(len(out) - 1, 0, -1):
            if out[i].startswith('GAME: '):
                game.fen = out[i][6:].strip()
                break
        return move, game
    elif game.bot in all_sf:
        transport, engine = await chess.engine.popen_uci("./stockfish")
        board = chess.Board(game.fen)
        skill = [1, 4, 8, 20]
        times = [0.2, 0.5, 1, 2]
        result = await engine.play(board, chess.engine.Limit(time=times[game.bot - Profile.sf1.value]), options={"Skill Level": skill[game.bot - Profile.sf1.value]})
        await engine.quit()
        if result.resigned:
            return 'RESIGN', game
        else:
            san = board.san_and_push(result.move)
            game.fen = board.fen()
            return san, game
    # elif game.bot == Profile.cbnnue.value:
    #     file_in = os.path.join(constants.TEMP_DIR, f'input-{person}.txt')
    #     file_out = os.path.join(constants.TEMP_DIR, f'output-{person}.txt')

    #     game = data.data_manager.get_game(person)

    #     f = open(file_in, 'w')
    #     f.write(
    #         f'setoption time_limit 20000\nsetoption use_nnue 1\ngo {game.fen}\nquit')
    #     f.close()
    #     await util.run(f'./engine < {file_in} > {file_out}')

    #     f = open(file_out)
    #     out = f.readlines()
    #     f.close()
    #     move = None
    #     for i in range(len(out) - 1, 0, -1):
    #         if out[i].startswith('COMPUTER PLAYED'):
    #             move = out[i][16:].strip()
    #             break
    #     for i in range(len(out) - 1, 0, -1):
    #         if out[i].startswith('GAME: '):
    #             game.fen = out[i][6:].strip()
    #             break
    #     return move, game


async def output_move(ctx, person, move):
    game = data.data_manager.get_game(person)

    embed = discord.Embed(
        title=f'{ctx.author}\'s game against {ProfileNames[Profile(game.bot).name].value}', description=f'{whiteblack[game.color].capitalize()} to move.', color=0x5ef29c)
    embed.set_footer(
        text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

    if move is not None:
        embed.add_field(
            name=f'{ProfileNames[Profile(game.bot).name].value} moved', value=move)

    get_image(person)

    file = discord.File(
        os.path.join(constants.TEMP_DIR, f'image-{person}.png'), filename='board.png')
    embed.set_image(url=f'attachment://board.png')

    await ctx.message.reply(file=file, embed=embed)


async def log(person, client, ctx):
    game = data.data_manager.get_game(person)

    if Profile(game.bot).name.startswith('cb'):
        log_channel = client.get_channel(constants.LOG_CHANNEL_ID)
        get_image(person)
        await log_channel.send(f'Output for {ctx.author} (id = {ctx.author.id})\n'
                               f'Request: {ctx.message.content}',
                               files=[
                                   discord.File(
                                       os.path.join(constants.TEMP_DIR, f'input-{person}.txt')),
                                   discord.File(
                                       os.path.join(constants.TEMP_DIR, f'output-{person}.txt')),
                                   discord.File(os.path.join(constants.TEMP_DIR, f'image-{person}.png'))])
