import discord
from discord import app_commands
from discord import ui
import copy

# Define the poll buttons
class PollButton(ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.gray)
        
    async def callback(self, interaction):
        index = self.view.options.index(self.label)
        self.view.embed.remove_field(index)
        
        # Add the user to the list of voters and what they voted for. If this is their first vote, add the user to the dict.
        if interaction.user in self.view.user_votes:
            # If casting multiple votes is disabled...
            if (self.view.multi == False):
                # If the user clicks an option they have already pressed before....
                if self.label in self.view.user_votes[interaction.user]:
                    if self.view.recast == False:
                        await interaction.response.send_message(ephemeral=True, embed=discord.Embed(title="You already voted!", description="Recasting your vote is disabled!", color=0xff2600))
                        return
                    
                    else:
                        self.view.user_votes[interaction.user].remove(self.label)
                        if self.label in self.view.votes:
                            if (self.view.votes[self.label] - 1) < 0:
                                self.view.votes[self.label] == 0
                            else:
                                self.view.votes[self.label] -= 1
                        else:
                            self.view.votes.update({self.label: 0})
                                
                else:
                    self.view.user_votes.update({interaction.user: [self.label]})
            
                    # Increase the number of votes for the option. If this is the first vote, add the option to the dict.
                    if self.label in self.view.votes:
                        self.view.votes[self.label] += 1
                        
                    else:
                        self.view.votes.update({self.label: 1})
                        
            else: 
                if self.label in self.view.user_votes[interaction.user]:
                    if self.view.recast == False:
                        await interaction.response.send_message(ephemeral=True, embed=discord.Embed(title="You already voted!", description="Recasting your vote is disabled!", color=0xff2600))
                        return
                    
                    # If recasting is allowed, remove the old vote
                    else:
                        self.view.user_votes[interaction.user].remove(self.label)
                        if self.label in self.view.votes:
                            if (self.view.votes[self.label] - 1) < 0:
                                self.view.votes[self.label] == 0
                            else:
                                self.view.votes[self.label] -= 1
                
                # Since multiple votes are allowed, if the user has not voted for this option, add it to the votes
                else:
                    self.view.user_votes[interaction.user].append(self.label)
                
                    if self.label in self.view.votes:
                        self.view.votes[self.label] += 1
                        
                    else:
                        self.view.votes.update({self.label: 1})
        
        else:
            self.view.user_votes.update({interaction.user: [self.label]})
            
            # Increase the number of votes for the option. If this is the first vote, add the option to the dict.
            if self.label in self.view.votes:
                self.view.votes[self.label] += 1
                
            else:
                self.view.votes.update({self.label: 1})
            
        self.view.embed.insert_field_at(index=index ,name=f"Total Votes for: {self.label}", value=f"{self.view.votes[self.label]}", inline=True)
        print(f"Votes: {self.view.votes}\nUser Votes: {self.view.user_votes}")
        await interaction.response.edit_message(view=self.view, embed=self.view.embed)
        
    
    
    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        embed=discord.Embed(title="Something went wrong!", description=error, color=0xff2600)
        await interaction.response.send_message(ephemeral=True, embed=embed)

# Define the View for the poll
class PollView(ui.View):
    def __init__(self, multi, recast, options, poll_embed):
        super().__init__(timeout=None)
        self.multi = multi
        self.recast = recast
        self.options = options
        self.votes = {}
        self.user_votes = {}
        self.embed = poll_embed
        
        for option in self.options:
            self.add_item(PollButton(option))
            
    
    
    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        embed=discord.Embed(title="Something went wrong!", description=error, color=0xff2600)
        await interaction.response.send_message(ephemeral=True, embed=embed)

