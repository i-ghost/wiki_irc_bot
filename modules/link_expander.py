# -*- coding: utf-8 -*-

import re
import urllib
from ircutils import client, events


class LinkExpander(events.EventListener):

    def __init__(self):
        events.EventListener.__init__(self)
        self.linkRE = re.compile(r'\[\[([^][|]+)(?:\|([^][|]+))?\]\]')
        self.templateRE = re.compile(r'\{\{([^|{}]+?)[|}]')

    def fix_url(self, url):
        return url.replace(r'%3A', ':').replace(r'%20', '_').replace(r'%2F', '/',)

    def expand_links(self, line):
        if line.startswith('`') or line.startswith('!'):
            return None

        links = []
        uniques = []

        for link in self.linkRE.findall(line):
            target = link[0]
            label = link[1]
            prettylink = 'http://wiki.tf/' + self.fix_url(urllib.quote(target.title()))
            if target.lower() in uniques:
                continue
            if label == r'':
                links.append((target.replace('_', ' ')).title() + ': ' + prettylink)
            else:
                links.append((label.replace('_', ' ')).title() + ': ' + prettylink)
            uniques.append(target.lower())

        for link in self.templateRE.findall(line):
            if link.startswith('Template:'):
                link = link.replace('Template:', '', 1)
            prettylink = 'http://wiki.tf/Template:' + self.fix_url(urllib.quote(link.title()))
            if 'template:' + link.lower() in uniques:
                continue
            links.append(('Template:' + link.replace('_', ' ')).title() + ': ' + prettylink)
            uniques.append('template:' + link.lower())

        if len(links) > 0:
            return ' | '.join(links)
        else:
            return None

    def notify(self, client, event):
        if event.command == 'PRIVMSG':
            response = self.expand_links(event.message)
            if response:
                if event.target.startswith('#'):
                    client.send_message(event.target, response)
                else:
                    client.send_message(event.source, response)
