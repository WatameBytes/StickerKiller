const { blacklist } = require('../../utility/blacklist');
const { SlashCommandBuilder } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('removebl')
        .setDescription('Remove a message from the blacklist. Usage: $removebl <message_id>')
        .addStringOption(option =>
            option.setName('message_id')
            .setDescription('The ID of a message you want to remove from the blacklist')
        ),
    async execute(interaction) {
        const message = interaction.options.getString('message_id');
        blacklist.delete(message);
        await interaction.reply(`Message with id of ${message} removed from blacklist!`);
    }
}