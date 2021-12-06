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

    if isinstance(game, data.Game):
        bot = game.bot
    else:
        bot = game.to_move()

    if bot in all_cb:
        file_in = os.path.join(constants.TEMP_DIR, f'input-{person}.txt')
        file_out = os.path.join(constants.TEMP_DIR, f'output-{person}.txt')

        f = open(file_in, 'w')
        time_control = [969, 1264, 3696, 9696, 20000]
        max_depth = [3, 5, 7, 13, 69]
        mcts_probs = [1000000000, 200000000, 100000000, 100000000, 30000000]
        mcts_depth = [10, 10, 5, 4, 2]
        f.write(
            f'setoption time_limit {time_control[bot]}\n'
            f'setoption depth_limit {max_depth[bot]}\n'
            f'setoption mcts_prob {mcts_probs[bot]}\n'
            f'setoption mcts_max_depth {mcts_depth[bot]}\n'
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
    elif bot in all_sf:
        transport, engine = await chess.engine.popen_uci("./stockfish")
        board = chess.Board(game.fen)
        skill = [1, 4, 8, 20]
        times = [0.2, 0.5, 1, 2]
        result = await engine.play(board, chess.engine.Limit(time=times[bot - Profile.sf1.value]), options={"Skill Level": skill[bot - Profile.sf1.value]})
        await engine.quit()
        if result.resigned:
            return 'RESIGN', game
        else:
            if result.move is None:
                return None, None
            san = board.san_and_push(result.move)
            game.fen = board.fen(en_passant='fen')
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

