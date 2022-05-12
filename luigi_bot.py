##############
# Luigi Bot is a bot created by Ndymario#2326!
##############

import discord
from discord import app_commands
import mongo_db.mongo_db as mongo_db
import bot_commands.char as ch
#import bot_commands.quest as quest
import bot_commands.about as about
#import bot_commands.music as music
import bot_commands.poll as poll

'''---Bot Declaration---'''
# My debug server ID
MY_GUILD = discord.Object(id=634581944025219091)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents, application_id: int):
        super().__init__(intents=intents, application_id=application_id)
        self.tree = app_commands.CommandTree(self)

    # Sync global commands with a specific guild for testing
    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.default()

client = MyClient(intents=intents, application_id=421169985617002496)
    
'''---Set up slash commands from other files---'''
about.define_slash(client) # Load the about command
poll.define_slash(client) # Load the poll command

# Connect to our MongoDB
mongo_db.db_connect()

# When the bot is ready, say so in the console
@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

# Run the bot!
with open("keys/token.key", "r") as s:
    token = s.read()
    client.run(token)