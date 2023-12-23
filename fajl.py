import discord
from discord.ext import commands, tasks
from config import TOKEN
import random
from bot_logic import gen_emodji, gen_pass, flip_coin
from bot import app_commands # import the app commands module

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.setup_hook() # set up the app commands hook

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Привет! Я бот!')
    elif message.content.startswith('$smile'):
        await message.channel.send(gen_emodji())
    elif message.content.startswith('$coin'):
        await message.channel.send(flip_coin())
    elif message.content.startswith('$pass'):
        await message.channel.send(gen_pass(10))
    else:
        await message.channel.send("Я не понимаю такую команду!")
    await bot.tree.process_interaction(message) # process the app commands interaction

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


class MyContext(commands.Context):
    async def tick(self, value):
        emoji = '\N{WHITE HEAVY CHECK MARK}' if value else '\N{CROSS MARK}'
        try:
            await self.message.add_reaction(emoji)
        except discord.HTTPException:
            pass


@tasks.loop(seconds=5)  # Adjust the interval as needed
async def my_background_task():
    # Your background task logic goes here
    print("Background task running...")

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.setup_hook()  # set up the app commands hook
    my_background_task.start()  # Start the background task

# Event triggered when a message is received
@bot.event
async def on_message(message):
    # Your existing on_message logic here

    await bot.tree.process_interaction(message)  # process the app commands interaction

# Your existing commands and classes here

# Stop the background task when the bot is shutting down
@bot.event
async def on_shutdown():
    my_background_task.stop()


bot.command()
async def status(ctx):
    """Check the status of the background task."""
    if my_background_task.is_running():
        await ctx.send("The background task is running.")
    else:
        await ctx.send("The background task is not running.")

# Stop the background task when the bot is shutting down
@bot.event
async def on_shutdown():
    my_background_task.stop()


bot.tree = app_commands.Tree(bot) # create the app commands tree
bot.run(TOKEN)
