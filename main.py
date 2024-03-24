import pyautogui
import readline
from threading import Thread


def editable_input(text):
    Thread(target=pyautogui.write, args=(text,)).start()
    modified_input = input()
    return modified_input


a = editable_input("This is a random text")
print("Received input : ", a)




"""import typer


def main():
    print("Hello World")


if __name__ == "__main__":
    typer.run(main)"""