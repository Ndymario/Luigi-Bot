import discord
from discord.ui import View, Button

class PollButton(discord.ui.Button):
    def __init__(self, label, emoji=None):
        super().__init__(label=label, style=discord.ButtonStyle.gray, emoji=emoji)

    def update_votes(self):
        vote_list = []
        votes = self.view.reaction_log.values()
        
        for option in self.view.children:
            if option.custom_id == "end":
                continue
            label = option.label
            count = sum(label in vote for vote in votes)
            vote_list.append(f"{label}: {count}")

        content = "\n".join(vote_list)

        return content

    async def callback(self, interaction):
        # If multiple votes are allowed and recasting is allowed, then "toggle" a person's vote
        if ((self.view.multi == True) and (self.view.recast == True)):
            if ((interaction.user.id in self.view.reaction_log.keys()) and (self.label in self.view.reaction_log[interaction.user.id])):
                self.view.reaction_log[interaction.user.id].remove(self.label)
                await interaction.response.edit_message(content=self.update_votes(), embeds=interaction.message.embeds)
                await interaction.followup.send(content=f"You have removed your vote for `{self.label}`", ephemeral=True)
            elif ((interaction.user.id in self.view.reaction_log.keys()) and not (self.label in self.view.reaction_log[interaction.user.id])):
                self.view.reaction_log[interaction.user.id].append(self.label)
                await interaction.response.edit_message(content=self.update_votes(), embeds=interaction.message.embeds)
                await interaction.followup.send(content=f"You have casted your vote for `{self.label}`", ephemeral=True)
            else:
                self.view.reaction_log.update({interaction.user.id: [self.label]})
                await interaction.response.edit_message(content=self.update_votes(), embeds=interaction.message.embeds)
                await interaction.followup.send(content=f"You have casted your vote for `{self.label}`", ephemeral=True)
        
        # If multiple votes are allowed, but recasting is not allowed, then lock in the person's vote
        elif ((self.view.multi == True) and (self.view.recast == False)):
            if interaction.user.id in self.view.reaction_log.keys():
                if self.label not in self.view.reaction_log[interaction.user.id]:
                    self.view.reaction_log[interaction.user.id].append(self.label)
                    await interaction.response.edit_message(content=self.update_votes(), embeds=interaction.message.embeds)
                    await interaction.followup.send(content=f"You have casted your vote for `{self.label}`", ephemeral=True)
                else:
                    await interaction.response.send_message(content=f"You have already voted for {self.label}! (Removing your vote was not allowed)", ephemeral=True)
            else:
                self.view.reaction_log.update({interaction.user.id: [self.label]})
                await interaction.response.edit_message(content=self.update_votes(), embeds=interaction.message.embeds)
                await interaction.followup.send(content=f"You have casted your vote for `{self.label}`", ephemeral=True)

        # If multiple votes are not allowed, but recasting is allowed then just prevent a user from casting more than one vote
        elif ((self.view.multi == False) and (self.view.recast == True)):
            if ((interaction.user.id in self.view.reaction_log.keys())):
                old = self.view.reaction_log[interaction.user.id]
                self.view.reaction_log.pop(interaction.user.id)
                await interaction.response.edit_message(content=self.update_votes(), embeds=interaction.message.embeds)
                await interaction.followup.send(content=f"You have removed your vote for `{old}`", ephemeral=True)
            else:
                self.view.reaction_log.update({interaction.user.id: [self.label]})
                await interaction.response.edit_message(content=self.update_votes(), embeds=interaction.message.embeds)
                await interaction.followup.send(content=f"You have casted your vote for `{self.label}`", ephemeral=True)

        # If multiple votes are not allowed and recasting is not allowed, then lock in the first vote as the final vote
        elif ((self.view.multi == False) and (self.view.recast == False)):
            if ((interaction.user.id in self.view.reaction_log.keys())):
                await interaction.response.send_message(content=f"You have already voted in this poll! (You have previously voted `{self.view.reaction_log[interaction.user.id]}`)", ephemeral=True)
            else:
                self.view.reaction_log.update({interaction.user.id: [self.label]})
                await interaction.response.edit_message(content=self.update_votes(), embeds=interaction.message.embeds)
                await interaction.followup.send(content=f"You have casted your vote for `{self.label}`", ephemeral=True)

        else:
            await interaction.response.send_message(content=f"Something went wrong, try voting again later!", ephemeral=True)

class EndPollButton(discord.ui.Button):
    def __init__(self, style=discord.ButtonStyle.red, label="End Poll", custom_id="end"):
        super().__init__(style=style, label = label, custom_id = custom_id)

    async def callback(self, interaction):
        if self.view.owner == interaction.user.id:
            self.view.clear_items()
            await interaction.response.edit_message(content=interaction.message.content, view=None, embeds=interaction.message.embeds)
        else:
            await interaction.response.send_message(content="You can't end someone else's poll!", ephemeral=True)

