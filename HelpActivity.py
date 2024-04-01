from Activity import Activity


class HelpActivity(Activity):
    def __init__(self, widget, key_listener, parent_activity=None, activity_name=""):
        super().__init__(widget, key_listener, parent_activity, activity_name)
