import discord
from discord_slash.utils.manage_components import create_select, create_select_option, create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option
from mongo_db.mongo_db import create_character, get_chars, get_total_char

# List of buttons to create an action row for
create_confirm_buttons = [
            create_button(
                style=ButtonStyle.green,
                label="Let's go!",
                custom_id="create_confirm"
            ),
            create_button(
                style=ButtonStyle.red,
                label="Actually, never mind.",
                custom_id="create_cancel"
            )
          ]
# Create an action row for the buttons
create_confirm_row = create_actionrow(*create_confirm_buttons)

# Buttons to select for a new character
character_create_selections = [
            create_button(
                style=ButtonStyle.gray,
                label="Name",
                custom_id="char_name"
            ),
            create_button(
                style=ButtonStyle.gray,
                label="Avatar",
                custom_id="char_avatar"
            ),
            create_button(
                style=ButtonStyle.gray,
                label="Stored Stats",
                custom_id="char_stored"
            )
          ]

# Action row for the buttons
create_selection_row = create_actionrow(*character_create_selections)

# Buttons to confirm the creation of a new character
character_create_confirmation = [
            create_button(
                style=ButtonStyle.green,
                label="Submit Character",
                custom_id="char_confirm"
            ),
            create_button(
                style=ButtonStyle.red,
                label="Actually, nevermind",
                custom_id="char_giveup"
            )
          ]

create_confirmation_row = create_actionrow(*character_create_confirmation)

character_stat_select = create_select(
    options=[
        create_select_option("HP", value="hp", description="How many hits you can take before you fall (+5)"),
        create_select_option("SP", value="sp", description="Points used for performing special attacks (+5)"),
        create_select_option("Power", value="power", description="How much damage you deal (+2)"),
        create_select_option("Shield", value="shield", description="How damage resistant you are (+2)"),
        create_select_option("SPD", value="spd", description="How fast you are (determines turn order) (+2)"),
        create_select_option("LK", value="lk", description="How lucky you are (+1)"),
    ],
    placeholder="Select a starting stat bonus.",
    min_values=1,
    max_values=1,
    custom_id="stat_select"
)

create_stat_select = create_actionrow(character_stat_select)

# Buttons to confirm the creation of a new character
character_stored_return = [
            create_button(
                style=ButtonStyle.grey,
                label="Sweet, take me back",
                custom_id="char_return"
            )
          ]

create_return_row = create_actionrow(*character_stored_return)

class NewChar():
    char_name_wait = False
    char_avatar_wait = False
    char_name_user = ""
    char_name = ""
    char_avatar_user = ""
    char_avatar = ""
    char_preferred_stat = ""
    missing_components = []

character_dict = {}