class PollMessage(discord.ui.View):
    def __init__(self, multi, recast, owner):
        self.reaction_log = {}
        self.multi = multi
        self.recast = recast
        self.owner = owner
        super().__init__()

class PollOptionModal(discord.ui.Modal):
    def __init__(self, view) -> None:
        self.view = view
        super().__init__("Creating an option to vote on")
        self.add_item(discord.ui.InputText(style=discord.InputTextStyle.short, custom_id="option_name", min_length=1, max_length=80, label="Type the name of your option"))

    async def callback(self, interaction):
        if len(self.view.option_list) == 19:
            await interaction.response.send_message(content=f"You have the maximum number of options! (19)", ephemeral=True)
            return
        for option in self.view.option_list:
            if option.label == self.children[0].value:
                await interaction.response.send_message(content=f"You already have an option named: {self.children[0].value}", ephemeral=True)
                return
        self.view.option_list.append(PollButton(self.children[0].value))
        await interaction.response.send_message(content=f"Added option {self.children[0].value}", ephemeral=True)

class PollView(discord.ui.View):
    def __init__(self, *items, timeout: 180, channel, embed, multi, recast):
        self.channel = channel
        self.embed = embed
        self.multi = multi
        self.recast = recast
        self.option_list = []
        super().__init__(*items, timeout=timeout)

    # Confirm button
    @discord.ui.button(style=discord.ButtonStyle.green, label="Looks good!", custom_id="confirm")
    async def poll_confirm_callback(self, button, interaction):
        poll = PollMessage(self.multi, self.recast, interaction.user.id)
        try:
            for button in self.option_list:
                poll.add_item(button)
            poll.add_item(EndPollButton())
            await self.channel.send(embed=self.embed, view=poll)
            await interaction.response.edit_message(content=f"Poll created in `#{self.channel.name}`!", view=None, embed=None)
        except discord.errors.HTTPException:
            await interaction.response.edit_message(content="Oh no, your poll failed to create...", view=None, embed=None)
    
    # Add vote option
    @discord.ui.button(style=discord.ButtonStyle.blurple, label="Add Vote Option", custom_id="add")
    async def add_callback(self, button, interaction):
        await interaction.response.send_modal(PollOptionModal(self))

    # View vote options
    @discord.ui.button(style=discord.ButtonStyle.blurple, label="View Vote Option", custom_id="view")
    async def view_callback(self, button, interaction):
        await interaction.response.send_message(f"Here are your options so far: ", ephemeral=True)

    # Cancel button
    @discord.ui.button(style=discord.ButtonStyle.red, label="Nevermind", custom_id="cancel")
    async def poll_cancel_callback(self, button, interaction):
        await interaction.response.edit_message(content="Poll has been discarded", view=None, embed=None)

class PollModal(discord.ui.Modal):
    def __init__(self, channel, multi, recast) -> None:
        self.channel = channel
        self.multi = multi
        self.recast = recast
        super().__init__("Let's create a poll")
        self.add_item(discord.ui.InputText(style=discord.InputTextStyle.short, custom_id="poll_name", min_length=2, label="Type the name of your poll"))
        self.add_item(discord.ui.InputText(style=discord.InputTextStyle.paragraph, custom_id="poll_body", min_length=2, label="Type what your poll is about"))

    async def callback(self, interaction):
        embed = discord.Embed(title=self.children[0].value, description=self.children[1].value)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message("Does your poll look good to go?", ephemeral=True, embed=embed, view=PollView(timeout=None, channel=self.channel, embed=embed, multi=self.multi, recast=self.recast))

def define_slash(guild_ids, slash):
    @slash.slash_command(name="about", description="Some information about Luigi Bot", guild_ids=guild_ids)
    async def about(interaction):
        # Load the about info from a seperate .txt file
        about_txt = open("bot_commands/about.txt", "r")
        about = about_txt.read()
        about_txt.close()

        # Build the embed
        about_embed=discord.Embed(title="About me!", description=about, color=0x00f900)
        about_embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        about_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/634582132634943508/852749724583067648/King_Mario.png")

        # Create the url buttons
        yt_button = Button(style=discord.ButtonStyle.gray, label="Ndymario's YouTube", url="https://www.youtube.com/channel/UC0_ii78SpO_RPM82TeEibBw")
        git_button = Button(style=discord.ButtonStyle.gray, label="Ndymario's GitHub", url="https://github.com/Ndymario")

        # Construct the View
        view = View()
        view.add_item(yt_button)
        view.add_item(git_button)

        # Respond to the command
        await interaction.respond(embed=about_embed, view=view)

    @slash.slash_command(name="poll", description="Generate a poll", guild_ids=guild_ids)
    async def poll(
        interaction, 
        channel: discord.Option(discord.TextChannel, "What channel should the poll be posted to", required=True),
        multi: discord.Option(bool, "Can a user vote more than one option?", required=True),
        recast: discord.Option(bool, "Can a user re-cast their vote?", required=True)
        ):
        await interaction.response.send_modal(PollModal(channel, multi, recast))