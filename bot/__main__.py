import os
import hikari
import crescent
import miru

bot = hikari.GatewayBot(os.getenv("BOT_TOKEN"))
miru.install(bot)
client = crescent.Client(bot)

client.plugins.load_folder("bot.plugins")

bot.run()

