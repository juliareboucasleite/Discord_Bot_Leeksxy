const discord = require('discord.js');
const db = require('quick.db');

module.exports = {
	name: 'pay',
	category: 'economia',
	aliases: ['doar', 'pagar'],
	run: async (client, message, args) => {
		const member = message.mentions.members.first();
		let rep = db.fetch(`rep_${message.author.id}`);

		if (!member) return message.channel.send('Você precisa mencionar alguém!!');
		if (message.content.includes('-'))
			return message.channel.send('não abuse.');
		if (member.id === message.author.id)
			return message.channel.send(
				'Você não pode fazer uma doação para si mesmo!!'
			);
		if (rep < args[1])
			return message.channel.send(
				`Como você vai fazer uma doação com uma quantidade que você não tem?!`
			);
		if (!args[1]) return message.channel.send('Quanto você vai doar??');

    if (isNaN(args[1])) {
      return message.channel.send(`${args[1]} n e um numero!!!`)
    }

		message.channel
			.send(`Você quer realmente doar ${args[1]} reps para ${member}??\nSe sim reaja com o emoji: 👍`)
			.then(msg => {
				msg.react('👍');

				let filtro = (reaction, usuario) =>
					reaction.emoji.name === '👍' && usuario.id === message.author.id;
				let coletor = msg.createReactionCollector(filtro, { max: 1 });

				coletor.on('collect', cp => {
					msg.delete();
					cp.remove(message.author.id);
					message.channel.send('Pagamento efetuado com sucesso!!');

					db.add(`rep_${member.id}`, args[1]);
					db.subtract(`rep_${message.author.id}`, args[1]);
				});
			});
	}
};
