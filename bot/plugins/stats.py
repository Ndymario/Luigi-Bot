import typing
from bot.database import Database
import crescent
import hikari

plugin = crescent.Plugin[hikari.GatewayBot, Database]()


@plugin.include
@crescent.command(name="stats", description="View your current stats in the server")
class Stats:
    user = crescent.option(hikari.users.User, description="Who do you want the stats of?", default=None)

    async def callback(self, ctx: crescent.Context):

        level_dict = {0: "None", 1: "Super Mushroom", 2: "Fire Flower", 3: "Blue Shell", 4: "Super Star", 5: "Big Star",
                      6: "Mega Mushroom"}

        try:
            if self.user is not None:
                stats = plugin.model.fetch_user(self.user.id)
                if stats is None:
                    plugin.model.add_user(ctx.user.id)
                    stats = plugin.model.fetch_user(self.user.id)
            else:
                stats = plugin.model.fetch_user(ctx.user.id)
                if stats is None:
                    plugin.model.add_user(ctx.user.id)
                    stats = plugin.model.fetch_user(ctx.user.id)

            if self.user is not None:
                embed = hikari.Embed(title=f"{self.user.username}'s current stats, as requested!")
            else:
                embed = hikari.Embed(title="Your current stats, as requested!")

            if self.user is not None:
                embed.set_author(name=self.user.username, icon=self.user.avatar_url)
            else:
                embed.set_author(name=ctx.user.username, icon=ctx.user.avatar_url)

            embed.add_field(name="Level", value=level_dict[stats[1]])
            embed.add_field(name="EXP", value=stats[2])
            if stats[3] is not None:
                embed.add_field(name="Birthday", value=stats[3])
            else:
                embed.add_field(name="Birthday", value="No birthday set!")

            await ctx.respond(embed=embed, ephemeral=True)
        except():
            plugin.model.restart()
            await ctx.respond(content="Something went wrong, please try again!", ephemeral=True)
