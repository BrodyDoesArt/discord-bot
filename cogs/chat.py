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
        embed = discord.Embed(color=discord.Color.blue(), title='Listes des commandes')
        for cog in self.bot.cogs:
            if self.bot.get_cog(cog).get_commands():
                temp = []
                for cmd in self.bot.get_cog(cog).get_commands():
                    if not cmd.hidden:
                        temp.append(f"{cmd.brief}\n")
                embed.add_field(name=f'**{cog} :**', value=f"{''.join(temp)}", inline=False)
        await ctx.send(embed=embed)

    @commands.command(brief='!poll [question] [answers]')
    async def poll(self, ctx, *items):
        question = items[0]
        answers = '\n'.join(items[1:])
        embed = discord.Embed(title='Nouveaux sondage :', description=f":grey_question: __{question}__", color=discord.Colour.blue())
        for i in range(1, len(items)):
            embed.add_field(name=f"Option n°{i}", value=items[i], inline=False)
        await ctx.channel.purge(limit=1)
        message = await ctx.channel.send(embed=embed)
        reactions = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']

        for i in range(len(items[1:])):
            await message.add_reaction(reactions[i])

    @commands.command(brief='!meme')
    async def meme(self, ctx):
        data = get('https://meme-api.herokuapp.com/gimme').json()
        embed = (discord.Embed(title=f":speech_balloon: r/{data['subreddit']} :", color=0x3498db)
                .set_image(url=data['url'])
                .set_footer(text=data['postLink']))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(chat(bot))
