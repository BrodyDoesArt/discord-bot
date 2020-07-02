import discord
from discord.ext import commands

class chat(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='!clear [x]', description='Deletes the [x] previous messages', aliases=['delete', 'purge'])
    async def clear(self, ctx, limit):
        try:
            float(limit)
        except:
            await ctx.send('❌ Input must be an integer!')
        else:
            if str(ctx.channel) == 'bot':
                limit = int(limit) + 1
                await ctx.channel.purge(limit=limit)
            else:
                await ctx.send('❌ This command can only be used in "bot" channel!')
    
    @commands.command(brief='!help', description="Displays the help message")
    async def help(self, ctx):
        await ctx.channel.purge(limit=1)
        embed = discord.Embed(color=discord.Color.blue(), title='Listes des commandes')
        for cog in self.bot.cogs:
            temp = []
            for cmd in self.bot.get_cog(cog).get_commands():
                if not cmd.hidden:
                    temp.append(f"{cmd.brief}: {cmd.description}\n")
            embed.add_field(name=f'**{cog} :**', value=f"{''.join(temp)}", inline=False)
        await ctx.send(embed=embed)

                                
def setup(bot):
    bot.add_cog(chat(bot))
