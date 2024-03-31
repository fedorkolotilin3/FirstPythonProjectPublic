import curses

from Content import Content
import KeyCodes
import Log


class ContentList (Content):
    is_active = False
    items = []
    current_item_number = -1

    def __init__(self, text_of_content, widget, x, y, parent=None):
        super(ContentList, self).__init__(text_of_content, widget, x, y, parent)
        self.items = []

    def Activate(self):
        self.is_active = True
        self.items[self.current_item_number].color = curses.color_pair(2)
        self.PrintContent()
    def KeyIvent(self, key):
        if key == KeyCodes.Keys.ESCAPE:
            self.Disable()
        if key == KeyCodes.Keys.ACTIVATE:
            self.items[self.current_item_number].Action()
        if key == KeyCodes.Keys.UP:
            self.GoPrevious()
        if key == KeyCodes.Keys.DOWN:
            self.GoNext()
    def Disable(self):
        self.is_active = False
        self.items[self.current_item_number].color = curses.color_pair(1)
        self.PrintContent()
        Log.print(self.text_of_content + " printed")

    def GoNext(self):
        self.items[self.current_item_number].color = curses.color_pair(1)
        self.current_item_number += 1
        self.current_item_number %= len(self.items)
        self.items[self.current_item_number].color = curses.color_pair(2)
        self.PrintContent()
    def GoPrevious(self):
        self.items[self.current_item_number].color = curses.color_pair(1)
        self.current_item_number -= 1
        self.current_item_number %= len(self.items)
        self.items[self.current_item_number].color = curses.color_pair(2)
        self.PrintContent()
    def GetItem(self, ind):
        return self.items[ind]
    def AddItem(self, content, ind = -1):
        ind = (len(self.items) + ind) % len(self.items) + 1 if len(self.items) else 0
        Log.print("adding item to " + str(self))
        Log.print("size: " + str(len(self.items)))
        if (type(content) == str):
            created_content = Content(content, self.widget, 0, 0)
            content = created_content
        x, y = self.widget.getyx()
        self.widget.move(self.y + ind, 0)
        content.y = self.y + ind
        content.x = self.x
        self.items.insert(ind, content)
        for i in range(ind + 1, len(self.items)):
            self.items[i].y += 1
        self.current_item_number = 0
        self.PrintContent()
    def PrintContent(self):
        for item in self.items:
            item.PrintContent()
        self.widget.refresh()
