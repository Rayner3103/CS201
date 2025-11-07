#TODO: update the test_insert_and_search_time_against_dict_size_with_ranking to reduce insert time
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
        array_tree = Array_BKTree.Array_BKTree(MAXN, TOL, MAX_DIST)
        for w in subdict:
            array_tree.add(w)
        end = time.perf_counter()
        array_insert_times.append(end - start)

        start = time.perf_counter()
        linked_tree = Linked_BKTree.Linked_BKTree(TOL)
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
            array_tree.get_similar_words(w)
        end = time.perf_counter()
        array_search_times.append(end - start)

        # Linked BK Tree
        start = time.perf_counter()
        for w in search_list:
            linked_tree.get_similar_words(w)
        end = time.perf_counter()
        linked_search_times.append(end - start)

        print(f"n={n} [search]: linear={linear_search_times[-1]:.4f}s, array={array_search_times[-1]:.4f}s, linked={linked_search_times[-1]:.4f}s")

    # Plot insert time results
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, array_insert_times, marker='o', label='Array BK Tree')
    plt.plot(sizes, linked_insert_times, marker='o', label='Linked BK Tree')
    plt.xlabel('Dictionary size (n)')
    plt.ylabel(f'Total insert time (s)')
    plt.title('Total insert time vs dictionary size')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # plt.show()
    plt.savefig(f"{FIGURE_PATH}/insertTime_dictSize_{datetime.now().strftime(DATE_FORMAT)}.png")

    # Plot search time results
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, linear_search_times, marker='o', label='Linear Search')
    plt.plot(sizes, array_search_times, marker='o', label='Array BK Tree')
    plt.plot(sizes, linked_search_times, marker='o', label='Linked BK Tree')
    plt.xlabel('Dictionary size (n)')
    plt.ylabel(f'Total retrieval time for {sample_k} searches (seconds)')
    plt.title('Retrieval time vs dictionary size')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # plt.show()
    plt.savefig(f"{FIGURE_PATH}/searchTime_dictSize_{datetime.now().strftime(DATE_FORMAT)}.png")

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
        
        array_tree = Array_BKTree.Array_BKTree(MAXN, TOL, MAX_DIST)
        for w in subdict:
            array_tree.add(w)
        array_spaces.append(asizeof.asizeof(array_tree) / 1024)

        linked_tree = Linked_BKTree.Linked_BKTree(TOL)
        for w in subdict:
            linked_tree.add(w)
        linked_spaces.append(asizeof.asizeof(linked_tree) / 1024)

        print(f"n={n}: linear={linear_spaces[-1]} KB, array={array_spaces[-1]} KB, linked={linked_spaces[-1]} KB")

    # Plot insert time results
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, linear_spaces, marker='o', label='Linear')
    plt.plot(sizes, array_spaces, marker='o', label='Array BK Tree')
    plt.plot(sizes, linked_spaces, marker='o', label='Linked BK Tree')
    plt.xlabel('Dictionary size (n)')
    plt.ylabel(f'Total size taken (KB)')
    plt.title('Total size taken vs dictionary size')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # plt.show()
    plt.savefig(f"{FIGURE_PATH}/totalSize_dictSize_{datetime.now().strftime(DATE_FORMAT)}.png")

def test_search_time_against_tolerance(dictionary, lower, higher, sample_k=10):
    """
    For the dictionary, plot the time performance for varying edit distance tolerance between lower (inclusive) to higher (exclusive)
    """

    linear_search_times = []
    array_search_times = []
    linked_searc_times = []
    tols = [i for i in range(lower, higher)]

    for tol in tols:
        # build trees from the first n words (building time is not included in retrieval timing)
        array_tree = Array_BKTree.Array_BKTree(MAXN, tol, MAX_DIST)
        linked_tree = Linked_BKTree.Linked_BKTree(tol)
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
            array_tree.get_similar_words(w)
        end = time.perf_counter()
        array_search_times.append(end - start)

        # Linked BK Tree
        start = time.perf_counter()
        for w in search_list:
            linked_tree.get_similar_words(w)
        end = time.perf_counter()
        linked_searc_times.append(end - start)

        print(f"tol={tol} [search]: linear={linear_search_times[-1]:.4f}s, array={array_search_times[-1]:.4f}s, linked={linked_searc_times[-1]:.4f}s")

    # Plot results
    plt.figure(figsize=(8, 5))
    plt.plot(tols, linear_search_times, marker='o', label='Linear Search')
    plt.plot(tols, array_search_times, marker='o', label='Array BK Tree')
    plt.plot(tols, linked_searc_times, marker='o', label='Linked BK Tree')
    plt.xlabel('Tolerance (tol)')
    plt.ylabel(f'Total retrieval time for {sample_k} searches (seconds)')
    plt.title('Retrieval time vs tolerance')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # plt.show()
    plt.savefig(f"{FIGURE_PATH}/searchTime_tol_{datetime.now().strftime(DATE_FORMAT)}.png")

