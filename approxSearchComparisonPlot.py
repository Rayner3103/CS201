from collections import defaultdict
from datetime import datetime
import time
import random
from pympler import asizeof
import matplotlib.pyplot as plt
import pandas as pd

from data_structures import Array_BKTree
from data_structures import Linked_BKTree
from Levenshtein import distance as levenshtein_distance

from data_structures import *
from utils import *

def hashmap_approx(word_map, word, tol):
    """
    Perform an approximate search through the keys of word_map within the given tolerance.
    """    
    # Filter keys based on the edit distance tolerance
    matching_keys = [
        key for key in word_map.keys()
        if levenshtein_distance(word, key) <= tol
    ]
    
    # Collect and rank airlines based on the matching keys
    airline_frequencies = defaultdict(int)
    for key in matching_keys:
        for airline, freq in word_map[key].items():
            airline_frequencies[airline] += freq
    
    # Sort airlines by frequency in descending order
    ranked_airlines = sorted(airline_frequencies.items(), key=lambda x: x[1], reverse=True)
   
    return ranked_airlines

def test_search_time_against_tolerance(df, lower, higher, search_word):
    """
    For the dataframe, plot the time performance for varying edit distance tolerance between lower (inclusive) to higher (exclusive)
    """

    linear_search_times = []
    array_search_times = []
    linked_search_times = []
    tols = [i for i in range(lower, higher)]
    # build trees from the first n words (building time is not included in retrieval timing)
    array_tree = Array_BKTree.Array_BKTree(MAXN, MAX_DIST)
    linked_tree = Linked_BKTree.Linked_BKTree()
    word_map = defaultdict(lambda: defaultdict(int))

    for _, row in df.iterrows():
        airline = str(row["airline_name"])
        content = str(row["content"]).lower()
        tokens = re.findall(r"[a-z]+", content)
        for token in tokens:
            array_tree.add(token, airline)
            linked_tree.add(token, airline)
            word_map[token][airline] += 1

    for tol in tols:
        # additional variable declaration to avoid difference due to new variable declaration
        start = 0
        end = 0

        # Linear
        start = time.perf_counter()
        hashmap_approx(word_map, search_word, tol)
        end = time.perf_counter()
        linear_search_times.append(end - start)

        # Array BK Tree
        start = time.perf_counter()
        array_tree.get_similar_words(search_word, tol)
        end = time.perf_counter()
        array_search_times.append(end - start)

        # Linked BK Tree
        start = time.perf_counter()
        linked_tree.get_similar_words(search_word, tol)
        end = time.perf_counter()
        linked_search_times.append(end - start)

        print(f"✅ Completed tolerance {tol}")

    return tols, (linear_search_times, array_search_times, linked_search_times)


def plot_result(tols, linear_search_times_tol, array_search_times_tol, linked_search_times_tol):

    # Subplot 4: Search time vs tolerance
    plt.plot(tols, linear_search_times_tol, 'o-', label='Linear Search')
    plt.plot(tols, array_search_times_tol, 'o-', label='Array BK Tree')
    plt.plot(tols, linked_search_times_tol, 'o-', label='Linked BK Tree')
    plt.xlabel('Tolerance (Edit Distance)')
    plt.ylabel('Time (s)')
    plt.title(f'Search Time vs Tolerance')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(f"{FIGURE_PATH}/approx_search_results_{datetime.now().strftime(DATE_FORMAT)}.png")
    plt.show()

# Array BK Tree configs   
MAXN = 1
MAX_DIST = 50
TOL = 2

# Configs for file paths and date output format
FIGURE_PATH = "./figs"
DATE_FORMAT = "%Y-%m-%d_%H-%M-%S"
CSV_PATH = "./datasets/airline.csv"
COLUMN = "content"

SEARCH_WORD = "delay"
NUM_RUNS = 5

random.seed(123)

if __name__ == "__main__":
    create_folder(FIGURE_PATH)
    df = pd.read_csv(CSV_PATH)

    # Initialize accumulators for averaging
    avg_results = None
    
    for run in range(NUM_RUNS):
        print(f"Running experiment {run + 1}/{NUM_RUNS}...")
    
        tols, results = test_search_time_against_tolerance(df, 0, 21, SEARCH_WORD)

        # Initialize accumulators on the first run
        if avg_results is None:
            avg_results = [list(r) for r in results]
        else:
            # Accumulate results for averaging
            for i in range(len(results)):
                for j in range(len(results[i])):
                    avg_results[i][j] += results[i][j]
    
    # Average the results
    avg_results = [[value / NUM_RUNS for value in result] for result in avg_results]

    # Unpack averaged results
    linear_search_times, array_search_times, linked_search_times = avg_results

    # Create plot figure
    print("\nGenerating plot...")
    plot_result(tols, linear_search_times, array_search_times, linked_search_times)

    print(f"\nExperiments on BK tree for approximate search completed. You may find result figures in {FIGURE_PATH}")