import csv
import re
import os

def default_edit_distance(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] != b[j - 1]:
                dp[i][j] = min(
                    dp[i - 1][j] + 1,  # deletion
                    dp[i][j - 1] + 1,  # insertion
                    dp[i - 1][j - 1] + 1  # replacement
                )
            else:
                dp[i][j] = dp[i - 1][j - 1]
    return dp[m][n]

def baseline_linear_search(dictionary, target, edit_distance=default_edit_distance, TOL=2):
    result = []
    for word in dictionary:
        if edit_distance(word, target) <= TOL:
            result.append(word)

    return result

def extract_unique_words_from_csv(file_path, column_name):
    """Read the csv from file_path, get all unique words from the specified column_name. 
    Only retrieves alphabets & returns lower case letters"""
    unique_words = set()
    
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            content = row.get(column_name, "")
            # Extract words using regex and convert to lowercase
            words = re.findall(r'\b[a-z]+\b', content.lower())
            unique_words.update(words)
    
    return list(unique_words)
    
def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created folder: {path}")