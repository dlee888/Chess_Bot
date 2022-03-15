import chess
import chess.pgn
import asyncio
from Chess_Bot.util.Utility import run

engine1 = input('Engine playing white: ')
engine2 = input('Engine playing black: ')
time_control = int(input('Time: '))


async def main():
    board = chess.Board()
    while not board.is_game_over(claim_draw=True):
        print(board)
        print(board.fen(en_passant='fen'))
        with open('input.txt', 'w') as f:
            f.write(
                f'setoption time_limit {time_control}\n'
                f'go {board.fen(en_passant="fen")}\nquit')
        out = None
        if board.turn == chess.WHITE:
            out, _, _ = await run(f'./{engine1} < input.txt')
        else:
            out, _, _ = await run(f'./{engine2} < input.txt')
        out = out.split('\n')
        move = None
        for i in range(len(out) - 1, 0, -1):
            if out[i].startswith('COMPUTER PLAYED'):
                move = out[i][16:].strip()
                break
        if move == 'RESIGN':
            break
        try:
            board.push_san(move)
        except ValueError:
            board.push_uci(move)
    png = chess.pgn.Game()
    for move in list(board.move_stack):
        png = png.add_variation(move)
    print(png)

asyncio.run(main())