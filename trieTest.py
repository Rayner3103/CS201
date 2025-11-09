import pandas as pd
import re, time
from collections import defaultdict
from data_structures.Trie import Trie  # your Trie class file

# -----------------------------
# 1️ Load dataset
# -----------------------------
df = pd.read_csv("datasets/airline.csv")

# -----------------------------
# 2️ Build phase timing
# -----------------------------
trie = Trie()
start = time.time()

for _, row in df.iterrows():
    airline = str(row["airline_name"])
    content = str(row["content"]).lower()
    tokens = re.findall(r"[a-z]+", content)

    # Use set(tokens) to avoid double-counting same word in a single review
    for token in set(tokens):
        trie.insert(token, airline)

end = time.time()
build_time = end - start
print(f"✅ Trie built in {build_time:.2f} seconds for {len(df)} reviews.")

# -----------------------------
# 3 Query phase timing
# -----------------------------
prefixes = ["delay", "serv", "clean", "food"]
print("\n🔍 Query performance:")

for prefix in prefixes:
    start = time.time()
    ranking = trie.get_airline_ranking_for_prefix(prefix)
    end = time.time()
    query_time = end - start

    print(f"\nPrefix '{prefix}' → Top 10 airlines (time: {query_time:.6f} sec)")
    print("-" * 50)

    for i, (airline, total) in enumerate(ranking[:10], start=1):
        print(f"{i:2d}. {airline:25s} {total}")

    print("-" * 50)
