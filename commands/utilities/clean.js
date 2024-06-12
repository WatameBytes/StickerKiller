const { SlashCommandBuilder } = require("discord.js");

module.exports = {
    data: new SlashCommandBuilder()
        .setName("clean")
        .setDescription("Deletes a specified number of stickers from a specific user within 100 latest messages.")
        .addStringOption(option =>
            option.setName('user_id')
            .setDescription('ID of user whose messages you want to delete')
            .setRequired(true)
        ),
        // .addStringOption(option =>
        //     option.setName('max_count')
        //     .setDescription('Amount of messages you want to delete.')
        // ),
    async execute(interaction) {
        const user_id = interaction.options.getString('user_id');
        // const max_count = parseInt(interaction.options.getString('max_count'));
        
        await interaction.channel.messages.fetch({ limit: 100 })
            .then(messages => {
                for (const message of messages) {
                    // each message is an array, so message[1] returns the Message object containing author, id, and other properties
                    if (message[1].stickers.size > 0 && message[1].author.id === user_id) {
                        message.delete();
                    }
                }
            })
            .then(
                await interaction.reply({content: 'Deletion complete!', ephemeral: true})
            );
    },
}