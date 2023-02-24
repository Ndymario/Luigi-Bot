import crescent
import hikari
import miru
from miru.ext import nav

plugin = crescent.Plugin()


@plugin.include
@crescent.command(name="roles", description="Show the list of server roles.")
async def roles(ctx: crescent.Context):
    with open("./bot/plugins/roles/admin.txt", "r") as roles_txt:
        admin_txt = roles_txt.read()

    with open("./bot/plugins/roles/identity.txt", "r") as roles_txt:
        identity_txt = roles_txt.read()

    with open("./bot/plugins/roles/ping.txt", "r") as roles_txt:
        ping_txt = roles_txt.read()

    with open("./bot/plugins/roles/misc.txt", "r") as roles_txt:
        misc_txt = roles_txt.read()

    admin = hikari.Embed(title=f"**__Administrative Roles__**", description=f"{admin_txt}", color="#1E92F4")
    admin.set_footer("Administrative roles are earned through trust, "
                     "and as such asking for them will only lower your chances of getting them.")

    identity = hikari.Embed(title=f"**__Identity Roles__**", description=f"{identity_txt}", color="#1E92F4")
    identity.set_footer("Proof may be requested for acquiring the modding roles.")

    mention = hikari.Embed(title=f"**__Mention Roles__**", description=f"{ping_txt}", color="#1E92F4")
    mention.set_footer("These roles are self-assigned with the /role command.")

    misc = hikari.Embed(title=f"**__Miscellaneous Roles__**", description=f"{misc_txt}", color="#1E92F4")
    misc.set_footer("These roles are not given out.")

    navigator = nav.NavigatorView(pages=[admin, identity, mention, misc])
    await navigator.send(to=ctx.interaction, ephemeral=True)
