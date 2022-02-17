import discord

from mongo_db.mongo_db import create_character, get_chars, get_total_char

class CharNameModal(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__("Name your character!")
        self.add_item(discord.ui.InputText(style=discord.InputTextStyle.short, custom_id="char_name", min_length=2, label="Type the name of your character here!"))

    async def callback(self, interaction):
        global character_dict
        character_dict[interaction.user.name].char_name = self.children[0].value
        await interaction.response.send_message("You entered: " + self.children[0].value, ephemeral=True)

class CharURLModal(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__("Name your character!")
        self.add_item(discord.ui.InputText(style=discord.InputTextStyle.short, custom_id="char_avatar", min_length=2, label="Paste a link to your character's avatar here!"))

    async def callback(self, interaction):
        global character_dict
        character_dict[interaction.user.name].char_avatar = self.children[0].value
        await interaction.response.send_message(self.children[0].value, ephemeral=True)

class CreateView(discord.ui.View):
    # Stat options
    hp_option = discord.SelectOption(label="HP", value="hp", description="How many hits you can take before you fall (+5)")
    sp_option = discord.SelectOption(label="SP", value="sp", description="Points used for performing special attacks (+5)")
    pow_option = discord.SelectOption(label="Power", value="power", description="How much damage you deal (+2)")
    def_option = discord.SelectOption(label="Shield", value="shield", description="How damage resistant you are (+2)")
    spd_option = discord.SelectOption(label="Speed", value="spd", description="How fast you are (determines turn order) (+2)")
    lk_option = discord.SelectOption(label="Luck", value="lk", description="How lucky you are (+1)")

    stat_list = [hp_option, sp_option, pow_option, def_option, spd_option, lk_option]

    # Name Edit Name button
    @discord.ui.button(style=discord.ButtonStyle.gray, label="Name", custom_id="name_input")
    async def edit_name_button_callback(self, button, interaction):
        char_modal = CharNameModal()
        await interaction.response.send_modal(char_modal)

    # Name Edit URL button
    @discord.ui.button(style=discord.ButtonStyle.gray, label="Avatar", custom_id="url_input")
    async def edit_url_button_callback(self, button, interaction):
        char_modal = CharURLModal()
        await interaction.response.send_modal(char_modal)

    # Confirm button
    @discord.ui.button(style=discord.ButtonStyle.green, label="Make my Character!", custom_id="confirm")
    async def confirm_button_callback(self, button, interaction):
        character_request_embed=discord.Embed(title="Creating your character!", description="Sit tight while Luigi Bot creates your character...", color=0xfffb00)
        character_request_embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        # Give us time to process the request
        await interaction.response.defer()
        check_embed = character_check(interaction)
        await interaction.followup.edit_message(embed=check_embed, view=None, message_id=interaction.message.id)

    # Cancel button
    @discord.ui.button(style=discord.ButtonStyle.red, label="Cancel", custom_id="cancel")
    async def button_callback(self, button, interaction):
        global character_dict
        embed=discord.Embed(title="Oops, wrong button...", description="Looks like you changed your mind. (Use the command again if you'd like to make a new character after all!)", color=0xff2600)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        character_dict.pop(interaction.user.name)
        await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.select(custom_id="stat_select", min_values=1, max_values=1, placeholder="Select a starting stat bonus.", options=stat_list)
    async def stat_callback(self, select, interaction):
        global character_dict
        character_dict[interaction.user.name].char_preferred_stat = self.children[4].values[0]

# Subclassing View for our UI's
class CreateConfrim(discord.ui.View):
    # Confrim button
    @discord.ui.button(style=discord.ButtonStyle.green, label="Let's go!", custom_id="create_confirm")
    async def confirm_button_callback(self, button, interaction):
        global character_dict
        embed=discord.Embed(title="Build-A-Char", description="Go ahead and choose what you would like to make your character be. Press submit when ready!", color=0x00f900)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        character = NewChar()
        character_dict[interaction.user.name] = character
        create_view = CreateView()
        await interaction.response.edit_message(view=create_view, embed=embed)

    # Cancel button
    @discord.ui.button(style=discord.ButtonStyle.red, label="Actually, never mind.", custom_id="create_cancel")
    async def cancel_button_callback(self, button, interaction):
        embed=discord.Embed(title="My party is fine as is...", description="Looks like you changed your mind. (Use the command again if you'd like to make a new character after all!)", color=0xff2600)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        await interaction.response.edit_message(embed=embed, view=None)

# Button to return after seeing your stats
char_return = discord.ui.Button(style=discord.ButtonStyle.gray, label="Sweet, take me back", custom_id="char_return")

class NewChar():
    char_name = ""
    char_avatar = ""
    char_preferred_stat = ""
    missing_components = []

character_dict = {}

# Slash command descriptions
challenge_description = "Challenge someone to a battle (Note: no EXP will be gained, nor will items used remain used)"

# Slash command options
#challenge_user_option = discord.Option(input_type="6", description="The person you wish to battle!", required=True, name="user")
#challenge_options = [challenge_user_option]

def define_slash(guild_ids, bot):
    #@bot.slash_command(name = "challenge", description = challenge_description, options=challenge_options, guild_ids = guild_ids)
    #async def challenge(ctx, user: discord.Member):
    #    await ctx.send(content=f"You challenged {user.mention}!")

    @bot.slash_command(name="create", description="Create a new character with Luigi Bot?", guild_ids=guild_ids)
    async def create(ctx):
        character_create_embed=discord.Embed(title="Creating Character", description="Another character, huh? Let's get started!", color=0x00f900)
        character_create_embed.set_author(name=ctx.interaction.user.name, icon_url=ctx.interaction.user.display_avatar.url)
        create_view = CreateConfrim()
        await ctx.respond(embed=character_create_embed, view=create_view)

    @bot.slash_command(name="list", description="List the characters you have made with Luigi Bot.",guild_ids=guild_ids)
    async def list(ctx):
        character_list_embed=discord.Embed(title="Time for a head count...", description="Here's a list of your characters", color=0x00f900)
        character_list_embed.set_author(name=ctx.user.name, icon_url=ctx.user.display_avatar.url)
        result = get_chars(ctx.user.name)
        for character in result[1]:
            character_list_embed.add_field(name=character.name, value=f"Level: {character.level}\nEXP: {character.exp}\nHP: {character.hp}/{character.max_hp}\nSP: {character.sp}/{character.max_sp}\nPower: {character.power}\nShield: {character.shield}\nSpeed: {character.spd}\nLuck: {character.lk}", inline=True)
        await ctx.send(embed=character_list_embed, hidden=True)

# Create a function that checks if the requested character is valid
def character_check(interaction):

    failed = False

    character_failed_embed=discord.Embed(title="Oops! You forgot something.", description="It looks like you haven't defined these things:", color=0xff2600)
    character_failed_embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)

    character_success_embed=discord.Embed(title="Great Success!", description="You're all set! GL:HF!", color=0xff2600)
    character_success_embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)

    global character_dict

    if(character_dict[interaction.user.name].char_name == ""):
        character_dict[interaction.user.name].missing_components.append("Name")
        failed = True
    
    if(character_dict[interaction.user.name].char_avatar == ""):
        character_dict[interaction.user.name].missing_components.append("Avatar")
        failed = True

    if ("http" not in character_dict[interaction.user.name].char_avatar):
        character_dict[interaction.user.name].missing_components.append("Valid URL")
        failed = True

    if (character_dict[interaction.user.name].char_preferred_stat == ""):
        character_dict[interaction.user.name].missing_components.append("Preffered Stat")
        failed = True

    if (failed):
        for missing in character_dict[interaction.user.name].missing_components:
            character_failed_embed.add_field(name=f"Missing {missing}:", value=f"You are missing a {missing}", inline=False)
        character_dict.pop(interaction.user.name)
        return character_failed_embed
    else:
        create_character(interaction.user.name, character_dict[interaction.user.name].char_name, character_dict[interaction.user.name].char_avatar, get_total_char(), character_dict[interaction.user.name].char_preferred_stat)
        character_dict.pop(interaction.user.name)
        return character_success_embed

