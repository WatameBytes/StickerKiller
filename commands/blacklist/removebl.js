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
        try {
            if (isNaN(parseInt(message))) {
                throw new TypeError('User submitted invalid ID.');
            }
            if (!blacklist.has(message)) {
                await interaction.reply('The message doesn\'t exist in the blacklist.')
                    .then(message => setTimeout(message.delete(), 5000));
            } else {
                blacklist.delete(message);
                await interaction.reply(`Message with id of ${message} removed from blacklist!`);
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
