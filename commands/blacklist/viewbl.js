const { SlashCommandBuilder } = require('discord.js');

const { blacklist } = require('./blacklist');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('viewbl')
        .setDescription('View blacklisted messages'),
    async execute(interaction) {
        try {
            if (blacklist.size == 0) {
                await interaction.reply('There are no blacklisted messages')
            } else {
                let setData = Array.from(blacklist).join('\n');
                await interaction.reply(setData);
            }
        } catch (error) {
            console.error(error);
            if (interaction.replied || interaction.deferred) {
                await interaction.followUp({content: 'There was an error while executing this command', ephemeral: true});
            } else {
                await interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true });
            }
        }
    }
}