import curses

import LibraryManager
import Log
from Activity import Activity
from AddLibraryActivity import AddLibraryActivity
from Content import Content
from ContentList import ContentList
import json

from KeyListener import KeyListener


class ChooseLibraryActivity(Activity):
    def __init__(self, widget: curses.window, key_listener: KeyListener, parent_activity: Activity = None,
                 activity_name: str = ""):

        self.menu: ContentList = None
        self.activity_name = "Here you can choose your library, from which words will be select"
        super().__init__(widget, key_listener, parent_activity, activity_name=self.activity_name)

    def on_create(self):
        super().on_create()
        self.menu = ContentList("choose library menu", self.widget, 0, 3)
        # Log.print(self.menu.text_of_content)
        libs_names = LibraryManager.get_libraries()
        for lib_name in libs_names:
            self.add_lib(lib_name)
        add_lib_ref = Content("Add new Library", self.widget)

        def local_lambda():
            add_lib_activity = AddLibraryActivity(self.widget, self.key_listener, self)
            self.key_listener.add_activity(add_lib_activity)
            self.escape()
            add_lib_activity.show()
        add_lib_ref.set_action(local_lambda)
        self.menu.add_item(add_lib_ref)
        self.menu.current_item_number = 0 if LibraryManager.get_library_num() == -1 else LibraryManager.get_library_num()

    def show(self):
        super().show()
        self.menu.activate()
        self.menu.print_content()

    def activate_sign(self):
        self.menu.activate()

    def key_event(self, pair):
        flag, key = pair
        if flag:
            if self.menu.is_active:
                self.menu.key_event(key)
            else:
                super().key_event(pair)

    def escape(self):
        if self.menu.is_active:
            self.menu.disable()
        super().escape()

    def add_lib(self, lib_name, position=-1):
        lib_content = Content(lib_name, self.widget)

        def local_lambda_c(loc_ind):
            def local_lambda():
                # Log.print("lib seted to " + str(loc_ind + 0))
                LibraryManager.set_lib(loc_ind)
                LibraryManager.save()
                self.menu.disable()
            return local_lambda
        lib_content.set_action(local_lambda_c(len(self.menu.items) + position + 1))
        self.menu.add_item(lib_content, position)


