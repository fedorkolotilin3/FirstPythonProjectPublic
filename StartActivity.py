import LibraryManager
import Log
from Activity import Activity
from ChooseLibraryActivity import ChooseLibraryActivity
from Content import Content
from ContentList import ContentList
from PrintingActivity import PrintingActivity


class StartActivity(Activity):
    menu = None
    def __init__(self, widget, key_listener):
        self.activity_name = "Hello, User! You are in main menu"
        super().__init__(widget, key_listener)

    def OnCreate(self):
        self.name_content = Content(self.activity_name, self.widget)
        self.menu = ContentList("start_activity_main_manu",
                                self.widget, 0, 3)
        Log.print(self.menu.text_of_content)
        if LibraryManager.GetLibraryNum() != -1:
            printing_activity_ref = Content("Start printing", self.widget)

            def local_lambda():
                printing_activity = PrintingActivity(self.widget, self.key_listener, self)
                self.Escape()
                self.key_listener.AddActivity(printing_activity)
                printing_activity.Show()
            printing_activity_ref.SetAction(local_lambda)
            self.menu.AddItem(printing_activity_ref)

        choose_library_activity_ref = Content("Choose Library", self.widget)

        def local_lambda():
            choose_library_activity = ChooseLibraryActivity(self.widget, self.key_listener, self)
            self.key_listener.AddActivity(choose_library_activity)
            self.Escape()
            choose_library_activity.Show()
        choose_library_activity_ref.SetAction(local_lambda)

        help_activity_ref = Content("Help", self.widget)
        score_board_activity_ref = Content("Your score", self.widget)
        self.menu.AddItem(choose_library_activity_ref)
        self.menu.AddItem(help_activity_ref)
        self.menu.AddItem(score_board_activity_ref)

    def ActivateSign(self):
        self.menu.Activate()

    def Show(self):
        self.name_content.PrintContent()
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
