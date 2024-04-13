from Activity import Activity
from Attempt import Attempt
from Content import Content
from ContentGroup import ContentGroup
from CycleContentList import CycleContentList


class ScoreBoardActivity(Activity):
    def __init__(self, widget, key_listener, parent_activity=None, activity_name=""):
        title_string = "Библиотека    Число символов   Число ошибок/c  Время/c"
        self.table_title = Content(title_string, widget, 0, 2)
        self.menu = CycleContentList("", widget, 0, 3, 10)
        self.attempts: list[Attempt] = Attempt.LoadRooms()
        super().__init__(widget, key_listener, parent_activity, activity_name)

    def ItemCreation(self, attempt: Attempt):
        result: ContentGroup = ContentGroup("", self.widget)
        values = [str(i) for i in attempt.to_relative_list()]
        content = Content(values[3], self.widget, 0, 0)
        content.FillTo(13)
        result.AddItem(content)
        content = Content(values[1], self.widget, 14, 0)
        content.FillTo(16)
        result.AddItem(content)
        content = Content(values[0], self.widget, 31, 0)
        content.FillTo(14)
        result.AddItem(content)
        content = Content(values[2], self.widget, 47, 0)
        content.FillTo(10)
        result.AddItem(content)
        return result
    def OnCreate(self):
        super().OnCreate()
        for attempt in reversed(self.attempts):
            self.menu.AddItem(self.ItemCreation(attempt))

    def ActivateSign(self):
        self.menu.Activate()

    def Show(self):
        super().Show()
        self.table_title.PrintContent()
        self.menu.PrintContent()
        self.menu.Activate()
    def KeyEvent(self, pair):
        flag, key = pair
        if flag:
            if self.menu.is_active:
                self.menu.KeyIvent(key)
            else:
                super().KeyEvent(pair)
    def Escape(self):
        if self.menu.is_active:
            self.menu.Disable()
        super().Escape()
        # super().ReturnToParentActivity()
