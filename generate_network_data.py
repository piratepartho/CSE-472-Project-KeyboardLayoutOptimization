
import os
import re
import copy
import json
import tensorflow as tf
import numpy as np
import time
from classes.keyboard_structure import KeyboardStructure
from classes.characters_placement import CharactersPlacement

start_time = time.time()

random_seed=107
np.random.seed(random_seed)
tf.random.set_seed(random_seed)

punct = False
# random keyboard generated, make it small to run faster
number_of_characters_placements = 10

def buildCarpalxInput(keyboard):
    carpalx_file_name = "./etc/gen_net_keyboard.conf"
    with open(carpalx_file_name, 'w') as carpalx_file:
        carpalx_file.write(
            "<keyboard>\n<row 1>\nkeys    = `~ 1! 2@ 3\\# 4$ 5% 6^ 7& 8* 9( 0) -_ =+\nfingers =  0  1  1   2  3  3  3  6 7   7  8  9  9\n</row>\n<row 2>\nkeys    =")

        letters = 0
        for button, character in zip(keyboard_structure.buttons, keyboard):
            if character in my_letters:
                letters += 1
                carpalx_file.write(" " + character)

                if letters == 9:
                    carpalx_file.write(" ;: [{ ]} \\|\nfingers = 0 1 2 3 3 6 6 7 8 9  9  9  9\n</row>\n<row 3>\nkeys    =")

                if letters == 19:
                    carpalx_file.write(" '\"\nfingers = 0 1 2 3 3 6 6 7 8  9  9\n</row>\n<row 4>\nkeys    =")

                if letters == 26:
                    carpalx_file.write(" ,< .> /?\nfingers = 0 1 2 3 3 6 6  7  8  9\n</row>\n</keyboard>")
                    break

        carpalx_file.close()

def buildCarpalxInput_punct(keyboard):
    punct_map = {"-":"-_", "+":"=+", "{":"[{", "}":"]}", ";":";:", "'":"'\"", ",":",<", ".":".>", "?":"/?"}

    carpalx_file_name = "./etc/gen_net_keyboard_punct.conf"
    with open(carpalx_file_name, 'w') as carpalx_file:
        carpalx_file.write("<keyboard>\n<row 1>\nkeys    = `~ 1! 2@ 3\\# 4$ 5% 6^ 7& 8* 9( 0)")

        letters = 0
        for button, character in zip(keyboard_structure.buttons, keyboard):
            if character in my_letters:
                letters += 1

                if character in punct_map.keys():
                    carpalx_file.write(" " + punct_map[character])
                elif character>='a' and character<='z':
                    carpalx_file.write(" " + character)
                else:
                    print("wrong character: ", character)
                    exit(1)

                if letters == 2:
                    carpalx_file.write("\nfingers =  0  1  1   2  3  3  3  6 7   7  8  9  9\n</row>\n<row 2>\nkeys    =")

                if letters == 14:
                    carpalx_file.write(" \\|\nfingers = 0 1 2 3 3 6 6 7 8 9  9  9  9\n</row>\n<row 3>\nkeys    =")

                if letters == 25:
                    carpalx_file.write(" \nfingers = 0 1 2 3 3 6 6 7 8  9  9\n</row>\n<row 4>\nkeys    =")

                if letters == 35:
                    carpalx_file.write(" \nfingers = 0 1 2 3 3 6 6  7  8  9\n</row>\n</keyboard>")
                    break

        carpalx_file.close()


#open genetic_config
if(punct):
    path_str = "and_punctuations"
else:
    path_str = "only"

genetic_config_path = "./genetic_config_bangla.json"
with open(genetic_config_path, 'r') as file:
    genetic_config = json.load(file)
# characters placed on buttons. None if we want to search place for it
# CharactersPlacement assigns a character to each button. #! Probably Randomly
initial_characters_placement = CharactersPlacement(characters_set=genetic_config['characters_set']) 
keyboard_structure = KeyboardStructure(
    name=genetic_config['keyboard_structure']['name'],
    width=genetic_config['keyboard_structure']['width'],
    height=genetic_config['keyboard_structure']['height'],
    buttons=genetic_config['keyboard_structure']['buttons'],
    hands=genetic_config['hands']
)

#my buttons ids
my_letters = [] 
# my_buttons have all buttons info, their coord
my_buttons = [keyboard_structure.buttons[i].id for i in range(len(keyboard_structure.buttons))]
for c in initial_characters_placement.characters_set:
    if(c.button_id is not None):
        my_buttons.remove(c.button_id) # my_buttons have only buttons that need to be searched
    else:
        my_letters.append(c.character) # if c has null button id, then append to my_letters
number_of_characters = len(my_letters)


print("generating labeled keyboards...")
characters_placements = list()
labels = np.zeros([number_of_characters_placements], dtype=float)
for i in range(number_of_characters_placements):
    # making number_of_characters_placements(10000) keyboards randomly
    characters_placements.append(copy.deepcopy(initial_characters_placement))
    characters_placements[-1].randomize()

    # carpalx file creation
    if(punct):
        buildCarpalxInput_punct(characters_placements[-1])
    else:
        buildCarpalxInput(characters_placements[-1])
    # carpalx_keren perl file
    # conf files tell which finger press which key, it also has the corpus integrated
    # perl file return the effort of the keyboard configuartion effort value
    #! I should be using my keren.conf file. this code is using tutorial-00.conf file. something wrong?
    my_cmd = "perl carpalx_bangla -conf test.conf -keyboard_input gen_net_keyboard.conf"
    my_cmd_output = os.popen(my_cmd)
    for line in my_cmd_output:
        labels[i] = float(line.rstrip())

#one-hot from bzq
# for each keyboard, for each character, encode its position in one hot
features = np.zeros([number_of_characters_placements,number_of_characters,number_of_characters], dtype=int)
for cp in range(len(characters_placements)):
    for l in range(len(my_letters)):
        for button, character in zip(keyboard_structure.buttons, characters_placements[cp]):
            if character == my_letters[l]:
                #if (button.id==22):
                #    print(cp)
                #    for button, character in zip(keyboard_structure.buttons, characters_placements[cp]):
                #        print(button.id, character)
                #    exit()
                position = my_buttons.index(button.id)
                features[cp][l][position] = 1
                break


#save generated data
path_str = ""
if(punct):
    path_str = "_punct"

# this data file have indexes one hot encoded for each random keyboard and their effort value as target
data_file_path = "./data" + path_str + ".txt"
with open(data_file_path, 'w') as data_file:
    for f in range(len(features)):
        for i in range(len(my_letters)):
            for j in range(len(my_letters)):
                data_file.write(str(features[f][i][j]) + " ")
        data_file.write(str(labels[f]) + "\n")

data_file.close()

print("time: ", time.time() - start_time)