def define_slash(guild_ids, slash):
    @slash.slash(name="challenge",
             description="Challenge someone to a battle (Note: no EXP will be gained, nor will items used remain used)",
             options=[
               create_option(
                 name="user",
                 description="The person you wish to battle!",
                 option_type=6,
                 required=True
               ),
               create_option(
                 name="hidden",
                 description="Should Luigi Bot log the fight in chat?",
                 option_type=5,
                 required=True
               )
             ], guild_ids=guild_ids)
    async def challenge(ctx, user: discord.Member, hidden: bool):
        if (hidden):
            await ctx.send(content=f"You challenged {user.mention}!", hidden=True)
        else:
            await ctx.send(content=f"You challenged {user.mention}!")

    @slash.slash(name="create", description="Create a new character with Luigi Bot!",guild_ids=guild_ids)
    async def create(ctx):
        character_create_embed=discord.Embed(title="Creating Character", description="Another character, huh? Let's get started!", color=0x00f900)
        character_create_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=character_create_embed, components=[create_confirm_row], hidden=True)

    @slash.slash(name="list", description="List the characters you have made with Luigi Bot.",guild_ids=guild_ids)
    async def list(ctx):
        character_list_embed=discord.Embed(title="Time for a head count...", description="Here's a list of your characters", color=0x00f900)
        character_list_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        result = get_chars(ctx.author.name)
        for character in result[1]:
            character_list_embed.add_field(name=character.name, value=f"Level: {character.level}\nEXP: {character.exp}\nHP: {character.hp}/{character.max_hp}\nSP: {character.sp}/{character.max_sp}\nPower: {character.power}\nShield: {character.shield}\nSpeed: {character.spd}\nLuck: {character.lk}", inline=True)
        await ctx.send(embed=character_list_embed, hidden=True)

    @slash.component_callback()
    async def create_confirm(ctx):
        global character_dict

        embed=discord.Embed(title="Build-A-Char", description="Go ahead and choose what you would like to make your character be. Press submit when ready!", color=0x00f900)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        character = NewChar()
        character_dict[ctx.author.name] = character
        await ctx.edit_origin(embed=embed, components=[create_selection_row, create_stat_select, create_confirmation_row])

    @slash.component_callback()
    async def char_confirm(ctx):
        character_request_embed=discord.Embed(title="Creating your character!", description="Sit tight while Luigi Bot creates your character...", color=0xfffb00)
        character_request_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        # Give us time to process the request
        await ctx.defer(edit_origin=True)
        check_embed = character_check(ctx)
        await ctx.edit_origin(embed=check_embed, components=[])

    @slash.component_callback()
    async def char_giveup(ctx):
        character_request_embed=discord.Embed(title="My party is fine as is...", description="Looks like you changed your mind. (Use the command again if you'd like to make a new character after all!)", color=0xff2600)
        character_request_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        # Give us time to process the request
        await ctx.edit_origin(embed=character_request_embed, components=[])

    @slash.component_callback()
    async def create_cancel(ctx):
        global character_dict
        embed=discord.Embed(title="Oops, wrong button...", description="Looks like you changed your mind. (Use the command again if you'd like to make a new character after all!)", color=0xff2600)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        character_dict.pop(ctx.author.name)
        await ctx.edit_origin(embed=embed, components=[])

    @slash.component_callback()
    async def char_name(ctx):
        global character_dict
        character_dict[ctx.author.name].char_name_user = ctx.author.name
        character_dict[ctx.author.name].char_name_wait = True
        await ctx.defer(hidden=True)
        await ctx.send("Send the name of your character in chat, and Luigi Bot will store it for you")

    @slash.component_callback()
    async def char_stored(ctx):
        embed=discord.Embed(title="Here's your character so far.", description="Here's everything you've stored for your character so far.", color=0xff2600)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        global character_dict

        if (character_dict[ctx.author.name].char_name == ""):
            embed.add_field(name="Stored Name:", value="[Nothing stored]", inline=False)
        else:
             embed.add_field(name="Stored Name:", value=character_dict[ctx.author.name].char_name, inline=False)

        if (character_dict[ctx.author.name].char_avatar == ""):
            embed.add_field(name="Stored Avatar:", value="[Nothing stored]", inline=False)
        else:
            embed.add_field(name="Stored Avatar:", value=character_dict[ctx.author.name].char_avatar, inline=False)
        await ctx.edit_origin(embed=embed, components=[create_return_row])

    @slash.component_callback()
    async def char_return(ctx):
        embed=discord.Embed(title="Build-A-Char", description="Go ahead and choose what you would like to make your character be. Press submit when ready!", color=0x00f900)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.edit_origin(embed=embed, components=[create_selection_row, create_stat_select, create_confirmation_row])

    @slash.component_callback()
    async def char_avatar(ctx):
        global character_dict
        character_dict[ctx.author.name].char_avatar_user = ctx.author
        character_dict[ctx.author.name].char_avatar_wait = True
        await ctx.defer(hidden=True)
        await ctx.send("Send the url of your character's avatar in chat, and Luigi Bot will store it for you. (As of now, only URL's are supported!)")

    @slash.component_callback()
    async def stat_select(ctx):
        global character_dict

        character_dict[ctx.author.name].char_preferred_stat = ctx.selected_options[0]
        await ctx.defer(edit_origin=True)

# Create a function that checks if the requested character is valid
def character_check(ctx):

    failed = False

    character_failed_embed=discord.Embed(title="Oops! You forgot something.", description="It looks like you haven't defined these things:", color=0xff2600)
    character_failed_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

    character_success_embed=discord.Embed(title="Great Success!", description="You're all set! GL:HF!", color=0xff2600)
    character_success_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

    global character_dict

    if(character_dict[ctx.author.name].char_name == ""):
        character_dict[ctx.author.name].missing_components.append("Name")
        failed = True
    
    if(character_dict[ctx.author.name].char_avatar == ""):
        character_dict[ctx.author.name].missing_components.append("Avatar")
        failed = True

    if ("http" not in character_dict[ctx.author.name].char_avatar):
        character_dict[ctx.author.name].missing_components.append("Valid URL")
        failed = True

    if (character_dict[ctx.author.name].char_preferred_stat == ""):
        character_dict[ctx.author.name].missing_components.append("Preffered Stat")
        failed = True

    if (failed):
        for missing in character_dict[ctx.author.name].missing_components:
            character_failed_embed.add_field(name=f"Missing {missing}:", value=f"You are missing a {missing}", inline=False)
        character_dict.pop(ctx.author.name)
        return character_failed_embed
    else:
        create_character(ctx.author.name, character_dict[ctx.author.name].char_name, character_dict[ctx.author.name].char_avatar, get_total_char(), character_dict[ctx.author.name].char_preferred_stat)
        character_dict[ctx.author.name].char_name_wait = False
        character_dict[ctx.author.name].char_avatar_wait = False
        character_dict.pop(ctx.author.name)
        return character_success_embed

