import time
import os
import sys
import chess
from motor.motor_asyncio import AsyncIOMotorClient
import typing

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
        self.client = AsyncIOMotorClient(url)
        self.db = self.client.test if '-beta-bot' in sys.argv else self.client.database

    async def to_list(self, cursor):
        return [document async for document in cursor]

    async def get_game(self, person):
        white = self.db.games.find({'white': person})
        black = self.db.games.find({'black': person})
        rows = await self.to_list(white) + await self.to_list(black)
        return None if len(rows) == 0 else Game2().load_dict(rows[0])

    async def get_games(self):
        games = self.db.games.find()
        return [Game2().load_dict(g) async for g in games]

    async def current_games(self):
        return await self.db.games.count_documents({})

    async def change_game(self, new_game):
        await self.db.games.update_one({'white': new_game.white, 'black': new_game.black}, {
            '$set': new_game.to_dict()}, upsert=True)

    async def get_rating(self, person) -> typing.Optional[float]:
        data = await self.to_list(self.db.users.find({'id': person}))
        return data[0]['rating'] if data and 'rating' in data[0].keys() else None

    async def get_ratings(self):
        rows = self.db.users.find().sort([("rating", -1)]).limit(40)
        return {row['id']: row['rating'] async for row in rows if 'rating' in row.keys() and row['rating'] is not None}

    async def rated_users(self):
        return await self.db.users.count_documents({'rating': {'$ne': None}})

    async def change_rating(self, person, new_rating):
        await self.db.users.update_one(
            {'id': person}, {'$set': {'rating': new_rating}}, upsert=True)

    async def get_prefix(self, guild):
        rows = await self.to_list(self.db.prefixes.find({'id': guild}))
        return rows[0]['prefix'] if rows else '$'

    def change_prefix(self, guild, new_prefix):
        self.db.prefixes.update_one(
            {'id': guild}, {'$set': {'prefix': new_prefix}}, upsert=True)

    async def get_stats(self, person):
        """Returns (lost, won, draw)"""
        data = await self.to_list(self.db.users.find({'id': person}))
        if not data or 'won' not in data[0].keys() or data[0]['won'] is None:
            return 0, 0, 0
        return data[0]['lost'], data[0]['won'], data[0]['draw']

    async def change_stats(self, person, lost, won, drew):
        await self.db.users.update_one(
            {'id': person}, {'$set': {'lost': lost, 'won': won, 'draw': drew}}, upsert=True)

    async def total_games(self):
        total = await self.to_list(self.db.users.aggregate([{'$group': {'_id': 'null',
                                                               'total': {'$sum': {'$add': ['$lost', '$won', '$draw']}}}}]))
        return total[0]['total'] // 2

    async def delete_game(self, person, winner):
        game = await self.get_game(person)
        if game is None:
            return
        await self.db.games.delete_one(game.to_dict())
        white_lost, white_won, white_draw = await self.get_stats(game.white)
        black_lost, black_won, black_draw = await self.get_stats(game.black)
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
        await self.change_stats(game.white, white_lost, white_won, white_draw)
        await self.change_stats(game.black, black_lost, black_won, black_draw)

    async def get_theme(self, person):
        data = await self.to_list(self.db.users.find({'id': person}))
        if not data or 'theme' not in data[0].keys() or data[0]['theme'] is None:
            return 'default'
        return data[0]['theme']

    async def get_notifchannel(self, person):
        data = await self.to_list(self.db.users.find({'id': person}))
        if not data or 'notifchannel' not in data[0].keys() or data[0]['notifchannel'] == -1:
            return None
        return data[0]['notifchannel']

    async def change_settings(self, person, *, new_theme=None, new_notif=None):
        if new_theme is not None:
            await self.db.users.update_one(
                {'id': person}, {'$set': {'theme': new_theme}}, upsert=True)
        if new_notif is not None:
            await self.db.users.update_one(
                {'id': person}, {'$set': {'notifchannel': new_notif}}, upsert=True)

    async def change_theme(self, person, new_theme):
        await self.change_settings(person, new_theme=new_theme)

    async def has_claimed(self, person):
        rows = await self.to_list(self.db.votes.find({'id': person}))
        return len(rows) == 1

    async def get_claimed(self):
        rows = self.db.votes.find()
        return [x['id'] async for x in rows]

    async def add_vote(self, person):
        await self.db.votes.insert_one({'id': person})

    async def remove_vote(self, person):
        await self.db.votes.delete_one({'id': person})


data_manager = MongoData(os.getenv('MONGODB_URL'))
