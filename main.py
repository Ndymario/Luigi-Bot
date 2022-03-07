##############
# Luigi Bot is a bot created by Ndymario#2326!
##############

from discord.ext import commands
import mongo_db.mongo_db as mongo_db
import bot_commands.char as ch
#import bot_commands.quest as quest
import bot_commands.general_commands as general
#import bot_commands.music as music

# Since we're good and safe coders, we will read our token from an external file
token_file = open("token.txt", "r")
token = token_file.read()

bot = commands.Bot(command_prefix='$')
guild_ids = [334848602130219009, 427651547208482816, 787615718090080286, 399424476259024897, 634581944025219091, 915655039463333899, 813610703381987408]

# Set up slash commands from other files
ch.define_slash(guild_ids, bot)
general.define_slash(guild_ids, bot)

# Connect to our MongoDB
mongo_db.db_connect()

# When the bot is ready, say so in the console
@bot.event
async def on_ready():
    print("Ready!")

# Run the bot!
bot.run(token)