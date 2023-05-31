import math

import crescent
import hikari
from __main__ import Database

plugin = crescent.Plugin[hikari.GatewayBot, Database]()


@plugin.include
@crescent.command(name="exp-multiplier", description="Set how much EXP a single message is worth")
class ExpMultiplier:
    multiplier = crescent.option(int, description="What do you want to multiply each message by?")

    async def callback(self, ctx: crescent.Context):
        if self.multiplier < 0:
            await ctx.respond(content="You can't have a negative multiplier!", ephemeral=True)
            return

        plugin.model.exp_multiplier = math.floor(self.multiplier)
        await ctx.respond(content=f"I've set the multiplier to {math.floor(self.multiplier)}", ephemeral=True)
