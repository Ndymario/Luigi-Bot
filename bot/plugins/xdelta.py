import crescent
import hikari
import urllib3
from __main__ import Database

plugin = crescent.Plugin[hikari.GatewayBot, Database]()
#
# xdelta_group = crescent.Group("xdelta")
#
#
# @plugin.include
# @xdelta_group.child
# @crescent.command(name="create", description="Create an XDelta patch from your ROM")
# class Patcher:
#     rom = crescent.option(hikari.Attachment, description="Your modified US ROM")
#
#     async def callback(self, ctx: crescent.Context):
#
#         await ctx.respond(content=f"Success: {self.rom.is_ephemeral}, {self.rom.media_type}, {self.rom.filename}")
#
#         http = urllib3.PoolManager()
#         await ctx.defer(ephemeral=True)
#         with open("./nsmb.nds") as original:
#             rom = http.request("GET", self.rom.url)
#
#         await ctx.respond(content=f"Success! Here's your XDelta file!")
#
#
# @plugin.include
# @xdelta_group.child
# @crescent.command(name="patch", description="Patch your ROM with an XDelta")
# class Patcher:
#     rom = crescent.option(hikari.Attachment, description="Your clean US ROM")
#
#     async def callback(self, ctx: crescent.Context):
#         await ctx.defer(ephemeral=True)
#         await ctx.respond(content=f"Success: {self.rom.is_ephemeral}, {self.rom.media_type}, {self.rom.filename}")
