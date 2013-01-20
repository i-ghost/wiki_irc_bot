# -*- coding: utf-8 -*-

import os, imp, inspect
from botconfig import config
from ircutils import bot

modules_dir = 'modules'

class IRCBot(bot.SimpleBot):

	def enumerate_modules(self):
		filenames = []
		for fn in os.listdir(modules_dir):
			if fn.endswith('.py') and not fn.startswith('_'):
				filenames.append(os.path.join(modules_dir, fn))

		return filenames

	def load_modules(self):
		filenames = self.enumerate_modules()

		modules = []
		for filename in filenames:
			name = os.path.basename(filename)[:-3]
			try:
				module = imp.load_source(name, filename)
			except Exception, e:
				print('Error reading module {0}: {1}'.format(name, e))
			else:
				try:
					clsmembers = inspect.getmembers(module, inspect.isclass)
					for _class in clsmembers:
						try:
							name, path = _class
							self.register_listener(name, path())
							self[name].add_handler(path)
							print('Sucessfully loaded ' + name + '...')
						except:
							print('Failed to load ' + name + '...')
				except Exception, e:
					print('Error getting module classes: {0}'.format(e))


if __name__ == "__main__":

	bot = IRCBot(config['name'])
	bot.load_modules()

	# Let's connect to the host
	bot.connect(config['server'], channel=config['channels'])

	# Start running the bot
	bot.start()