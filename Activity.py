import curses

from Content import Content
import KeyCodes
import Log
from ContentList import ContentList
import typing

class Activity:
    activity_name = "basic_activity"
    widget = None
    key_listener = None
    name_content = None
    parent_activity = None

    def __init__(self, widget, key_listener, parent_activity=None, activity_name=""):
        self.widget = widget
        self.key_listener = key_listener
        self.OnCreate()
        self.parent_activity = parent_activity
    def PrintHelp(self):
        string_to_print = "It's basic activity, no print info here\n"
        self.widget.addstr(string_to_print)
    def OnCreate(self):
        self.name_content = Content(self.activity_name, self.widget)
    def Escape(self):
        self.widget.clear()
        self.key_listener.RemoveActivity(self)
    def ReturnToParentActivity(self):
        if self.parent_activity:
            self.key_listener.AddActivity(self.parent_activity)
            self.parent_activity.Show()

    # def LaunchParentActivity(self):
    #     if self.parent_activity:
    #         activity = type(self.parent_activity)(self.parent_activity.parent_activity)
    #         self.key_listener.AddActivity(self.parent_activity)
    #         self.parent_activity.Show()

    def Show(self):
        self.name_content.PrintContent()
    def ActivateSign(self):
        pass
    def KeyEvent(self, pair):
        flag, key = pair
        if (flag):
            if (key == KeyCodes.Keys.ACTIVATE):
                self.ActivateSign()
            if (key == KeyCodes.Keys.ESCAPE):
                self.Escape()
                self.ReturnToParentActivity()
