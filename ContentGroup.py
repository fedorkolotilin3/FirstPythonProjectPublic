from copy import copy

from Content import Content


class ContentGroup(Content):
    def __init__(self, text_of_content, widget, x=0, y=0, parent=None):
        self.items = []
        super().__init__(text_of_content, widget, x, y, parent)

    def AddItem(self, content):
        self.items.append(content)
    def PrintContent(self):
        for item in self.items:
            item_copy = copy(item)
            item_copy.x += self.x
            item_copy.y += self.y
            item_copy.PrintContent()

    def SetColor(self, color):
        for item in self.items:
            item.SetColor(color)

    def ClearContent(self):
        for item in self.items:
            item_copy = item
            item_copy.x += self.x
            item_copy.y += self.y
            item_copy.ClearContent()
