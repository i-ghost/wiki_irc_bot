# -*- coding: utf-8 -*-

import re
from ircutils import client, events


class FunResponses(events.EventListener):
    def __init__(self):
        events.EventListener.__init__(self)
        self.commandRE = re.compile(r'!(\w+)\s*\w*')

    def cake(self, user, line):
        params = line.split()
        return "{0} will be baked, and then there will be cake.".format(
                " ".join(params[1:]) or user)

    def notify(self, client, event):
        if event.command == 'PRIVMSG' and self.commandRE.search(event.message):
            command = self.commandRE.search(event.message).group(1)
            response = None
            if command == 'cake':
                response = self.cake(event.source, event.message)
            if response:
                if event.target.startswith('#'):
                    client.send_message(event.target, response)
                else:
                    client.send_message(event.source, response)
