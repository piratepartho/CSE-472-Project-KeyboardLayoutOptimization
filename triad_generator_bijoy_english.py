import pandas as pd
import re

OUTPUT_FILE = 'triads_count.txt'

bengali_to_english = {
    '১': '1',
    '২': '2',
    '৩': '3',
    '৪': '4',
    '৫': '5',
    '৬': '6',
    '৭': '7',
    'ঁ' : '&',
    '৮': '8',
    '৯': '9',
    '০': '0',
    'ঙ': 'q',
    'ং': 'Q',
    'য': 'w',
    'য়': 'W',
    'ড': 'e',
    'ঢ': 'E',
    'প': 'r',
    'ফ': 'R',
    'ট': 't',
    'ঠ': 'T',
    'চ': 'y',
    'ছ': 'Y',
    'জ': 'u',
    'ঝ': 'U',
    'হ': 'i',
    'ঞ': 'I',
    'গ': 'o',
    'ঘ': 'O',
    'ড়': 'p',
    'ঢ়': 'P',
    'ৎ': '\\',
    'ঃ': '|',
    'ৃ': 'a',
   'র্' : 'A',
    'ু': 's',
    'ূ': 'S',
    'ি': 'd',
    'ী': 'D',
    'া': 'f',
    'অ': 'F',
    'আ': 'Ff',
    '্': 'g',
    '।': 'G',
    'ব': 'h',
    'ভ': 'H',
    'ক': 'j',
    'খ': 'J',
    'ত': 'k',
    'থ': 'K',
    'দ': 'l',
    'ধ': 'L',
    '্র': 'z',
    '্য': 'Z',
    'ও': 'x',
    'ৗ': 'X',
    'ে': 'c',
    'ৈ': 'C',
    'এ': 'gc',
    'ঐ': 'gC',
    'ঔ': 'gX',
    'ই' : 'gd',
    'ঈ' : 'gD',
    'উ' : 'gs',
    'ঊ' : 'gS',
    'ঋ': 'ga',
    'ো': 'cf',
    'ৌ': 'cX',
    'র' : 'v',
    'ল' : 'V',
    'ন' : 'b',
    'ণ' : 'B',
    'স' : 'n',
    'ষ' : 'N',
    'ম' : 'm',
    'শ' : 'M',
    '‘' : '`',
    '“' : '~',
    '”' : '"',
    '’' : '\'',
    ' ' : ' ',
}

def convert_bengali_to_english(bengali_text):
    english_text = ''
    buffer = ''
    for char in bengali_text:
        if char is None:
            print(f'char in none')
        if buffer is None:
            print(f'buffer is none, char={char}')
        if buffer == '':
            buffer = char
        else:
            if buffer+char in bengali_to_english:
                english_text += bengali_to_english[buffer+char] 
                buffer = ''
            elif char == 'ো' :
                english_text +='c'+ bengali_to_english.get(buffer) + 'f'
                buffer = ''
            elif char == 'ৌ' :
                english_text +='c'+ bengali_to_english.get(buffer) + 'X'
                buffer = ''
            else:
                english_text += bengali_to_english.get(buffer)
                buffer = char

    if buffer:
        english_text += bengali_to_english.get(buffer, buffer)

    return english_text