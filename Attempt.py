import json
import typing

import LibraryManager
import Log


class KeyStat:
    def __init__(self):
        self.value = ""
        self.sum_fails = 0
        self.sum_time = 0.0
        self.use_count = 0

    def __add__(self, other):
        result = KeyStat()
        result.value = self.value
        result.sum_fails = self.sum_fails + other.sum_fails
        result.sum_time = self.sum_time + other.sum_time
        result.use_count = self.use_count + other.use_count
        return result

    def toDict(self):
        return self.__dict__
    @staticmethod
    def fromDict(dict_o):
        # Log.print(dict_o)
        # Log.print(type(dict_o))
        ans = KeyStat()
        for key, value in dict_o.items():
            setattr(ans, key, value)
        return ans

class Attempt:
    def __init__(self):
        self.ind = 0
        self.errors_count = 0
        self.chars_count = 0
        self.time = 0
        # self.library = LibraryManager.GetLibrary()
        self.library = ""
        self.lib_counter = 0
        self.key_stat_dict: dict[KeyStat] = {}
    def to_json_list(self):
        json_key_stat_dict = {a: self.key_stat_dict[a].toDict() for a in self.key_stat_dict}
        return [self.errors_count, self.chars_count, round(self.time, 4), self.library, json_key_stat_dict]

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
        attempt.key_stat_dict = {key: KeyStat.fromDict(value) for key, value in obj[4].items()}
        attempt.lib_counter = 1
        return attempt

    def Save(self):
        with open(LibraryManager.path_to_dir + "/" + "attempts.json", 'r+') as json_file:
            file_values = json.load(json_file)
            n = file_values["counter"]
            if n == 0:
                file_values["attempt_list"] = [self.to_json_list()]
            else:
                pass
                file_values["attempt_list"].append(self.to_json_list())
            file_values["counter"] += 1
            json_file.truncate(0)
            json_file.flush()
            json_file.seek(0)
            print(file_values)
            json.dump(file_values, json_file, indent=4)
    @staticmethod
    def LoadAttempts() -> list:
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
    def LoadAttempt(index: int):
        with open(LibraryManager.path_to_dir + "/" + "attempts.json", 'r+') as json_file:
            file_values = json.load(json_file)
            result = Attempt.from_list(file_values["attempt_list"][index])
            result.ind = index
            return result

    def ShortInfoString(self):
        return (f'{self.library} {self.chars_count} '
                f'{self.errors_count} {round(self.time, 4)}')

    def __add__(self, other):
        sum_res = Attempt()
        sum_res.time = self.time + other.time
        sum_res.errors_count = self.errors_count + other.errors_count
        sum_res.chars_count = self.chars_count + other.chars_count
        sum_res.key_stat_dict = {}
        sum_res.library = other.library
        sum_res.lib_counter = self.lib_counter + other.lib_counter
        for key in other.key_stat_dict:
            sum_res.key_stat_dict[key] = (other.key_stat_dict[key] +
                                          (self.key_stat_dict[key] if key in self.key_stat_dict else KeyStat()))

        return sum_res



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