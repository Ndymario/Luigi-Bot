import crescent
import hikari
from __main__ import Database

plugin = crescent.Plugin[hikari.GatewayBot, Database]()


@plugin.include
@crescent.command(name="poll", description="Make a poll")
async def about(ctx: crescent.Context):
    await ctx.respond(ephemeral=True, content="This command is not ready yet!")
