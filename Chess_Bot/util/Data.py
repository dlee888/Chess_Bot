import psycopg2
import time
import os
import sys
import sqlite3
import chess
from pymongo import MongoClient

from Chess_Bot import constants


class Game2:

    def __init__(self, row=['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', -1, -1, time.time(), False, None]) -> None:
        self.fen = row[0]
        self.white = row[1]
        self.black = row[2]
        self.last_moved = row[3]
        self.warned = row[4]
        if len(row) == 5 or row[5] is None:
            self.time_control = constants.DEFAULT_TIME_CONTROL
        else:
            self.time_control = row[5]

    def __str__(self) -> str:
        return self.fen

    def to_dict(self):
        return {'white': self.white, 'black': self.black, 'fen': self.fen, 'time_control': self.time_control, 'last_moved': self.last_moved, 'warned': self.warned}

    def load_dict(self, dict):
        self.white = dict['white']
        self.black = dict['black']
        self.last_moved = dict['last_moved']
        self.warned = dict['warned']
        self.time_control = dict['time_control']
        self.fen = dict['fen']
        return self

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
        self.DATABASE_URL = url

        self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')

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
        rows = self.execute(
            'SELECT * FROM games2 where white = %s or black = %s;', (person, person))
        if len(rows) == 0:
            return None
        return Game2(rows[0])

    def get_games(self):
        games = []
        rows = self.execute('SELECT * FROM games2')
        for row in rows:
            games.append(Game2(row))
        return games

    def change_game(self, new_game):
        cur = self.get_conn().cursor()
        cur.execute(
            f'DELETE FROM games2 WHERE white = {new_game.white} and black = {new_game.black};')
        cur.execute('INSERT INTO games2 VALUES (%s, %s, %s, %s, %s, %s)', (
            new_game.fen,
            new_game.white,
            new_game.black,
            new_game.last_moved,
            int(new_game.warned),
            new_game.time_control
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
        if len(rows) == 0 or rows[0][2] is None:
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
            if row[2] is not None and row[3] is not None and row[4] is not None:
                ans += row[2] + row[3] + row[4]
        return ans // 2

    def delete_game(self, person, winner):
        cur = self.get_conn().cursor()
        game = self.get_game(person)

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
        if len(rows) == 0 or rows[0][5] is None:
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


old_data = Data(os.getenv('NEW_DB_URL'))


class MongoData:

    def __init__(self, url):
        self.DATABASE_URL = url

        self.client = MongoClient(url)
        self.db = self.client.database

    def transfer_data(self):
        games = old_data.get_games()
        self.db.games.drop()
        self.db.games.insert_many([g.to_dict() for g in games])
        print('Games transferred')
        rows = old_data.execute('SELECT * FROM prefixes')
        update = [{'id': r[0], 'prefix': r[1]} for r in rows]
        self.db.prefixes.drop()
        self.db.prefixes.insert_many(update)
        print('Prefixes transferred')
        rows = old_data.execute(f'SELECT * FROM users')
        update = [{'id': r[0], 'rating': r[1], 'lost': r[2], 'won': r[3],
                   'draw': r[4], 'theme': r[5], 'notifchannel': r[6]} for r in rows]
        self.db.users.drop()
        self.db.users.insert_many(update)
        print('User data transferred')

    def get_game(self, person):
        white = self.db.games.find({'white': person})
        black = self.db.games.find({'black': person})
        rows = [x for x in white] + [x for x in black]
        if len(rows) == 0:
            return None
        return Game2().load_dict(rows[0])

    def get_games(self):
        games = self.db.games.find()
        return [Game2().load_dict(g) for g in games]

    def change_game(self, new_game):
        self.db.games.update_one({'white': new_game.white, 'black': new_game.black}, {
                                 '$set': new_game.to_dict()}, upsert=True)

    def get_rating(self, person):
        data = list(self.db.users.find({'id': person}))
        if len(data) == 0:
            return None
        return data[0]['rating']

    def get_ratings(self):
        rows = self.db.users.find()
        ratings = {}
        for row in rows:
            if row['rating'] is not None:
                ratings[row['id']] = row['rating']
        return ratings

    def change_rating(self, person, new_rating):
        self.db.users.update_one(
            {'id': person}, {'$set': {'rating': new_rating}}, upsert=True)

    def get_prefix(self, guild):
        rows = list(self.db.guilds.find({'id': guild}))
        if len(rows) == 0:
            return '$'
        return rows[0]['prefix']

    def change_prefix(self, guild, new_prefix):
        self.db.guilds.update_one(
            {'id': guild}, {'$set': {'prefix': new_prefix}}, upsert=True)

    def get_stats(self, person):
        """Returns (lost, won, draw)"""
        data = list(self.db.users.find({'id': person}))
        if len(data) == 0 or data[0]['won'] is None:
            return None
        return data[0]['lost'], data[0]['won'], data[0]['draw']

    def change_stats(self, person, lost, won, drew):
        self.db.users.update_one(
            {'id': person}, {'$set': {'lost': lost, 'won': won, 'draw': drew}}, upsert=True)

    def total_games(self):
        rows = list(self.db.users.find())
        ans = 0
        for row in rows:
            if row['lost'] is not None and row['won'] is not None and row['draw'] is not None:
                ans += row['lost'] + row['won'] + row['draw']
        return ans // 2

    def delete_game(self, person, winner):
        game = self.get_game(person)
        self.db.games.delete_one(game.to_dict())
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

    def get_theme(self, person):
        data = list(self.db.users.find({'id': person}))
        if len(data) == 0 or data[0]['theme'] is None:
            return 'default'
        return data[0]['theme']

    def get_notifchannel(self, person):
        data = list(self.db.users.find({'id': person}))
        if len(data) == 0 or data[0]['notifchannel'] == -1:
            return None
        return data[0]['notifchannel']

    def change_settings(self, person, *, new_theme=None, new_notif=None):
        if new_theme is not None:
            self.db.users.update_one(
                {'id': person}, {'$set': {'theme': new_theme}}, upsert=True)
        if new_notif is not None:
            self.db.users.update_one(
                {'id': person}, {'$set': {'notifchannel': new_notif}}, upsert=True)

    def change_theme(self, person, new_theme):
        self.change_settings(person, new_theme=new_theme)

    def has_claimed(self, person):
        rows = list(self.db.votes.find({'id': person}))
        return len(rows) == 1

    def get_claimed(self):
        rows = self.db.votes.find()
        return [x['id'] for x in rows]

    def add_vote(self, person):
        self.db.votes.insert_one({'id': person})

    def remove_vote(self, person):
        self.db.votes.delete_one({'id': person})


data_manager = MongoData(os.getenv('MONGODB_URL'))
