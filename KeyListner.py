import KeyCodes
import Log


class KeyListner:
    widget = None
    listening = False
    listening_activities = []
    def __init__(self, widget):
        self.widget = widget
        self.listening_activities = []
    def AddActivity(self, activity):
        # Log.print(activity.activity_name + " add")
        self.listening_activities.append(activity)
    def RemoveActivity(self, activity):
        if (activity in self.listening_activities):
            # Log.print(activity.activity_name + " rm)")
            self.listening_activities.remove(activity)
        # else:
            # Log.print(activity.activity_name + " rm(")
    def Activate(self):
        self.listening = True
        while (self.listening and self.listening_activities):
            # Log.print("all activities")
            # for activity in self.listening_activities:
            #     Log.print(activity.activity_name, " ")
            # Log.print("")
            self.raw_key = self.widget.get_wch()
            # Log.print(self.raw_key)
            key = KeyCodes.GetKey(self.raw_key)
            for activity in self.listening_activities:
                activity.KeyEvent(key)
    def WaitForEnter(self):
        while not (self.widget.get_wch() in KeyCodes[KeyCodes.Keys.ACTIVATE]):
            pass