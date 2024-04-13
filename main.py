import curses

import Attempt
import KeyCodes
import Log
from KeyListner import KeyListner
from StartActivity import StartActivity

def main(stdscr):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)

    stdscr.get_wch()
    key_listener = KeyListner(stdscr)
    start_activity = StartActivity(stdscr, key_listener)
    start_activity.Show()
    key_listener.AddActivity(start_activity)
    key_listener.Activate()


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except [Exception]:
        print(Exception)
        Log.close()
