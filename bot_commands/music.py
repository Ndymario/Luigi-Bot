from discord import FFmpegPCMAudio, VoiceClient, utils
from discord_slash.utils.manage_commands import create_option
import asyncio
import pafy
import youtube_dl

queue = []
in_queue = []

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

        has_queue = False

        await ctx.defer(hidden=True)

        # Join the user's VC
        voice_client: VoiceClient = utils.get(client.voice_clients, guild=guild)

        # If there's a song playing, add it to the queue instead
        if voice_client.is_playing():
            video = pafy.new(song)

            with youtube_dl.YoutubeDL() as ydl:
                 song_info = ydl.extract_info(song, download=False)

            queue.append({video.title, song_info["formats"][0]["url"]})

            has_queue = True

            await ctx.send("I added your song to the queue! (There are now {0} songs in queue)".format(len(queue)), hidden=True)

        if not has_queue:

            failed = False

            try:
                # Get video information and the video's audio
                video = pafy.new(song)

            except(KeyError):
                failed = True
                await ctx.send("I was unable to play the song you requested :/", hidden=True)

            except(ValueError):
                failed = True
                await ctx.send("This doesn't look like a YouTube link!", hidden=True)

            if not failed:
                title = video.title
                length = video.duration

                # Get a json library with general video information, as well as the url we need to stream the audio.
                with youtube_dl.YoutubeDL() as ydl:
                     song_info = ydl.extract_info(song, download=False)

                audio_source = FFmpegPCMAudio(song_info["formats"][0]["url"])
                await ctx.defer(hidden=True)
                if not voice_client.is_playing():
                    voice_client.play(audio_source, after=None)
                    await ctx.send("Now playing: {0}".format(title), hidden=True)

    @slash.slash(name="queue", description="See what's in the queue",guild_ids=guild_ids)
    async def leave(ctx):
        i = 0
        global queue
        global in_queue
        for song in queue:
            print("For song in queue...\n")
            if in_queue == None:
                print("in_queue is none!")
                in_queue = list(song + ", ")
                print(in_queue[i])
                print("\n")
                i += 1
            elif i != len(in_queue):
                print("i = {0}\n").format(i)
                in_queue.append(song.keys() + ", ")
                i += 1
            else:
                print("This is the last song\n")
                in_queue.append(song.keys() + ".")
                print(in_queue)
        if len(queue) == 0:
            await ctx.send("There is nothing in the queue!", hidden=True)
        else:
            await ctx.send("The current queue is: {0}".format(in_queue), hidden=True)
