import os
import hikari
import crescent
import miru
from bot.plugins.welcome import WelcomeView

bot = hikari.GatewayBot(os.getenv("BOT_TOKEN"), intents=hikari.Intents.ALL)
miru.install(bot)
client = crescent.Client(bot)

client.plugins.load_folder("bot.plugins")


@bot.listen()
async def startup_views(event: hikari.StartedEvent) -> None:
    view = WelcomeView(timeout=None)
    await view.start()


@bot.listen()
async def starboard(event: hikari.ReactionAddEvent):
    message = await bot.rest.fetch_message(event.channel_id, event.message_id)
    print(message)
    for reaction in message.reactions:
        if reaction.emoji == "⭐" and reaction.count >= 5:
            star_embed = hikari.Embed(title=f"<#{message.channel_id}>", description=message.content,
                                      url=message.make_link(message.guild_id))
            star_embed.set_author(name=message.author.username, icon=message.author.avatar_url)
            await bot.rest.create_message(channel=796089340433793044, embed=star_embed)


bot.run()
