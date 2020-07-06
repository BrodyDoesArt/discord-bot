import discord
from discord.ext import commands

class chat(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='!clear [x]', aliases=['delete', 'purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, limit):
        limit = int(limit) + 1
        await ctx.channel.purge(limit=limit)
    
    @commands.command(brief='!help')
    async def help(self, ctx):
        await ctx.channel.purge(limit=1)
        embed = discord.Embed(color=discord.Color.blue(), title='Commands list:')
        for cog in self.bot.cogs:
            temp = []
            for cmd in self.bot.get_cog(cog).get_commands():
                if not cmd.hidden:
                    temp.append(f"{cmd.brief}\n")
            embed.add_field(name=f'**{cog} :**', value=f"{''.join(temp)}", inline=False)
        await ctx.send(embed=embed)

                                
def setup(bot):
    bot.add_cog(chat(bot))
