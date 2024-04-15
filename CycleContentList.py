import curses
from copy import copy

import Log
from Content import Content
from ContentList import ContentList


class CycleContentList(ContentList):
    def __init__(self, text_of_content, widget, x, y, max_height=10, parent=None):
        super().__init__(text_of_content, widget, x, y, parent)
        self.max_height = max_height
        self.first_view_item = 0
        self.last_view_item = self.max_height - 1

    def activate(self):
        super().activate()

    def key_event(self, key):
        super().key_event(key)

    def get_height(self):
        return self.max_height

    def disable(self):
        super().disable()

    def go_next(self):
        if self.current_item_number == len(self.items) - 1:
            return
        if self.current_item_number == self.last_view_item:
            self.last_view_item += 1
            self.first_view_item += 1
        super().go_next()

    def go_previous(self):
        if self.current_item_number == 0:
            return
        if self.current_item_number == self.first_view_item:
            self.last_view_item -= 1
            self.first_view_item -= 1
        super().go_previous()

    def get_item(self, ind):
        return super().get_item(ind)

    def add_item(self, content, ind=-1, indent=0, split=0):
        super().add_item(content, ind)

    def print_content(self):
        for i in range(self.first_view_item,
                       min(len(self.items), self.last_view_item + 1)):
            item = copy(self.items[i])
            item.y = self.y + i - self.first_view_item + self.parent_y()
            item.x += self.parent_x()
            item.print_content()
        self.widget.refresh()

    def __copy__(self):
        copy_res = super().__copy__()
        copy_res.max_height = self.max_height
        copy_res.first_view_item = self.first_view_item
        copy_res.last_view_item = self.last_view_item
        copy_res.set_color(self.color)
        return copy_res
