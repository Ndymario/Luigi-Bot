import crescent
import hikari
import miru
import os
from miru.ext import nav
from __main__ import Database

plugin = crescent.Plugin[hikari.GatewayBot, Database]()


class WelcomeView(miru.View):
    @miru.button(label="Rules", style=hikari.ButtonStyle.PRIMARY, emoji="📜", custom_id="rules_button")
    async def rules_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        rules = []
        cur_rule = 0
        for rule in os.listdir("./bot/plugins/rules"):
            cur_rule += 1
            with open(f"./bot/plugins/rules/{cur_rule}.txt", "r") as rule_txt:
                rules.append(hikari.Embed(title=f"{rule_txt.readline()}", description=f"{rule_txt.readline()}",
                                          color="#2b2d31"))
        navigator = nav.NavigatorView(pages=rules)
        await navigator.send(to=ctx.interaction, ephemeral=True)

    @miru.button(label="Roles", style=hikari.ButtonStyle.SECONDARY, emoji="🪪", custom_id="roles_button")
    async def role_list(self, button: miru.Button, ctx: miru.ViewContext):
        with open("./bot/plugins/roles/admin.txt", "r") as roles_txt:
            admin_txt = roles_txt.read()

        with open("./bot/plugins/roles/identity.txt", "r") as roles_txt:
            identity_txt = roles_txt.read()

        with open("./bot/plugins/roles/ping.txt", "r") as roles_txt:
            ping_txt = roles_txt.read()

        with open("./bot/plugins/roles/misc.txt", "r") as roles_txt:
            misc_txt = roles_txt.read()

        with open("./bot/plugins/roles/levels.txt", "r") as roles_txt:
            level_txt = roles_txt.read()

        admin = hikari.Embed(title=f"**__Administrative Roles__**", description=f"{admin_txt}", color="#2b2d31")
        admin.set_footer("Administrative roles are earned through trust, "
                         "and as such asking for them will only lower your chances of getting them.")

        identity = hikari.Embed(title=f"**__Identity Roles__**", description=f"{identity_txt}", color="#2b2d31")
        identity.set_footer("Proof may be requested for acquiring the modding roles.")

        mention = hikari.Embed(title=f"**__Mention Roles__**", description=f"{ping_txt}", color="#2b2d31")
        mention.set_footer("These roles are self-assigned.")

        misc = hikari.Embed(title=f"**__Miscellaneous Roles__**", description=f"{misc_txt}", color="#2b2d31")
        misc.set_footer("These roles are not given out.")

        misc = hikari.Embed(title=f"**__Level Roles__**", description=f"{level_txt}", color="#2b2d31")
        misc.set_footer("You can earn these by talking in chat. The EXP requirement is hidden until at least one person"
                        " has the role for some fun!")

        navigator = nav.NavigatorView(pages=[admin, identity, mention, misc])
        await navigator.send(to=ctx.interaction, ephemeral=True)

    @miru.text_select(placeholder="Optionally, assign yourself some mention roles!", min_values=0, max_values=5,
                      options=[
                          miru.SelectOption(label="Server Pings", emoji="📣",
                                            description="Receive a ping for *any* announcement"),
                          miru.SelectOption(label="Mod Updates", emoji="🎮",
                                            description="Receive a ping for mod related announcements"),
                          miru.SelectOption(label="Event Updates", emoji="🗣️",
                                            description="Receive a ping for any server event announcement"),
                          miru.SelectOption(label="Server Updates", emoji="🆕",
                                            description="Receive a ping for any server changes or updates"),
                          miru.SelectOption(label="Luigi Bot Updates", emoji="🤖",
                                            description="Receive a ping for any Luigi Bot updates")
                      ], custom_id="role_select")
    async def role_select(self, select: miru.RoleSelect, ctx: miru.ViewContext):
        roles = select.values
        role_map = {"Server Pings": "784515404202508358", "Mod Updates": "908837812583927900",
                    "Event Updates": "908838004699828294", "Server Updates": "908837906532167731",
                    "Luigi Bot Updates": "1078566718198272071"}

        if len(roles) != 0:
            role_list = []
            for role in roles:
                await ctx.app.rest.remove_role_from_member(guild=ctx.guild_id, user=ctx.user.id, role=role_map[role],
                                                           reason="Self-assigned role")
                await ctx.app.rest.add_role_to_member(guild=ctx.guild_id, user=ctx.user.id, role=role_map[role],
                                                      reason="Self-assigned role")
                role_list.append(role)

        else:
            for role in role_map:
                await ctx.app.rest.remove_role_from_member(guild=ctx.guild_id, user=ctx.user.id, role=role_map[role],
                                                           reason="Self-assigned role")


@plugin.include
@crescent.command(name="welcome", description="Creates the welcome message")
async def welcome(ctx: crescent.Context):
    content = "# Welcome!" \
            "\nWelcome to the central location for all things New Super Mario Bros. DS!" \
            "\n## Join the community" \
            "\n- Introduce yourself in <#751831145225912481>" \
            "\n- Say hello in <#399424476728655893>" \
            "\n## NSMB DS Modding" \
            "\nIf you need help on your project, or just want to talk about modifying the game, " \
            "check out the NSMB DS Modding Category." \
            "\n## Invite some friends" \
            "\nHere's an invite link that will never expire:" \
            "\nhttps://discord.gg/x7gr3M9"

    view = WelcomeView(timeout=None)

    await ctx.respond(ephemeral=True, content="Done.")
    message = await ctx.app.rest.create_message(content=content, channel=ctx.channel.id, components=view)
    await view.start(message)
