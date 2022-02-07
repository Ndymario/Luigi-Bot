import discord
from discord_slash.utils.manage_components import create_select, create_select_option, create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle
from mongo_db.mongo_db import get_chars

quest_buttons = [
            create_button(
                style=ButtonStyle.green,
                label="Let's go!",
                custom_id="quest_confirm"
            ),
            create_button(
                style=ButtonStyle.red,
                label="Actually, never mind.",
                custom_id="quest_cancel"
            )
          ]
quest_action_row = create_actionrow(*quest_buttons)

quest_select = create_select(
    options=[
        create_select_option("Shipwreck Isle", value="isle"),
        create_select_option("The Lost Underground", value="mines"),
        create_select_option("The Lake of Legend", value="lake"),
    ],
    placeholder="Where to?",
    min_values=1,
    max_values=1,
    custom_id="map_select"
)

location_select_buttons = [
            create_button(
                style=ButtonStyle.green,
                label="Let's go!",
                custom_id="location_confirm"
            ),
            create_button(
                style=ButtonStyle.red,
                label="Actually, let me pick someone else.",
                custom_id="location_cancel"
            )
          ]
location_action_row = create_actionrow(*location_select_buttons)

selected_char = ""
selected_location = ""

def define_slash(guild_ids, slash):
    @slash.slash(name="quest", description="Go on en epic quest with one of your characters",guild_ids=guild_ids)
    async def quest(ctx):
        embed=discord.Embed(title="Going on a quest!", description="Ready for adventure? Let's get started!", color=0x00f900)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed, components=[create_actionrow(char_list_generator(ctx.author.name)), quest_action_row], hidden=True)

    # Component callback is a response to a specific ID (def a function named the ID you want to respond to)
    @slash.component_callback()
    async def quest_confirm(ctx):
        global selected_char
        embed=discord.Embed(title="Quest Confirmed!", description=f"Alright! Now that you've confirmed your quest, where would you like to advenure to?", color=0x00f900)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.edit_origin(embed=embed, components=[create_actionrow(quest_select), location_action_row])

    @slash.component_callback()
    async def quest_cancel(ctx):
        embed=discord.Embed(title="On second thought...", description="You changed your mind. (use the command again if you changed your mind on changing your mind!)", color=0xff2600)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.edit_origin(embed=embed, components=[])

    @slash.component_callback()
    async def map_select(ctx):
        global selected_location
        selected_location = ctx.selected_options[0]
        await ctx.defer(edit_origin=True)

    @slash.component_callback()
    async def char_select(ctx):
        global selected_char
        selected_char = ctx.selected_options[0]
        await ctx.defer(edit_origin=True)

    @slash.component_callback()
    async def location_confirm(ctx):
        embed=discord.Embed(title="Coming soon!", description="Questing is coming soon!", color=0x00f900)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.edit_origin(embed=embed, components=[])

    @slash.component_callback()
    async def location_cancel(ctx):
        embed=discord.Embed(title="Going on a quest!", description="Ready for adventure? Let's get started!", color=0x00f900)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.edit_origin(embed=embed, components=[create_actionrow(char_list_generator(ctx.author.name)), quest_action_row], hidden=True)

def char_list_generator(user):
    # Fetch the list of characters the user has, then generate a list of options for them
    result = get_chars(user)

    options = []

    for character in result[1]:
        options.append(create_select_option(character.name, value=f"{character.name}.{character.id}"))

    return create_select(options = options, placeholder="Select your character!", min_values=1, max_values=1, custom_id="char_select")
