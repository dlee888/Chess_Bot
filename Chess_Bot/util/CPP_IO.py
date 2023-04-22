import chess
import chess.engine

import Chess_Bot.util.Data as data
import Chess_Bot.util.Utility as util
from Chess_Bot.util.Images import *
from Chess_Bot.cogs.Profiles import Profile


whiteblack = ['black', 'white']

# Chess Bot levels
time_control = [969, 1264, 3696, 9696, 20000]
max_depth = [3, 5, 7, 15, 69]
mcts_probs = [1000000000, 200000000, 10000000, 100000, 0]
mcts_depth = [10, 10, 5, 4, 2]
# Stockfish levels
skill = [0, 3, 8, 20]
times = [0.2, 0.5, 2, 5]

all_cb = [bot.value for bot in Profile if bot.name.startswith('cb')]
all_sf = [bot.value for bot in Profile if bot.name.startswith('sf')]


async def run_engine(person):
    game = await data.data_manager.get_game(person)
    if game is None:
        return None

    bot = game.to_move()

    if bot in all_cb:
        stdin = (f'setoption time_limit {time_control[bot]}\n'
                 f'setoption depth_limit {max_depth[bot]}\n'
                 f'setoption mcts_prob {mcts_probs[bot]}\n'
                 f'setoption mcts_max_depth {mcts_depth[bot]}\n'
                 'setoption table_size 666667\n'
                 f'go {game.fen}\nquit')
        out, _, _ = await util.run('./engine', stdin=stdin)
        out = out.split('\n')
        if 'COMPUTER PLAYED' not in out:
            logging.error(f'Chess Bot {bot} failed to play a move. Output:\n{out}')
        return next((line[16:].strip() for line in out if line.startswith('COMPUTER PLAYED')), None)
    elif bot in all_sf:
        transport, engine = await chess.engine.popen_uci("./stockfish")
        board = chess.Board(game.fen)
        result = await engine.play(board, chess.engine.Limit(time=times[bot - Profile.sf1.value]), options={"Skill Level": skill[bot - Profile.sf1.value]})
        await engine.quit()
        return 'RESIGN' if result.resigned else str(result.move)
