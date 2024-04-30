import curses

import Log
from Activity import Activity
from KeyListener import KeyListener


class HelpActivity(Activity):
    def __init__(self, widget: curses.window, key_listener: KeyListener, parent_activity: 'Activity' = None,
                 activity_name: str = ""):

        super().__init__(widget, key_listener, parent_activity, activity_name)
        self.name_content.text_of_content = open("files/HelpText.txt", 'r').read()
