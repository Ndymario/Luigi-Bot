import os
import hikari
import crescent
import miru
from bot.plugins.welcome import WelcomeView

bot = hikari.GatewayBot(os.getenv("BOT_TOKEN"))
miru.install(bot)
client = crescent.Client(bot)

client.plugins.load_folder("bot.plugins")


@bot.listen()
async def startup_views(event: hikari.StartedEvent) -> None:
    view = WelcomeView(timeout=None)
    await view.start()


bot.run()
