import typing
from bot.database import Database
import crescent
import hikari

plugin = crescent.Plugin[hikari.GatewayBot, Database]()


@plugin.include
@crescent.command(name="leaderboard", description="View the leaderboard")
async def leaderboard(ctx: crescent.Context):
    level_dict = {0: "None", 1: "Super Mushroom", 2: "Fire Flower", 3: "Blue Shell", 4: "Super Star",5: "Big Star",
                  6: "Mega Mushroom"}
    await ctx.defer(ephemeral=True)
    try:
        stats = plugin.model.fetch_leaderboard()

        text_form = ""

        embed = hikari.Embed(title="Here are current server stats!")

        counter = 0
        for stat in stats:
            if counter == 10:
                break
            user = True
            level = True
            for info in stat:
                if user:
                    user_id = await ctx.app.rest.fetch_user(info)
                    text_form += user_id.mention + ": "
                    user = False
                    continue

                if level:
                    text_form += f"Level = **{level_dict[info]}** "
                    level = False
                    continue

                text_form += f"Exp = **{info}**"
            text_form += "\n\n"
            counter += 1

        embed.add_field(name="Rankings", value=text_form)
        embed.set_footer(text="These are the top 10 users in the server")

        await ctx.respond(embed=embed, ephemeral=True)
    except():
        plugin.model.restart()
        await ctx.respond(content="Something went wrong, please try again!", ephemeral=True)
