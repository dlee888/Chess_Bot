import psycopg2
import time
import os
import sys
import sqlite3
import chess

sys.path.insert(1, '/home/apple/bots/Chess_Bot')
from Chess_Bot import constants

class Game:

    def __init__(self, row=[-1, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 0, 0, time.time(), False]):
        self.fen = row[1]
        self.color = row[3]
        self.last_moved = row[4]
        self.warned = row[5]
        self.bot = row[2]

    def __str__(self):
        return self.fen


class Game2:

    def __init__(self, row=['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', -1, -1, time.time(), False, None]) -> None:
        self.fen = row[0]
        self.white = row[1]
        self.black = row[2]
        self.last_moved = row[3]
        self.warned = row[4]
        if len(row) == 5 or row[5] is None:
            self.time_control = constants.MAX_TIME_PER_MOVE
        else:
            self.time_control = row[7]

    def __str__(self) -> str:
        return self.fen

    def turn(self):
        board = chess.Board(self.fen)
        return board.turn

    def to_move(self):
        board = chess.Board(self.fen)
        if board.turn == chess.WHITE:
            return self.white
        else:
            return self.black

    def not_to_move(self):
        board = chess.Board(self.fen)
        if board.turn == chess.WHITE:
            return self.black
        else:
            return self.white

    def get_color(self, person):
        if person == self.white:
            return chess.WHITE
        else:
            return chess.BLACK

    def get_person(self, color):
        if color == chess.WHITE:
            return self.white
        else:
            return self.black

    def time_left(self):
        return self.time_control - (time.time() - self.last_moved)

    def parse_move(self, move):
        board = chess.Board(self.fen)
        try:
            return board.push_san(move)
        except ValueError:
            try:
                return board.push_uci(move)
            except ValueError:
                return None


