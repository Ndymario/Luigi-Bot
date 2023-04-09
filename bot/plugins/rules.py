import crescent
import hikari
import miru
import os
from __main__ import Database

plugin = crescent.Plugin[hikari.GatewayBot, Database]()


@plugin.include
@crescent.command(name="rules", description="Shows you the server rules")
class Rules:
    rule_number = crescent.option(int, description="Specify a rule to show", default=0, name="rule-number")

    async def callback(self, ctx: crescent.Context) -> None:
        rules = []
        cur_rule = 0
        for rule in os.listdir("./bot/plugins/rules"):
            cur_rule += 1
            with open(f"./bot/plugins/rules/{cur_rule}.txt", "r") as rule_txt:
                rules.append(hikari.Embed(title=f"{rule_txt.readline()}", description=f"{rule_txt.readline()}",
                             color="#2f3136"))

        await ctx.app.rest.create_message(channel=ctx.channel.id, embed=rules[self.rule_number])
        await ctx.respond(content="Showed the rules!", ephemeral=True)
