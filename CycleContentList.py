from ContentList import ContentList


class CycleContentList(ContentList):
    def __init__(self, text_of_content, widget, x, y, max_height=10, parent=None):
        super().__init__(text_of_content, widget, x, y, parent)
        self.max_height = max_height
        self.first_view_item = 0
        self.last_view_item = self.max_height - 1

    def Activate(self):
        super().Activate()

    def KeyIvent(self, key):
        super().KeyIvent(key)

    def Disable(self):
        super().Disable()

    def GoNext(self):
        if self.current_item_number == len(self.items) - 1:
            return
        if self.current_item_number == self.last_view_item:
            self.last_view_item += 1
            self.first_view_item += 1
        super().GoNext()

    def GoPrevious(self):
        if self.current_item_number == 0:
            return
        if self.current_item_number == self.first_view_item:
            self.last_view_item -= 1
            self.first_view_item -= 1
        super().GoPrevious()

    def GetItem(self, ind):
        return super().GetItem(ind)

    def AddItem(self, content, ind=-1, indent=0):
        super().AddItem(content, ind)

    def PrintContent(self):
        for i in range(self.first_view_item,
                       min(len(self.items), self.last_view_item + 1)):
            item = self.items[i]
            item.y = self.y + i - self.first_view_item
            item.PrintContent()
        self.widget.refresh()
