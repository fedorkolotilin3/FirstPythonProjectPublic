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


def get_libraries():
    return libs_names


def get_library_num():
    return json_dict["current_lib_num"]


def get_library():
    if get_library_num() == -1:
        return None
    return libs_names[get_library_num()]


def set_lib(num):
    json_dict["current_lib_num"] = num
    generate_texts()


def save():
    with open(path_to_file, 'w') as json_file:
        json.dump(json_dict, json_file, indent=4)
        json_file.close()


def load():
    with open(path_to_file, 'r') as json_file:
        global json_dict, libs_names
        json_dict = json.load(json_file)
        libs_names = json_dict["libraries"]


def add_library(dir_path):
    global path_to_dir
    abs_path_to_dir = os.path.abspath(".")
    dir_name = os.path.basename(dir_path)
    list_dir = os.listdir(dir_path)
    for file in list_dir:
        if not file.endswith("txt"):
            # Log.print("LM-er error" + file)
            return "Ошибка, укажиите КОРРЕКТНУЮ дирректорию", ""

    lib_content = ""
    for file in list_dir:
        lib_content += get_data_from_file(dir_path + "/" + file)
    open(abs_path_to_dir + "/" + path_to_dir + "/" + dir_name + ".txt", "w").write(lib_content)
    # shutil.copytree(dir_path, abs_path_to_dir + "/" + path_to_dir + "/" + dir_name)
    load()
    global json_dict
    json_dict["libraries"].append(dir_name)
    save()
    return "", dir_name


def get_text():
    global texts_count
    if texts_count == 0:
        generate_texts()
    texts_count -= 1
    return texts[texts_count]


def generate_texts():
    if get_library_num() == -1:
        return
    lib_dir = path_to_dir + "/" + get_library()
    data = get_data_from_file(lib_dir + ".txt")
    words = data.split()
    start_positions = [random.randint(0, len(words) - words_count) for i in range(40)]
    for i in start_positions:
        text = ""
        for j in range(words_count):
            text += words[i + j] + (" " if j != words_count - 1 else '')
        texts.append(text)
    # Log.print(texts)


def get_data_from_file(file):
    with open(file, 'rb') as o_file:
        data = o_file.read().decode("utf-8", "replace").replace("�", "").replace('\n', '').replace('–', '').replace(
            '  ', ' ').replace('…', '...')
        return data


load()
