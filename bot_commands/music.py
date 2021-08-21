from discord import FFmpegPCMAudio
import asyncio

def define_slash(guild_ids, slash):
    voice = 0

    @slash.slash(name="join", description="Summon DJ Luigi Bot to the party!",guild_ids=guild_ids)
    async def join(ctx):
        channel = ctx.author.voice.channel
        global voice
        voice = await channel.connect()
        await ctx.send("Let's get this party started!", hidden=True)

    @slash.slash(name="leave", description="Party's over, go home DJ Luigi Bot",guild_ids=guild_ids)
    async def leave(ctx):
        global voice
        await voice.disconnect()
        await ctx.send("See you next time!", hidden=True)

    @slash.slash(name="play", description="Play some tunes!",guild_ids=guild_ids)
    async def play(ctx):
        global voice
        player = voice.create_ffmpeg_player('Boat Battle - Bonus Time.mp3', after=lambda: print('done'))
        player.start()
        while not player.is_done():
            await asyncio.sleep(1)
        # disconnect after the player has finished
        player.stop()