import curses
from copy import copy

from Content import Content
import KeyCodes
import Log
from ContentGroup import ContentGroup


class ContentList (ContentGroup):
    def __init__(self, text_of_content: str, widget: curses.window, x: int = 0, y: int = 0, parent: Content = None):
        self.is_active: bool = False
        self.current_item_number: int = 0
        self.splits: list[int] = []
        super(ContentList, self).__init__(text_of_content, widget, x, y, parent)

    def activate(self):
        if self.items:
            self.is_active = True
            if self.parent is not None:
                self.parent.active_child = self
            if self.active_child is not None:
                self.active_child.activate()
            else:
                self.items[self.current_item_number].set_color(curses.color_pair(2))
                self.print_content()

    def key_event(self, key):
        if self.active_child is None:
            if key == KeyCodes.Keys.ESCAPE:
                self.disable()
            if key == KeyCodes.Keys.ACTIVATE:
                if self.items:
                    self.items[self.current_item_number].set_color(curses.color_pair(1))
                    self.print_content()
                    self.items[self.current_item_number].action()
            if key == KeyCodes.Keys.UP:
                self.go_previous()
            if key == KeyCodes.Keys.DOWN:
                self.go_next()
        else:
            self.active_child.key_event(key)

    def disable(self):
        self.is_active = False
        if self.parent is not None:
            self.parent.active_child = None
            self.parent.items[self.parent.current_item_number].set_color(curses.color_pair(2))
            self.parent.print_content()
        else:
            self.items[self.current_item_number].set_color(curses.color_pair(1))
            self.print_content()

    def go_next(self):
        self.items[self.current_item_number].set_color(curses.color_pair(1))
        self.current_item_number += 1
        self.current_item_number %= len(self.items)
        self.items[self.current_item_number].set_color(curses.color_pair(2))
        self.print_content()

    def go_previous(self):
        self.items[self.current_item_number].set_color(curses.color_pair(1))
        self.current_item_number -= 1
        self.current_item_number %= len(self.items)
        self.items[self.current_item_number].set_color(curses.color_pair(2))
        self.print_content()

    def get_item(self, ind: int):
        return self.items[ind]

    def add_item(self, content: Content, ind=-1, indent=0, split=0):
        ind = (len(self.items) + ind) % len(self.items) + 1 if len(self.items) else 0
        if type(content) is str:
            created_content = Content(content, self.widget, 0, 0)
            content = created_content
        height_of_prev = 0
        for i in range(0, ind):
            height_of_prev += self.items[i].get_height() + self.splits[i]
        content.y = height_of_prev
        content.x = indent
        self.items.insert(ind, content)
        self.splits.insert(ind, split)
        for i in range(ind + 1, len(self.items)):
            self.items[i].y += 1

    def __copy__(self):
        copy_res = self.__class__("", self.widget, self.x, self.y)
        copy_res.is_active = self.is_active
        copy_res.items = self.items
        copy_res.current_item_number = self.current_item_number
        copy_res.set_color(self.color)
        return copy_res
