"""Handles everything related to config files"""
from collections import defaultdict
import json


class BackedUpDict(dict):
    """A dictionary that is backed up with a function

    if an item is not found in self, calls the backup"""
    def __init__(self, backup, **kwargs):
        super(BackedUpDict, self).__init__(**kwargs)
        self.backup = backup

    def __missing__(self, item):
        return self.backup(item)


class Config(defaultdict):
    """Represents the configuration of the application

    Can be created from a config file encoded in json and can be persisted at any time
    """
    GLOBAL = 'global'

    def __init__(self, config_dict=None, **kwargs):
        """Creates a configuration object given a config dictionary

        A config dictionary contains keys for sections and each sections are pairs of
        key values where they represent option name and option value respectively.

        When looking for a value in a section, if the section or the option name
        don't exist, values from "global" sections will be taken
        if a global section exists
        """
        super(Config, self).__init__(lambda: self[self.GLOBAL])
        config_dict = config_dict or {}
        config_dict.update(kwargs)
        # Makes each section to default to the global
        self["global"] = config_dict.pop("global", {})
        for section, conf in config_dict.items():
            if isinstance(conf, dict):
                self[section] = BackedUpDict(self._get_global_option, **conf)
            else:
                self[section] = conf

    def _get_global_option(self, option_name):
        """Gets the option from the global section"""
        return self[self.GLOBAL][option_name]

    @classmethod
    def load(cls, config_file):
        """Reads a file and returns the configuration stores in it

        If the file does not exist, an exception is thrown
        """
        with open(config_file) as fp:
            raw_config = json.load(fp)
        return cls(raw_config)

    def save(self, config_file):
        """Reads a file and returns the configuration stores in it

        If the file does not exist, an exception is thrown
        """
        with open(config_file, "w") as fp:
            json.dump(self, fp)
