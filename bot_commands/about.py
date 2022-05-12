import discord
from discord.ui import View, Button

def define_slash(client):
    @client.tree.command(name="about", description="About the bot")
    async def about(interaction: discord.Interaction):
        # Build the embed
        with open("bot_commands/about.txt", "r") as about:
            file_content = about.read()
            about_embed=discord.Embed(title="About me!", description=file_content, color=0x00f900)
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
        await interaction.response.send_message(embed=about_embed, view=view)