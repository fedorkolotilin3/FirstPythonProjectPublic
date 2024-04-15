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

    def on_create(self):
        super().on_create()
        self.edit_text = EditTextContent("", self.widget, 0, 3)

        def local_lambda():
            result_fl = ""
            result_name = ""
            try:
                result_fl, result_name = LibraryManager.add_library(self.edit_text.text_of_content)
            except BaseException as e:
                result_fl = str(e)
            if result_fl:
                old_text = self.edit_text.text_of_content
                self.edit_text.text_of_content = result_fl
                self.edit_text.color = curses.color_pair(3)
                self.edit_text.print_content()
                self.edit_text.text_of_content = old_text
                self.edit_text.color = curses.color_pair(1)
            else:
                if self.parent_activity:
                    Log.print("adding lib from addlibrary activity")
                    self.parent_activity.add_lib(result_name, -2)
                self.escape()
                self.return_to_parent_activity()
        self.edit_text.set_action(local_lambda)

    def key_event(self, pair):
        fl, value = pair
        if fl:
            super().key_event(pair)
            if value == KeyCodes.Keys.BACKSPACE:
                self.edit_text.delete()
        else:
            self.edit_text.add(str(value))

    def activate_sign(self):
        self.edit_text.action()
