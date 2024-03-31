import curses

import KeyCodes
import LibraryManager
import Log
from Activity import Activity
from EditTextContent import EditTextContent


class PrintingActivity(Activity):
    def __init__(self, widget, key_listener, parent_activity=None, activity_name=""):
        self.position = 0
        self.activity_name = LibraryManager.GetText()
        super().__init__(widget, key_listener, parent_activity, activity_name)

    def OnCreate(self):
        super().OnCreate()
        self.edit_text = EditTextContent("", self.widget,0,  curses.getsyx()[0] + 2)
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
                pass
                # self.edit_text.Delete()
        else:
            # self.edit_text.Add(str(value))
            if str(value) == self.activity_name[self.position]:
                self.edit_text.Add(str(value))
                self.position+=1

    def ActivateSign(self):
        self.edit_text.Action()
