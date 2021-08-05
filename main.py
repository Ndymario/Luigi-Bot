##############
# Luigi Bot is a bot created by Ndymario#2326!
##############

import discord
from discord.ext import commands
import mongo_db.mongo_db as mongo_db
import bot_commands.char as ch
import bot_commands.quest as quest
from discord_slash import SlashCommand

# Since we're good and safe coders, we will read our token from an external file
token_file = open("token.txt", "r")
token = token_file.read()

client = commands.Bot(command_prefix='$', intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
guild_ids = [634581944025219091, 787615718090080286, 692071084014567534]

# Set up slash commands from other files
ch.define_slash(guild_ids, slash)
quest.define_slash(guild_ids, slash)

# Connect to our MongoDB
mongo_db.db_connect()

# When the bot is ready, say so in the client
@client.event
async def on_ready():
    print("Ready!")

@client.event
async def on_message(ctx):
    try:
        if ((ctx.author.name == ch.character_dict[ctx.author.name].char_name_user) & ch.character_dict[ctx.author.name].char_name_wait):
            ch.character_dict[ctx.author.name].char_name = ctx.content
            ch.character_dict[ctx.author.name].char_name_wait = False
            await ctx.delete()
        
        if ((ctx.author.name == ch.character_dict[ctx.author.name].char_name_user) & ch.character_dict[ctx.author.name].char_avatar_wait):
            ch.character_dict[ctx.author.name].char_avatar = ctx.content
            ch.character_dict[ctx.author.name].char_avatar_wait = False
            await ctx.delete()
    except(KeyError):
        return
        
client.run(token)