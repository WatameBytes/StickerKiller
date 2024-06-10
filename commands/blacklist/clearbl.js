const { SlashCommandBuilder } = require('discord.js');

const { blacklist } = require('./blacklist');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('clearbl')
        .setDescription('VClear the blacklist'),
    async execute(interaction) {
        if (blacklist.size == 0) {
            await interaction.reply('There are no blacklisted messages');
        } else {
            blacklist.clear();
            await interaction.reply('The blacklist has been cleared');
        }
    }
}