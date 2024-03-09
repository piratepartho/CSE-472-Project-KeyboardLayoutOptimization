
import os
import re
import copy
import json
import tensorflow as tf
import numpy as np
import time
from classes.keyboard_structure import KeyboardStructure
from classes.characters_placement import CharactersPlacement

from PIL import Image, ImageDraw, ImageFont

start_time = time.time()

random_seed=107
np.random.seed(random_seed)
tf.random.set_seed(random_seed)


genetic_config_path = "./genetic_config_bangla.json"
with open(genetic_config_path, 'r') as file:
    genetic_config = json.load(file)

# initial_characters_placement = CharactersPlacement(characters_set=genetic_config['characters_set']) 
# keyboard_structure = KeyboardStructure(
#     name=genetic_config['keyboard_structure']['name'],
#     width=genetic_config['keyboard_structure']['width'],
#     height=genetic_config['keyboard_structure']['height'],
#     buttons=genetic_config['keyboard_structure']['buttons'],
#     hands=genetic_config['hands']
# )

# keyboard_structure.visualize(characters_placement=initial_characters_placement, dirpath=os.path.dirname(genetic_config_path))

keyboard = '''
<keyboard>
<row 1>
keys    = `~ 1! 2@ 3\# 4$ 5% 6^ 7& 8* 9( 0) -_ =+
fingers =  0  1  1   2  3  3  3  6 7   7  8  9  9
</row>
<row 2>
keys    = q o h w t i s n a ;: [{ ]} \|
fingers = 0 1 2 3 3 6 6 7 8 9  9  9  9
</row>
<row 3>
keys    = z j d v k g f c b m '"
fingers = 0 1 2 3 3 6 6 7 8  9  9
</row>
<row 4>
keys    = p e l y x u r ,< .> /?
fingers = 0 1 2 3 3 6 6  7  8  9
</row>
</keyboard>
'''
import re

keys_pattern = r"keys\s*=\s*(.*?)\n"
matches = re.findall(keys_pattern, keyboard, re.DOTALL)
button_id = 0
character_set = []
for keys in matches:
    chars = re.findall(r"[^\s]+", keys)
    for char in chars:
        if char[0] == '\\':
            continue
        character_set.append({"character": char[0], "button_id": button_id})
        button_id += 1

char_placement = CharactersPlacement(characters_set=character_set)
for c in char_placement.characters_set:
    print(c.character, c.button_id)


keyboard_structure = KeyboardStructure(
    name=genetic_config['keyboard_structure']['name'],
    width=genetic_config['keyboard_structure']['width'],
    height=genetic_config['keyboard_structure']['height'],
    buttons=genetic_config['keyboard_structure']['buttons'],
    hands=genetic_config['hands']
)

keyboard_structure.visualize(characters_placement=char_placement, dirpath=os.path.dirname(genetic_config_path))