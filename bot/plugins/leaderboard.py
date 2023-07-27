import typing
from bot.database import Database
import crescent
import hikari

plugin = crescent.Plugin[hikari.GatewayBot, Database]()


@plugin.include
@crescent.command(name="leaderboard", description="View the leaderboard")
async def leaderboard(ctx: crescent.Context):
    await ctx.defer(ephemeral=True)

    lb = plugin.model.fetch_leaderboard(1)

    text_form = ""

    embed = hikari.Embed(title="Here are current server stats!")

    for user in lb:
        text_form += f"{user.username}: " \
                     f"**{plugin.model.level_table[user.level][0]}** " \
                     f"`{user.exp}`\n"

    embed.add_field(name="Rankings", value=text_form)
    embed.set_footer(text="These are the top 10 users in the server")

    await ctx.respond(embed=embed, ephemeral=True)
