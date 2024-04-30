from __future__ import annotations

import json
import typing
import LibraryManager
import Log


class KeyStat:
    def __init__(self):
        self.value: int = ""
        self.sum_fails: int = 0
        self.sum_time: float = 0.0
        self.use_count: int = 0

    def __add__(self, other: KeyStat):
        result: KeyStat = KeyStat()
        result.value = self.value
        result.sum_fails = self.sum_fails + other.sum_fails
        result.sum_time = self.sum_time + other.sum_time
        result.use_count = self.use_count + other.use_count
        return result

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(dict_o: dict):
        ans: KeyStat = KeyStat()
        for key, value in dict_o.items():
            setattr(ans, key, value)
        return ans


class Attempt:
    def __init__(self):
        self.ind: int = 0
        self.errors_count: int = 0
        self.chars_count: int = 0
        self.time: int = 0
        self.library: str = ""
        self.lib_counter: int = 0
        self.key_stat_dict: dict[KeyStat] = {}

    def to_json_list(self):
        json_key_stat_dict = {a: self.key_stat_dict[a].to_dict() for a in self.key_stat_dict}
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
        attempt.key_stat_dict = {key: KeyStat.from_dict(value) for key, value in obj[4].items()}
        attempt.lib_counter = 1
        return attempt

    def save(self):
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
            json.dump(file_values, json_file, indent=4)

    @staticmethod
    def load_attempts() -> list:
        with open(LibraryManager.path_to_dir + "/" + "attempts.json", 'r+') as json_file:
            file_values = json.load(json_file)
            n: int = file_values["counter"]
            ans: list = []
            if n == 0:
                return ans
            for i in range(n):
                attempt_i = Attempt.from_list(file_values["attempt_list"][i])
                attempt_i.ind = i
                ans.append(attempt_i)
            return ans

    @staticmethod
    def load_attempt(index: int):
        with open(LibraryManager.path_to_dir + "/" + "attempts.json", 'r+') as json_file:
            file_values = json.load(json_file)
            result: Attempt = Attempt.from_list(file_values["attempt_list"][index])
            result.ind = index
            return result

    def short_info_string(self):
        return (f'{self.library} {self.chars_count} '
                f'{self.errors_count} {round(self.time, 4)}')

    def __add__(self, other: Attempt):
        sum_res: Attempt = Attempt()
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
