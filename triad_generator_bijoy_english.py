import pandas as pd
import re

OUTPUT_FILE = 'triads_count.txt'
INPUT_FILE = 'wiki.csv'

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

    non_bengali_regex = '[^\u0980-\u09FF]'
    df[column] = df[column].apply(lambda x: re.sub(non_bengali_regex, '', str(x)))
    cnt = 0

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
                try:
                    english_text +='c'+ bengali_to_english.get(buffer) + 'f'
                except:
                    cnt += 1
                finally:
                    buffer = ''
            elif char == 'ৌ' :
                try:
                    english_text +='c'+ bengali_to_english.get(buffer) + 'X'
                except:
                    cnt += 1
                finally:
                    buffer = ''
            else:
                try:
                    english_text += bengali_to_english.get(buffer)
                except:
                    cnt += 1
                buffer = char

    if buffer:
        english_text += bengali_to_english.get(buffer)

    return english_text

df = pd.read_csv(INPUT_FILE)
text_columns = df.select_dtypes(include=['object']).columns

triad_counts = {}

non_bengali_regex = '[^\u0980-\u09FF]'
bengali_text = ''
for column in text_columns:
    if column == 'text':
        df[column] = df[column].apply(lambda x: re.sub(non_bengali_regex, '', str(x)))
        for row in df[column]:
            bengali_text += row

english_text = convert_bengali_to_english(bengali_text)

for i in range(len(english_text)-2):
    triad = english_text[i : i+3]
    if triad in triad_counts:
        triad_counts[triad] += 1 
    else:
        triad_counts[triad] = 1

sorted_triad_counts = sorted(triad_counts.items(), key=lambda item: item[1], reverse=True)

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    for triad, count in sorted_triad_counts:
        f.write(f"{triad} {count}\n")

    for triad, count in triad_counts.items():
        print(f"Triad: {triad} ||| Count: {count}")