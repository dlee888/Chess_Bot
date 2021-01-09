import discord
import os
from discord.ext import commands

from cogs.Utility import *

class Misc(commands.Cog):
		
	def __init__(self, client):
		self.client = client
			
	@commands.Cog.listener()
	async def on_ready(self):
		pull_ratings()
		pull_games()
		print('Bot is ready')
		
	@commands.command()
	async def ping(self, ctx):
		'''
		Sends "Pong!"
		'''
		await ctx.send('Pong!')
		
	@commands.command()
	async def update(self, ctx):
		'''
		Compiles the latest version of Beat Jamin
		Compile message of 1 means that there were compile errors
		Compiler: g++
		'''
		#os.system('echo hi')
		compile_cmd = 'g++ '
		for filename in os.listdir('engine'):
			#os.system(f'echo {filename}')
			#print(filename, filename[-4:], filename[-2:])
			if filename[-4:] == '.cpp' or filename[-2:] == '.h':
				compile_cmd += f'engine/{filename} '
		compile_cmd += '-o jamin'
		#os.system(f'echo {compile_cmd}')
		out = os.system(compile_cmd)
		
		await ctx.send(f'Updated\nCompile Message: {out}')

	@commands.command()
	async def rating(self, ctx):
		'''
		Tells you your rating
		'''
		await ctx.send(f'Your rating is {get_rating(ctx.message.author.id)}')
