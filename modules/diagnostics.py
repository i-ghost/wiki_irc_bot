# -*- coding: utf-8 -*-

from ircutils import client, events

class Diagnostics(events.EventListener):

	def notify(self, client, event):
		if event.command == 'PRIVMSG' and event.message.startswith('!ping'):
			response = '!pong'
			if response:
				if event.target.startswith('#'):
					client.send_message(event.target, response)
				else:
					client.send_message(event.source, response)
