import discord
from discord.ext import commands

class chat(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.base_xp = 200
        self.factor = 2

    @staticmethod
    def get_data():
        with open('members.json', 'r') as file:
            return loads(file.read())

    @staticmethod
    def set_data(members):
        with open('members.json', 'w') as file:
            file.write(dumps(members, indent=2))

    @commands.command(brief='!clear [x]', description='Supprime les [x] derniers messages', aliases=['delete', 'purge'])
    async def clear(self, ctx, limit):
        try:
            float(limit)
        except:
            await ctx.send('❌ Vous devez entrer un nombre entier !')
        else:
            if str(ctx.channel) == 'bot':
                limit = int(limit) + 1
                await ctx.channel.purge(limit=limit)
            else:
                await ctx.send('❌ Cette commande ne peut être utilisée que dans le channel "bot" !')
    
    @commands.command(brief='!help [catégorie/rien]', description="Afficher toutes les commandes ou les commandes d'une catégorie")
    async def help(self, ctx, *c):
        if not c:
            await ctx.channel.purge(limit=1)
            temp = []
            embed = discord.Embed(color=discord.Color.blue(), title='Listes des commandes')
            for x in self.bot.cogs:
                for y in self.bot.get_cog(x).get_commands():
                    if not y.hidden:
                        temp.append(f"\n{y.brief}")
                embed.add_field(name=f'**{x} :**', value=f"{''.join(temp[0:len(temp)])}", inline=False)
                temp = []
            await ctx.send(embed=embed)
        elif len(c) == 1:
            c = ''.join(c[:])
            if self.bot.get_cog(c):
                await ctx.channel.purge(limit=1)
                embed = discord.Embed(color=discord.Color.blue(), title=f'Commandes de la catégorie "{c}"')
                for x in self.bot.get_cog(c).get_commands():
                    if not x.hidden:
                        embed.add_field(name=f'**{x.brief} :**', value=f"{x.description}", inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Nom de catégorie invalide !")
        else:
            await ctx.send("❌ Vous devez entrer seulement une catégorie !")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        members = self.get_data()
        members.append({'name': member.name, 'id': member.id, 'xp': 0})
        self.set_data(members)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        members = self.get_data()
        members.remove({'name': member.name, 'id': member.id, 'xp': 0})
        self.set_data(members)

    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author.id
        members = self.get_data()
        for member in members:
            if author == member['id']:
                member['xp'] += randint(5, 10)
            if member['xp'] > self.base_xp * (member['level']+1 * self.factor):
                member['level'] += 1
                await message.channel.send(f"🎉 {message.author.mention} a level up ! Il est maintenant niveau {member['level']}")
        self.set_data(members)
        

    @commands.command(brief='!xp', description='Afficher son niveau et son xp', aliases=['level', 'lvl', 'niveau', 'niv'])
    async def xp(self, ctx):
        members = self.get_data()
        for member in members:
            if ctx.author.id == member['id']:
                await ctx.send(f"🎚️ Tu es niveau {member['level']} ({member['xp']}/{self.base_xp * (member['level']+1 * self.factor)})")

def setup(bot):
    bot.add_cog(chat(bot))
