import crescent
import hikari
import miru

plugin = crescent.Plugin()


class ConfirmationView(miru.View):

    def __init__(self, post):
        super().__init__(timeout=None)
        self.post = post

    @miru.button(label="Approve", style=hikari.ButtonStyle.SUCCESS)
    async def approve_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await ctx.edit_response(content=f"Post approved by {ctx.user.mention}", components=None)
        await ctx.app.rest.create_message(channel=901105564522782751, embed=self.post)

    @miru.button(label="Deny", style=hikari.ButtonStyle.DANGER)
    async def deny_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await ctx.edit_response(content=f"Post denied by {ctx.user.mention}", components=None)


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
    channel = 1078876445734096968
    title = None
    message = None

    @miru.button(label="Create a post!", style=hikari.ButtonStyle.PRIMARY, custom_id="mod_announce_modal_present")
    async def modal_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        modal = MyModal(title="Mod Announcement", view=self)
        await ctx.respond_with_modal(modal)
        sent_embed = hikari.Embed(title="Request sent!",
                                  description="The admin have received your request for a mod announcement!")
        await ctx.edit_response(components=None, embed=sent_embed)


@plugin.include
@crescent.command(name="mod-announce", description="Post an announcement")
async def mod_announce(ctx: crescent.Context) -> None:
    embed = hikari.Embed(title=f"So, you want to make an announcement?",
                         description=f"Click the button to get started!\n"
                                     f"(You'll be presented with a Modal to make the announcement)",
                         color="#2f3136")
    view = ModalView(timeout=None)

    message = await ctx.respond(components=view, ensure_message=True, embed=embed, ephemeral=True)
    await view.start(message)
    await view.wait()

    embed = hikari.Embed(title=f"{view.title}", description=f"{view.message}")
    embed.set_footer(text=f"Author: {ctx.user.username}", icon=ctx.user.avatar_url)

    approve_view = ConfirmationView(embed)

    message = await ctx.app.rest.create_message(int(view.channel), embed=embed, components=approve_view)
    await approve_view.start(message)
