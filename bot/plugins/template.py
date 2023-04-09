import crescent
import hikari
import miru
from bot.url_button import UrlButton
from __main__ import Database

plugin = crescent.Plugin[hikari.GatewayBot, Database]()


@plugin.include
@crescent.command(name="template", description="Get information the NSMB Code Template")
async def about(ctx: crescent.Context):
    with open("./bot/plugins/template.txt", "r") as about_txt:
        text = about_txt.read()

    embed = hikari.Embed(title=f"The NSMB Code Template", description=f"{text}", color="#1E92F4")

    view = miru.View()
    view.add_item(UrlButton("The NSMB Code Template", "https://github.com/MammaMiaTeam/NSMB-Code-Template"))
    view.add_item(UrlButton("The NSMB Code Reference", "https://github.com/MammaMiaTeam/NSMB-Code-Reference"))

    message = await ctx.respond(embed=embed, components=view, ensure_message=True)
    await view.start(message=message)