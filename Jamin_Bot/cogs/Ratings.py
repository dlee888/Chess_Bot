import discord
import os
from discord.ext import commands

class Ratings(commands.Cog):
	
	def __init__(self, client):
		self.client = client
	
