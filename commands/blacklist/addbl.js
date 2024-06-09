const { SlashCommandBuilder } = require('discord.js');

const { blacklist } = require('./blacklist');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('addbl')
        .setDescription('Add a message to the blacklist')
        .addStringOption(option =>
            option.setName('message_id')
            .setDescription('The ID of a message you want to remove from the blacklist')),
    async execute(interaction) {
        const message = interaction.options.getString('message_id');
        blacklist.add(message);
        await interaction.reply(`Successfully added message ${message} to the blacklist!`);
    }
}