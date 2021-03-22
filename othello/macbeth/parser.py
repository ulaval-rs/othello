from configparser import ConfigParser


class MacbethParser(ConfigParser):

    def __init__(self, filepath: str, encoding=None) -> None:
        super().__init__()
        self.read(filepath, encoding)
