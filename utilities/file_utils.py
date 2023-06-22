import os

from difflib import SequenceMatcher

class FileUtils:
    @staticmethod
    def read_file(filename):
        with open(filename, 'r') as file:
            return file.read().strip()

    @staticmethod
    def similarity(a, b):
        return SequenceMatcher(None, a, b).ratio()

    @staticmethod
    def write_to_file(filename, content):
        with open(filename, 'w') as file:
            file.write(content)

    @staticmethod
    def create_directories():
        if not os.path.exists("data"):
            os.mkdir("data")
        if not os.path.exists("data/output"):
            os.mkdir("data/output")
        if not os.path.exists("data/script"):
            os.mkdir("data/script")