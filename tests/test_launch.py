import curses
import os
import time


# import main

def test_launch():
    # screen = curses.initscr()
    # curses.start_color()
    os.system("xterm -e python3 ./src/main.py")
    # os.system("xterm")
    # time.sleep(10000)
    print("end of tests")
    # screen = curses.newwin(30, 80, 0, 0)
