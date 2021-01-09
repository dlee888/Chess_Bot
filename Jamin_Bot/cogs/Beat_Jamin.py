import discord
import os
import subprocess
from discord.ext import commands
import random

from cogs.Utility import *

class Beat_Jamin(commands.Cog):
	
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def move(self, ctx, move):
		'''
		Plays <move> against the computer
		Please enter the move in algebraic notation
		For example, Nxe4, Nge5, c4, Ke2, etc
		'''
		if not ctx.author.id in games.keys():
			await ctx.send('You do not have a game in progress with Beat_Jamin')
			return
		
		person = ctx.author.id
		file_in = f'data/input-{person}.txt'
		file_out = f'data/output-{person}.txt'
		if not file_in[5:] in os.listdir('data'):
			f = open(file_in, 'x')
			f.close()
		if not file_out[5:] in os.listdir('data'):
			f = open(file_out, 'x')
			f.close()
				
		f = open(file_in, 'w')
		f.write('play\n')
		if len(games[ctx.author.id]) == 0:
			f.write('no\n')
		else:
			f.write('yes2\n')
			game_str = ''
			for i in range(len(games[ctx.author.id])):
				if i%2==0:
					game_str += str(i//2+1) + '. '
				game_str += str(games[ctx.author.id][i]) + ' '
			game_str += '*'
			f.write(game_str + '\n')
		f.write('60\n')
		if colors[ctx.author.id] == 0:
			f.write('white\n')
		else:
			f.write('black\n')
		f.write(move + '\nquit\nquit\n')
		f.close()
		await ctx.send('Beat_Jamin is thinking...')
		subprocess.call(['./jamin'], stdin=open(file_in), stdout=open(file_out, 'w'))
		f = open(file_out)
		out = f.readlines()
		f.close()
		if out[-3] != 'GAME STILL IN PROGRESS\n':
			if out[-3] == 'ILLEGAL MOVE PLAYED\n':
				await ctx.send('Haha, nice try')
				return
			winner = 0
			if out[-3] == 'DRAW\n':
				update_rating(ctx.author.id, 1/2)
				await ctx.send('Draw')
			else:
				if out[-3] == 'WHITE WON\n':
					winner = 1
				if winner == colors[ctx.author.id]:
					update_rating(ctx.author.id, 1)
					await ctx.send('You won!')
				else:
					update_rating(ctx.author.id, 0)
					await ctx.send('You lost.')
			
			await ctx.send(f'Your new rating is {get_rating(ctx.author.id)}')
			games.pop(ctx.author.id)
			push_games()
			return
		move = int(out[-24][31:-2])
		await ctx.send(out[-24])
		await ctx.send(out[-23])
		msg1 = '```\n'
		for i in range(-21,-4, 2):
			#os.system(f'echo {i}')
			msg1 += out[i] + '\n'
			#os.system(f'echo "{msg1}"')
		msg1 += '```'
		await ctx.send(msg1)
		game_str = out[-2][:-1].split(' ')
		games[ctx.message.author.id].clear()
		for i in game_str:
			if i == '' or i == '\n':
				continue
			games[ctx.message.author.id].append(int(i))
			#os.system(f'echo {i}')
		push_games()			

	@commands.command()
	async def challenge(self, ctx):
		'''
		Challenges Beat_Jamin
		'''
		if ctx.author.id in games.keys():
			await ctx.send('You already have a game in progress')
			return
		
		games[ctx.author.id] = []
		colors[ctx.author.id] = random.randint(0, 1) # 1 if white, 0 if black
		
		await ctx.send('Game started with Beat_Jamin')
		if colors[ctx.author.id] == 0:
			await ctx.send('You are black')
		else:
			await ctx.send('You are white')
		
		if colors[ctx.author.id] == 0:
			person = ctx.author.id
			file_in = f'data/input-{person}.txt'
			file_out = f'data/output-{person}.txt'
			if not file_in[5:] in os.listdir('data'):
				f = open(file_in, 'x')
				f.close()
			if not file_out[5:] in os.listdir('data'):
				f = open(file_out, 'x')
				f.close()

			f = open(file_in, 'w')
			f.write('play\nno\n60\nwhite\nquit\nquit')
			f.close()
			print('Starting Jamin')

			subprocess.call(['./jamin'], stdin=open(file_in), stdout=open(file_out, 'w'))
			f = open(file_out)
			out = f.readlines()
			move = int(out[-24][31:-2])
			await ctx.send(out[-24])
			await ctx.send(out[-23])
			msg1 = '```\n'
			for i in range(-21,-6, 2):
				#os.system(f'echo {i}')
				msg1 += out[i] + '\n'
				#os.system(f'echo "{msg1}"')
			msg1 += '```'
			await ctx.send(msg1)
			await ctx.send(out[-5])
			game_str = out[-2].split(' ')
			games[ctx.author.id].clear()
			for i in game_str:
				if i == '' or i == '\n':
					continue
				games[ctx.author.id].append(int(i))
			push_games()
	
	@commands.command()
	async def abort(self, ctx, user):
		'''
		Aborts a game
		'''
		if not is_mooderator(ctx.author):
			await ctx.send('You do not have permission to abort games')
			return
		
		person = int(user[3:-1])
		
		if not person in games.keys():
			await ctx.send('You do not have a game in progress')
			return
		
		games.pop(person)
		await ctx.send('Game aborted')
		push_games()
		
	
	@commands.command()
	async def resign(self, ctx):
		'''
		Resigns the game
		'''
		if not ctx.author.id in games.keys():
			await ctx.send('You do not have a game in progress')
			return
		
		games.pop(ctx.message.author.id)
		update_rating(ctx.author.id, 0)
		await ctx.send(f'Game resigned. Your new rating is {get_rating(ctx.author.id)}')
		push_games()
		
	@commands.command()
	async def view(self, ctx, *user):
		'''
		Views your current game
		'''
		
		person = -1
		if len(user) == 1:
			person = int(user[0][3:-1])
		else:
			person = ctx.author.id
		
		if not person in games.keys():
			if len(user)==1:
				await ctx.send(f'{user[0]} does not have a game in progress')
			else:
				await ctx.send('You do not have a game in progress')
			return
		
		person = ctx.author.id
		file_in = f'data/input-{person}.txt'
		file_out = f'data/output-{person}.txt'
		#for asdf in os.listdir('data'):
		#	os.system(f'echo {asdf}')
		os.system(f'echo {file_in[5:]}')
		if not file_in[5:] in os.listdir('data'):
			f = open(file_in, 'x')
			f.close()
		if not file_out[5:] in os.listdir('data'):
			f = open(file_out, 'x')
			f.close()

		f = open(file_in, 'w')
		f.write('play\n')
		if len(games[person]) == 0:
			f.write('no\n')
		else:
			f.write('yes2\n')
			game_str = ''
			for i in range(len(games[person])):
				if i%2==0:
					game_str += str(i//2+1) + '. '
				game_str += str(games[person][i]) + ' '
			game_str += '*'
			f.write(game_str + '\n')
		f.write('60\n')
		if colors[person] == 0:
			f.write('white\n')
		else:
			f.write('black\n')
		f.write('\nquit\nquit\n')
		f.close()
		subprocess.call(['./jamin'], stdin=open(file_in), stdout=open(file_out, 'w'))
		f = open(file_out)
		out = f.readlines()
		f.close()
		game = '```\n'
		for i in range(-20,-4, 2):
			#os.system(f'echo {i}')
			game += out[i] + '\n'
			#os.system(f'echo "{msg1}"')
		game += '```'
		await ctx.send(game)
