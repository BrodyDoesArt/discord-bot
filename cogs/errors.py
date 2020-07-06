import discord
from discord.ext import commands

class ErrorManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            msg = 'You must input an integer!'
        elif isinstance(error, commands.MissingRequiredArgument):
            msg = f'You must input these following arguments: {error.param.name}'
        elif isinstance(error, commands.CommandNotFound):
            msg = 'Unknown command!'
        elif isinstance(error, commands.CommandInvokeError):
            if 'index' in str(error):
                msg = "Argument is too big!"
            elif 'NoneType' in str(error):
                msg = "I'm not connected to any channel!" if 'is_playing' in str(error) else "You're not connected to any channel!"

        embed = discord.Embed(title="❌ Oops :", description=msg, color=discord.Color.red())
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=embed, delete_after=5.0)

def setup(bot):
    bot.add_cog(ErrorManager(bot))
