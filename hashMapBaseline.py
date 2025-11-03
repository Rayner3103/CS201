from collections import defaultdict
import re, pandas as pd, time

df = pd.read_csv("datasets/airline.csv")

# HashMap: word -> airline -> count
word_map = defaultdict(lambda: defaultdict(int))

start = time.time()
for _, row in df.iterrows():
    airline = str(row["airline_name"])
    content = str(row["content"]).lower()
    tokens = re.findall(r"[a-z]+", content)
    for token in tokens:
        word_map[token][airline] += 1
end = time.time()

print(f"Indexed in {end - start:.2f} sec")

# Lookup for exact word
start = time.time()
word = "delay"
print(f"\nAirlines mentioning '{word}':")
print(dict(word_map[word]))
end = time.time()
print(f"Exact word lookup took {end - start:.6f} sec")

# Aggregate prefix
# Prefix lookup
prefix = "del"
start = time.time()
agg_counts = defaultdict(int)
for w, airlines in word_map.items():
    if w.startswith(prefix):
        for airline, cnt in airlines.items():
            agg_counts[airline] += cnt
end = time.time()
print(f"Prefix lookup took {end - start:.6f} sec")            
ranked = sorted(agg_counts.items(), key=lambda x: x[1], reverse=True)
print(f"\nAirlines ranked(hash map) for prefix '{prefix}':")
for airline, total in ranked[:20]:
    print(f"{airline:25s} {total}")
