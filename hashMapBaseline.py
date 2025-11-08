from collections import defaultdict
import re, pandas as pd, time


def build_index(csv_path):
    """
    Build a HashMap index: word -> airline -> count
    Returns the index and total build time.
    """
    df = pd.read_csv(csv_path)
    word_map = defaultdict(lambda: defaultdict(int))

    start = time.time()
    for _, row in df.iterrows():
        airline = str(row["airline_name"])
        content = str(row["content"]).lower()
        tokens = re.findall(r"[a-z]+", content)
        for token in tokens:
            word_map[token][airline] += 1
    end = time.time()

    print(f"✅ Indexed in {end - start:.2f} sec")
    return word_map


def lookup_exact_word(word_map, word):
    """
    Lookup airlines mentioning the exact word.
    Returns a dict of airline -> count and lookup time.
    """
    start = time.time()
    result = dict(word_map.get(word, {}))
    end = time.time()

    print(f"\n🔍 Airlines mentioning '{word}':")
    print(result)
    print(f"Exact word lookup took {end - start:.6f} sec")
    return result


def lookup_prefix(word_map, prefix):
    """
    Lookup all words starting with a prefix.
    Aggregate counts and rank airlines by total frequency.
    Returns sorted list of (airline, total_count).
    """
    start = time.time()
    agg_counts = defaultdict(int)

    for w, airlines in word_map.items():
        if w.startswith(prefix):
            for airline, cnt in airlines.items():
                agg_counts[airline] += cnt

    ranked = sorted(agg_counts.items(), key=lambda x: x[1], reverse=True)
    end = time.time()

    print(f"\n🔡 Airlines ranked (hash map) for prefix '{prefix}':")
    for airline, total in ranked[:20]:
        print(f"{airline:25s} {total}")
    print(f"Prefix lookup took {end - start:.6f} sec")

    return ranked


# ------------------- Example Usage -------------------
if __name__ == "__main__":
    # Step 1: Build index
    word_map = build_index("datasets/airline.csv")

    # Step 2: Exact word lookup
    lookup_exact_word(word_map, "delay")

    # Step 3: Prefix lookup
    lookup_prefix(word_map, "del")