# Define a modal for creating options
class OptionModal(ui.Modal, title="Creating an option"):
    def __init__(self, view):
        super().__init__()
        self.original_view = view
    
    # First modal input: name of the poll
    option = ui.TextInput(
        label='Option Name',
        placeholder='Name of the option goes here...',
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        # If there are 19 options, disable the abilty to add more options (Discord limits us to 20 options)
        if len(self.original_view.options_list) == 19:
            for child in self.original_view.children:
                if child.label == "Add Option":
                    self.original_view.children[self.original_view.children.index(child)].disabled = True
                    
        for child in self.original_view.children:
            if child.label == "Remove Option":
                self.original_view.children[self.original_view.children.index(child)].disabled = False
            
            if child.label == "Finalize Poll":
                self.original_view.children[self.original_view.children.index(child)].disabled = False
        
        # Add the option to the list and update the embed
        self.original_view.options_list.append(self.option.value)
        self.original_view.options_embed.add_field(name=f"Option {len(self.original_view.options_list)}", value=f"{self.option.value}", inline=False)
        await interaction.response.edit_message(view=self.original_view, embed=self.original_view.options_embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        embed=discord.Embed(title="Something went wrong!", description=error, color=0xff2600)
        await interaction.response.send_message(ephemeral=True, embed=embed)

# Define a dropdown for removing options
class OptionsRemovalDropdown(ui.Select):
    def __init__(self, options_view):
        self.options_view = options_view

        # Make a list to hold the options
        options = []
        
        # Now, populate the list
        i = 0
        j = 1
        for option in self.options_view.options_list:
            options.append(discord.SelectOption(label=f"Option {j}", description=f"{option}", value=i))
            i += 1
            j += 1
        
        super().__init__(placeholder='Select options to remove...', min_values=1, max_values=len(self.options_view.options_list), options=options)

    async def callback(self, interaction: discord.Interaction):
        temp_options = copy.copy(self.options_view.options_list)
        options_to_remove = []
        final_options = []
        
        # Get the options to remove
        for option in self.values:
            options_to_remove.append(temp_options[int(option)])
        
        # Remove the options from the list
        for option in temp_options:
            if option not in options_to_remove:
                final_options.append(option)
        
        # Update the list
        self.options_view.options_list = final_options
        
        # Now, rebuild the embed
        self.options_view.options_embed.clear_fields()
        i = 1
        for option in final_options:
            self.options_view.options_embed.add_field(name=f"Option {i}", value=f"{option}", inline=False)
            i += 1
            
        if len(self.options_view.options_list) == 0:
            for child in self.options_view.children:
                if child.label == "Remove Option":
                    self.options_view.children[self.options_view.children.index(child)].disabled = True
                    
                if child.label == "Finalize Poll":
                    self.options_view.children[self.options_view.children.index(child)].disabled = True
                    
        for child in self.options_view.children:
            if child.label == "Add Option":
                self.options_view.children[self.options_view.children.index(child)].disabled = False
            
        await interaction.response.edit_message(embed=self.options_view.options_embed, view=self.options_view)
        
# Define a view for removing options
class OptionsRemovalView(ui.View):
    def __init__(self, previous_view):
        super().__init__()
        self.previous_view = previous_view
    
        self.add_item(OptionsRemovalDropdown(previous_view))

# Define the View that handels adding options to the poll
class OptionsView(ui.View):
    def __init__(self, name, description, channel, multi, recast):
        super().__init__()
        self.name = name
        self.description = description
        self.options_list = []
        self.options_embed = discord.Embed(title="List of Options", description="Here's the current list of your options")
        self.channel = channel
        self.multi = multi
        self.recast = recast
    
    @discord.ui.button(label='Add Option', style=discord.ButtonStyle.green)
    async def add(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(OptionModal(self))
        
    @discord.ui.button(label='Remove Option', style=discord.ButtonStyle.red, disabled=True)
    async def remove(self, interaction: discord.Interaction, button: discord.ui.Button):
        if len(self.options_list) == 0:
            button.disabled = True
        else:
            button.disabled = False
        await interaction.response.edit_message(view=OptionsRemovalView(self), embed=self.options_embed)
    
    @discord.ui.button(label='Finalize Poll', style=discord.ButtonStyle.blurple, disabled=True)
    async def finalize(self, interaction: discord.Interaction, button: discord.ui.Button):
        for button in self.children:
            button.disabled = True
            
        embed=discord.Embed(title="Success!", url=self.channel.jump_url ,description=f"Your poll has been sent to `#{self.channel}`", color=0x00f900)
        await interaction.response.edit_message(embed=embed)
        
        poll_embed=discord.Embed(title=self.name, description=self.description, color=0x00f900)
        
        for option in self.options_list:
            poll_embed.add_field(name=f"Total Votes for: {option}", value="0", inline=True)
        
        await self.channel.send(view=PollView(self.multi, self.recast, self.options_list, poll_embed), embed=poll_embed)
        self.stop()

# Define a simple View that gives us a confirmation menu
class Confirm(ui.View):
    def __init__(self, embed, name, description, channel, multi, recast):
        super().__init__()
        self.embed = embed
        self.name = name
        self.description = description
        self.channel = channel
        self.multi = multi
        self.recast = recast

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        options_view = OptionsView(self.name, self.description, channel=self.channel, multi=self.multi, recast=self.recast)
        await interaction.response.edit_message(view=options_view, embed=options_view.options_embed)

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        for button in self.children:
            button.disabled = True
        await interaction.response.edit_message(view=self, embed=self.embed)
        self.stop()

class Poll(ui.Modal, title="Create a Poll"):
    def __init__(self, channel, multi, recast):
        super().__init__()
        self.channel = channel
        self.multi = multi
        self.recast = recast
    
    # First modal input: name of the poll
    name = ui.TextInput(
        label='Poll Name',
        placeholder='Name of the poll goes here...',
    )
    
    # Second modal input: description of the poll
    description = ui.TextInput(
        label='Optional description of your poll',
        style= discord.TextStyle.long,
        placeholder='Type your description here...',
        required=False,
        max_length=300,
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        embed=discord.Embed(title="Poll Check", description='Everything look good?', color=0xfffb00)
        embed.add_field(name="Name", value=self.name, inline=False)
        if self.description.value != "":
            embed.add_field(name="Description", value=self.description, inline=False)
        embed.add_field(name="Channel", value=f"Your poll will be sent to: `#{self.channel}`", inline=True)
        embed.add_field(name="Multi-casting", value=f"Casting multiple votes is set to: `{self.multi}`", inline=True)
        embed.add_field(name="Recasting", value=f"Recasting votes is set to: `{self.recast}`", inline=True)
        view = Confirm(embed, name=self.name, description=self.description, channel=self.channel, multi=self.multi, recast=self.recast)
        await interaction.response.send_message(ephemeral=True, view=view, embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        embed=discord.Embed(title="Something went wrong!", description=error, color=0xff2600)
        await interaction.response.send_message(ephemeral=True, embed=embed)

def define_slash(client):
    @client.tree.command(name="poll", description="Generate a poll")
    @app_commands.describe(
        channel="The channel to send the poll in",
        multi="Whether or not the poll is multiple choice", 
        recast="Whether or not a vote can be recast"
    )
    async def poll( interaction, channel: discord.TextChannel, multi: bool, recast: bool):
        await interaction.response.send_modal(Poll(channel, multi, recast))