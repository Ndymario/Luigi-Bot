import crescent
import hikari
import miru
from bot.url_button import UrlButton

plugin = crescent.Plugin()


@plugin.include
@crescent.command(name="about", description="Get information about the bot.")
async def about(ctx: crescent.Context):
    with open("./bot/plugins/about.txt", "r") as about_txt:
        text = about_txt.read()

    embed = hikari.Embed(title=f"About me, Luigi!", description=f"{text}", color="#42f54b")
    embed.set_author(name=f"{ctx.user.username}", icon=f"{ctx.user.avatar_url}")
    embed.set_thumbnail("./bot/res/LuigiBot.png")

    view = miru.View()
    view.add_item(UrlButton("GitHub", "https://github.com/Ndymario/Luigi-Bot"))

    message = await ctx.respond(embed=embed, components=view, ensure_message=True)
    await view.start(message=message)
