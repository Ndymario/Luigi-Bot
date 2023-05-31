import typing
from bot.database import Database
import crescent
import hikari
from datetime import datetime

plugin = crescent.Plugin[hikari.GatewayBot, Database]()


@plugin.include
@crescent.command(name="birthday", description="Set your birthday for Luigi Bot to remember")
class Birthday:
    month = crescent.option(int, description="What month you were born", name="month")
    day = crescent.option(int, description="What day you were born", name="day")
    year = crescent.option(int, description="What year you were born", name="year")

    async def callback(self, ctx: crescent.Context):
        user = plugin.model.get_user(ctx.user.id)

        if user is None:
            plugin.model.add_user(ctx.user.id, ctx.user.username)

        plugin.model.set_birthday(ctx.user.id, datetime.strptime(f"{self.month}/{self.day}/{self.year}", "%m/%d/%Y"))

        embed = hikari.Embed(title="Birthday Updated", description="Your birthday has been updated successfully!",
                             color="#22fa05")

        await ctx.respond(embed=embed, ephemeral=True)
