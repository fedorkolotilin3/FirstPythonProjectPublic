import json
import os
import random
import shutil

import Log

path_to_dir = "files"
path_to_file = path_to_dir + "/libraries_info.json"
libs_names = []
json_dict = {}

words_count = 20
texts = []
texts_count = 0

def GetLibraries():
    return libs_names
def GetLibraryNum():
    return json_dict["current_lib_num"]
def GetLibrary():
    if GetLibraryNum() == -1:
        return None
    return libs_names[GetLibraryNum()]
def SetLib(num):
    json_dict["current_lib_num"] = num
    GenerateTexts()
def Save():
    with open(path_to_file, 'w') as json_file:
        json.dump(json_dict, json_file, indent=4)
        json_file.close()
def Load():
    with open(path_to_file, 'r') as json_file:
        global json_dict, libs_names
        json_dict = json.load(json_file)
        libs_names = json_dict["libraries"]

def AddLibrary(dir_path):
    abs_path_to_dir = os.path.abspath(".")
    list_dir = os.listdir(dir_path)
    for file in list_dir:
        if not file.endswith("txt"):
            Log.print("LM-er error" + file)
            return "Ошибка, укащите КОРРЕКТНУЮ дирректорию", ""
    global path_to_dir
    dir_name = os.path.basename(dir_path)
    shutil.copytree(dir_path, abs_path_to_dir + "/" + path_to_dir + "/" + dir_name)
    Load()
    global json_dict
    json_dict["libraries"].append(dir_name)
    Save()
    return "", dir_name

def GetText():
    global texts_count
    if texts_count == 0:
        GenerateTexts()
    texts_count -= 1
    return texts[texts_count]

def GenerateTexts():
    if GetLibraryNum() == -1:
        return
    lib_dir = path_to_dir + "/" + GetLibrary()
    for file in os.listdir(lib_dir):
        with open(lib_dir + "/" + file, 'rb') as o_file:
            data = o_file.read().decode("utf-8", "replace").replace("�", "").replace('\n', '').replace('–', '').replace('  ', ' ').replace('…', '...')
            words = data.split()
            start_positions = [random.randint(0, len(words) - words_count) for i in range(40)]
            for i in start_positions:
                text = ""
                for j in range(words_count):
                    text += words[i + j] + (" " if j != words_count - 1 else '')
                texts.append(text)
    Log.print(texts)


Load()
