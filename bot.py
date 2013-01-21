# -*- coding: utf-8 -*-

import os
import imp
import inspect
import traceback
from ConfigParser import SafeConfigParser
from ircutils import bot


class ConfigError(Exception):
    pass


class Config(object):
    """A configuration object"""
    def __init__(self, config_file):
        self.config_file = config_file
        self.channels = {}
        self.bot = {}
        self.load_config()

    def load_config(self):
        """(Re)load configuration from disk"""
        try:
            _config = SafeConfigParser()
            _config.optionxform = str
            _config.read(self.config_file)
            for i in _config.sections():
                if i == "Bot":
                    self.bot["name"] = _config.get("Bot", "name")
                    self.bot["server"] = _config.get("Bot", "server")
                else:
                    # Everything else is a channel
                    for o in _config.options(i):
                        self.channels[i] = {o: _config.get(i, o)}
        except Exception:
            traceback.print_exc()
        else:
            del(_config)

    def _write_config(self):
        """Write the state back to disk"""
        _write = SafeConfigParser()
        _write.add_section("Bot")
        _write.set("Bot", "name", self.bot["name"])
        _write.set("Bot", "server", self.bot["server"])
        for chan in self.channels:
            _write.add_section(chan)
            for prop in self.channels[chan]:
                _write.set(chan, prop, self.channels[chan][prop])
        with open(self.config_file, "wt") as write_config_file:
            _write.write(write_config_file)

    def set_name(self, new_name):
        """Set a new name for the bot"""
        self.bot["name"] = new_name
        self._write_config()

    def add_channel(self, channel, key=None):
        """Adds/overwrites channels in config"""
        if key:
            self.channels[channel] = {"key": key}
        else:
            self.channels[channel] = {}
        self._write_config()

    def add_channel_properties(self, channel, props):
        """Add arbitrary properties to channels, props must be a dict"""
        if channel not in self.channels:
            self.add_channel(channel)
        for p in props:
            self.channels[channel][p] = props[p]
        self._write_config()


class IRCBot(bot.SimpleBot):
    """An IRC Bot"""

    def __init__(self, config):
        self.config = config

    def _enumerate_modules(self):
        filenames = []
        for fn in os.listdir(modules_dir):
            if fn.endswith(".py") and not fn.startswith("_"):
                filenames.append(os.path.join(modules_dir, fn))

        return filenames

    def load_modules(self):
        filenames = self._enumerate_modules()

        modules = []
        for filename in filenames:
            name = os.path.splitext(filename)[0]
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
                            print("Sucessfully loaded {0}...".format(name))
                        except Exception, e:
                            print("Failed to load {0}: {1}".format(name, e))
                except Exception, e:
                    print("Error getting module classes: {0}".format(e))


if __name__ == "__main__":

    config = Config("config.cfg")
    bot = IRCBot(config)
    bot.load_modules()

    channels = [i for i in config.channels]
    # Let's connect to the host
    bot.connect(config.bot["server"], channel=channels)

    # Start running the bot
    bot.start()
