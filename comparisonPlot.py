import re, time, pandas as pd, matplotlib.pyplot as plt
from collections import defaultdict
from Trie import Trie   # import your Trie class here (or paste above)


# ---------------- HashMap Functions ----------------
def build_hashmap(df):
    word_map = defaultdict(lambda: defaultdict(int))
    start = time.time()
    for _, row in df.iterrows():
        airline = str(row["airline_name"])
        content = str(row["content"]).lower()
        tokens = re.findall(r"[a-z]+", content)
        for token in tokens:
            word_map[token][airline] += 1
    return word_map, time.time() - start


def hashmap_exact(word_map, word):
    start = time.time()
    _ = dict(word_map.get(word, {}))
    return time.time() - start


def hashmap_prefix(word_map, prefix):
    start = time.time()
    agg_counts = defaultdict(int)
    for w, airlines in word_map.items():
        if w.startswith(prefix):
            for a, c in airlines.items():
                agg_counts[a] += c
    return time.time() - start


# ---------------- Trie Functions ----------------
def build_trie(df):
    trie = Trie()
    start = time.time()
    for _, row in df.iterrows():
        airline = str(row["airline_name"])
        content = str(row["content"]).lower()
        tokens = re.findall(r"[a-z]+", content)
        for token in tokens:
            trie.insert(token, airline)
    return trie, time.time() - start


def trie_exact(trie, word):
    start = time.time()
    _ = trie.get_airlines_for_word(word)
    return time.time() - start


def trie_prefix(trie, prefix):
    start = time.time()
    _ = trie.get_airline_ranking_for_prefix(prefix)
    return time.time() - start


# ---------------- Experiment Runner ----------------
def run_experiment(csv_path, word="delay", prefix="del", sample_sizes=[1000, 5000, 10000, 20000]):
    df = pd.read_csv(csv_path)
    hash_insert, trie_insert = [], []
    hash_exact, trie_exact_t = [], []
    hash_prefix, trie_prefix_t = [], []

    for n in sample_sizes:
        subset = df.head(n)

        # Build HashMap
        word_map, t_build_h = build_hashmap(subset)
        hash_insert.append(t_build_h)
        hash_exact.append(hashmap_exact(word_map, word))
        hash_prefix.append(hashmap_prefix(word_map, prefix))

        # Build Trie
        trie, t_build_t = build_trie(subset)
        trie_insert.append(t_build_t)
        trie_exact_t.append(trie_exact(trie, word))
        trie_prefix_t.append(trie_prefix(trie, prefix))

        print(f"✅ Completed {n} reviews")

    return sample_sizes, (hash_insert, trie_insert, hash_exact, trie_exact_t, hash_prefix, trie_prefix_t)


# ---------------- Plotting ----------------
def plot_results(sample_sizes, hash_insert, trie_insert, hash_exact, trie_exact_t, hash_prefix, trie_prefix_t):
    plt.figure(figsize=(14, 10))

    # Build time
    plt.subplot(3, 1, 1)
    plt.plot(sample_sizes, hash_insert, 'o-', label="HashMap")
    plt.plot(sample_sizes, trie_insert, 'o-', label="Trie")
    plt.title("Insertion Time vs Input Size")
    plt.xlabel("Number of Reviews")
    plt.ylabel("Time (s)")
    plt.legend()

    # Exact lookup
    plt.subplot(3, 1, 2)
    plt.plot(sample_sizes, hash_exact, 'o-', label="HashMap")
    plt.plot(sample_sizes, trie_exact_t, 'o-', label="Trie")
    plt.title("Exact Lookup Time vs Input Size")
    plt.xlabel("Number of Reviews")
    plt.ylabel("Time (s)")
    plt.legend()

    # Prefix lookup
    plt.subplot(3, 1, 3)
    plt.plot(sample_sizes, hash_prefix, 'o-', label="HashMap")
    plt.plot(sample_sizes, trie_prefix_t, 'o-', label="Trie")
    plt.title("Prefix Lookup Time vs Input Size")
    plt.xlabel("Number of Reviews")
    plt.ylabel("Time (s)")
    plt.legend()

    plt.tight_layout()
    plt.show()


# ---------------- Main ----------------
if __name__ == "__main__":
    sizes, (h_i, t_i, h_e, t_e, h_p, t_p) = run_experiment(
        "datasets/airline.csv",
        word="delay",
        prefix="del",
        sample_sizes=[1000, 5000, 10000, 20000, 40000]
    )

    plot_results(sizes, h_i, t_i, h_e, t_e, h_p, t_p)
