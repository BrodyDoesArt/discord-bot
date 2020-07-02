import discord
from discord.ext import commands

from random import randint

class RPG(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['r'], brief='!roll [x]')
    async def roll(self, ctx, arg):
        try:
            float(arg)
        except:
            await ctx.send('❌ You must input an integer !')
        else:
            number = randint(1, int(arg))
            await ctx.send(f'🎲 You rolled a {number} !')

def setup(bot):
    bot.add_cog(RPG(bot))
