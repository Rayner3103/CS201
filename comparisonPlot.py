import re, time, pandas as pd, matplotlib.pyplot as plt
from collections import defaultdict
from Trie import Trie   # import your Trie class here (or paste above)
from data_structures.Array_BKTree import Array_BKTree
from data_structures.Linked_BKTree import Linked_BKTree


# ---------------- HashMap Functions ----------------
def build_hashmap(df):
    word_map = defaultdict(lambda: defaultdict(int))
    start = time.perf_counter()
    for _, row in df.iterrows():
        airline = str(row["airline_name"])
        content = str(row["content"]).lower()
        tokens = re.findall(r"[a-z]+", content)
        for token in tokens:
            word_map[token][airline] += 1
    return word_map, time.perf_counter() - start


def hashmap_exact(word_map, word):
    start = time.perf_counter()
    _ = dict(word_map.get(word, {}))
    return time.perf_counter() - start


def hashmap_prefix(word_map, prefix):
    start = time.perf_counter()
    agg_counts = defaultdict(int)
    for w, airlines in word_map.items():
        if w.startswith(prefix):
            for a, c in airlines.items():
                agg_counts[a] += c
    return time.perf_counter() - start


# ---------------- Trie Functions ----------------
def build_trie(df):
    trie = Trie()
    start = time.perf_counter()
    for _, row in df.iterrows():
        airline = str(row["airline_name"])
        content = str(row["content"]).lower()
        tokens = re.findall(r"[a-z]+", content)
        for token in tokens:
            trie.insert(token, airline)
    return trie, time.perf_counter() - start


def trie_exact(trie, word):
    start = time.perf_counter()
    _ = trie.get_airlines_for_word(word)
    return time.perf_counter() - start


def trie_prefix(trie, prefix):
    start = time.perf_counter()
    _ = trie.get_airline_ranking_for_prefix(prefix)
    return time.perf_counter() - start


# ---------------- Linked BK-Tree Functions ----------------
def build_linked_bk(df):
    linked_bk_tree = Linked_BKTree()
    start = time.perf_counter()
    for _, row in df.iterrows():
        airline = str(row["airline_name"])
        content = str(row["content"]).lower()
        tokens = re.findall(r"[a-z]+", content)
        for token in tokens:
            linked_bk_tree.add(token, airline)
    return linked_bk_tree, time.perf_counter() - start


def linked_bk_search(linked_bk_tree, word, tol):
    start = time.perf_counter()
    _ = linked_bk_tree.get_entity_rank_by_similar_words(word, tol)
    return time.perf_counter() - start


# ---------------- Array BK-Tree Functions ----------------
def build_array_bk(df):
    array_bk_tree = Array_BKTree()
    start = time.perf_counter()
    for _, row in df.iterrows():
        airline = str(row["airline_name"])
        content = str(row["content"]).lower()
        tokens = re.findall(r"[a-z]+", content)
        for token in tokens:
            array_bk_tree.add(token, airline)
    return array_bk_tree, time.perf_counter() - start


def array_bk_search(array_bk_tree, word, tol):
    start = time.perf_counter()
    _ = array_bk_tree.get_entity_rank_by_similar_words(word, tol)
    return time.perf_counter() - start


