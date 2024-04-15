import curses
import LibraryManager
import Log
from Activity import Activity
from Attempt import Attempt
from AttemptFullStatisticActivity import AttemptFullStatisticActivity
from Content import Content
from ContentGroup import ContentGroup
from ContentList import ContentList
from CycleContentList import CycleContentList
from KeyListener import KeyListener


class ScoreBoardActivity(Activity):
    def __init__(self, widget: curses.window, key_listener: KeyListener, parent_activity: 'Activity' = None,
                 activity_name: str = ""):
        super().__init__(widget, key_listener, parent_activity, activity_name)

    def item_creation(self, attempt: Attempt):
        result: ContentGroup = ContentGroup("", self.widget)
        values = [str(i) for i in attempt.to_relative_list()]
        content = Content(values[3], self.widget, 0, 0)
        content.fill_to(13)
        result.add_item(content)
        content = Content(values[1], self.widget, 14, 0)
        content.fill_to(16)
        result.add_item(content)
        content = Content(values[0], self.widget, 31, 0)
        content.fill_to(14)
        result.add_item(content)
        content = Content(values[2], self.widget, 47, 0)
        content.fill_to(10)
        result.add_item(content)

        def local_lambda():
            Log.print("attempt activity launching")
            attempt_activity = AttemptFullStatisticActivity(self.widget, self.key_listener, self, attempt=attempt)
            self.key_listener.add_activity(attempt_activity)
            self.escape()
            attempt_activity.show()
        result.set_action(local_lambda)
        return result

    def on_create(self):
        super().on_create()
        title_string = "Библиотека    Число символов   Ошибок/cимвол   Время/cимвол"
        self.table_title = Content(title_string, self.widget, 0, 2)
        self.menu = ContentList("", self.widget, 0, 3)
        # self.menu = CycleContentList("", self.widget, 0, 3, 10)
        attempt_menu = CycleContentList("", self.widget, 0, 0, 7, parent=self.menu)
        attempt_menu.set_action(attempt_menu.activate)

        self.attempts: list[Attempt] = Attempt.load_attempts()
        for attempt in reversed(self.attempts):
            attempt_menu.add_item(self.item_creation(attempt))

        all_time_stat: CycleContentList = CycleContentList("", self.widget, 0, 0, 5,
                                                           parent=self.menu)
        libraries: list[str] = LibraryManager.get_libraries()
        for lib in libraries:
            lib_content: Content = Content(lib, self.widget)

            def local_lambda_w(lib: str):
                def local_lambda():
                    summ_attempt = Attempt()
                    for _attempt in Attempt.load_attempts():
                        if _attempt.library == lib:
                            summ_attempt += _attempt
                    all_time_lib_activity = AttemptFullStatisticActivity(self.widget, self.key_listener, self,
                                                                         "", attempt=summ_attempt)
                    self.key_listener.add_activity(all_time_lib_activity)
                    self.escape()
                    all_time_lib_activity.show()
                return local_lambda
            lib_content.set_action(local_lambda_w(lib))
            all_time_stat.add_item(lib_content)
        all_time_stat.set_action(all_time_stat.activate)

        self.menu.add_item(attempt_menu, split=1)
        self.menu.add_item(all_time_stat)

    def activate_sign(self):
        self.menu.activate()

    def show(self):
        super().show()
        self.table_title.print_content()
        if self.menu.items:
            self.menu.print_content()
            self.menu.activate()

    def key_event(self, pair):
        flag, key = pair
        if flag:
            if self.menu.is_active:
                self.menu.key_event(key)
            else:
                super().key_event(pair)

    def escape(self):
        if self.menu.is_active:
            self.menu.disable()
        super().escape()
