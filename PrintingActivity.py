import curses
import threading
import time

import Attempt
import KeyCodes
import KeyListener
import LibraryManager
import Log
from Activity import Activity
from Content import Content
from EditTextContent import EditTextContent


class PrintingActivity(Activity):
    def __init__(self, widget: curses.window, key_listener: KeyListener, parent_activity: 'Activity' = None,
                 activity_name: str = ""):
        self.position: int = 0
        self.best_position: int = 0
        self.activity_name: str = LibraryManager.get_text()
        self.error_counter: int = Content("errors count: 0", widget, 0, 14)
        self.start_time: int = time.time();
        self.last_true_time: int = self.start_time
        self.attempt: Attempt = Attempt.Attempt()
        super().__init__(widget, key_listener, parent_activity, self.activity_name)

    def on_create(self):
        super().on_create()
        self.attempt.chars_count = len(self.activity_name)
        self.attempt.library = LibraryManager.get_library()

        def calculate_timer():
            time.sleep(0.1)
            start_time = time.time()
            while self.timer_thread_active:
                # _time = time.time()
                self.timer.text_of_content = "time: " + str(round(time.time() - start_time, 1))
                self.timer.print_content()
                y, x = self.edit_text.next_symbol()
                if self.false_text.text_of_content:
                    y, x = self.false_text.next_symbol()
                self.widget.move(y, x)
                self.widget.refresh()
                time.sleep(0.1)
        self.timer_thread_active: bool = True
        self.timer: Content = Content("time: ", self.widget, 0, 10)
        self.timer_thread: threading.Thread = threading.Thread(target=calculate_timer)
        self.timer_thread.daemon = True
        self.edit_text: EditTextContent = EditTextContent("", self.widget, 0, 3)
        self.false_text: EditTextContent = EditTextContent("", self.widget, 0, 3)
        self.false_text.color = curses.color_pair(3)

        def local_lambda():
            Log.print("aim:\n" + self.activity_name)
            Log.print("result:\n" + self.edit_text.text_of_content)
            if self.activity_name == self.edit_text.text_of_content:
                self.end_attempt()
                self.escape()
                self.return_to_parent_activity()

        self.edit_text.set_action(local_lambda)

    def key_event(self, pair):
        Log.print("ed", " ")
        Log.print(self.edit_text)
        Log.print("fal", " ")
        Log.print(self.false_text)
        fl, value = pair
        if fl:
            super().key_event(pair)
            if value == KeyCodes.Keys.BACKSPACE:
                if self.false_text.text_of_content != "":
                    self.false_text.delete()
                else:
                    if self.edit_text.text_of_content != "":
                        self.edit_text.delete()
                        self.prev_symb()
        else:
            if self.false_text.text_of_content:
                self.false_text.add(str(value))
                self.on_error()
            else:
                if self.position >= len(self.activity_name):
                    return
                if str(value) == self.activity_name[self.position]:
                    self.edit_text.add(str(value))
                    self.next_symb()
                else:
                    n_y, n_x = self.edit_text.next_symbol()
                    self.false_text.start = n_x
                    self.false_text.y = n_y
                    self.false_text.add(str(value))
                    self.false_symb()
                    self.on_error()

    def show(self):
        super().show()
        self.timer.print_content()
        self.timer_thread.start()
        self.error_counter.print_content()

    def escape(self):
        self.timer_thread_active = False
        super().escape()

    def activate_sign(self):
        self.edit_text.action()

    def on_error(self):
        self.attempt.errors_count += 1
        self.error_counter.text_of_content = "errors count: " + str(self.attempt.errors_count)
        self.error_counter.print_content()

    def end_attempt(self):
        self.attempt.time = time.time() - self.start_time
        self.attempt.save()

    def next_symb(self):
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

    def prev_symb(self):
        self.position -= 1

    def false_symb(self):
        cur_ch = self.activity_name[self.position]
        if cur_ch in self.attempt.key_stat_dict:
            self.attempt.key_stat_dict[cur_ch].sum_fails += 1
        else:
            new_stat = Attempt.KeyStat()
            new_stat.value = cur_ch
            new_stat.sum_fails = 1
            self.attempt.key_stat_dict[cur_ch] = new_stat
