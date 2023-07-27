import os
import datetime
import pytz
import hikari
import crescent
import miru
from bot.database import Database

from bot.plugins.welcome import WelcomeView


bot = hikari.GatewayBot(os.getenv("BOT_TOKEN"), intents=hikari.Intents.ALL)
miru.install(bot)
client = crescent.Client(bot, Database())

client.plugins.load_folder("bot.plugins")

# If you're using the bot for yourself, you'll need to edit these ID's to match your channel IDs
starboard = int(os.getenv("STARBOARD"))
mod_log = int(os.getenv("MOD_LOG"))
member_count = int(os.getenv("MEMBER_COUNT"))
guild_id = int(os.getenv("GUILD_ID"))


async def get_channel_num():
    channel = await client.app.rest.fetch_channel(member_count)
    name = channel.name[9:]
    return int(name)


@bot.listen()
async def startup(event: hikari.StartedEvent) -> None:
    # Start up persistent views
    view = WelcomeView(timeout=None)
    await view.start()

    # Fetch the current member count and update the channel name if it's out of date
    num = await get_channel_num()
    count = 0

    for member in await client.app.rest.fetch_members(guild_id):
        count += 1

    if num != count:
        await client.app.rest.edit_channel(member_count, name=f"Members: {count}")


@bot.listen()
async def starboard(event: hikari.ReactionAddEvent):
    if bot.get_me().username == os.getenv("BETA_NAME"):
        return

    message = await bot.rest.fetch_message(event.channel_id, event.message_id)
    for reaction in message.reactions:
        if reaction.emoji == "⭐" and reaction.count >= 5:
            star_embed = hikari.Embed(title=f"<#{message.channel_id}>", description=message.content,
                                      url=message.make_link(message.guild_id))
            star_embed.set_author(name=message.author.username, icon=message.author.avatar_url)
            await bot.rest.create_message(channel=starboard, embed=star_embed)


@bot.listen()
async def exp(event: hikari.MessageCreateEvent):
    if bot.get_me().username == os.getenv("BETA_NAME"):
        return

    exp_per_message = client.model.exp_multiplier

    if event.is_human:
        author_id = event.author.id
        author_name = event.author.username
        user = client.model.get_user(author_id)

        if user is not None:
            leveled_up = client.model.set_exp(author_id, user.exp + exp_per_message)

            # If the user leveled up, level them up
            if leveled_up:
                level_table = {30: 1093830095866708048, 490: 1093830149029511178, 2130: 1093830236849836093,
                               6860: 1093830289345757224,
                               22500: 1093830321679646752, 50000: 1093830355791912992}

                await event.app.rest.add_role_to_member(guild=event.message.guild_id, user=author_id,
                                                        role=level_table[user.exp + exp_per_message],
                                                        reason=f"User ranked up (EXP = {user.exp + exp_per_message})")

                embed = hikari.Embed(title="Level up!", description=f"Way to go, "
                                                                    f"you leveled up to "
                                                                    f"<@&{level_table[user.exp + exp_per_message]}>!")
                embed.set_author(name=event.author.username, icon=event.author.avatar_url)

                await event.app.rest.create_message(channel=event.channel_id, embed=embed)

        else:
            # If the user doesn't exist, add them to the table
            try:
                client.model.add_user(author_id, author_name)
                client.model.set_exp(author_id, exp_per_message)
            except:
                print(f"Failed to add {author_id} ({author_name}) to the database!")


@bot.listen()
async def del_log(event: hikari.MessageDeleteEvent):
    if bot.get_me().username == os.getenv("BETA_NAME"):
        return

    if event.old_message is not None:
        if not event.old_message.author.is_bot:
            author = event.old_message.author
            content = event.old_message.content
            channel = await bot.rest.fetch_channel(event.old_message.channel_id)

            embed = hikari.Embed(description=f"{author.mention} deleted a message in {channel.mention}",
                                 timestamp=datetime.datetime.now(tz=pytz.timezone("America/Chicago")), color="#FF0000")

            embed.set_author(name=f"{author.username}#{author.discriminator}", icon=author.avatar_url)

            embed.add_field(name="Deleted message:", value=content)
            embed.add_field(name="ID", value=f"```\nUser: {author.id}\nMessage: {event.old_message.id}```")

            await bot.rest.create_message(channel=mod_log, embed=embed)


@bot.listen()
async def edit_log(event: hikari.MessageUpdateEvent):
    if bot.get_me().username == os.getenv("BETA_NAME"):
        return

    if event.old_message is not None:
        if not event.old_message.author.is_bot:
            author = event.message.author
            before_content = event.old_message.content
            after_content = event.message.content
            message = event.message

            embed = hikari.Embed(
                description=f"{author.mention} updated their message\n{message.make_link(message.guild_id)}",
                timestamp=datetime.datetime.now(tz=pytz.timezone("America/Chicago")), color="#FFFF00")

            embed.set_author(name=f"{author.username}#{author.discriminator}", icon=author.avatar_url)

            embed.add_field(name="Before the Edit:", value=before_content)
            embed.add_field(name="After the Edit:", value=after_content)
            embed.add_field(name="ID", value=f"```\nUser: {author.id}\nMessage: {message.id}```")

            await bot.rest.create_message(channel=mod_log, embed=embed)


@bot.listen()
async def join_log(event: hikari.events.MemberCreateEvent):
    if bot.get_me().username == os.getenv("BETA_NAME"):
        return

    if not event.user.is_bot:
        user = event.user
        embed = hikari.Embed(title=f"{user.username}", description=f"{user.mention} joined the server",
                             color="#00FF00", timestamp=datetime.datetime.now(tz=pytz.timezone("America/Chicago")))
        embed.add_field(name="**ID**", value=f"```\nUser: {user.id}```")
        await client.app.rest.create_message(channel=mod_log, embed=embed)


@bot.listen()
async def leave_log(event: hikari.events.MemberDeleteEvent):
    if bot.get_me().username == os.getenv("BETA_NAME"):
        return

    if not event.user.is_bot:
        user = event.user
        embed = hikari.Embed(title=f"{user.username}", description=f"{user.mention} left the server",
                             color="#FFFFFF", timestamp=datetime.datetime.now(tz=pytz.timezone("America/Chicago")))
        embed.add_field(name="**ID**", value=f"```\nUser: {user.id}```")
        await client.app.rest.create_message(channel=mod_log, embed=embed)


@bot.listen()
async def ban_log(event: hikari.events.BanEvent):
    if bot.get_me().username == os.getenv("BETA_NAME"):
        return

    if not event.user.is_bot:
        banned_user = event.user
        embed = hikari.Embed(title=f"{banned_user.username}", description=f"{banned_user.mention} was banned",
                             color="#FFFFFF", timestamp=datetime.datetime.now(tz=pytz.timezone("America/Chicago")))
        embed.add_field(name="**ID**", value=f"```\nUser: {banned_user.id}```")
        await client.app.rest.create_message(channel=mod_log, embed=embed)


@bot.listen()
async def inc_member_count(event: hikari.MemberCreateEvent):
    if bot.get_me().username == os.getenv("BETA_NAME"):
        return

    current = await get_channel_num()
    await client.app.rest.edit_channel(member_count, name=f"Members: {current + 1}")


@bot.listen()
async def dec_member_count(event: hikari.MemberDeleteEvent):
    if bot.get_me().username == os.getenv("BETA_NAME"):
        return

    current = await get_channel_num()
    await client.app.rest.edit_channel(member_count, name=f"Members: {current - 1}")


bot.run()
