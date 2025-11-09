import re, time, pandas as pd, matplotlib.pyplot as plt
from collections import defaultdict
from data_structures.Trie import Trie   # import your Trie class here (or paste above)
from data_structures.Array_BKTree import Array_BKTree
from data_structures.Linked_BKTree import Linked_BKTree
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


# ---------------- Linked BK-Tree Functions ----------------
def build_linked_bk(df):
    linked_bk_tree = Linked_BKTree()
    for _, row in df.iterrows():
        airline = str(row["airline_name"])
        content = str(row["content"]).lower()
        tokens = re.findall(r"[a-z]+", content)
        for token in tokens:
            linked_bk_tree.add(token, airline)
    return linked_bk_tree, asizeof.asizeof(linked_bk_tree)


# ---------------- Array BK-Tree Functions ----------------
def build_array_bk(df):
    array_bk_tree = Array_BKTree()
    for _, row in df.iterrows():
        airline = str(row["airline_name"])
        content = str(row["content"]).lower()
        tokens = re.findall(r"[a-z]+", content)
        for token in tokens:
            array_bk_tree.add(token, airline)
    return array_bk_tree, asizeof.asizeof(array_bk_tree)


# ---------------- Experiment Runner ----------------
def run_experiment(csv_path, sample_sizes=[1000, 5000, 10000, 20000]):
    df = pd.read_csv(csv_path)
    word_counts = []
    hash_size, trie_size, linked_bk_size, array_bk_size = [], [], [], []

    for n in sample_sizes:
        subset = df.sample(n, random_state=42)
        
        words = []
        for _, row in subset.iterrows():
            content = str(row["content"]).lower()
            words += re.findall(r"[a-z]+", content)
        word_counts.append(len(set(words)))

        # Build HashMap
        _, h_size = build_hashmap(subset)
        hash_size.append(h_size)

        # Build Trie
        _, t_size = build_trie(subset)
        trie_size.append(t_size)

        # Build Linked BK-Tree
        _, linked_size = build_linked_bk(subset)
        linked_bk_size.append(linked_size)

        # Build Array BK-Tree
        _, array_size = build_array_bk(subset)
        array_bk_size.append(array_size)

        print(f"✅ Completed {n} reviews")

    return word_counts, (hash_size, trie_size, linked_bk_size, array_bk_size)


# ---------------- Plotting ----------------
def plot_results(saved_fig_path, word_counts, hash_size, trie_size, linked_bk_size, array_bk_size):
    plt.figure(figsize=(14, 10))

    # Build time
    plt.plot(word_counts, hash_size, 'o-', label="HashMap")
    plt.plot(word_counts, trie_size, 'o-', label="Trie")
    plt.plot(word_counts, linked_bk_size, 'o-', label="Linked BK Tree")
    plt.plot(word_counts, array_bk_size, 'o-', label="Array BK Tree")
    plt.title("Space Taken vs Input Size")
    plt.xlabel("Number of unique words")
    plt.ylabel("Space Taken (Bytes)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(saved_fig_path)
    plt.show()


# ---------------- Main ----------------
if __name__ == "__main__":
    num_runs = 5  # Number of times to repeat the experiment
    sample_sizes = [max(1, int(i / 10 * 40000)) for i in range(1, 11)]
    csv_path = "datasets/airline.csv"
    word = "delay"
    prefix = "del"
    saved_fig_path = "./figs/space_comparison_plots.png"

    # Initialize accumulators for averaging
    avg_results = None

    for run in range(num_runs):
        print(f"Running experiment {run + 1}/{num_runs}...")
        word_counts, results = run_experiment(csv_path, sample_sizes=sample_sizes)

        # Initialize accumulators on the first run
        if avg_results is None:
            avg_results = [list(r) for r in results]
        else:
            # Accumulate results for averaging
            for i in range(len(results)):
                for j in range(len(results[i])):
                    avg_results[i][j] += results[i][j]

    # Average the results
    avg_results = [[value / num_runs for value in result] for result in avg_results]

    # Unpack averaged results
    (
        hash_size, trie_size, linked_bk_size, array_bk_size
    ) = avg_results

    # Plot the averaged results
    plot_results(saved_fig_path, word_counts, hash_size, trie_size, linked_bk_size, array_bk_size)