import psycopg2
import time
import os


class Game:

    def __init__(self, color, bot, moves=[], last_moved=time.time(), warned=False):
        self.moves = moves
        self.color = color
        self.last_moved = last_moved
        self.warned = warned
        self.bot = bot

    def __str__(self):
        game_str = ' '.join(str(i) for i in self.moves)
        game_str += ' -1'
        return game_str


class Data:

    def __init__(self, url):
        self.DATABASE_URL = url

        self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')

        create_games_table = '''CREATE TABLE IF NOT EXISTS games (
										id bigint NOT NULL PRIMARY KEY UNIQUE,
										moves text,
                                        bot integer,
										color integer,
										last_moved real,
										warned integer
									);'''
        create_ratings_table = '''CREATE TABLE IF NOT EXISTS ratings (
										id bigint NOT NULL PRIMARY KEY UNIQUE,
										rating real
									);'''
        create_prefix_table = '''CREATE TABLE IF NOT EXISTS prefixes (
										id bigint NOT NULL PRIMARY KEY UNIQUE,
										prefix text
									);'''
        create_themes_table = '''CREATE TABLE IF NOT EXISTS themes (
										id bigint NOT NULL PRIMARY KEY UNIQUE,
										theme text
									);'''
        create_votes_table = '''CREATE TABLE IF NOT EXISTS votes (
										id bigint NOT NULL PRIMARY KEY UNIQUE
									);'''

        cur = self.get_conn().cursor()
        cur.execute(create_games_table)
        cur.execute(create_ratings_table)
        cur.execute(create_prefix_table)
        cur.execute(create_themes_table)
        cur.execute(create_votes_table)

    def get_conn(self):
        if self.conn.closed:
            print('Connection is closed. Restarting...')
            self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        return self.conn

    def get_game(self, person):
        cur = self.get_conn().cursor()
        cur.execute(f'SELECT * FROM games WHERE id = {person};')
        rows = cur.fetchall()

        if len(rows) == 0:
            return None

        row = rows[0]

        moves_str = row[1].split(' ')
        moves = []
        for move in moves_str:
            try:
                moves.append(int(move))
            except:
                pass

        return Game(row[2], row[3], moves, row[4], row[5])

    def get_games(self):
        cur = self.get_conn().cursor()
        cur.execute('SELECT * FROM games')
        rows = cur.fetchall()

        games = {}

        for row in rows:
            moves_str = row[1].split(' ')
            moves = []
            for move in moves_str:
                try:
                    moves.append(int(move))
                except:
                    pass

            games[row[0]] = Game(row[2], row[3], moves, row[4], row[5])

        return games

    def change_game(self, person, new_game: Game):
        cur = self.get_conn().cursor()
        moves_str = ' '.join(str(move) for move in new_game.moves)

        update_sql = f'''INSERT INTO games VALUES ({person}, '{moves_str}', {new_game.bot}, {new_game.color}, {new_game.last_moved}, {int(new_game.warned)});'''

        cur.execute(f'DELETE FROM games WHERE id = {person};')
        cur.execute(update_sql)

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

    def delete_game(self, person):
        cur = self.get_conn().cursor()
        cur.execute(f'DELETE FROM games WHERE id = {person};')

        self.conn.commit()

    def get_theme(self, person):
        cur = self.get_conn().cursor()
        cur.execute(f'SELECT * FROM themes WHERE id = {person};')
        rows = cur.fetchall()

        if len(rows) == 0:
            return 'default'
        return rows[0][1]

    def change_theme(self, person, new_theme):
        cur = self.get_conn().cursor()
        cur.execute(f'DELETE FROM themes WHERE id = {person};')
        cur.execute(f'INSERT INTO themes VALUES ({person}, \'{new_theme}\');')

        self.conn.commit()

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


data_manager = Data(os.environ['DATABASE_URL'])
