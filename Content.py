import curses

import Log


class Content:
    parent = None
    text_of_content = ""
    widget = None
    color = None
    has_action = False

    def __init__(self, text_of_content, widget, x = 0, y = 0, parent=None):
        self.x = x
        self.y = y
        self.text_of_content = text_of_content
        self.widget = widget
        self.parent = parent
        self.color = curses.color_pair(1)

    # OnAction = lambda self, arg: 1
    def Action(self):
        pass
        # self.OnAction(self)
        # self.color = curses.color_pair(3)
        # self.PrintContent()
        # self.widget.refresh()

    def PrintContent(self):
        self.ClearString(self.y)
        self.widget.addstr(self.y, self.x, self.text_of_content, self.color)

    def ClearString(self, y):
        for x in range(self.widget.getmaxyx()[1] - self.x):
            self.widget.delch(y, self.x)


    def SetAction(self, action):
        self.Action = action
        self.has_action = True