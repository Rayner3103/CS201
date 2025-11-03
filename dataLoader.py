import csv
import re

def extract_unique_words_from_csv(file_path, column_name):
    unique_words = set()
    
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            content = row.get(column_name, "")
            # Extract words using regex and convert to lowercase
            words = re.findall(r'\b\w+\b', content.lower())
            unique_words.update(words)
    
    return list(unique_words)

# Filepath to the CSV file
# csv_file_path = "./airline.csv"

# # Column name to extract words from
# column_name = "content"

# # Extract unique words
# unique_words = extract_unique_words_from_csv(csv_file_path, column_name)

# # Print the unique words
# print(f"Total unique words: {len(unique_words)}")
# print(unique_words)