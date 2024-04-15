import LibraryManager
import Log
from Activity import Activity
from ChooseLibraryActivity import ChooseLibraryActivity
from Content import Content
from ContentList import ContentList
from HelpActivity import HelpActivity
from PrintingActivity import PrintingActivity
from ScoreBoardActivity import ScoreBoardActivity


class StartActivity(Activity):
    def __init__(self, widget, key_listener):
        self.activity_name = "Hello, User! You are in main menu"
        super().__init__(widget, key_listener, activity_name=self.activity_name)

    def on_create(self):
        super().on_create()
        # self.name_content = Content(self.activity_name, self.widget)
        self.menu = ContentList("start_activity_main_manu",
                                self.widget, 0, 3)
        if LibraryManager.get_library_num() != -1:
            printing_activity_ref = Content("Start printing", self.widget)

            def local_lambda():
                printing_activity = PrintingActivity(self.widget, self.key_listener, self)
                self.escape()
                self.key_listener.add_activity(printing_activity)
                printing_activity.show()
            printing_activity_ref.set_action(local_lambda)
            self.menu.add_item(printing_activity_ref)

        choose_library_activity_ref = Content("Choose Library", self.widget)

        def local_lambda():
            choose_library_activity = ChooseLibraryActivity(self.widget, self.key_listener, self)
            self.key_listener.add_activity(choose_library_activity)
            self.escape()
            choose_library_activity.show()
        choose_library_activity_ref.set_action(local_lambda)

        def local_lambda():
            help_activity = HelpActivity(self.widget, self.key_listener, self, "it's help")
            self.key_listener.add_activity(help_activity)
            self.escape()
            help_activity.show()
        help_activity_ref = Content("Help", self.widget)
        help_activity_ref.set_action(local_lambda)

        score_board_activity_ref = Content("Your score", self.widget)

        def local_lambda():
            score_board_activity = ScoreBoardActivity(self.widget, self.key_listener, self, "Score Board")
            self.key_listener.add_activity(score_board_activity)
            self.escape()
            score_board_activity.show()
        score_board_activity_ref.set_action(local_lambda)
        self.menu.add_item(choose_library_activity_ref)
        self.menu.add_item(help_activity_ref)
        self.menu.add_item(score_board_activity_ref)

    def activate_sign(self):
        self.menu.activate()

    def show(self):
        super().show()
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
