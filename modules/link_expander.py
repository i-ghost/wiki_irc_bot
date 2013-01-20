# -*- coding: utf-8 -*-

import re
from ircutils import client, events

class LinkExpander(events.EventListener):

	def expand_links(self, line):
		if line.startswith('`'):
			return None
		templateRE = re.compile(r'\{\{([^\}]+?)\}\}')
		simplelinkRE = re.compile(r'\[\[([^\]\|]+?)\]\]')
		complexlinkRE = re.compile(r'\[\[([^\]\|]+?)\|([^\]\|]+?)\]\]')

		templatelinks = ['Template:' + link + ' : ' + 'http://wiki.tf/Template:' + link.replace(' ', '_') for link in templateRE.findall(line)]
		simplelinks = [link + ' : ' + 'http://wiki.tf/' + link.replace(' ', '_') for link in simplelinkRE.findall(line)]
		complexlinks = [link[1] + ' : ' + 'http://wiki.tf/' + link[0].replace(' ', '_') for link in complexlinkRE.findall(line)]
		links = templatelinks + simplelinks + complexlinks

		if len(links) > 0:
			return ' , '.join(links)
		else:
			return None

	def notify(self, client, event):
		if event.command == 'PRIVMSG':
			res = self.expand_links(event.message)
			if res:
				if event.target.startswith('#'):
					client.send_message(event.target, res)
				else:
					client.send_message(event.source, res)
