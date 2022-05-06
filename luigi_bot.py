##############
# Luigi Bot is a bot created by Ndymario#2326!
##############

import discord
from discord.ext import commands
import mongo_db.mongo_db as mongo_db
import bot_commands.char as ch
#import bot_commands.quest as quest
import bot_commands.about as about
import bot_commands.music as music
import bot_commands.poll as poll

# Since we're good and safe coders, we will read our token from an external file
token_file = open("token.txt", "r")
token = token_file.read()
token_file.close()

secret_file = open("client_secret.txt", "r")
secret = secret_file.read()
secret_file.close()

class LuigiBot(commands.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
        #self.ipc = ipc.Server(self,secret_key = secret)

    # When the bot is ready, say so in the console
    async def on_ready(self):
        print("Luigi Bot Ready!")
    
    # When the IPC is ready, say so in the console
    async def on_ipc_ready(self):
        print("Ipc Server Ready!")
    
    # If something goes wrong with IPC, handel it
    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)

bot = LuigiBot(command_prefix='$', intents = discord.Intents.default())
guild_ids = [334848602130219009, 427651547208482816, 787615718090080286, 399424476259024897, 634581944025219091, 915655039463333899, 813610703381987408, 610396457962307604]

# Set up slash commands from other files
ch.define_slash(guild_ids, bot)
about.define_slash(guild_ids, bot)
poll.define_slash(guild_ids, bot)

# Until the music re-write happens, the music commands are offline!
# music.define_slash(guild_ids, bot)

# Likewise, until the RPG engine is implemented, the quest commands are offline!
# quest.define_slash(guild_ids, bot)

# Connect to our MongoDB
mongo_db.db_connect()

'''
@bot.ipc.route()
async def get_guild_count(data):
	return len(bot.guilds) # returns the len of the guilds to the client

@bot.ipc.route()
async def get_guild_ids(data):
	final = []
	for guild in bot.guilds:
		final.append(guild.id)
	return final # returns the guild ids to the client

@bot.ipc.route()
async def get_guild(data):
	guild = bot.get_guild(data.guild_id)
	if guild is None: return None

	guild_data = {
		"name": guild.name,
		"id": guild.id,
		"prefix" : "?"
	}

	return guild_data
'''

# When the bot is ready, say so in the console
@bot.event
async def on_ready():
    print("Ready!")

# Run the bot!
#bot.ipc.start()
bot.run(token)