#TODO: modify to suite another style
from datetime import datetime
import time
import random
from pympler import asizeof
import matplotlib.pyplot as plt
import pandas as pd

from data_structures import Array_BKTree
from data_structures import Linked_BKTree

from data_structures import *
from utils import *

#dictionary words
def test_insert_and_search_time_against_dict_size(dictionary, sample_k=10, steps=10):
    """
    For a sequence of dictionary sizes, build both BK-trees from a random sample of n words,
    pick `sample_k` random words from the original dictionary and measure total
    retrieval time for each method. Plot one line per method.
    """
    n_total = len(dictionary)
    # generate `steps` increasing sizes from ~10%..100% (at least 1)
    sizes = sorted({max(1, int(n_total * i / steps)) for i in range(1, steps + 1)})

    array_insert_times = []
    linked_insert_times = []

    linear_search_times = []
    array_search_times = []
    linked_search_times = []

    for n in sizes:
        subdict = random.sample(dictionary, n)

        # additional variable declaration to avoid difference due to new variable declaration
        start = 0
        end = 0
        
        start = time.perf_counter()
        array_tree = Array_BKTree.Array_BKTree(MAXN, MAX_DIST)
        for w in subdict:
            array_tree.add(w)
        end = time.perf_counter()
        array_insert_times.append(end - start)

        start = time.perf_counter()
        linked_tree = Linked_BKTree.Linked_BKTree()
        for w in subdict:
            linked_tree.add(w)
        end = time.perf_counter()
        linked_insert_times.append(end - start)

        print(f"n={n} [insert]: array={array_insert_times[-1]:.4f}s, linked={linked_insert_times[-1]:.4f}s")

        k = min(sample_k, n)
        search_list = random.sample(dictionary, k)

        # Linear
        start = time.perf_counter()
        for w in search_list:
            baseline_linear_search(subdict, w)
        end = time.perf_counter()
        linear_search_times.append(end - start)

        # Array BK Tree
        start = time.perf_counter()
        for w in search_list:
            array_tree.get_similar_words(w, TOL)
        end = time.perf_counter()
        array_search_times.append(end - start)

        # Linked BK Tree
        start = time.perf_counter()
        for w in search_list:
            linked_tree.get_similar_words(w, TOL)
        end = time.perf_counter()
        linked_search_times.append(end - start)

        print(f"n={n} [search]: linear={linear_search_times[-1]:.4f}s, array={array_search_times[-1]:.4f}s, linked={linked_search_times[-1]:.4f}s")

    return sizes, array_insert_times, linked_insert_times, linear_search_times, array_search_times, linked_search_times


def test_spaces_against_dict_size(dictionary, steps=10):
    """
    For a sequence of dictionary sizes, build both BK-trees from a random sample of n words
    and measure total space taken for each method. Plot one line per method.
    """
    n_total = len(dictionary)
    # generate `steps` increasing sizes from ~10%..100% (at least 1)
    sizes = sorted({max(1, int(n_total * i / steps)) for i in range(1, steps + 1)})

    linear_spaces = []
    array_spaces = []
    linked_spaces = []

    for n in sizes:
        subdict = random.sample(dictionary, n)

        linear_spaces.append(asizeof.asizeof(subdict) / 1024)
        
        array_tree = Array_BKTree.Array_BKTree(MAXN, MAX_DIST)
        for w in subdict:
            array_tree.add(w)
        array_spaces.append(asizeof.asizeof(array_tree) / 1024)

        linked_tree = Linked_BKTree.Linked_BKTree()
        for w in subdict:
            linked_tree.add(w)
        linked_spaces.append(asizeof.asizeof(linked_tree) / 1024)

        print(f"n={n}: linear={linear_spaces[-1]} KB, array={array_spaces[-1]} KB, linked={linked_spaces[-1]} KB")

    return sizes, linear_spaces, array_spaces, linked_spaces


