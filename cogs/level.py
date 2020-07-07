import discord
from discord.ext import commands

from json import dumps, loads
from random import randint

class Leveling(commands.Cog, name='Niveaux'):
    def __init__(self, bot):
        self.bot = bot
        self.base_xp = 200
        self.factor = 2

    @staticmethod
    def get_data(guild, reset=False):
        with open('members.json', 'r') as file:
            guild_info = loads(file.read())
            return guild_info[guild] if not reset else guild_info

    @staticmethod
    def set_data(members):
        with open('members.json', 'w') as file:
            file.write(dumps(members, indent=2))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        members = self.get_data(str(member.guild.id)))
        members.append({'name': member.name, 'id': member.id, 'level': 0,'xp': 0})
        self.set_data(members)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        members = self.get_data(str(member.guild.id)))
        members.remove({'name': member.name, 'id': member.id, 'level': member.level,'xp': member.xp})
        self.set_data(members)

    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author.id
        members = self.get_data(str(message.guild.id))
        for member in members:
            if author == member['id']:
                member['xp'] += randint(5, 10)
            if member['xp'] > self.base_xp * (member['level']+1 * self.factor):
                member['level'] += 1
                await message.channel.send(f"🎉 {message.author.mention} leveled up! He's now lvl {member['level']}")
        self.set_data(members)

    @commands.command()
    async def reset(self, ctx):
        data = self.get_data(str(ctx.guild.id), True)
        data[ctx.guild.id] = []
        if ctx.author.name == 'Mr_Spaar':
            for member in ctx.guild.members:
                data[ctx.guild.id].append({'name': member.name, 'id': member.id, 'level': 0,'xp': 0})
        self.set_data(data)
                                           
    @commands.command(brief='!xp', aliases=['level', 'lvl', 'niveau', 'niv'])
    async def xp(self, ctx):
        members = self.get_data()
        for member in members:
            if ctx.author.id == member['id']:
                await ctx.send(f"🎚️ You're level {member['level']} ({member['xp']}/{self.base_xp * (member['level']+1 * self.factor)})")

def setup(bot):
    bot.add_cog(Leveling(bot))
