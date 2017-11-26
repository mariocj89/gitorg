"""Definitions to work with the gitorg file that lays out the folder"""
import os
import yaml


class File:
    DEFAULT_FILENAME = ".gitorg"

    def __init__(self, *, filename=DEFAULT_FILENAME, lists=None):
        self._lists = lists or []
        self.filename = filename

    def sync(self):
        """Saves the file locally"""
        config = dict()
        config["lists"] = self.lists
        with open(self.filename, "w") as fp:
            yaml.dump(config, fp, default_flow_style=False)

    @classmethod
    def from_file(cls, filename):
        """Creates an instance from a filename"""
        with open(filename) as fp:
            config = yaml.load(fp)
        return cls(
            filename=filename,
            lists=config["lists"],
        )

    @classmethod
    def from_path(cls, path):
        """Creates an instance with default filename on the path passed in"""
        return cls.from_file(os.path.join(path, cls.DEFAULT_FILENAME))

    @classmethod
    def from_ws(cls):
        """Creates an instance with default filename on the current workspace"""
        return cls.from_path(os.getcwd())

    @property
    def lists(self):
        return self._lists

    @lists.setter
    def lists(self, value):
        self._lists = value
        self.sync()

