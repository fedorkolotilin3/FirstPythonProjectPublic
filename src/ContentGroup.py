import curses
from copy import copy

import Log
from Content import Content


class ContentGroup(Content):
    def __init__(self, text_of_content: str, widget: curses.window, x: int = 0, y: int = 0, parent: Content = None):
        self.active_child: Content = None
        self.items: list[Content] = []
        super().__init__(text_of_content, widget, x, y, parent)

    def add_item(self, content: Content):
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

    def __getitem__(self, item) -> Content:
        return self.items[item]

    def __copy__(self) -> 'ContentGroup':
        copy_res: ContentGroup = self.__class__("", self.widget, self.x, self.y)
        copy_res.items = self.items
        copy_res.set_color(self.color)
        return copy_res

    def get_height(self) -> int:
        height = 1
        for item in self.items:
            height = max(height, item.get_height() + item.y)
        return height
