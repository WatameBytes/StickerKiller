# Sticker Killer README

This Discord bot, written in Python, provides several commands for managing messages in a server. It's designed to help moderate a server by allowing the deletion of messages with stickers and enabling the "nuke" of messages from specific users.

## Prerequisites

Before running this bot, make sure you have the following prerequisites installed:

- Python 3.x

You will also need to create a Discord bot and obtain a token. Follow the official Discord developer documentation to : [Creating a Bot Account](https://discordpy.readthedocs.io/en/stable/discord.html).

# Setup

Clone or download this repository to your local machine.

Install the necessary Python libraries. You can do this by manually installing each library your project depends on using pip.

Create a .env file in the project directory and add the following environment variables:

    DISCORD_TOKEN=<Your Discord Bot Token>
    BOT_CREATOR_ID=<Your Discord User ID>

# Configuration

You can customize the bot's behavior by modifying the following global variables in the code:

    STICKER_CHAIN_LIMIT: The maximum number of consecutive messages with stickers before stopping the cleaning process.

    CLEAN_INTERVAL_SECONDS: The interval in seconds for checking and cleaning messages with stickers.

    DELETE_MESSAGE_TIME: The time in seconds to delete response messages automatically.

    MESSAGE_HISTORY_LIMIT: The maximum number of messages to check during cleaning.

    NUKE_LIMIT: The maximum number of messages to nuke when using the $1984 command.

    ASYNC_SLEEP: The delay in seconds between message deletions during cleaning and nuking.

    COMMAND_PREFIX: The prefix used for bot commands.

# Bot Commands
    $addbl [message_id]: Add a message to the blacklist to prevent $1984 from deleting it.
    $removebl [message_id]: Removes a message from the blacklist, allowing $1984 to delete it.
    $clearbl: Clear's the blacklist.
    $clean [user_id] [max_count]: Deletes a specified number of messages with stickers sent by a user.
    $hello: Greets the user with a simple message.
    $health: Checks if the bot is operational and displays its latency.
    $1984 [user_id] [max_count]: "Nukes" a specified number of messages from a user by deleting them.
    $ping: Checks the bot's latency.

# Running the Bot

To run the bot, execute the following command in your terminal:

    python main.py

The bot will log in using the provided token and will be ready to respond to commands in your Discord server.

# Bot Creator

This bot is intended for use by the creator, whose user ID is specified in the BOT_CREATOR_ID environment variable. Only the bot creator can execute certain commands and actions.

# Permissions

Make sure the bot has the necessary permissions, especially the "Manage Messages" permission, in the channels where you intend to use it. If it lacks this permission, it won't be able to delete messages.

# Acknowledgments

This Discord bot was created with the help of the Discord.py library. Feel free to modify and extend it to suit your server's needs.
