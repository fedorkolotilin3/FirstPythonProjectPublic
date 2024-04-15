from copy import copy

import Log
from Content import Content


class ContentGroup(Content):
    def __init__(self, text_of_content, widget, x=0, y=0, parent=None):
        self.active_child = None
        self.items = []
        super().__init__(text_of_content, widget, x, y, parent)

    def add_item(self, content):
        self.items.append(content)

    def print_content(self):
        for item in self.items:
            item_copy = copy(item)
            item_copy.x += self.x + self.parent_x()
            item_copy.y += self.y + self.parent_y()
            item_copy.print_content()

    def set_color(self, color):
        self.color = color
        for item in self.items:
            item.set_color(color)

    def clear_content(self):
        for item in self.items:
            item_copy = item
            item_copy.x += self.x + self.parent_x()
            item_copy.y += self.y + self.parent_y()
            item_copy.clear_content()

    def __getitem__(self, item):
        return self.items[item]

    def __copy__(self):
        copy_res = self.__class__("", self.widget, self.x, self.y)
        copy_res.items = self.items
        copy_res.set_color(self.color)
        return copy_res

    def get_height(self):
        height = 1
        for item in self.items:
            height = max(height, item.get_height() + item.y)
        return height
