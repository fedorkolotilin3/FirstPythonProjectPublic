from Content import Content


class EditTextContent(Content):

    def __init__(self, text_of_content, widget, x=0, y=0, parent=None):
        super().__init__(text_of_content, widget, x, y, parent)

    def action(self):
        super().Action()

    def print_content(self):
        super().print_content()

    def set_action(self, action):
        super().set_action(action)

    def delete(self):
        if len(self.text_of_content) > 0:
            self.clear_content()
            self.text_of_content = self.text_of_content[:-1]
            self.re_count_geometry()
        self.print_content()

    def add(self, string):
        self.text_of_content += string
        self.re_count_geometry()
        self.print_content()
