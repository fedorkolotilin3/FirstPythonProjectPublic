import time

import Log
from Activity import Activity
from Attempt import Attempt, KeyStat
from Content import Content
from ContentGroup import ContentGroup
from CycleContentList import CycleContentList


class AttemptFullStatisticActivity(Activity):
    def __init__(self, widget, key_listener, parent_activity=None, activity_name="", attempt=Attempt()):
        self.attempt = attempt
        activity_name = "Detail statistic"
        super().__init__(widget, key_listener, parent_activity, activity_name)

    def on_create(self):
        title_string = "Библиотека    Число символов   Ошибок/cимвол   Время/cимвол"
        self.title_content = Content(title_string, self.widget, 0, 2)
        self.stat_values = ContentGroup("", self.widget, 0, 3)
        values = [str(i) for i in self.attempt.to_relative_list()]
        content = Content(f'{values[3]}({self.attempt.lib_counter})', self.widget, 0, 0)
        content.fill_to(13)
        self.stat_values.add_item(content)
        content = Content(values[1], self.widget, 14, 0)
        content.fill_to(16)
        self.stat_values.add_item(content)
        content = Content(values[0], self.widget, 31, 0)
        content.fill_to(14)
        self.stat_values.add_item(content)
        content = Content(values[2], self.widget, 47, 0)
        content.fill_to(10)
        self.stat_values.add_item(content)

        list_header_string = "Символ      Число ошибок    Число встреч    Среднее время    Среднее число ошибок"
        self.list_header = Content(list_header_string, self.widget, 0, 5)
        self.key_stat_list = CycleContentList("", self.widget, 0, 6, 7)
        # Log.print(type(self.attempt.key_stat_dict))
        # Log.print(self.attempt.key_stat_dict)
        key_arr = [key for key in self.attempt.key_stat_dict]
        key_arr.sort()
        for key in key_arr:
            key_stat: KeyStat = self.attempt.key_stat_dict[key]
            # Log.print(type(key_stat))
            stat_values = ContentGroup("", self.widget, 0, 3)
            content = Content("|" + str(key_stat.value) + "|", self.widget, 0, 0)
            content.fill_to(13)
            stat_values.add_item(content)
            content = Content(str(key_stat.sum_fails), self.widget, 14, 0)
            content.fill_to(16)
            stat_values.add_item(content)
            content = Content(str(key_stat.use_count), self.widget, 31, 0)
            content.fill_to(14)
            stat_values.add_item(content)
            content = Content(str(round(key_stat.sum_time / key_stat.use_count, 4)), self.widget, 47, 0)
            content.fill_to(10)
            stat_values.add_item(content)
            content = Content(str(round(key_stat.sum_fails / key_stat.use_count, 4)), self.widget, 65, 0)
            content.fill_to(10)
            stat_values.add_item(content)
            self.key_stat_list.add_item(stat_values)
        super().on_create()

    def activate_sign(self):
        self.key_stat_list.activate()

    def show(self):
        Log.print("attempt activity show")
        super().show()
        self.title_content.print_content()
        self.stat_values.print_content()
        self.list_header.print_content()
        if self.key_stat_list.items:
            self.key_stat_list.print_content()
            self.key_stat_list.activate()

    def key_event(self, pair):
        flag, key = pair
        if flag:
            if self.key_stat_list.is_active:
                self.key_stat_list.key_event(key)
            else:
                super().key_event(pair)

    def escape(self):
        if self.key_stat_list.is_active:
            self.key_stat_list.disable()
        super().escape()
