from discord import FFmpegPCMAudio, VoiceClient, utils, Option, TextChannel
import pafy
import youtube_dl

queue = []
in_queue = []

# Define a function that will add the appropriate slash commands whent he bot starts
def define_slash(guild_ids, bot):

    # Join the channel the user is in
    @bot.slash_command(name="join", description="Summon DJ Luigi Bot to the party!",guild_ids=guild_ids)
    async def join(ctx):
        try:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.response.send_message("Let's get this party started!", ephemeral=True)
        except(AttributeError):
            await ctx.response.send_message("You're not in a VC!", ephemeral=True)

    @bot.slash_command(name="leave", description="Party's over, go home DJ Luigi Bot",guild_ids=guild_ids)
    async def leave(ctx):
        for vc in bot.voice_clients:
            if vc.channel.id == ctx.user.voice.channel.id:
                await vc.disconnect()
                await ctx.response.send_message("See you next time!", ephemeral=True)

    @bot.slash_command(name="play", description="Play some tunes!", guild_ids=guild_ids)
    # : discord.Option(discord.TextChannel, "What channel should the poll be posted to"
    async def play(ctx, song: Option(str, "The song you wish to play!")):
        guild = ctx.guild

        has_queue = False

        await ctx.response.defer(ephemeral=True)

        # Join the user's VC
        voice_client: VoiceClient = utils.get(bot.voice_clients, guild=guild)

        # If there's a song playing, add it to the queue instead
        if voice_client.is_playing():
            video = pafy.new(song)

            with youtube_dl.YoutubeDL() as ydl:
                 song_info = ydl.extract_info(song, download=False)

            queue.append({video.title, song_info["formats"][0]["url"]})

            has_queue = True

            await ctx.followup.send(content="I added your song to the queue! (There are now {0} songs in queue)".format(len(queue)), ephemeral=True)

        if not has_queue:

            failed = False

            try:
                # Get video information and the video's audio
                video = pafy.new(song)

            except(KeyError):
                failed = True
                await ctx.followup.send(content="I was unable to play the song you requested :/", ephemeral=True)

            except(ValueError):
                failed = True
                await ctx.followup.send(content="This doesn't look like a YouTube link!", ephemeral=True)

            if not failed:
                title = video.title
                length = video.duration

                # Get a json library with general video information, as well as the url we need to stream the audio.
                with youtube_dl.YoutubeDL() as ydl:
                     song_info = ydl.extract_info(song, download=False)

                audio_source = FFmpegPCMAudio(song_info["formats"][0]["url"])
                if not voice_client.is_playing():
                    voice_client.play(audio_source, after=None)
                    await ctx.followup.send(content="Now playing: {0}".format(title), ephemeral=True)

    @bot.slash_command(name="queue", description="See what's in the queue",guild_ids=guild_ids)
    async def leave(ctx):
        i = 0
        global queue
        global in_queue
        for song in queue:
            if in_queue == None:
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
                in_queue.append(song)
                print(in_queue)
        if len(queue) == 0:
            await ctx.response.send_message("There is nothing in the queue!", ephemeral=True)
        else:
            await ctx.response.send_message("The current queue is: {0}".format(in_queue), ephemeral=True)