class Data:

    def __init__(self, url):
        if not '-beta' in sys.argv or '-use-real-db' in sys.argv:
            self.DATABASE_URL = url

            self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        else:
            self.DATABASE_URL = None
            self.conn = sqlite3.connect(os.path.join(
                constants.DB_DIR, 'database'))

        create_games_table = ('CREATE TABLE IF NOT EXISTS games ('
                              'id bigint NOT NULL PRIMARY KEY UNIQUE,'
                              'position text,'
                              'bot integer,'
                              'color integer,'
                              'last_moved real,'
                              'warned integer'
                              ');')
        create_games2_table = ('CREATE TABLE IF NOT EXISTS games2 ('
                               'position text,'
                               'white bigint,'
                               'black bigint,'
                               'lastmoved real,'
                               'warned integer,'
                               'time_control integer'
                               ');')
        create_user_table = ('CREATE TABLE IF NOT EXISTS users ('
                             'id bigint NOT NULL PRIMARY KEY UNIQUE,'
                             'rating real,'
                             'lost int,'
                             'won int,'
                             'drew int,'
                             'theme text,'
                             'notifchannel bigint'
                             ');')
        create_votes_table = ('CREATE TABLE IF NOT EXISTS votes ('
                              'id bigint NOT NULL PRIMARY KEY UNIQUE'
                              ');')
        create_prefix_table = ('CREATE TABLE IF NOT EXISTS prefixes ('
                               'id bigint NOT NULL PRIMARY KEY UNIQUE,'
                               'prefix text'
                               ');')

        cur = self.get_conn().cursor()
        cur.execute(create_games_table)
        cur.execute(create_games2_table)
        cur.execute(create_user_table)
        cur.execute(create_votes_table)
        cur.execute(create_prefix_table)

    def get_conn(self):
        if not '-beta' in sys.argv and self.conn.closed:
            print('Connection is closed. Restarting...')
            self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        return self.conn

    def execute(self, sql, params=()):
        cur = self.get_conn().cursor()
        cur.execute(sql, params)
        self.conn.commit()
        try:
            rows = cur.fetchall()
            return rows
        except Exception as e:
            return None

    def get_game(self, person):
        rows = self.execute(f'SELECT * FROM games WHERE id = {person};')

        if len(rows) == 0:
            rows = self.execute(f'SELECT * FROM games2;')
            for row in rows:
                g = Game2(row)
                if g.white == person or g.black == person:
                    return g
            return None
        return Game(rows[0])

    def get_games(self):
        cur = self.get_conn().cursor()
        cur.execute('SELECT * FROM games')
        rows = cur.fetchall()
        games = []
        for row in rows:
            games.append((row[0], Game(row)))

        cur.execute('SELECT * FROM games2')
        rows = cur.fetchall()
        for row in rows:
            games.append(Game2(row))
        return games

    def get_games2(self):
        cur = self.get_conn().cursor()
        cur.execute('SELECT * FROM games2')
        rows = cur.fetchall()
        games = []
        for row in rows:
            games.append(Game2(row))
        return games

    def change_game(self, person, new_game):
        cur = self.get_conn().cursor()

        if isinstance(new_game, Game):
            update_sql = f'''INSERT INTO games VALUES ({person}, '{new_game.fen}', {new_game.bot}, {new_game.color}, {new_game.last_moved}, {int(new_game.warned)});'''
            cur.execute(f'DELETE FROM games WHERE id = {person};')
            cur.execute(update_sql)
        elif isinstance(new_game, Game2):
            cur.execute(
                f'DELETE FROM games2 WHERE white = {new_game.white} and black = {new_game.black};')
            cur.execute('INSERT INTO games2 VALUES (%s, %s, %s, %s, %s)', (
                new_game.fen,
                new_game.white,
                new_game.black,
                new_game.last_moved,
                int(new_game.warned)
            ))

        self.conn.commit()

    def get_rating(self, person):
        rows = self.execute('SELECT * FROM users WHERE id = %s;', (person,))
        if len(rows) == 0:
            return None
        return rows[0][1]

    def get_ratings(self):
        rows = self.execute('SELECT * FROM users')
        ratings = {}
        for row in rows:
            if row[1] is not None:
                ratings[row[0]] = row[1]
        return ratings

    def change_rating(self, person, new_rating):
        if len(self.execute('SELECT * FROM users where id = %s', (person,))) == 0:
            self.execute('INSERT INTO users (id) VALUES (%s)', (person,))
        self.execute('UPDATE users SET rating = %s WHERE id = %s;',
                     (new_rating, person))

    def get_prefix(self, guild):
        cur = self.get_conn().cursor()
        cur.execute(f'SELECT * FROM prefixes WHERE id = {guild};')
        rows = cur.fetchall()

        if len(rows) == 0:
            return '$'
        return rows[0][1]

    def change_prefix(self, guild, new_prefix):
        cur = self.get_conn().cursor()
        cur.execute(f'DELETE FROM prefixes WHERE id = {guild};')
        cur.execute('INSERT INTO prefixes VALUES (%s, %s);',
                    (guild, new_prefix))

        self.conn.commit()

    def get_stats(self, person):
        rows = self.execute('SELECT * FROM users WHERE id = %s;', (person,))
        if len(rows) == 0:
            return 0, 0, 0
        return rows[0][2], rows[0][3], rows[0][4]

    def change_stats(self, person, lost, won, drew):
        if len(self.execute('SELECT * FROM users where id = %s', (person,))) == 0:
            self.execute('INSERT INTO users (id) VALUES (%s)', (person,))
        self.execute(
            'UPDATE users SET lost = %s, won = %s, drew = %s WHERE id = %s', (lost, won, drew, person))

    def total_games(self):
        rows = self.execute('SELECT * FROM users;')
        ans = 0
        for row in rows:
            ans += row[2] + row[3] + row[4]
        return ans // 2

    def delete_game(self, person, winner):
        cur = self.get_conn().cursor()
        game = self.get_game(person)
        if isinstance(game, Game):
            num_lost, num_won, num_draw = self.get_stats(person)
            bot_lost, bot_won, bot_draw = self.get_stats(game.bot)
            if winner is None:
                self.change_stats(person, num_lost, num_won, num_draw + 1)
                self.change_stats(game.bot, bot_lost, bot_won, bot_draw + 1)
            elif winner == 1:
                self.change_stats(person, num_lost, num_won + 1, num_draw)
                self.change_stats(game.bot, bot_lost + 1, bot_won, bot_draw)
            elif winner == 0:
                self.change_stats(person, num_lost + 1, num_won, num_draw)
                self.change_stats(game.bot, bot_lost, bot_won + 1, bot_draw)
            cur.execute(f'DELETE FROM games WHERE id = {person};')
        elif isinstance(game, Game2):
            white_lost, white_won, white_draw = self.get_stats(game.white)
            black_lost, black_won, black_draw = self.get_stats(game.black)
            if winner is not None:
                if winner == chess.WHITE:
                    white_won += 1
                    black_lost += 1
                elif winner == chess.BLACK:
                    black_won += 1
                    white_lost += 1
                else:
                    white_draw += 1
                    black_draw += 1
            self.change_stats(game.white, white_lost, white_won, white_draw)
            self.change_stats(game.black, black_lost, black_won, black_draw)
            cur.execute(
                f'DELETE FROM games2 WHERE white = {game.white} and black = {game.black};')

        self.conn.commit()

    def get_theme(self, person):
        rows = self.execute('SELECT * FROM users WHERE id = %s;', (person,))
        if len(rows) == 0:
            return 'default'
        return rows[0][5]

    def get_notifchannel(self, person):
        rows = self.execute('SELECT * FROM users WHERE id = %s;', (person,))
        if len(rows) == 0 or rows[0][6] == -1:
            return None
        return rows[0][6]

    def change_settings(self, person, *, new_theme=None, new_notif=None):
        if len(self.execute('SELECT * FROM users where id = %s', (person,))) == 0:
            self.execute('INSERT INTO users (id) VALUES (%s)', (person,))
        if new_theme is not None:
            self.execute(
                'UPDATE users SET theme = %s WHERE id = %s', (new_theme, person))
        if new_notif is not None:
            self.execute(
                'UPDATE users SET notifchannel = %s WHERE id = %s', (new_notif, person))

    def change_theme(self, person, new_theme):
        self.change_settings(person, new_theme=new_theme)

    def has_claimed(self, person):
        cur = self.get_conn().cursor()
        cur.execute(f'SELECT * FROM votes WHERE id = {person}')
        rows = cur.fetchall()

        return len(rows) == 1

    def get_claimed(self):
        cur = self.get_conn().cursor()
        cur.execute(f'SELECT * FROM votes')
        rows = cur.fetchall()
        return rows

    def add_vote(self, person):
        cur = self.get_conn().cursor()
        cur.execute(f'DELETE FROM votes WHERE id = {person}')
        cur.execute(f'INSERT INTO votes VALUES ({person})')
        self.conn.commit()

    def remove_vote(self, person):
        cur = self.get_conn().cursor()
        cur.execute(f'DELETE FROM votes WHERE id = {person}')
        self.conn.commit()


data_manager = Data(os.getenv('NEW_DB_URL'))
