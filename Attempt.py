import json

import LibraryManager


class Attempt:
    def __init__(self):
        self.errors_count = 0
        self.chars_count = 0
        self.time = 0
        self.library = LibraryManager.GetLibrary()


def Save():
    with open(LibraryManager.path_to_dir + "/" + "attempts.json") as json_file:
        json.load()