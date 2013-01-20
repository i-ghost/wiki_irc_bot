# -*- coding: utf-8 -*-

from ircutils import client, events

class FunResponses(events.EventListener):

	def respond(self, user, line):
		if line.startswith('!cake'):
			params = line.split(' ')
			if params[1:]:
				return params[1:] + ' will be baked, and then there will be cake.'
			else:
				return user + ' will be baked, and then there will be cake.'
		return None

	def notify(self, client, event):
		if event.command == 'PRIVMSG' and event.message.startswith('!'):
			res = self.respond(event.source, event.message)
			if res:
				if event.target.startswith('#'):
					client.send_message(event.target, res)
				else:
					client.send_message(event.source, res)
