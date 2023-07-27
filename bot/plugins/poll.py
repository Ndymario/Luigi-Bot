import os

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
    bio = miru.TextInput(label="Poll", placeholder="Type what the poll is about",
                         style=hikari.TextInputStyle.PARAGRAPH, required=True, max_length=4000)

    # The callback function is called after the user hits 'Submit'
    async def callback(self, ctx: miru.ModalContext) -> None:
        # You can also access the values using ctx.values, Modal.values, or use ctx.get_value_by_id()
        self.view.title = self.name.value
        self.view.message = self.bio.value
        self.view.stop()
        await ctx.defer()


class VoteView(miru.View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.yes = 0
        self.no = 0
        self.voters = {}

    @miru.button(label="0", style=hikari.ButtonStyle.SECONDARY,
                 emoji=hikari.Emoji.parse("<:mariothumbsup:471792643882352641>"), custom_id="yes_button")
    async def yes_counter_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        if ctx.author.id not in self.voters:
            self.voters[ctx.author.id] = "yes"
            self.yes += 1
            button.label = f"{self.yes}"

        if self.voters[ctx.author.id] == "no":
            for item in self.children:
                if item.custom_id == "no_button":
                    self.no -= 1
                    item.label = f"{self.no}"
            self.voters[ctx.author.id] = "yes"
            self.yes += 1
            button.label = f"{self.yes}"

        await ctx.edit_response(components=self)

    @miru.button(label="0", style=hikari.ButtonStyle.SECONDARY,
                 emoji=hikari.Emoji.parse("<:mariothumbsdown:1114068712593559642>"), custom_id="no_button")
    async def no_counter_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        if ctx.author.id not in self.voters:
            self.voters[ctx.author.id] = "no"
            self.no += 1
            button.label = f"{self.no}"

        if self.voters[ctx.author.id] == "yes":
            for item in self.children:
                if item.custom_id == "yes_button":
                    self.yes -= 1
                    item.label = f"{self.yes}"
            self.voters[ctx.author.id] = "no"
            self.no += 1
            button.label = f"{self.no}"

        await ctx.edit_response(components=self)

    @miru.button(label="End poll", style=hikari.ButtonStyle.DANGER, custom_id="stop_button")
    async def stop_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        member = await ctx.app.rest.fetch_member(ctx.guild_id, ctx.author.id)
        if 603298209011466252 in member.role_ids:
            for item in self.children:
                item.disabled = True
            self.stop()

            yes_votes = ""
            no_votes = ""

            for voter in self.voters:
                if self.voters[voter] == "yes":
                    yes_votes += f"<@{voter}>\n"

                if self.voters[voter] == "no":
                    no_votes += f"<@{voter}>\n"

            if yes_votes == "":
                yes_votes = "(No one was in favor)"

            if no_votes == "":
                no_votes = "(No one was opposed)"

            results = hikari.Embed(title="Poll Results",
                                   description=f"The results for [this]({ctx.message.make_link(int(os.getenv('GUILD_ID')))})"
                                               f" poll are in!")
            results.add_field(name=f"In Favor ({self.yes})", value=yes_votes, inline=True)
            results.add_field(name=f"Opposed ({self.no})", value=no_votes, inline=True)

            results_msg = await ctx.message.respond(content=results)
            embed = ctx.message.embeds[0]
            embed.add_field(name="Results are in!", value=f"[Here they are.]({results_msg.make_link(int(os.getenv('GUILD_ID')))})")
            embed.set_footer(f"This poll is now closed, thanks for voting!")
            await ctx.edit_response(embed=embed, components=self)

        else:
            await ctx.edit_response(components=self, user_mentions=False)


class ModalView(miru.View):
    channel = None
    mentions = None
    title = None
    message = None

    @miru.channel_select(channel_types=[hikari.ChannelType.GUILD_TEXT, hikari.ChannelType.GUILD_NEWS],
                         placeholder="Channel to send the message to",
                         max_values=1)
    async def channel_select(self, select: miru.TextSelect, ctx: miru.ViewContext):
        self.channel = select.values[0]
        if self.mentions is not None:
            for child in self.children:
                if child.custom_id == "poll_present":
                    child.disabled = False
        await ctx.edit_response(components=self)

    @miru.role_select(placeholder="Roles to ping", min_values=1, max_values=5)
    async def role_select(self, select: miru.RoleSelect, ctx: miru.ViewContext):
        self.mentions = select.values
        if self.channel is not None:
            for child in self.children:
                if child.custom_id == "poll_present":
                    child.disabled = False
        await ctx.edit_response(components=self)

    @miru.button(label="Let's make the poll!", style=hikari.ButtonStyle.PRIMARY,
                 disabled=True, custom_id="poll_present")
    async def modal_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        modal = MyModal(title="Poll", view=self)
        await ctx.respond_with_modal(modal)
        sent_embed = hikari.Embed(title="Modal sent!",
                                  description="When you see this, your poll should be live")
        await ctx.edit_response(components=None, embed=sent_embed)


@plugin.include
@crescent.command(name="poll", description="Make a poll")
class PollCommand:
    async def callback(self, ctx: crescent.Context) -> None:
        embed = hikari.Embed(title=f"So, you want to make a poll?",
                             description=f"Pick a channel you want to make the poll in and let's go!"
                                         f" (You'll be presented with a Modal to make the poll)",
                             color="#2b2d31")
        view = ModalView(timeout=None)

        message = await ctx.respond(components=view, ensure_message=True, embed=embed, ephemeral=True)
        await view.start(message)
        await view.wait()

        embed = hikari.Embed(title=f"{view.title}", description=f"{view.message}", color="#2b2d31")

        pings = ""
        for role in view.mentions:
            pings += role.mention + " "

        vote = VoteView(timeout=None)
        message = await ctx.app.rest.create_message(int(view.channel), embed=embed, role_mentions=True, content=pings,
                                                    components=vote)
        await vote.start(message)
