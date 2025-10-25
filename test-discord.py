import discord
from discord.ext import commands
import dotenv
import os
from container_builder import containermessage

dotenv.load_dotenv()
TOKEN = os.getenv('BETA_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

container = containermessage(TOKEN)

@bot.event
async def on_ready():
    print(f'✅ {bot.user} is online!')

@bot.command()
async def test(ctx):
    await container.send(ctx.channel, "**Test** This is a basic container message")
    
    await container.send_multiple(ctx.channel, [
        "**First line** of text",
        "**Second line** of text",
        "**Third line** of text"
    ])

if __name__ == '__main__':
    bot.run(TOKEN)
