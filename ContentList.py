import curses
from copy import copy

from Content import Content
import KeyCodes
import Log
from ContentGroup import ContentGroup


class ContentList (ContentGroup):
    is_active = False
    current_item_number = 0

    def __init__(self, text_of_content, widget, x, y, parent=None):
        self.splits = []
        super(ContentList, self).__init__(text_of_content, widget, x, y, parent)

    def Activate(self):
        self.is_active = True
        if self.parent != None:
            self.parent.active_child = self
        if self.active_child != None:
            self.active_child.Activate()
        else:
            self.items[self.current_item_number].SetColor(curses.color_pair(2))
            self.PrintContent()
    def KeyIvent(self, key):
        if self.active_child is None:
            if key == KeyCodes.Keys.ESCAPE:
                self.Disable()
            if key == KeyCodes.Keys.ACTIVATE:
                self.items[self.current_item_number].SetColor(curses.color_pair(1))
                self.PrintContent()
                self.items[self.current_item_number].Action()
            if key == KeyCodes.Keys.UP:
                self.GoPrevious()
            if key == KeyCodes.Keys.DOWN:
                self.GoNext()
        else:
            self.active_child.KeyIvent(key)
    def Disable(self):
        self.is_active = False
        if self.parent != None:
            self.parent.active_child = None
            self.parent.items[self.parent.current_item_number].SetColor(curses.color_pair(2))
            self.parent.PrintContent()
        else:
            self.items[self.current_item_number].SetColor(curses.color_pair(1))
            self.PrintContent()
        # Log.print(self.text_of_content + " printed")

    def GoNext(self):
        self.items[self.current_item_number].SetColor(curses.color_pair(1))
        self.current_item_number += 1
        self.current_item_number %= len(self.items)
        self.items[self.current_item_number].SetColor(curses.color_pair(2))
        self.PrintContent()
    def GoPrevious(self):
        self.items[self.current_item_number].SetColor(curses.color_pair(1))
        self.current_item_number -= 1
        self.current_item_number %= len(self.items)
        self.items[self.current_item_number].SetColor(curses.color_pair(2))
        self.PrintContent()
    def GetItem(self, ind):
        return self.items[ind]
    def AddItem(self, content, ind = -1, indent=0, split=0):
        ind = (len(self.items) + ind) % len(self.items) + 1 if len(self.items) else 0
        if type(content) == str:
            created_content = Content(content, self.widget, 0, 0)
            content = created_content
        height_of_prev = 0
        for i in range(0, ind):
            height_of_prev += self.items[i].GetHeight() + self.splits[i]
        content.y = height_of_prev
        content.x = indent
        self.items.insert(ind, content)
        self.splits.insert(ind, split)
        for i in range(ind + 1, len(self.items)):
            self.items[i].y += 1
        # self.current_item_number = 0
        # self.PrintContent()

    def __copy__(self):
        copy_res = self.__class__("", self.widget, self.x, self.y)
        # Log.print(type(copy_res))
        copy_res.is_active = self.is_active
        copy_res.items = self.items
        copy_res.current_item_number = self.current_item_number
        copy_res.SetColor(self.color)
        return copy_res
