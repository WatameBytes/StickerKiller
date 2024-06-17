const { SlashCommandBuilder } = require('discord.js');
const { blacklist } = require('../../utility/blacklist');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('viewbl')
        .setDescription('View blacklisted messages'),
    async execute(interaction) {
        if (blacklist.size == 0) {
            await interaction.reply('There are no blacklisted messages')
        } else {
            let setData = Array.from(blacklist).join('\n');
            await interaction.reply('Blacklist:\n' + setData);
        }
    }
}