def test_search_time_against_tolerance(dictionary, lower, higher, sample_k=10):
    """
    For the dictionary, plot the time performance for varying edit distance tolerance between lower (inclusive) to higher (exclusive)
    """

    linear_search_times = []
    array_search_times = []
    linked_search_times = []
    tols = [i for i in range(lower, higher)]

    for tol in tols:
        # build trees from the first n words (building time is not included in retrieval timing)
        array_tree = Array_BKTree.Array_BKTree(MAXN, MAX_DIST)
        linked_tree = Linked_BKTree.Linked_BKTree()
        for w in dictionary:
            array_tree.add(w)
            linked_tree.add(w)

        search_list = random.sample(dictionary, sample_k)

        # additional variable declaration to avoid difference due to new variable declaration
        start = 0
        end = 0

        # Linear
        start = time.perf_counter()
        for w in search_list:
            baseline_linear_search(dictionary, w)
        end = time.perf_counter()
        linear_search_times.append(end - start)

        # Array BK Tree
        start = time.perf_counter()
        for w in search_list:
            array_tree.get_similar_words(w, tol)
        end = time.perf_counter()
        array_search_times.append(end - start)

        # Linked BK Tree
        start = time.perf_counter()
        for w in search_list:
            linked_tree.get_similar_words(w, tol)
        end = time.perf_counter()
        linked_search_times.append(end - start)

        print(f"tol={tol} [search]: linear={linear_search_times[-1]:.4f}s, array={array_search_times[-1]:.4f}s, linked={linked_search_times[-1]:.4f}s")

    return tols, linear_search_times, array_search_times, linked_search_times


def plot_all_results(sizes, array_insert_times, linked_insert_times, linear_search_times, 
                     array_search_times, linked_search_times, linear_spaces, array_spaces, 
                     linked_spaces, tols, linear_search_times_tol, array_search_times_tol, 
                     linked_search_times_tol, sample_k):
    """
    Create a 2x2 subplot figure with all experimental results
    """
    plt.figure(figsize=(14, 10))

    # Subplot 1: Insert time vs dictionary size
    plt.subplot(2, 2, 1)
    plt.plot(sizes, array_insert_times, 'o-', label='Array BK Tree')
    plt.plot(sizes, linked_insert_times, 'o-', label='Linked BK Tree')
    plt.xlabel('Dictionary Size (n)')
    plt.ylabel('Time (s)')
    plt.title('Insertion Time vs Dictionary Size')
    plt.legend()
    plt.grid(True)

    # Subplot 2: Search time vs dictionary size
    plt.subplot(2, 2, 2)
    plt.plot(sizes, linear_search_times, 'o-', label='Linear Search')
    plt.plot(sizes, array_search_times, 'o-', label='Array BK Tree')
    plt.plot(sizes, linked_search_times, 'o-', label='Linked BK Tree')
    plt.xlabel('Dictionary Size (n)')
    plt.ylabel('Time (s)')
    plt.title(f'Search Time vs Dictionary Size ({sample_k} searches)')
    plt.legend()
    plt.grid(True)

    # Subplot 3: Space vs dictionary size
    plt.subplot(2, 2, 3)
    plt.plot(sizes, linear_spaces, 'o-', label='Linear')
    plt.plot(sizes, array_spaces, 'o-', label='Array BK Tree')
    plt.plot(sizes, linked_spaces, 'o-', label='Linked BK Tree')
    plt.xlabel('Dictionary Size (n)')
    plt.ylabel('Size (KB)')
    plt.title('Memory Usage vs Dictionary Size')
    plt.legend()
    plt.grid(True)

    # Subplot 4: Search time vs tolerance
    plt.subplot(2, 2, 4)
    plt.plot(tols, linear_search_times_tol, 'o-', label='Linear Search')
    plt.plot(tols, array_search_times_tol, 'o-', label='Array BK Tree')
    plt.plot(tols, linked_search_times_tol, 'o-', label='Linked BK Tree')
    plt.xlabel('Tolerance (Edit Distance)')
    plt.ylabel('Time (s)')
    plt.title(f'Search Time vs Tolerance ({sample_k} searches)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(f"{FIGURE_PATH}/combined_results_{datetime.now().strftime(DATE_FORMAT)}.png")
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

random.seed(123)

if __name__ == "__main__":
    create_folder(FIGURE_PATH)
    dictionary = extract_unique_words_from_csv(CSV_PATH, COLUMN)

    # Run all experiments and collect data
    print("Running insert and search time experiments...")
    sizes, array_insert, linked_insert, linear_search, array_search, linked_search = \
        test_insert_and_search_time_against_dict_size(dictionary)
    
    print("\nRunning space experiments...")
    sizes_space, linear_spaces, array_spaces, linked_spaces = \
        test_spaces_against_dict_size(dictionary)
    
    print("\nRunning tolerance experiments...")
    tols, linear_search_tol, array_search_tol, linked_search_tol = \
        test_search_time_against_tolerance(dictionary, 1, 100)
    
    # Create combined subplot figure
    print("\nGenerating combined plot...")
    plot_all_results(sizes, array_insert, linked_insert, linear_search, array_search, 
                    linked_search, linear_spaces, array_spaces, linked_spaces, 
                    tols, linear_search_tol, array_search_tol, linked_search_tol, 
                    sample_k=10)

    print(f"\nExperiments on BK tree for approximate search completed. You may find result figures in {FIGURE_PATH}")