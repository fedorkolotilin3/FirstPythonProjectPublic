import curses

import Log


class Content:
    parent = None
    text_of_content = ""
    widget = None
    color = None

    def __init__(self, text_of_content, widget, x=0, y=0, parent=None):
        self.x = x
        self.y = y
        self.start = x
        self.text_of_content = text_of_content
        self.widget = widget
        self.parent = parent
        self.color = curses.color_pair(1)
        self.max_width = self.widget.getmaxyx()[1] - self.x
        self.re_count_geometry()

    def action(self):
        pass
        # self.OnAction(self)
        # self.color = curses.color_pair(3)
        # self.PrintContent()
        # self.widget.refresh()

    def print_content(self):
        self.re_count_geometry()
        self.clear_content()
        # y, x = self.widget.getyx()
        self.widget.addstr(self.y, self.start, self.text_of_content, self.color)
        # self.widget.move(y, x)
        self.re_count_geometry()

    def clear_content(self):
        for y in range(self.height):
            for x in range(self.max_width):
                if y > 0:
                    self.widget.delch(self.y + y, self.x)
                else:
                    self.widget.delch(self.y + y, self.start)

    def re_count_geometry(self):
        self.height = (self.start + len(self.text_of_content) - 1) // self.max_width + 1
        self.last_width = (self.start + len(self.text_of_content)) % self.max_width

    def next_symbol(self):
        if self.last_width == 0:
            return self.y + self.height, self.last_width
        return self.y + self.height - 1, self.last_width

    def set_action(self, action):
        self.Action = action

    def set_color(self, color):
        self.color = color

    def fill_to(self, count, ch=" "):
        ln = len(self.text_of_content)
        if ln <= count:
            self.text_of_content += ch * (count - ln)

    def get_height(self):
        self.re_count_geometry()
        return self.height

    def parent_x(self):
        if self.parent is None:
            return 0
        return self.parent.x

    def parent_y(self):
        if self.parent is None:
            return 0
        return self.parent.y

    def __copy__(self):
        # Log.print("copy runs")
        copy_res = Content(self.text_of_content, self.widget, self.x, self.y, self.parent)
        copy_res.set_color(self.color)
        copy_res.start = self.start
        copy_res.max_width = self.max_width
        copy_res.last_width = self.last_width
        copy_res.height = self.height
        return copy_res

    def __str__(self):
        return str(self.max_width) + " " + str(self.height) + " " + str(self.last_width) + " " + str(self.start)