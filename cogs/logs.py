import discord
from discord.ext import commands

from datetime import datetime

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
        elif isinstance(error, commands.MissingPermissions):
            msg = "You're not allowed to use this command!"
        elif isinstance(error, commands.BotMissingPermissions):
            perms = ", ".join(error.missing_perms)
            msg = f"I'm missing permissions to execute this command: {perms} !"
        elif isinstance(error, commands.CommandInvokeError) and ('index' in str(error) or 'NoneType' in str(error))::
            if 'index' in str(error):
                msg = "Argument is too big!"
            elif 'NoneType' in str(error):
                msg = "I'm not connected to any channel!" if 'is_playing' in str(error) else "You're not connected to any channel!"
        else:
            print(error)
            return

        embed = discord.Embed(title="❌ Oops :", description=msg, color=discord.Color.red())
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=embed, delete_after=5.0)

        @commands.Cog.listener()
        async def on_command_completion(self, ctx):
            for channel in ctx.guild.text_channels:
                if channel.name == "logs":
                    command = f"{ctx.author.mention}: !{ctx.command.name}{ctx.message.content[(len(ctx.command.name)+1):]}"
                    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    embed = discord.Embed(title=':pager: Commande exécutée :', description=command, color=0x3498db)
                    embed.add_field(name='\u200b', value=now)
                    await channel.send(embed=embed)
        
def setup(bot):
    bot.add_cog(ErrorManager(bot))
