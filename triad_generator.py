import pandas as pd
import re

OUTPUT_FILE = 'triads_count.txt'
INPUT_FILE = 'wiki-short.csv'

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

        for row in df[column]:
            # if '\u09CB' in row:
            #     print('o kar found')
            # if '\u0986' in row:
            #     print('aa found')
            # if '\u09CD\u09B0' in row:
            #     print('found ro fola')
            # if '\u09CD\u09AF' in row:
            #     print('found jo fola')
            # if '\u09B0\u09CD' in row:
            #     print('ref pair')
            # if '\u09CB' in row:
            #     print('o kar found')
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
