from Content import Content


class EditTextContent(Content):

    def __init__(self, text_of_content, widget, x=0, y=0, parent=None):
        super().__init__(text_of_content, widget, x, y, parent)

    def Action(self):
        super().Action()

    def PrintContent(self):
        super().PrintContent()

    def SetAction(self, action):
        super().SetAction(action)

    def Delete(self):
        if len(self.text_of_content) > 0:
            self.text_of_content = self.text_of_content[:-1]
        self.PrintContent()

    def Add(self, string):
        self.text_of_content += string
        self.PrintContent()
