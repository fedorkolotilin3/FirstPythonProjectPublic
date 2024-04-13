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

    def OnCreate(self):
        title_string = "Библиотека    Число символов   Ошибок/cимвол   Время/cимвол"
        self.title_content = Content(title_string, self.widget, 0, 2)
        self.stat_values = ContentGroup("", self.widget, 0, 3)
        values = [str(i) for i in self.attempt.to_relative_list()]
        content = Content(f'{values[3]}({self.attempt.lib_counter})', self.widget, 0, 0)
        content.FillTo(13)
        self.stat_values.AddItem(content)
        content = Content(values[1], self.widget, 14, 0)
        content.FillTo(16)
        self.stat_values.AddItem(content)
        content = Content(values[0], self.widget, 31, 0)
        content.FillTo(14)
        self.stat_values.AddItem(content)
        content = Content(values[2], self.widget, 47, 0)
        content.FillTo(10)
        self.stat_values.AddItem(content)

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
            content.FillTo(13)
            stat_values.AddItem(content)
            content = Content(str(key_stat.sum_fails), self.widget, 14, 0)
            content.FillTo(16)
            stat_values.AddItem(content)
            content = Content(str(key_stat.use_count), self.widget, 31, 0)
            content.FillTo(14)
            stat_values.AddItem(content)
            content = Content(str(round(key_stat.sum_time / key_stat.use_count, 4)), self.widget, 47, 0)
            content.FillTo(10)
            stat_values.AddItem(content)
            content = Content(str(round(key_stat.sum_fails / key_stat.use_count, 4)), self.widget, 65, 0)
            content.FillTo(10)
            stat_values.AddItem(content)
            self.key_stat_list.AddItem(stat_values)
        super().OnCreate()

    def ActivateSign(self):
        self.key_stat_list.Activate()

    def Show(self):
        Log.print("attempt activity show")
        super().Show()
        self.title_content.PrintContent()
        self.stat_values.PrintContent()
        self.list_header.PrintContent()
        if self.key_stat_list.items:
            self.key_stat_list.PrintContent()
            self.key_stat_list.Activate()
    def KeyEvent(self, pair):
        flag, key = pair
        if flag:
            if self.key_stat_list.is_active:
                self.key_stat_list.KeyIvent(key)
            else:
                super().KeyEvent(pair)
    def Escape(self):
        if self.key_stat_list.is_active:
            self.key_stat_list.Disable()
        super().Escape()
