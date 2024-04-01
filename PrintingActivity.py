import curses
import threading
import time

import KeyCodes
import LibraryManager
import Log
from Activity import Activity
from Content import Content
from EditTextContent import EditTextContent


class PrintingActivity(Activity):
    def __init__(self, widget, key_listener, parent_activity=None, activity_name=""):
        self.position = 0
        self.activity_name = LibraryManager.GetText()
        super().__init__(widget, key_listener, parent_activity, self.activity_name)

    def OnCreate(self):
        super().OnCreate()
        def CalculateTimer():
            start_time = time.time()
            while self.timer_thread_active:
                # _time = time.time()
                self.timer.text_of_content = "time: " + str(round(time.time() - start_time, 1))
                self.timer.PrintContent()
                self.widget.move(self.false_text.y, self.false_text.x + len(self.false_text.text_of_content))
                self.widget.refresh()
                time.sleep(0.01)
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
                self.Escape()
                self.ReturnToParentActivity()

        self.edit_text.SetAction(local_lambda)

    def KeyEvent(self, pair):
        fl, value = pair
        if fl:
            super().KeyEvent(pair)
            if value == KeyCodes.Keys.BACKSPACE:
                if self.false_text.text_of_content != "":
                    self.false_text.Delete()
                else:
                    self.edit_text.Delete()
                    self.position -= 1
                    self.false_text.x -= 1
        else:
            # self.edit_text.Add(str(value))
            if self.false_text.text_of_content:
                self.false_text.Add(str(value))
            else:
                if str(value) == self.activity_name[self.position]:
                    self.edit_text.Add(str(value))
                    self.false_text.x += 1
                    self.position += 1
                else:
                    self.false_text.Add(str(value))

    def Show(self):
        super().Show()
        self.timer.PrintContent()
        self.timer_thread.start()

    def Escape(self):
        self.timer_thread_active = False
        super().Escape()
    def ActivateSign(self):
        self.edit_text.Action()
