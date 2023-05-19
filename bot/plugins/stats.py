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
        unknown_embed = hikari.Embed(title="Unknown user!",
                                     description="Hmm, it looks like this person is not in the database. "
                                                 "Try again later!",
                                     color="#FF0000")
        unknown_embed.set_footer(text="Users get added to the database when they send their first message")

        if self.user is not None:
            user = plugin.model.get_user(self.user.id)
            if user is None:
                await ctx.respond(embed=unknown_embed, ephemeral=True)
                return

        else:
            user = plugin.model.get_user(ctx.user.id)
            if user is None:
                plugin.model.add_user(ctx.user.id, ctx.user.username)
                user = plugin.model.get_user(ctx.user.id)

        if self.user is not None:
            embed = hikari.Embed(title=f"{self.user.username}'s current stats, as requested!", color="#05acfa")
        else:
            embed = hikari.Embed(title="Your current stats, as requested!")

        if self.user is not None:
            embed.set_author(name=self.user.username, icon=self.user.avatar_url)
        else:
            embed.set_author(name=ctx.user.username, icon=ctx.user.avatar_url)

        embed.add_field(name="Level", value=plugin.model.level_table[user.level][0])
        embed.add_field(name="EXP", value=user.exp)

        if user.birthday != "":
            embed.add_field(name="Birthday", value=user.birthday)
        else:
            embed.add_field(name="Birthday", value="No birthday set!")

        await ctx.respond(embed=embed, ephemeral=True)
