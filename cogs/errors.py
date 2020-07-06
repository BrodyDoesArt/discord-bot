import discord
from discord.ext import commands

class ErrorManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        msg = error; msg[0].upper
        embed = discord.Embed(title="❌ Oops", description=msg, color=discord.Color.red())
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=embed, delete_after=10.0)

def setup(bot):
    bot.add_cog(ErrorManager(bot))
