from copy import copy

import Log
from Content import Content


class ContentGroup(Content):
    def __init__(self, text_of_content, widget, x=0, y=0, parent=None):
        self.active_child = None
        self.items = []
        super().__init__(text_of_content, widget, x, y, parent)

    def AddItem(self, content):
        self.items.append(content)
    def PrintContent(self):
        # Log.print(f"printing content: {len(self.items)}")
        for item in self.items:
            item_copy = copy(item)
            item_copy.x += self.x + self.ParentX()
            item_copy.y += self.y + self.ParentY()
            item_copy.PrintContent()

    def SetColor(self, color):
        self.color = color
        # Log.print(type(self))
        # Log.print("color_seted")
        for item in self.items:
            item.SetColor(color)

    def ClearContent(self):
        for item in self.items:
            item_copy = item
            item_copy.x += self.x + self.ParentX()
            item_copy.y += self.y + self.ParentY()
            item_copy.ClearContent()
    def __getitem__(self, item):
        return self.items[item]

    def __copy__(self):
        copy_res = self.__class__("", self.widget, self.x, self.y)
        copy_res.items = self.items
        copy_res.SetColor(self.color)
        return copy_res

    def GetHeight(self):
        height = 1
        for item in self.items:
            height = max(height, item.GetHeight() + item.y)
        return height
