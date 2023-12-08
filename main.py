# Standard library imports
import asyncio
import datetime
import os
import random

# Third-party imports
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

# Local application imports
from response_data import response_messages
from utils import hello_cmd, ping_cmd, health_cmd

# Load environment variables
load_dotenv()

# Globals for configuration
STICKER_CHAIN_LIMIT = 5
CLEAN_INTERVAL_SECONDS = 10
DELETE_MESSAGE_TIME = 5
COMMAND_PREFIX = "$"

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_E1')
BOT_CREATOR_ID = int(os.getenv('BOT_CREATOR_ID'))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)
ongoing_clean_operations = set()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    clean_sticker_chains.start()

@bot.command(help="Greets the user.")
async def hello(ctx):
    await hello_cmd(ctx, DELETE_MESSAGE_TIME)

@bot.command(help="Checks the bot's latency.")
async def ping(ctx):
    await ping_cmd(ctx, bot, DELETE_MESSAGE_TIME)

@bot.command(help="Checks if the bot is operational.")
async def health(ctx):
    await health_cmd(ctx, bot, DELETE_MESSAGE_TIME)




@bot.command(help="Updates the sticker chain limit.")
@commands.is_owner()
async def updateChain(ctx, value: int):
    global STICKER_CHAIN_LIMIT
    STICKER_CHAIN_LIMIT = value
    await ctx.send(f"Sticker chain limit updated to {STICKER_CHAIN_LIMIT}.", delete_after=DELETE_MESSAGE_TIME)

@bot.command(help="Updates the clean interval in seconds.")
@commands.is_owner()
async def updateInterval(ctx, value: int):
    global CLEAN_INTERVAL_SECONDS
    CLEAN_INTERVAL_SECONDS = value
    if clean_sticker_chains.is_running():
        clean_sticker_chains.restart()
    await ctx.send(f"Clean interval updated to {CLEAN_INTERVAL_SECONDS} seconds.", delete_after=DELETE_MESSAGE_TIME)

@bot.command(help="Displays the current settings.")
@commands.is_owner()
async def showSettings(ctx):
    await ctx.send(f"Current settings:\n- Clean Interval: {CLEAN_INTERVAL_SECONDS} seconds\n- Sticker Chain Limit: {STICKER_CHAIN_LIMIT}\n- Delete Message Time: {DELETE_MESSAGE_TIME} seconds", delete_after=DELETE_MESSAGE_TIME)

@bot.command(help="Updates the time after which command messages are deleted.")
@commands.is_owner()
async def updateDeleteMessageTime(ctx, value: int):
    global DELETE_MESSAGE_TIME
    DELETE_MESSAGE_TIME = value
    await ctx.send(f"Message delete time updated to {DELETE_MESSAGE_TIME} seconds.", delete_after=DELETE_MESSAGE_TIME)

@bot.command(help="Shows all the commands available for the admin/owner.")
@commands.is_owner()
async def showcommands(ctx):
    commands_list = "\n".join([
        "$activate_janitor - Toggle automatic cleaning",
        "$invoke - Manually invoke cleaning",
        "$updateChain <value> - Update sticker chain limit",
        "$updateInterval <value> - Update clean interval",
        "$updateDeleteMessageTime <value> - Update command message delete time",
        "$showSettings - Show current settings"
    ])
    await ctx.send(f"Available commands:\n{commands_list}", delete_after=DELETE_MESSAGE_TIME)


# Global variable to track the state of janitor
janitor_active = False

@bot.command(help="Toggle the automatic cleaning of sticker chains.")
async def activate_janitor(ctx):
    global janitor_active
    # Check if the command is issued by the bot creator
    if ctx.author.id != BOT_CREATOR_ID:
        return await ctx.send("You do not have permission to use this command.")

    janitor_active = not janitor_active
    state = "activated" if janitor_active else "deactivated"
    await ctx.send(f"Janitor has been {state}.")
    if janitor_active and not clean_sticker_chains.is_running():
        clean_sticker_chains.start()

@bot.command(help="Manually invoke the sticker chain cleaning process.")
async def invoke(ctx):
    # Check if the command is issued by the bot creator
    if ctx.author.id != BOT_CREATOR_ID:
        return await ctx.send("You do not have permission to use this command.")

    await ctx.send("Invoking the janitor to clean sticker chains.")
    await clean_sticker_chains()

@tasks.loop(seconds=CLEAN_INTERVAL_SECONDS)
async def clean_sticker_chains():
    for guild in bot.guilds:
        for channel in guild.text_channels:
            try:
                if not channel.permissions_for(guild.me).read_message_history or \
                   not channel.permissions_for(guild.me).manage_messages:
                    continue

                async for message in channel.history(limit=100):
                    if message.stickers:
                        sticker_chain = [message]
                        async for history_message in channel.history(limit=100, before=message):
                            if history_message.author == message.author and history_message.stickers:
                                sticker_chain.append(history_message)
                            else:
                                if len(sticker_chain) >= STICKER_CHAIN_LIMIT:
                                    break
                                sticker_chain = []

                        if len(sticker_chain) >= STICKER_CHAIN_LIMIT:
                            for sticker_message in sticker_chain:
                                await sticker_message.delete()
                                await asyncio.sleep(1)  # Manage rate limits
                            break
            except Exception as e:
                print(f"Error in clean_sticker_chains: {e}")


# Function to handle cleaning logic
async def handle_clean(ctx, user_id, max_count):
    # Validation for user_id and max_count
    if user_id is None or max_count is None:
        return await ctx.send("Usage: $clean [user_id] [max_count]. Both parameters are required.", delete_after=5)

    # Check if this user ID is already being cleaned
    if user_id in ongoing_clean_operations:
        return await ctx.send(f"Clean operation already in progress for user ID {user_id}.", delete_after=5)

    # Add the user_id to the ongoing operations set
    ongoing_clean_operations.add(user_id)

    # Check if the bot has 'Manage Messages' permission
    if not ctx.channel.permissions_for(ctx.guild.me).manage_messages:
        ongoing_clean_operations.remove(user_id)
        return await ctx.send("I need the 'Manage Messages' permission to delete stickers.")

    try:
        # Cleaning logic
        message_count = 0
        async for message in ctx.channel.history(limit=100):
            if message.stickers and message.author.id == user_id:
                await message.delete()
                message_count += 1
                await asyncio.sleep(1)
                if message_count >= max_count:
                    break
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}", delete_after=5)
    finally:
        ongoing_clean_operations.remove(user_id)

@bot.command(help="Deletes a specified number of messages with stickers. Usage: $clean [user_id] [max_count]")
async def clean(ctx, user_id: int = None, max_count: int = None):
    # Delete the command message
    await ctx.message.delete()

    # Check if the command is issued by the bot creator
    if not await check_owner_permission(ctx):
        return

    # Proceed with the cleaning operation
    await handle_clean(ctx, user_id, max_count)

async def check_owner_permission(ctx):
    if ctx.author.id != BOT_CREATOR_ID:
        response = random.choice(response_messages)
        # Send the response message and delete it after DELETE_MESSAGE_TIME  seconds
        await ctx.send(response, delete_after=DELETE_MESSAGE_TIME)
        return False
    return True

bot.run(TOKEN)
