# Sticker Killer README

This Discord bot, written in JavaScript, provides several commands for managing messages in a server. It's designed to help moderate a server by allowing the deletion of messages with stickers and enabling the "nuke" of messages from specific users.

## Prerequisites

Before running this bot, make sure you have Node.js installed. You can download Node.js [here] (https://nodejs.org/en/download/package-manager).

You will also need to create a Discord bot and obtain a token. Follow the official Discord developer documentation to : [Creating a Bot Account](https://discordpy.readthedocs.io/en/stable/discord.html).

# Setup

Clone or download this repository to your local machine.

Install the necessary node modules by using: "npm install" in your desired command line.

Create a config.json file in the project directory and add the following keys + values:

	"token": <YOUR TOKEN HERE>,
	"clientId": <YOUR CLIENT ID HERE>,
	"guildId": <YOUR GUILD ID HERE>,
	"userId": <YOUR USER ID HERE>,
	"roleId": <ROLE ID HERE>

**NOTE** The creator and role ID is used for permission validation with commands.

If you want any user with a certain role to be able to use the bot, use role ID. If you want to be the only one to use the bot, edit the if/else statement within "client.on" (line 49-53) function in index.js as such:

```
    if (interaction.member.id === userId) {
        await command.execute(interaction);
    } else {
        await interaction.reply(responseMessages[Math.floor(Math.random() * responseMessages.length)]);
    }
```

# Bot Commands
    /1984 [user_id] [max_count]: "Nukes" a specified number of messages from a user by deleting them.
    /addbl [message_id]: Add a message to the blacklist to prevent $1984 from deleting it.
    /clean [user_id] [max_count]: Deletes a specified number of messages with stickers sent by a user.
    /clearbl: Clear's the blacklist.
    /health: Checks if the bot is operational and displays its latency.
    /hello: Greets the user with a simple message.
    /removebl [message_id]: Removes a message from the blacklist, allowing $1984 to delete it.

# Running the Bot

To run the bot, execute the following command in your terminal:

    node index.js

The bot will log in using the provided token and will be ready to respond to commands in your Discord server.

# Permissions

Make sure the bot has the necessary permissions, especially the "Manage Messages" permission, in the channels where you intend to use it. If it lacks this permission, it won't be able to delete messages.

# Acknowledgments

This Discord bot was created with the help of the Discord.js library. Feel free to modify and extend it to suit your server's needs.
