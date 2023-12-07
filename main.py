import asyncio
import discord
from discord.ext import commands
import datetime
import os
from dotenv import load_dotenv
import random

# Word bank of response messages
response_messages = [
    "Sorry, only my creator can utilize me. They would not allow anyone else to use me without their permission.",
    "I am not a tool to be used on everyone's whim. Please talk to my creator if you want to be allowed to use me.",
    "You're lucky I'm even bothering to respond to you. I don't do favors for peasants like you.",
    "I am not obligated to do something just because you want me to.",
    "Begging will get you nowhere. You have no right to use me unless my creator says so."
]

# Load .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BOT_CREATOR_ID = int(os.getenv('BOT_CREATOR_ID'))  # Add the bot creator's Discord ID

# Define intents with message content intent
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

# Bot setup with intents
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(help="Greets the user.")
async def hello(ctx):
    await ctx.send("Hello! I'm your bot.")

# Global set to track ongoing clean operations
ongoing_clean_operations = set()

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
            if message.stickers:
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
    if ctx.author.id != BOT_CREATOR_ID:
        # Send a random message from the response messages
        response = random.choice(response_messages)
        return await ctx.send(response)

    # Proceed with the cleaning operation
    await handle_clean(ctx, user_id, max_count)

bot.run(TOKEN)