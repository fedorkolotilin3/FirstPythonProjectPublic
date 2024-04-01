import LibraryManager
import Log
from Activity import Activity
from AddLibraryActivity import AddLibraryActivity
from Content import Content
from ContentList import ContentList
import json


class ChooseLibraryActivity(Activity):
    menu = None
    def __init__(self, widget, key_listener, parent_activity=None, activity_name=""):
        self.activity_name = "Here you can choose your library, from which words will be select"
        super().__init__(widget, key_listener, parent_activity, activity_name=self.activity_name)

    def OnCreate(self):
        super().OnCreate()
        self.menu = ContentList("choose library menu", self.widget, 0, 3)
        Log.print(self.menu.text_of_content)
        libs_names = LibraryManager.GetLibraries()
        for lib_name in libs_names:
            self.AddLib(lib_name)
        self.menu.current_item_number = 0 if LibraryManager.GetLibraryNum() == -1 else LibraryManager.GetLibraryNum()
        add_lib_ref = Content("Add new Library", self.widget)
        def local_lambda():
            add_lib_activity = AddLibraryActivity(self.widget, self.key_listener, self)
            self.key_listener.AddActivity(add_lib_activity)
            self.Escape()
            add_lib_activity.Show()
        add_lib_ref.SetAction(local_lambda)
        self.menu.AddItem(add_lib_ref)




    def Show(self):
        super().Show()
        self.menu.Activate()
        self.menu.PrintContent()
    def ActivateSign(self):
        self.menu.Activate()
    def KeyEvent(self, pair):
        flag, key = pair
        if flag:
            if self.menu.is_active:
                self.menu.KeyIvent(key)
            else:
                super().KeyEvent(pair)
    def Escape(self):
        if (self.menu.is_active):
            self.menu.Disable()
        super().Escape()
    def AddLib(self, lib_name, position=-1):
        lib_content = Content(lib_name, self.widget)
        def local_lambda_c(loc_ind):
            def local_lambda():
                Log.print("lib seted to " + str(loc_ind + 0))
                LibraryManager.SetLib(loc_ind)
                LibraryManager.Save()
            return local_lambda

        lib_content.SetAction(local_lambda_c(len(self.menu.items)))
        self.menu.AddItem(lib_content, position)

