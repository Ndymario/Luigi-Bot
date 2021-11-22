import discord
from discord_slash.utils.manage_components import create_select, create_select_option, create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle

about_buttons = [
            create_button(
                style=ButtonStyle.URL,
                label="Ndymario's YouTube",
                url="https://www.youtube.com/channel/UC0_ii78SpO_RPM82TeEibBw"
            ),
            create_button(
                style=ButtonStyle.URL,
                label="Ndymario's GitHub",
                url="https://github.com/Ndymario"
            ),
            create_button(
                style=ButtonStyle.URL,
                label="Luigi Bot Invite!",
                url="https://discord.com/oauth2/authorize?client_id=421169985617002496&scope=bot+applications.commands"
            )
          ]

about_row = create_actionrow(*about_buttons)

def define_slash(guild_ids, slash):
    @slash.slash(name="about", description="What this bot is and the invite for the bot.",guild_ids=guild_ids)
    async def about(ctx):
        about_embed=discord.Embed(title="About me!", description="Hi, I'm Luigi Bot! I'm a bot coded and maintained by __Ndymario#2326__! You probably added me for the RPG engine or because someone mentioned you should try it. If you're enjoying the bot, make sure to check out my other projects!", color=0x00f900)
        about_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        about_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/634582132634943508/852749724583067648/King_Mario.png")
        await ctx.send(embed=about_embed, components=[about_row], hidden=True)