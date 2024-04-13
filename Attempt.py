import json
import typing

import LibraryManager


class KeyStat:
    def __init__(self):
        self.value = ""
        self.sum_fails = 0
        self.sum_time = 0.0
        self.use_count = 0

class Attempt:
    def __init__(self):
        self.ind = 0
        self.errors_count = 0
        self.chars_count = 0
        self.time = 0
        # self.library = LibraryManager.GetLibrary()
        self.library = ""
        self.key_stat_dict = {}
    def to_list(self):
        return [self.errors_count, self.chars_count, round(self.time, 4), self.library, self.key_stat_dict]

    def to_relative_list(self):
        if self.chars_count != 0:
            return [round(self.errors_count / self.chars_count, 4), self.chars_count, round(self.time / self.chars_count, 4),  self.library, self.key_stat_dict]
        return [0.0, 0, 0.0, self.library]

    @staticmethod
    def from_list(obj: list):
        attempt = Attempt()
        attempt.errors_count = int(obj[0])
        attempt.chars_count = int(obj[1])
        attempt.time = float(obj[2])
        attempt.library = obj[3]
        attempt.key_stat_dict = obj[4]
        return attempt

    def Save(self):
        with open(LibraryManager.path_to_dir + "/" + "attempts.json", 'r+') as json_file:
            file_values = json.load(json_file)
            n = file_values["counter"]
            if n == 0:
                file_values["attempt_list"] = [self.to_list()]
            else:
                pass
                file_values["attempt_list"].append(self.to_list())
            file_values["counter"] += 1
            json_file.truncate(0)
            json_file.flush()
            json_file.seek(0)
            print(file_values)
            json.dump(file_values, json_file, indent=4)
    @staticmethod
    def LoadRooms() -> list:
        with open(LibraryManager.path_to_dir + "/" + "attempts.json", 'r+') as json_file:
            file_values = json.load(json_file)
            n = file_values["counter"]
            ans = []
            if n == 0:
                return ans
            for i in range(n):
                attempt_i = Attempt.from_list(file_values["attempt_list"][i])
                attempt_i.ind = i
                ans.append(attempt_i)
            return ans

    @staticmethod
    def LoadRoom(index: int):
        with open(LibraryManager.path_to_dir + "/" + "attempts.json", 'r+') as json_file:
            file_values = json.load(json_file)
            result = Attempt.from_list(file_values["attempt_list"][index])
            result.ind = index
            return result

    def ShortInfoString(self):
        return (f'{self.library} {self.chars_count} '
                f'{self.errors_count} {round(self.time, 4)}')


class AttemptEncoder(json.JSONEncoder):
    def default(self, obj: Attempt):
        return [obj.errors_count, obj.chars_count, obj.time, obj.library]

def decode_default(obj: list):
    attempt = Attempt()
    attempt.errors_count = int(obj[0])
    attempt.chars_count = int(obj[1])
    attempt.time = int(obj[2])
    attempt.library = obj[3]
    return attempt