import pandas as pd
import re

OUTPUT_FILE = 'triads_count.txt'
INPUT_FILE = 'wiki.csv'

def read_and_process_csv(file_path):
    df = pd.read_csv(file_path)

    text_columns = df.select_dtypes(include=['object']).columns

    # Regular expression to match non-Bengali characters
    non_bengali_regex = '[^\u0980-\u09FF]'

    # Initialize an empty dictionary to store triad counts
    triad_counts = {}

    # Process each text column
    for column in text_columns:
        # Remove non-Bengali characters
        df[column] = df[column].apply(lambda x: re.sub(non_bengali_regex, '', str(x)))
        # replace o kar with e kar + aa kar
        df[column] = df[column].apply(lambda x: re.sub('\u09CB', '\u09C7\u09BE', str(x)))
        # replace aa with aw + aa kar
        df[column] = df[column].apply(lambda x: re.sub('\u0986', '\u0985\u09BE', str(x)))
        # replace ro fola to euro
        df[column] = df[column].apply(lambda x: re.sub('\u09CD\u09B0', '\u20AC', str(x)))
        # replace jo fola to yen9CD + 9AF -> \u00A5
        df[column] = df[column].apply(lambda x: re.sub('\u09CD\u09AF', '\u00A5', str(x)))
        # replace ref to rupee \u09B0\u09CD-> \u20B9
        df[column] = df[column].apply(lambda x: re.sub('\u09B0\u09CD', '\u20B9', str(x)))
        # replace roshoi with hoshonto and roshoi kar \u0987-> \u09CD\u09BF
        df[column] = df[column].apply(lambda x: re.sub('\u0987', '\u09CD\u09BF', str(x)))
        #replacce dirgho i with hoshonto and dirgho i kar \u0988-> \u09CD\u09C0
        df[column] = df[column].apply(lambda x: re.sub('\u0988', '\u09CD\u09C0', str(x)))
        #replace rosho u with hoshonto and rosho u kar \u0989-> \u09CD\u09C1
        df[column] = df[column].apply(lambda x: re.sub('\u0989', '\u09CD\u09C1', str(x)))
        #replace dirgho u with hoshonto and dirgho u kar \u098A-> \u09CD\u09C2
        df[column] = df[column].apply(lambda x: re.sub('\u098A', '\u09CD\u09C2', str(x)))
        #replace rosho ri with hoshonto and rosho ri kar \u098B-> \u09CD\u09C3
        df[column] = df[column].apply(lambda x: re.sub('\u098B', '\u09CD\u09C3', str(x)))
        #replace ae with hoshonto and ae kar \u098F-> \u09CD\u09C7
        df[column] = df[column].apply(lambda x: re.sub('\u098F', '\u09CD\u09C7', str(x)))
        #replace oi with hoshonto and oi kar \u0990-> \u09CD\u09C8
        df[column] = df[column].apply(lambda x: re.sub('\u0990', '\u09CD\u09C8', str(x)))
        #replace ou with hoshonto and ou kar \u0994-> \u09CD\u09CC
        df[column] = df[column].apply(lambda x: re.sub('\u0994', '\u09CD\u09CC', str(x)))

        for row in df[column]:
            for i in range(0, len(row) - 2):  # Subtract 2 to avoid index out of range
                triad = row[i:i+3]  # Get the triad starting at position i
                if len(triad) == 3:  # Ensure the triad has exactly 3 characters
                    if triad in triad_counts:
                        triad_counts[triad] += 1
                    else:
                        triad_counts[triad] = 1

    sorted_triad_counts = sorted(triad_counts.items(), key=lambda item: item[1], reverse=True)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for triad, count in sorted_triad_counts:
            f.write(f"{triad} {count}\n")

    for triad, count in triad_counts.items():
        print(f"Triad: {triad}, Count: {count}")

read_and_process_csv(INPUT_FILE)
