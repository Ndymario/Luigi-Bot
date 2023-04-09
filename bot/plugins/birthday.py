import typing
from bot.database import Database
import crescent
import hikari

plugin = crescent.Plugin[hikari.GatewayBot, Database]()


@plugin.include
@crescent.command(name="birthday", description="Set your birthday for Luigi Bot to remember")
class Birthday:
    year = crescent.option(int, description="What year you were born", name="year")
    month = crescent.option(int, description="What month you were born", name="month")
    day = crescent.option(int, description="What day you were born", name="day")

    async def callback(self, ctx: crescent.Context):
        try:
            plugin.model.cursor.execute(
                f"UPDATE users SET birthday='{self.year}-{self.month}-{self.day}' WHERE user_id={ctx.user.id}")
            await ctx.respond(content="You have set your birthday!", ephemeral=True)
        except():
            plugin.model.restart()
            await ctx.respond(content="Something went wrong, please try again!", ephemeral=True)
