import psycopg2
import time
import os

class Game:

	def __init__(self, color, time_control, moves=[], last_moved=time.time(), warned=False):
		self.moves = moves
		self.color = color
		self.time_control = time_control
		self.last_moved = last_moved
		self.warned = warned

	def __str__(self):
		game_str = ''
		for i in range(len(self.moves)):
			if i % 2 == 0:
				game_str += str(i//2+1) + '. '
			game_str += str(self.moves[i]) + ' '
		game_str += '*'
		return game_str


class Data:

	def __init__(self):
		self.DATABASE_URL = os.environ['DATABASE_URL']

		self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
  
		create_games_table = '''CREATE TABLE IF NOT EXISTS games (
										id integer NOT NULL PRIMARY KEY UNIQUE ON CONFLICT REPLACE,
										moves text,
										color integer,
										time_control integer,
										last_moved real,
										warned integer
									);'''
		create_ratings_table = '''CREATE TABLE IF NOT EXISTS ratings (
										id integer NOT NULL PRIMARY KEY UNIQUE ON CONFLICT REPLACE,
										rating real
									);'''
		create_prefix_table = '''CREATE TABLE IF NOT EXISTS prefixes (
										id integer NOT NULL PRIMARY KEY UNIQUE ON CONFLICT REPLACE,
										prefix text
									);'''
         
		cur = self.conn.cursor()
		cur.execute(create_games_table)
		cur.execute(create_ratings_table)
		cur.execute(create_prefix_table)

	def get_game(self, person):
		cur = self.conn.cursor()
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
		cur = self.conn.cursor()
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
		cur = self.conn.cursor()
		moves_str = ' '.join(str(move) for move in new_game.moves)

		update_sql = f'''INSERT INTO games
VALUES ({person}, '{moves_str}', {new_game.color}, {new_game.time_control}, {new_game.last_moved}, {int(new_game.warned)});'''

		cur.execute(f'DELETE FROM games WHERE id = {person};')  
		cur.execute(update_sql)

		self.conn.commit()

	def get_rating(self, person):
		cur = self.conn.cursor()
		cur.execute(f'SELECT * FROM ratings WHERE id = {person};')
		rows = cur.fetchall()

		if len(rows) == 0:
			return None
		return rows[0][1]

	def get_ratings(self):
		cur = self.conn.cursor()
		cur.execute(f'SELECT * FROM ratings;')
		rows = cur.fetchall()

		ratings = {}
		for row in rows:
			ratings[row[0]] = row[1]
   
		return ratings

	def change_rating(self, person, new_rating):
		cur = self.conn.cursor()

		cur.execute(f'DELETE FROM ratings WHERE id = {person};')  
		cur.execute(f'INSERT INTO ratings VALUES ({person}, {new_rating});')

		self.conn.commit()

	def get_prefix(self, guild):
		cur = self.conn.cursor()
		cur.execute(f'SELECT * FROM prefixes WHERE id = {guild};')
		rows = cur.fetchall()

		if len(rows) == 0:
			return '$'
		return rows[0][1]

	def change_prefix(self, guild, new_prefix):
		cur = self.conn.cursor()
		cur.execute(f'DELETE FROM prefixes WHERE id = {guild};')  
		cur.execute(f'INSERT INTO prefixes VALUES ({guild}, \'{new_prefix}\');')

		self.conn.commit()

	def delete_game(self, person):
		cur = self.conn.cursor()
		cur.execute(f'DELETE FROM games WHERE id = {person};')

		self.conn.commit()


data_manager = Data()

# for testing
if __name__ == '__main__':
	# data_manager.change_game(69, Game(0, 30))
	print(data_manager.get_games())
	print(data_manager.get_game(69))
