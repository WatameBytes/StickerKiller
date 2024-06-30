const { SlashCommandBuilder } = require("discord.js");
const { blacklist } = require('../../utility/blacklist');

module.exports = {
    data: new SlashCommandBuilder()
        .setName("1984")
        .setDescription("Deletes a specified number of messages from a specific user within 1000 latest messages.")
        .addStringOption(option =>
            option.setName('user_id')
            .setDescription('ID of user whose messages you want to delete')
            .setRequired(true)
        )
        .addIntegerOption(option =>
            option.setName('max_count')
            .setDescription('Amount of messages you want to delete.')
            .setRequired(true)
        ),
    async execute(interaction) {
        const user_id = interaction.options.getString('user_id');
        const max_count = interaction.options.getInteger('max_count');
        try {
            interaction.channel.messages.fetch({ limit: 100 })
            .then(messages => {
                let msgDeleted = 0;
                for (const message of messages) {
                    // each message is an array, so message[1] returns the Message object containing author, id, and other properties
                    if (message[1].author.id === user_id && msgDeleted < max_count && !blacklist.has(message[1].id)) {
                        // message[1] is the actual message object, not message. therefore, the delete function is called on message[1]
                        message[1].delete();
                        msgDeleted++;
                    }
                    if (msgDeleted >= max_count) {
                        break;
                    }
                }
            })
            .then(
                interaction.reply({content: 'Deletion complete!', ephemeral: true})
            );
        } catch (error) {
            console.error(`A(n) ${error.name} has occurred: ${error.message}.`);
            if (interaction.replied || interaction.deferred) {
                await interaction.followUp({content: error.message, ephemeral: true});
            } else {
                await interaction.reply({ content: error.message, ephemeral: true });
            }
        }
    },
}
