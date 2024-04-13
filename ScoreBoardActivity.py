import LibraryManager
import Log
from Activity import Activity
from Attempt import Attempt
from AttemptFullStatisticActivity import AttemptFullStatisticActivity
from Content import Content
from ContentGroup import ContentGroup
from ContentList import ContentList
from CycleContentList import CycleContentList


class ScoreBoardActivity(Activity):
    def __init__(self, widget, key_listener, parent_activity=None, activity_name=""):
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
        def local_lambda():
            Log.print("attempt activity launching")
            attempt_activity = AttemptFullStatisticActivity(self.widget, self.key_listener, self, attempt=attempt)
            self.key_listener.AddActivity(attempt_activity)
            self.Escape()
            attempt_activity.Show()
        result.SetAction(local_lambda)
        return result
    def OnCreate(self):
        super().OnCreate()
        title_string = "Библиотека    Число символов   Ошибок/cимвол   Время/cимвол"
        self.table_title = Content(title_string, self.widget, 0, 2)
        self.menu = ContentList("", self.widget, 0, 3)
        # self.menu = CycleContentList("", self.widget, 0, 3, 10)
        attempt_menu = CycleContentList("", self.widget, 0, 0, 7, parent=self.menu)
        attempt_menu.SetAction(attempt_menu.Activate)

        self.attempts: list[Attempt] = Attempt.LoadAttempts()
        for attempt in reversed(self.attempts):
            attempt_menu.AddItem(self.ItemCreation(attempt))

        all_time_stat = CycleContentList("", self.widget, 0, 0, 5, parent=self.menu)
        libraries = LibraryManager.GetLibraries()
        for lib in libraries:
            lib_content = Content(lib, self.widget)

            def local_lambda_w(lib):
                def local_lambda():
                    summ_attempt = Attempt()
                    for _attempt in Attempt.LoadAttempts():
                        if _attempt.library == lib:
                            summ_attempt += _attempt
                    all_time_lib_activity = AttemptFullStatisticActivity(self.widget, self.key_listener, self,
                                                                         "", attempt=summ_attempt)
                    self.key_listener.AddActivity(all_time_lib_activity)
                    self.Escape()
                    all_time_lib_activity.Show()
                return local_lambda
            lib_content.SetAction(local_lambda_w(lib))
            all_time_stat.AddItem(lib_content)
        all_time_stat.SetAction(all_time_stat.Activate)

        self.menu.AddItem(attempt_menu, split=1)
        self.menu.AddItem(all_time_stat)

    def ActivateSign(self):
        self.menu.Activate()

    def Show(self):
        super().Show()
        self.table_title.PrintContent()
        if self.menu.items:
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
