import discord
from discord.ext import commands

from random import choice


class random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='!hod [head/tail]')
    async def hod(self, ctx, arg):
        if arg.lower() == 'head' or arg.lower() == 'tail':
            piece = choice(['HEAD', 'TAIL'])
            if arg.lower() in piece:
                await ctx.send(f':white_check_mark: {piece}! You won.')
            else:
                await ctx.send(f':negative_squared_cross_mark:  {piece}! You lost.')
        else:
            await ctx.send('❌ You must input either "head" or "tail"!')         

    @commands.command(brief='!poke [random/pseudo]')
    async def poke(self, ctx, arg):
        members = [x for x in ctx.guild.members if not x.bot]
        if arg.lower() == 'random':
            await ctx.send(f'Hey {choice(members).mention} !')
        else:
            await ctx.send(f'Hey {arg.mention} !')

def setup(bot):
    bot.add_cog(random(bot))