# ---------------- Experiment Runner ----------------
def run_experiment(csv_path, word="delay", prefix="del", sample_sizes=[1000, 5000, 10000, 20000]):
    df = pd.read_csv(csv_path)
    hash_insert, trie_insert = [], []
    hash_exact, trie_exact_t = [], []
    hash_prefix, trie_prefix_t = [], []
    linked_bk_insert, array_bk_insert = [], []
    linked_bk_search_t, array_bk_search_t = [], []
    linked_bk_exact_t, array_bk_exact_t = [], []

    for n in sample_sizes:
        subset = df.sample(n, random_state=42)

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

        # Build Linked BK-Tree
        linked_bk_tree, linked_build_t = build_linked_bk(subset)
        linked_bk_insert.append(linked_build_t)
        linked_bk_exact_t.append(linked_bk_search(linked_bk_tree, word, 0))
        linked_bk_search_t.append(linked_bk_search(linked_bk_tree, word, 2))

        # Build Array BK-Tree
        array_bk_tree, array_build_t = build_array_bk(subset)
        array_bk_insert.append(array_build_t)
        array_bk_exact_t.append(array_bk_search(array_bk_tree, word, 0))
        array_bk_search_t.append(array_bk_search(array_bk_tree, word, 2))

        print(f"✅ Completed {n} reviews")

    return sample_sizes, (
        hash_insert, trie_insert, hash_exact, trie_exact_t, hash_prefix, trie_prefix_t,
        linked_bk_insert, array_bk_insert, linked_bk_exact_t, array_bk_exact_t, linked_bk_search_t,
        array_bk_search_t
    )


# ---------------- Plotting ----------------
def plot_results(sample_sizes, hash_insert, trie_insert, hash_exact, trie_exact_t, hash_prefix, trie_prefix_t, linked_bk_insert, array_bk_insert, linked_bk_exact_t, array_bk_exact_t, linked_bk_search_t, array_bk_search_t):
    plt.figure(figsize=(14, 10))

    # Build time
    plt.subplot(2, 2, 1)
    plt.plot(sample_sizes, hash_insert, 'o-', label="HashMap")
    plt.plot(sample_sizes, trie_insert, 'o-', label="Trie")
    plt.plot(sample_sizes, linked_bk_insert, 'o-', label="Linked BK Tree")
    plt.plot(sample_sizes, array_bk_insert, 'o-', label="Array BK Tree")
    plt.title("Insertion Time vs Input Size")
    plt.xlabel("Number of Reviews")
    plt.ylabel("Time (s)")
    plt.legend()

    # Exact lookup
    plt.subplot(2, 2, 2)
    plt.plot(sample_sizes, hash_exact, 'o-', label="HashMap")
    plt.plot(sample_sizes, trie_exact_t, 'o-', label="Trie")
    plt.plot(sample_sizes, linked_bk_exact_t, 'o-', label="Linked BK Tree")
    plt.plot(sample_sizes, array_bk_exact_t, 'o-', label="Array BK Tree")
    plt.title("Exact Lookup Time vs Input Size")
    plt.xlabel("Number of Reviews")
    plt.ylabel("Time (s)")
    plt.legend()

    # Prefix lookup
    plt.subplot(2, 2, 3)
    plt.plot(sample_sizes, hash_prefix, 'o-', label="HashMap")
    plt.plot(sample_sizes, trie_prefix_t, 'o-', label="Trie")
    plt.title("Prefix Lookup Time vs Input Size")
    plt.xlabel("Number of Reviews")
    plt.ylabel("Time (s)")
    plt.legend()

    # Fuzzy lookup
    plt.subplot(2, 2, 4)
    plt.plot(sample_sizes, linked_bk_search_t, 'o-', label="Linked BK Tree")
    plt.plot(sample_sizes, array_bk_search_t, 'o-', label="Array BK Tree")
    plt.title("Fuzzy Lookup Time vs Input Size")
    plt.xlabel("Number of Reviews")
    plt.ylabel("Time (s)")
    plt.legend()

    plt.tight_layout()
    plt.show()


# ---------------- Main ----------------
if __name__ == "__main__":
    sizes, (h_i, t_i, h_e, t_e, h_p, t_p, l_bk_i, a_bk_i, l_bk_e, a_bk_e, l_bk_s, a_bk_s) = run_experiment(
        "datasets/airline.csv",
        word="delay",
        prefix="del",
        sample_sizes=[max(1, int(i / 10 * 40000)) for i in range(1, 11)]
    )

    plot_results(sizes, h_i, t_i, h_e, t_e, h_p, t_p, l_bk_i, a_bk_i, l_bk_e, a_bk_e, l_bk_s, a_bk_s)
