# Standard library imports
import asyncio
import os
import random

# Third-party imports
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Local application imports
from response_data import response_messages

# Load environment variables
load_dotenv()

# Globals for configuration
ASYNC_SLEEP = 1
BLACKLIST = set()  # Add this line for blacklist
BOT_CREATOR_ID = int(os.getenv('BOT_CREATOR_ID'))
CLEAN_INTERVAL_SECONDS = 10
COMMAND_PREFIX = "$"
DELETE_MESSAGE_TIME = 5
MESSAGE_HISTORY_LIMIT = 100
NUKE_LIMIT = 1000
STICKER_CHAIN_LIMIT = 5
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# Helper function to handle blacklist modification
async def modify_blacklist(ctx, message_id, operation):
    if not is_bot_creator(ctx):
        response = random.choice(response_messages)
        await ctx.send(response, delete_after=DELETE_MESSAGE_TIME)
        return

    if message_id is None:
        await ctx.send("Please provide a valid message ID.", delete_after=DELETE_MESSAGE_TIME)
        return

    if operation == "add":
        BLACKLIST.add(message_id)
        await ctx.send(f"Message ID {message_id} added to blacklist.", delete_after=DELETE_MESSAGE_TIME)
    elif operation == "remove":
        BLACKLIST.discard(message_id)
        await ctx.send(f"Message ID {message_id} removed from blacklist.", delete_after=DELETE_MESSAGE_TIME)


@bot.command(name="addbl", help="Add a message ID to the blacklist. Usage: $addbl <message_id>")
async def add_to_blacklist(ctx, message_id: int = None):
    await ctx.message.delete()
    await modify_blacklist(ctx, message_id, "add")


@bot.command(name="clearbl", help="Clear the entire blacklist. Usage: $clearbl")
async def clear_blacklist(ctx):
    await ctx.message.delete()

    if not is_bot_creator(ctx):
        response = random.choice(response_messages)
        await ctx.send(response, delete_after=DELETE_MESSAGE_TIME)
        return

    BLACKLIST.clear()
    await ctx.send("Blacklist has been cleared.", delete_after=DELETE_MESSAGE_TIME)


@bot.command(name="removebl", help="Remove a message ID from the blacklist. Usage: $removebl <message_id>")
async def remove_from_blacklist(ctx, message_id: int = None):
    await ctx.message.delete()
    await modify_blacklist(ctx, message_id, "remove")


@bot.command(name="clean", help="Deletes a specified number of messages with stickers. Usage: $clean [user_id] [max_count]")
async def clean_stickers(ctx, user_id: int = None, max_count: int = None):
    valid, response = await validate_command(ctx, user_id, max_count)
    if not valid:
        return response

    try:
        message_count = 0
        async for message in ctx.channel.history(limit=MESSAGE_HISTORY_LIMIT):
            if message.stickers and message.author.id == user_id:
                await message.delete()
                message_count += 1
                await asyncio.sleep(ASYNC_SLEEP)

                if message_count >= max_count:
                    break
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}", delete_after=DELETE_MESSAGE_TIME)

@bot.command(help="Greets the user.")
async def hello(ctx):
    await ctx.send("Hello! I'm your bot.", delete_after=DELETE_MESSAGE_TIME)

@bot.command(help="Checks if the bot is operational.")
async def health(ctx):
    # Delete the command message
    await ctx.message.delete()

    message = await ctx.send("I'm alive and kicking!", delete_after=DELETE_MESSAGE_TIME)
    latency = bot.latency * 1000
    await message.edit(content=f"I'm alive and kicking! Latency: {latency:.2f} ms", delete_after=DELETE_MESSAGE_TIME)

@bot.command(name="1984", help="Nukes a specified number of messages from a user. Usage: $1984 <user_id> <number>")
async def nuke(ctx, user_id: int = None, max_count: int = None):
    valid, response = await validate_command(ctx, user_id, max_count)
    if not valid:
        return response

    deleted_count = 0

    try:
        async for message in ctx.channel.history(limit=NUKE_LIMIT):  # Adjust the limit as needed
            if message.author.id == user_id and message.id not in BLACKLIST:
                await message.delete()
                deleted_count += 1
                await asyncio.sleep(ASYNC_SLEEP)
                if deleted_count >= max_count:
                    break
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}", delete_after=DELETE_MESSAGE_TIME)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(help="Checks the bot's latency.")
async def ping(ctx):
    latency = bot.latency * 1000  # Convert to milliseconds
    await ctx.send(f"Pong! Latency: {latency:.2f} ms", delete_after=DELETE_MESSAGE_TIME)

# Helper function to check if the user is the bot creator
def is_bot_creator(ctx):
    return ctx.author.id == BOT_CREATOR_ID


async def validate_command(ctx, user_id, max_count):
    await ctx.message.delete()

    # Check 'Manage Messages' permission
    if not ctx.channel.permissions_for(ctx.guild.me).manage_messages:
        return False, await ctx.send("I need 'Manage Messages' permission.", delete_after=DELETE_MESSAGE_TIME)

    # Restrict command to the bot creator
    if ctx.author.id != BOT_CREATOR_ID:
        response = random.choice(response_messages)
        return False, await ctx.send(response, delete_after=DELETE_MESSAGE_TIME)

    # Validation for user_id and max_count
    if user_id is None or max_count is None:
        return False, await ctx.send("Usage: [command] [user_id] [max_count]", delete_after=DELETE_MESSAGE_TIME)

    return True, None

bot.run(TOKEN)
