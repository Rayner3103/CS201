import re, time, pandas as pd, matplotlib.pyplot as plt
from collections import defaultdict
from data_structures.Trie import Trie   # import your Trie class here (or paste above)
from data_structures.hashMapBaseline import *
from pympler import asizeof


# ---------------- HashMap Functions ----------------
def build_hashmap(df):
    word_map = defaultdict(lambda: defaultdict(int))
    for _, row in df.iterrows():
        airline = str(row["airline_name"])
        content = str(row["content"]).lower()
        tokens = re.findall(r"[a-z]+", content)
        for token in tokens:
            word_map[token][airline] += 1
    return word_map, asizeof.asizeof(word_map)


# ---------------- Trie Functions ----------------
def build_trie(df):
    trie = Trie()
    for _, row in df.iterrows():
        airline = str(row["airline_name"])
        content = str(row["content"]).lower()
        tokens = re.findall(r"[a-z]+", content)
        for token in tokens:
            trie.insert(token, airline)
    return trie, asizeof.asizeof(trie)

def prefix_search_experiment(csv_path, prefixes=["del", "serv", "clean"], sample_sizes=[1000, 5000, 10000, 20000]):
    df = pd.read_csv(csv_path)
    hash_times = []
    trie_times = []
    word_counts = []

    for n in sample_sizes:
        subset = df.sample(min(n, len(df)), random_state=42)
        words = []
        for _, row in subset.iterrows():
            content = str(row["content"]).lower()
            words += re.findall(r"[a-z]+", content)
        word_counts.append(len(set(words)))

        # Build HashMap
        word_map, _ = build_hashmap(subset)

        # Build Trie
        trie = Trie()
        for _, row in subset.iterrows():
            airline = str(row["airline_name"])
            content = str(row["content"]).lower()
            tokens = re.findall(r"[a-z]+", content)
            for token in tokens:
                trie.insert(token, airline)

        # Measure HashMap prefix search
        start = time.perf_counter()
        for p in prefixes:
            lookup_prefix(word_map, p)
        end = time.perf_counter()
        hash_times.append(end - start)

        # Measure Trie prefix search
        start = time.perf_counter()
        for p in prefixes:
            trie.get_words_and_airlines_starting_with(p)
        end = time.perf_counter()
        trie_times.append(end - start)

        print(f"n={n}: hash={hash_times[-1]:.4f}s, trie={trie_times[-1]:.4f}s")

    # Plot results
    plt.figure(figsize=(8,5))
    plt.plot(word_counts, hash_times, marker='o', label="HashMap prefix search")
    plt.plot(word_counts, trie_times, marker='o', label="Trie prefix search")
    plt.xlabel("Number of unique words")
    plt.ylabel("Total prefix search time (s)")
    plt.title("Prefix search time: HashMap vs Trie")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ---------------- Main ----------------
if __name__ == "__main__":
    csv_path = "datasets/airline.csv"
    word_counts, hash_time, trie_time = prefix_search_experiment(csv_path, prefixes=["del", "serv", "clean"], sample_sizes=[1000, 5000, 10000, 20000])
