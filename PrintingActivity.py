import curses
import threading
import time

import Attempt
import KeyCodes
import KeyListner
import LibraryManager
import Log
from Activity import Activity
from Content import Content
from EditTextContent import EditTextContent


class PrintingActivity(Activity):
    def __init__(self, widget, key_listener, parent_activity=None, activity_name=""):
        self.position = 0
        self.best_position = 0
        self.activity_name = LibraryManager.GetText()
        self.error_counter = Content("errors count: 0", widget, 0, 14)
        self.start_time = time.time();
        self.last_true_time = self.start_time
        self.attempt = Attempt.Attempt()
        super().__init__(widget, key_listener, parent_activity, self.activity_name)

    def OnCreate(self):
        super().OnCreate()
        self.attempt.chars_count = len(self.activity_name)
        self.attempt.library = LibraryManager.GetLibrary()
        def CalculateTimer():
            time.sleep(0.1)
            start_time = time.time()
            while self.timer_thread_active:
                # _time = time.time()
                self.timer.text_of_content = "time: " + str(round(time.time() - start_time, 1))
                self.timer.PrintContent()
                # Log.print(str(self.false_text.height) + " " + str(self.false_text.last_width) + " " + str(self.false_text.max_width))
                y, x = self.edit_text.NextSymbol()
                if self.false_text.text_of_content:
                    y, x = self.false_text.NextSymbol()
                self.widget.move(y, x)
                self.widget.refresh()
                time.sleep(0.1)
        self.timer_thread_active = True
        self.timer = Content("time: ", self.widget, 0, 10)
        self.timer_thread = threading.Thread(target=CalculateTimer)
        self.timer_thread.daemon = True
        self.edit_text = EditTextContent("", self.widget, 0, 3)
        self.false_text = EditTextContent("", self.widget, 0, 3)
        self.false_text.color = curses.color_pair(3)

        def local_lambda():
            Log.print("aim:\n" + self.activity_name)
            Log.print("result:\n" + self.edit_text.text_of_content)
            if self.activity_name == self.edit_text.text_of_content:
                self.EndAttempt()
                self.Escape()
                self.ReturnToParentActivity()

        self.edit_text.SetAction(local_lambda)

    def KeyEvent(self, pair):
        Log.print("ed", " ")
        Log.print(self.edit_text)
        Log.print("fal", " ")
        Log.print(self.false_text)
        fl, value = pair
        if fl:
            super().KeyEvent(pair)
            if value == KeyCodes.Keys.BACKSPACE:
                if self.false_text.text_of_content != "":
                    self.false_text.Delete()
                else:
                    if self.edit_text.text_of_content != "":
                        self.edit_text.Delete()
                        self.PrevSymb()
        else:
            if self.false_text.text_of_content:
                self.false_text.Add(str(value))
                self.OnError()
            else:
                if self.position >= len(self.activity_name):
                    return
                if str(value) == self.activity_name[self.position]:
                    self.edit_text.Add(str(value))
                    self.NextSymb()
                else:
                    n_y, n_x = self.edit_text.NextSymbol()
                    self.false_text.start = n_x
                    self.false_text.y = n_y
                    self.false_text.Add(str(value))
                    self.FalseSymb()
                    self.OnError()


    def Show(self):
        super().Show()
        self.timer.PrintContent()
        self.timer_thread.start()
        self.error_counter.PrintContent()

    def Escape(self):
        self.timer_thread_active = False
        super().Escape()
    def ActivateSign(self):
        self.edit_text.Action()

    def OnError(self):
        self.attempt.errors_count += 1
        self.error_counter.text_of_content = "errors count: " + str(self.attempt.errors_count)
        self.error_counter.PrintContent()
    def EndAttempt(self):
        self.attempt.time = time.time() - self.start_time
        self.attempt.Save()
    def NextSymb(self):
        if self.best_position == self.position:
            cur_ch = self.activity_name[self.position]
            cur_ch = cur_ch.lower()
            next_time = time.time()
            if cur_ch in self.attempt.key_stat_dict:
                self.attempt.key_stat_dict[cur_ch].use_count += 1
                self.attempt.key_stat_dict[cur_ch].sum_time += next_time - self.last_true_time
            else:
                new_stat = Attempt.KeyStat()
                new_stat.value = cur_ch
                new_stat.sum_time = next_time - self.last_true_time
                new_stat.use_count = 1
                self.attempt.key_stat_dict[cur_ch] = new_stat
            self.last_true_time = next_time
        self.position += 1
        self.best_position = max(self.best_position, self.position)
    def PrevSymb(self):
        self.position -= 1
    def FalseSymb(self):
        cur_ch = self.activity_name[self.position]
        if cur_ch in self.attempt.key_stat_dict:
            self.attempt.key_stat_dict[cur_ch].sum_fails += 1
        else:
            new_stat = Attempt.KeyStat()
            new_stat.value = cur_ch
            new_stat.sum_fails = 1
            self.attempt.key_stat_dict[cur_ch] = new_stat
