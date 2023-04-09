import crescent
import hikari
import miru
from __main__ import Database

plugin = crescent.Plugin[hikari.GatewayBot, Database]()


class MyModal(miru.Modal):
    def __init__(self, view, title: str):
        super().__init__(title)
        self.view = view

    name = miru.TextInput(label="Title", placeholder="Type a title", required=True, max_length=256)
    bio = miru.TextInput(label="Announcement", placeholder="Type a message to announce",
                         style=hikari.TextInputStyle.PARAGRAPH, required=True, max_length=4000)

    # The callback function is called after the user hits 'Submit'
    async def callback(self, ctx: miru.ModalContext) -> None:
        # You can also access the values using ctx.values, Modal.values, or use ctx.get_value_by_id()
        self.view.title = self.name.value
        self.view.message = self.bio.value
        self.view.stop()
        await ctx.defer()


class ModalView(miru.View):
    channel = None
    mentions = None
    title = None
    message = None

    @miru.channel_select(channel_types=[hikari.ChannelType.GUILD_TEXT, hikari.ChannelType.GUILD_NEWS], placeholder="Channel to send the message to",
                         max_values=1)
    async def channel_select(self, select: miru.TextSelect, ctx: miru.ViewContext):
        self.channel = select.values[0]
        if self.mentions is not None:
            for child in self.children:
                if child.custom_id == "announce_modal_present":
                    child.disabled = False
        await ctx.edit_response(components=self)

    @miru.role_select(placeholder="Roles to ping", min_values=1, max_values=5)
    async def role_select(self, select: miru.RoleSelect, ctx: miru.ViewContext):
        self.mentions = select.values
        if self.channel is not None:
            for child in self.children:
                if child.custom_id == "announce_modal_present":
                    child.disabled = False
        await ctx.edit_response(components=self)

    @miru.button(label="Let's make the announcement!", style=hikari.ButtonStyle.PRIMARY,
                 disabled=True, custom_id="announce_modal_present")
    async def modal_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        modal = MyModal(title="Announcement", view=self)
        await ctx.respond_with_modal(modal)
        sent_embed = hikari.Embed(title="Modal sent!",
                                  description="When you see this, your announcement should be live")
        await ctx.edit_response(components=None, embed=sent_embed)


@plugin.include
@crescent.command(name="announce", description="Post an announcement")
class SayCommand:
    anonymous = crescent.option(bool, default=False)

    async def callback(self, ctx: crescent.Context) -> None:
        embed = hikari.Embed(title=f"So, you want to make an announcement?",
                             description=f"Pick a channel you want to make the announcement in and let's go!"
                                         f" (You'll be presented with a Modal to make the announcement)",
                             color="#2f3136")
        view = ModalView(timeout=None)

        message = await ctx.respond(components=view, ensure_message=True, embed=embed, ephemeral=True)
        await view.start(message)
        await view.wait()

        embed = hikari.Embed(title=f"{view.title}", description=f"{view.message}")

        if not self.anonymous:
            embed.set_footer(text=f"Author: {ctx.user.username}", icon=ctx.user.avatar_url)
        else:
            embed.set_footer(text=f"Author: NSMB Central Admin",
                             icon="https://cdn.discordapp.com/attachments/1019800557776556092/1044115750476075041/"
                                  "NSMBCentral_Animated.gif")

        pings = ""
        for role in view.mentions:
            pings += role.mention + " "
        await ctx.app.rest.create_message(int(view.channel), embed=embed, role_mentions=True, content=pings)
