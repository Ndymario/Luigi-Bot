import crescent
import hikari
import miru
from bot.url_button import UrlButton
from __main__ import Database

plugin = crescent.Plugin[hikari.GatewayBot, Database]()

nsmbe_group = crescent.Group("nsmbe")


@plugin.include
@nsmbe_group.child
@crescent.command(name="info", description="Get information on NSMBe and a download link")
async def about(ctx: crescent.Context):
    with open("./bot/plugins/nsmbe.txt", "r") as about_txt:
        text = about_txt.read()

    embed = hikari.Embed(title=f"About NSMBe", description=f"{text}", color="#1E92F4")
    embed.set_footer("Note: The NSMBe downloads on NSMB HD are no longer maintained")

    view = miru.View()
    view.add_item(UrlButton("Download NSMBe", "https://github.com/MammaMiaTeam/NSMB-Editor/releases"))

    message = await ctx.respond(embed=embed, components=view, ensure_message=True)
    await view.start(message=message)