import KeyCodes
import Log


class KeyListener:
    widget = None
    listening = False
    listening_activities = []

    def __init__(self, widget):
        self.raw_key = None
        self.widget = widget
        self.listening_activities = []

    def add_activity(self, activity):
        # Log.print(activity.activity_name + " add")
        self.listening_activities.append(activity)

    def remove_activity(self, activity):
        if activity in self.listening_activities:
            self.listening_activities.remove(activity)

    def activate(self):
        self.listening = True
        while self.listening and self.listening_activities:
            self.raw_key = self.widget.get_wch()
            # Log.print(self.raw_key)
            key = KeyCodes.get_key(self.raw_key)
            for activity in self.listening_activities:
                activity.key_event(key)

    def wait_for_enter(self):
        while not (self.widget.get_wch() in KeyCodes.key_codes_new[KeyCodes.Keys.ACTIVATE]):
            pass
