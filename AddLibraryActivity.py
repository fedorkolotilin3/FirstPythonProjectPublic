import curses

import KeyCodes
import LibraryManager
import Log
from Activity import Activity
from ContentList import ContentList
from EditTextContent import EditTextContent


class AddLibraryActivity(Activity):
    def __init__(self, widget, key_listener, parent_activity=None, activity_name=""):
        self.activity_name = ("Введите путь до папки с библиотекой\n "
                              "Формат папки: Папка без вложенных папок с .txt файлам, содержащими примеры для ввода")
        super().__init__(widget, key_listener, parent_activity, activity_name=self.activity_name)

    def OnCreate(self):
        super().OnCreate()
        self.edit_text = EditTextContent("", self.widget, 0, 3)
        def local_lambda():
            result_fl = ""
            result_name = ""
            # try:
            result_fl, result_name = LibraryManager.AddLibrary(self.edit_text.text_of_content)
            # except BaseException as e:
            #     result_fl = str(e)
            if result_fl:
                old_text = self.edit_text.text_of_content
                self.edit_text.text_of_content = result_fl
                self.edit_text.color = curses.color_pair(3)
                self.edit_text.PrintContent()
                self.edit_text.text_of_content = old_text
                self.edit_text.color = curses.color_pair(1)
            else:
                if self.parent_activity:
                    self.parent_activity.AddLib(result_name, -2)
                self.Escape()
                self.ReturnToParentActivity()
        self.edit_text.SetAction(local_lambda)
    def KeyEvent(self, pair):
        fl, value = pair
        if fl:
            super().KeyEvent(pair)
            if value == KeyCodes.Keys.BACKSPACE:
                self.edit_text.Delete()
        else:
            self.edit_text.Add(str(value))

    def ActivateSign(self):
        self.edit_text.Action()
