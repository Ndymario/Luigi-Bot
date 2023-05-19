import typing
from bot.database import Database
import crescent
import hikari

plugin = crescent.Plugin[hikari.GatewayBot, Database]()


@plugin.include
@crescent.command(name="check-level", description="Refresh the level of a user")
class CheckLevel:
    user = crescent.option(hikari.users.User, description="Who do you want to refresh?")

    async def callback(self, ctx: crescent.Context):

        plugin.model.set_exp(self.user.id, plugin.model.get_exp(self.user.id))
        await ctx.respond(content="I've updated their level!", ephemeral=True)
