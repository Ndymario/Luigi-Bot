import typing
from bot.database import Database
import crescent
import hikari

plugin = crescent.Plugin[hikari.GatewayBot, Database]()


@plugin.include
@crescent.command(name="settings", description="View and change any Luigi Bot preferences for yourself")
class Settings:
    async def callback(self, ctx: crescent.Context):
        await ctx.respond(content="This command is still WIP!", ephemeral=True)
