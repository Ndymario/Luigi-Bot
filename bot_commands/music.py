from discord import FFmpegPCMAudio, VoiceClient, utils
from discord_slash.utils.manage_commands import create_option
import asyncio

# Define a function that will add the appropriate slash commands whent he bot starts
def define_slash(guild_ids, slash, client):
    voice = 0

    # Join the channel the user is in
    @slash.slash(name="join", description="Summon DJ Luigi Bot to the party!",guild_ids=guild_ids)
    async def join(ctx):
        try:
            channel = ctx.author.voice.channel
            voice = await channel.connect()
            await ctx.send("Let's get this party started!", hidden=True)
        except(AttributeError):
            await ctx.send("You're not in a VC!", hidden=True)

    @slash.slash(name="leave", description="Party's over, go home DJ Luigi Bot",guild_ids=guild_ids)
    async def leave(ctx):
        global voice
        await voice.disconnect()
        await ctx.send("See you next time!", hidden=True)

    @slash.slash(name="play", description="Play some tunes!",guild_ids=guild_ids, options=[create_option(name="song",description="The song you wish to play!",option_type=3,required=True)])
    async def play(ctx, song: str):
        guild = ctx.guild
        voice_client: VoiceClient = utils.get(client.voice_clients, guild=guild)
        audio_source = FFmpegPCMAudio('Boat Battle - Bonus Time.mp3')
        await ctx.send("Now playing: {0}".format(song), hidden=True)
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
        #except(AttributeError):
            #await ctx.send("You're not in a VC!", hidden=True)
