import curses

from Content import Content
from KeyListener import KeyListener
import KeyCodes
import Log
from ContentList import ContentList
import typing


class Activity:
    def __init__(self, widget: curses.window, key_listener: KeyListener, parent_activity: 'Activity' = None,
                 activity_name: str = ""):
        self.name_content: Content = None
        self.widget: curses.window = widget
        self.key_listener: KeyListener = key_listener
        self.parent_activity: Activity = parent_activity
        self.activity_name: str = activity_name
        self.on_create()

    def print_help(self):
        string_to_print = "It's basic activity, no info to print here\n"
        self.widget.addstr(string_to_print)

    def on_create(self):
        self.name_content = Content(self.activity_name, self.widget)

    def escape(self):
        self.widget.clear()
        self.key_listener.remove_activity(self)

    def return_to_parent_activity(self):
        if self.parent_activity:
            self.key_listener.add_activity(self.parent_activity)
            self.parent_activity.show()

    def show(self):
        self.name_content.print_content()

    def activate_sign(self):
        pass

    def key_event(self, pair):
        flag, key = pair
        if flag:
            if key == KeyCodes.Keys.ACTIVATE:
                self.activate_sign()
            if key == KeyCodes.Keys.ESCAPE:
                self.escape()
                self.return_to_parent_activity()
