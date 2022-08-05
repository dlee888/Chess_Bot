import time
import os
import sys
import chess
from pymongo import MongoClient

from Chess_Bot import constants


class Game2:

    def __init__(self, row=None) -> None:
        if row is None:
            row = ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', -
                   1, -1, time.time(), False, None]

        self.fen = row[0]
        self.white = row[1]
        self.black = row[2]
        self.last_moved = row[3]
        self.warned = row[4]
        if len(row) == 5 or row[5] is None:
            self.time_control = constants.DEFAULT_TIME_CONTROL
        else:
            self.time_control = row[5]
        self.white_draw = False
        self.black_draw = False

    def __str__(self) -> str:
        return self.fen

    def to_dict(self):
        return {
            'white': self.white,
            'black': self.black,
            'fen': self.fen,
            'time_control': self.time_control,
            'last_moved': self.last_moved,
            'warned': self.warned,
            'white_draw': self.white_draw,
            'black_draw': self.black_draw
        }

    def load_dict(self, dict):
        self.white = dict.get('white')
        self.black = dict.get('black')
        self.last_moved = dict.get('last_moved')
        self.warned = dict.get('warned')
        self.time_control = dict.get('time_control')
        self.fen = dict.get('fen')
        self.white_draw = dict.get('white_draw')
        self.black_draw = dict.get('black_draw')
        return self

    def turn(self):
        board = chess.Board(self.fen)
        return board.turn

    def to_move(self):
        board = chess.Board(self.fen)
        return self.white if board.turn == chess.WHITE else self.black

    def not_to_move(self):
        board = chess.Board(self.fen)
        return self.black if board.turn == chess.WHITE else self.white

    def get_color(self, person):
        return chess.WHITE if person == self.white else chess.BLACK

    def get_person(self, color):
        return self.white if color == chess.WHITE else self.black

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

    def player(self):
        """Player that is not a computer"""
        return self.black if self.white < 69 else self.white

    def bot(self):
        """Player that is a computer"""
        if self.white < 69:
            return self.white
        return self.black if self.black < 69 else None


class MongoData:

    def __init__(self, url):
        self.DATABASE_URL = url
        self.client = MongoClient(url)
        self.db = self.client.test if '-beta-bot' in sys.argv else self.client.database

    def get_game(self, person):
        white = self.db.games.find({'white': person})
        black = self.db.games.find({'black': person})
        rows = list(white) + list(black)
        return None if len(rows) == 0 else Game2().load_dict(rows[0])

    def get_games(self):
        games = self.db.games.find()
        return [Game2().load_dict(g) for g in games]

    def change_game(self, new_game):
        self.db.games.update_one({'white': new_game.white, 'black': new_game.black}, {
                                 '$set': new_game.to_dict()}, upsert=True)

    def get_rating(self, person):
        data = list(self.db.users.find({'id': person}))
        return data[0]['rating'] if data and 'rating' in data[0].keys() else None

    def get_ratings(self):
        rows = self.db.users.find()
        return {row['id']: row['rating'] for row in rows if 'rating' in row.keys() and row['rating'] is not None}

    def change_rating(self, person, new_rating):
        self.db.users.update_one(
            {'id': person}, {'$set': {'rating': new_rating}}, upsert=True)

    def get_prefix(self, guild):
        rows = list(self.db.prefixes.find({'id': guild}))
        return rows[0]['prefix'] if rows else '$'

    def change_prefix(self, guild, new_prefix):
        self.db.prefixes.update_one(
            {'id': guild}, {'$set': {'prefix': new_prefix}}, upsert=True)

    def get_stats(self, person):
        """Returns (lost, won, draw)"""
        data = list(self.db.users.find({'id': person}))
        if not data or 'won' not in data[0].keys() or data[0]['won'] is None:
            return 0, 0, 0
        return data[0]['lost'], data[0]['won'], data[0]['draw']

    def change_stats(self, person, lost, won, drew):
        self.db.users.update_one(
            {'id': person}, {'$set': {'lost': lost, 'won': won, 'draw': drew}}, upsert=True)

    def total_games(self):
        rows = list(self.db.users.find())
        return sum(row['lost'] + row['won'] + row['draw'] for row in rows if 'lost' in row.keys() and row['lost'] is not None) // 2

    def delete_game(self, person, winner):
        game = self.get_game(person)
        if game is None:
            return
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
        if not data or 'theme' not in data[0].keys() or data[0]['theme'] is None:
            return 'default'
        return data[0]['theme']

    def get_notifchannel(self, person):
        data = list(self.db.users.find({'id': person}))
        if not data or 'notifchannel' not in data[0].keys() or data[0]['notifchannel'] == -1:
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
