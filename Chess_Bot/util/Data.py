import psycopg2
import time
import os
import sys
import sqlite3
import chess

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

    def __init__(self, row=['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', -1, -1, time.time(), time.time(), False, False]) -> None:
        self.fen = row[0]
        self.white = row[1]
        self.black = row[2]
        self.white_last_moved = row[3]
        self.black_last_moved = row[4]
        self.white_warned = row[5]
        self.black_warned = row[6]

    def __str__(self) -> str:
        return self.fen

    def turn(self):
        board = chess.Board(self.fen)
        if board.turn == chess.WHITE:
            return self.white
        else:
            return self.black

    def get_color(self, person):
        if person == self.white:
            return chess.WHITE
        else:
            return chess.BLACK

    def time_left(self, person):
        if person == self.white:
            return constants.MAX_TIME_PER_MOVE - (time.time() - self.white_last_moved)
        else:
            return constants.MAX_TIME_PER_MOVE - (time.time() - self.black_last_moved)


class Data:

    def __init__(self, url):
        if not '-beta' in sys.argv:
            self.DATABASE_URL = url

            self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        else:
            self.DATABASE_URL = None
            self.conn = sqlite3.connect(os.path.join(
                constants.DATA_DIR, 'db', 'database'))

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
                               'white_lastmoved real,'
                               'black_lastmoved real,'
                               'white_warned integer,'
                               'black_warned integer'
                               ');')
        create_ratings_table = ('CREATE TABLE IF NOT EXISTS ratings ('
                                'id bigint NOT NULL PRIMARY KEY UNIQUE,'
                                'rating real'
                                ');')
        create_prefix_table = ('CREATE TABLE IF NOT EXISTS prefixes ('
                               'id bigint NOT NULL PRIMARY KEY UNIQUE,'
                               'prefix text'
                               ');')
        create_settings_table = ('CREATE TABLE IF NOT EXISTS settings ('
                                 'id bigint NOT NULL PRIMARY KEY UNIQUE,'
                                 'theme text,'
                                 'notifchannel bigint'
                                 ');')
        create_votes_table = ('CREATE TABLE IF NOT EXISTS votes ('
                              'id bigint NOT NULL PRIMARY KEY UNIQUE'
                              ');')
        create_stats_table = ('CREATE TABLE IF NOT EXISTS stats ('
                              'id bigint NOT NULL PRIMARY KEY UNIQUE,'
                              'lost int,'
                              'won int,'
                              'drew int'
                              ');')

        cur = self.get_conn().cursor()
        cur.execute(create_games_table)
        cur.execute(create_games2_table)
        cur.execute(create_ratings_table)
        cur.execute(create_prefix_table)
        cur.execute(create_settings_table)
        cur.execute(create_votes_table)
        cur.execute(create_stats_table)

    def get_conn(self):
        if not '-beta' in sys.argv and self.conn.closed:
            print('Connection is closed. Restarting...')
            self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        return self.conn

    def get_game(self, person):
        cur = self.get_conn().cursor()
        cur.execute(f'SELECT * FROM games WHERE id = {person};')
        rows = cur.fetchall()

        if len(rows) == 0:
            cur.execute(f'SELECT * FROM games2;')
            rows = cur.fetchall()
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
        games = {}
        for row in rows:
            games[row[0]] = Game(row)

        cur = self.get_conn().cursor()
        cur.execute('SELECT * FROM games2')
        rows = cur.fetchall()
        for row in rows:
            g = Game2(row)
            games[g.white] = g
            games[g.black] = g
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
            cur.execute('INSERT INTO games2 VALUES (?, ?, ?, ?, ?, ?, ?)', (
                new_game.fen,
                new_game.white,
                new_game.black,
                new_game.white_last_moved,
                new_game.black_last_moved,
                new_game.white_warned,
                new_game.black_warned
            ))

        self.conn.commit()

    def get_rating(self, person):
        cur = self.get_conn().cursor()
        cur.execute(f'SELECT * FROM ratings WHERE id = {person};')
        rows = cur.fetchall()

        if len(rows) == 0:
            return None
        return rows[0][1]

    def get_ratings(self):
        cur = self.get_conn().cursor()
        cur.execute(f'SELECT * FROM ratings;')
        rows = cur.fetchall()

        ratings = {}
        for row in rows:
            ratings[row[0]] = row[1]

        return ratings

    def change_rating(self, person, new_rating):
        cur = self.get_conn().cursor()

        cur.execute(f'DELETE FROM ratings WHERE id = {person};')
        cur.execute(f'INSERT INTO ratings VALUES ({person}, {new_rating});')

        self.conn.commit()

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
        cur.execute(
            f'INSERT INTO prefixes VALUES ({guild}, \'{new_prefix}\');')

        self.conn.commit()

    def get_stats(self, person):
        cur = self.get_conn().cursor()
        cur.execute(f'SELECT * FROM stats WHERE id = {person};')
        rows = cur.fetchall()
        if len(rows) == 0:
            return 0, 0, 0
        return rows[0][1], rows[0][2], rows[0][3]

    def change_stats(self, person, lost, won, drew):
        cur = self.get_conn().cursor()
        cur.execute(f'DELETE FROM stats WHERE id = {person};')
        cur.execute(
            f'INSERT INTO stats VALUES ({person}, {lost}, {won}, {drew});')
        self.conn.commit()

    def total_games(self):
        cur = self.get_conn().cursor()
        cur.execute(f'SELECT * FROM stats;')
        rows = cur.fetchall()
        ans = 0
        for row in rows:
            ans += row[1] + row[2] + row[3]
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
        cur = self.get_conn().cursor()
        try:
            cur.execute(f'SELECT * FROM themes WHERE id = {person};')
            rows = cur.fetchall()
        except sqlite3.OperationalError:
            rows = []

        if len(rows) == 0:
            cur.execute(f'SELECT * FROM settings WHERE id = {person}')
            rows = cur.fetchall()
            if len(rows) == 0:
                return 'default'
            return rows[0][1]
        return rows[0][1]

    def get_notifchannel(self, person):
        cur = self.get_conn().cursor()
        cur.execute(f'SELECT * FROM settings WHERE id = {person}')
        rows = cur.fetchall()
        if len(rows) == 0:
            return None
        return rows[0][2]

    def change_settings(self, person, *, new_theme=None, new_notif=None):
        cur = self.get_conn().cursor()
        cur.execute(f'SELECT * FROM settings WHERE id = {person}')
        rows = cur.fetchall()
        if len(rows) == 0:
            row = ['default', -1]
        else:
            row = rows[0]
        if new_theme is not None:
            row[0] = new_theme
        if new_notif is not None:
            row[1] = new_notif
        cur.execute(f'DELETE FROM settings WHERE id = {person}')
        cur.execute('INSERT INTO settings VALUES (?, ?, ?)',
                    (person, row[0], row[1]))
        self.conn.commit()

    def change_theme(self, person, new_theme):
        cur = self.get_conn().cursor()
        cur.execute(f'DELETE FROM themes WHERE id = {person};')
        self.conn.commit()
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


data_manager = Data(os.getenv('DATABASE_URL'))
