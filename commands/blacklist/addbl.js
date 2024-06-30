const { SlashCommandBuilder } = require('discord.js');

const { blacklist } = require('../../utility/blacklist');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('addbl')
        .setDescription('Add a message to the blacklist')
        .addStringOption(option =>
            option.setName('message_id')
            .setDescription('The ID of a message you want to remove from the blacklist')
            .setRequired(true)),
    async execute(interaction) {
        const message = interaction.options.getString('message_id');
        try {
            if (isNaN(parseInt(message))) {
                throw new TypeError('Message IDs only contains numbers!');
            }
            if (blacklist.has(message)) {
                await interaction.reply('The message was already exists in the blacklist.')
                    .then(message => setTimeout(message.delete(), 5000));
            } else {
                blacklist.add(message);
                await interaction.reply(`Successfully added message ${message} to the blacklist!`);
            }
        } catch (error) {
            console.error(`A(n) ${error.name} has occurred: ${error.message}.`);
            if (interaction.replied || interaction.deferred) {
                await interaction.followUp({content: 'There was an error while executing this command!', ephemeral: true});
            } else {
                await interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true });
            }
        }
    }
}