def test_insert_and_search_time_against_dict_size_with_ranking(df, steps=10):
    """
    For a dataframe df, build both BK-trees from first n rows,
    and measure total retrieval time for each method. 
    Plot one line per method.
    """
    n_total = df.shape[0]
    # generate `steps` increasing sizes from ~10%..100% (at least 1)
    num_of_rows = sorted({max(1, int(n_total * i / steps)) for i in range(1, steps + 1)})
    sizes = []

    array_insert_times = []
    linked_insert_times = []

    array_search_times = []
    linked_search_times = []

    for n in num_of_rows:
        sub_df = df.iloc[:n]
        tokens = []
        dict_to_loop = dict()
        for _, row in sub_df.iterrows():
            content = str(row["content"]).lower()
            tokens += re.findall(r"[a-z]+", content)

        sizes.append(len(set(tokens)))

        # additional variable declaration to avoid difference due to new variable declaration
        start = 0
        end = 0

        array_tree = Array_BKTree.Array_BKTree(MAXN, TOL, MAX_DIST)
        start = time.time()
        for _, row in sub_df.iterrows():
            airline = str(row["airline_name"])
            content = str(row["content"]).lower()
            tokens = re.findall(r"[a-z]+", content)

            # Use set(tokens) to avoid double-counting same word in a single review
            for token in set(tokens):
                array_tree.add(token, airline)
        end = time.time()
        array_insert_times.append(end - start)

        linked_tree = Linked_BKTree.Linked_BKTree(TOL)
        start = time.time()
        for _, row in sub_df.iterrows():
            airline = str(row["airline_name"])
            content = str(row["content"]).lower()
            tokens = re.findall(r"[a-z]+", content)

            # Use set(tokens) to avoid double-counting same word in a single review
            for token in set(tokens):
                linked_tree.add(token, airline)
        end = time.time()
        linked_insert_times.append(end - start)

        print(f"n={n} [insert]: array={array_insert_times[-1]:.4f}s, linked={linked_insert_times[-1]:.4f}s")

        search_list = ["del", "serv", "clean", "food"]

        # # Linear
        # start = time.perf_counter()
        # for w in search_list:
        #     baseline_linear_search(subdict, w)
        # end = time.perf_counter()
        # linear_search_times.append(end - start)

        # Array BK Tree
        start = time.time()
        for w in search_list:
            array_tree.get_entity_rank_by_similar_words(w)
        end = time.time()
        array_search_times.append(end - start)

        # Linked BK Tree
        start = time.time()
        for w in search_list:
            linked_tree.get_entity_rank_by_similar_words(w)
        end = time.time()
        linked_search_times.append(end - start)

        # print(f"n={n} [search]: linear={linear_search_times[-1]:.4f}s, array={array_search_times[-1]:.4f}s, linked={linked_search_times[-1]:.4f}s")
        print(f"n={n} [search]: array={array_search_times[-1]:.4f}s, linked={linked_search_times[-1]:.4f}s")

    # Plot insert time results
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, array_insert_times, marker='o', label='Array BK Tree')
    plt.plot(sizes, linked_insert_times, marker='o', label='Linked BK Tree')
    plt.xlabel('Dictionary size (n)')
    plt.ylabel(f'Total insert time (s)')
    plt.title('Total insert time vs dictionary size - with airline ranking')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # plt.show()
    plt.savefig(f"{FIGURE_PATH}/insertTime_dictSize_{datetime.now().strftime(DATE_FORMAT)}.png")

    # Plot search time results
    plt.figure(figsize=(8, 5))
    # plt.plot(sizes, linear_search_times, marker='o', label='Linear Search')
    plt.plot(sizes, array_search_times, marker='o', label='Array BK Tree')
    plt.plot(sizes, linked_search_times, marker='o', label='Linked BK Tree')
    plt.xlabel('Dictionary size (n)')
    plt.ylabel(f'Total retrieval time for {len(search_list)} searches (seconds)')
    plt.title('Retrieval time vs dictionary size')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # plt.show()
    plt.savefig(f"{FIGURE_PATH}/ranking_searchTime_dictSize_{datetime.now().strftime(DATE_FORMAT)}.png")
    
MAXN = 1
MAX_DIST = 50
TOL = 2
FIGURE_PATH = "./figs"
DATE_FORMAT = "%Y-%m-%d_%H-%M-%S"
random.seed(123)

if __name__ == "__main__":
    create_folder(FIGURE_PATH)
    dictionary = extract_unique_words_from_csv("./datasets/airline.csv", "content")

    test_insert_and_search_time_against_dict_size(dictionary)
    test_search_time_against_tolerance(dictionary, 1, 10)
    test_spaces_against_dict_size(dictionary)

    print(f"Experiments on BK tree for approximate search completed. You may find result figures in {FIGURE_PATH}")

    # df = pd.read_csv("datasets/airline.csv")
    # array_tree = Array_BKTree.Array_BKTree(MAXN, TOL, MAX_DIST)
    # for _, row in df.iterrows():
    #     airline = str(row["airline_name"])
    #     content = str(row["content"]).lower()
    #     tokens = re.findall(r"[a-z]+", content)

    #     # Use set(tokens) to avoid double-counting same word in a single review
    #     for token in set(tokens):
    #         array_tree.add(token, airline)
    # print(array_tree.get_entity_rank_by_similar_words("del"))
    
    # df = pd.read_csv("datasets/airline.csv")
    # test_insert_and_search_time_against_dict_size_with_ranking(df)