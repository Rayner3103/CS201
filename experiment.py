#python 3 program to demonstrate working of BK-Tree
from datetime import datetime
import time
import random
import os
import matplotlib.pyplot as plt

import dataLoader

class Array_BKTree:
    class Node:
        def __init__(self, max_dist=20, x=None):
            self.word = x
            self.MAX_DIST = max_dist
            self.next = [0] * self.MAX_DIST

    def __init__(self, maxn=1, tol=2, max_dist=20):
        self.MAXN = maxn
        self.TOL = tol
        self.max_dist = max_dist
        self.root = self.Node(self.max_dist)
        self.tree = [self.Node(self.max_dist) for _ in range(self.MAXN)]
        self.ptr = 0

    def add(self, word):
        curr = self.Node(self.max_dist, word)
        if not self.root.word:
            self.root.word = curr.word
            self.root.next = curr.next
            return
        self.add_helper(self.root, curr)

    def add_helper(self, node, curr):
        # ensure node.next is large enough for the distance index
        dist = edit_distance(curr.word, node.word)
        if dist >= len(node.next):
            node.next.extend([0] * (dist - len(node.next) + 1))

        idx = node.next[dist]
        if idx == 0 or not self.tree[idx] or not self.tree[idx].word:
            self.ptr += 1
            if self.ptr >= self.MAXN:
                self.tree.extend([self.Node(self.max_dist) for _ in range(self.MAXN)])
                self.MAXN *= 2
            self.tree[self.ptr] = curr
            node.next[dist] = self.ptr
        else:
            self.add_helper(self.tree[idx], curr)

    def get_similar_words(self, s):
        return self.get_similar_words_helper(self.root, s)

    def get_similar_words_helper(self, curr, s):
        ret = []
        if not curr or not curr.word:
            return ret

        dist = edit_distance(curr.word, s)

        if dist <= self.TOL:
            ret.append(curr.word)
        start = dist - self.TOL if dist - self.TOL > 0 else 1
        while start <= dist + self.TOL and start < self.max_dist:
            tmp = self.get_similar_words_helper(self.tree[curr.next[start]], s)
            ret += tmp
            start += 1
        return ret

class Linked_BKTree:
    class Node:
        def __init__(self, x=None):
            self.word = x
            self.children = {}  # distance -> Node

    def __init__(self, tol=2):
        self.root = self.Node()
        self.tol = tol

    def add_helper(self, root, node):
        if not root.word:
            root.word = node.word
            root.children = node.children
            return

        d = edit_distance(node.word, root.word)
        child = root.children.get(d)
        if not child or not child.word:
            root.children[d] = node
        else:
            self.add_helper(child, node)

    def add(self, word):
        self.add_helper(self.root, self.Node(word))

    def get_similar_words_helper(self, root, s, results):
        if not root or not root.word:
            return
        d = edit_distance(root.word, s)
        if d <= self.tol:
            results.append(root.word)

        low = max(0, d - self.tol)
        high = d + self.tol
        for dist_key, child in root.children.items():
            if low <= dist_key <= high:
                self.get_similar_words_helper(child, s, results)

    def get_similar_words(self, s):
        results = []
        self.get_similar_words_helper(self.root, s, results)
        return results

def edit_distance(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] != b[j - 1]:
                dp[i][j] = min(
                    dp[i - 1][j] + 1,  # deletion
                    dp[i][j - 1] + 1,  # insertion
                    dp[i - 1][j - 1] + 1  # replacement
                )
            else:
                dp[i][j] = dp[i - 1][j - 1]
    return dp[m][n]

def baseline_linear_search(dictionary, target):
    result = []
    for word in dictionary:
        if edit_distance(word, target) <= TOL:
            result.append(word)

    return result

#dictionary words
def test_search_time_against_dict_size(dictionary, sample_k=10, steps=10):
    """
    For a sequence of dictionary sizes, build both BK-trees from the first n words,
    pick `sample_k` random words from that n-sized subset and measure total
    retrieval time for each method. Plot one line per method.
    """
    n_total = len(dictionary)
    # generate `steps` increasing sizes from ~10%..100% (at least 1)
    sizes = sorted({max(1, int(n_total * i / steps)) for i in range(1, steps + 1)})

    linear_times = []
    array_times = []
    linked_times = []

    for n in sizes:
        subdict = dictionary[:n]

        # build trees from the first n words (building time is not included in retrieval timing)
        arrayTree = Array_BKTree(MAXN, TOL, MAX_DIST)
        linkedTree = Linked_BKTree(TOL)
        for w in subdict:
            arrayTree.add(w)
            linkedTree.add(w)

        k = min(sample_k, n)
        search_list = random.sample(subdict, k)

        # Linear
        start = time.perf_counter()
        for w in search_list:
            baseline_linear_search(subdict, w)
        end = time.perf_counter()
        linear_times.append(end - start)

        # Array BK Tree
        start = time.perf_counter()
        for w in search_list:
            arrayTree.get_similar_words(w)
        end = time.perf_counter()
        array_times.append(end - start)

        # Linked BK Tree
        start = time.perf_counter()
        for w in search_list:
            linkedTree.get_similar_words(w)
        end = time.perf_counter()
        linked_times.append(end - start)

        print(f"n={n}: linear={linear_times[-1]:.4f}s, array={array_times[-1]:.4f}s, linked={linked_times[-1]:.4f}s")

    # Plot results
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, linear_times, marker='o', label='Linear Search')
    plt.plot(sizes, array_times, marker='o', label='Array BK Tree')
    plt.plot(sizes, linked_times, marker='o', label='Pointer BK Tree')
    plt.xlabel('Dictionary size (n)')
    plt.ylabel(f'Total retrieval time for {sample_k} searches (seconds)')
    plt.title('Retrieval time vs dictionary size')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # plt.show()
    plt.savefig(f"{FIGURE_PATH}/time_dictSize_{datetime.now().strftime(DATE_FORMAT)}.png")

def test_search_time_against_tolerance(dictionary, lower, higher, sample_k=10):
    """
    For the dictionary, plot the time performance for varying edit distance tolerance between lower (inclusive) to higher (exclusive)
    """

    linear_times = []
    array_times = []
    linked_times = []
    tols = [i for i in range(lower, higher)]

    for tol in tols:

        # build trees from the first n words (building time is not included in retrieval timing)
        arrayTree = Array_BKTree(MAXN, tol, 100)
        linkedTree = Linked_BKTree(tol)
        for w in dictionary:
            arrayTree.add(w)
            linkedTree.add(w)

        search_list = random.sample(dictionary, sample_k)

        # Linear
        start = time.perf_counter()
        for w in search_list:
            baseline_linear_search(dictionary, w)
        end = time.perf_counter()
        linear_times.append(end - start)

        # Array BK Tree
        start = time.perf_counter()
        for w in search_list:
            arrayTree.get_similar_words(w)
        end = time.perf_counter()
        array_times.append(end - start)

        # Linked BK Tree
        start = time.perf_counter()
        for w in search_list:
            linkedTree.get_similar_words(w)
        end = time.perf_counter()
        linked_times.append(end - start)

        print(f"tol={tol}: linear={linear_times[-1]:.4f}s, array={array_times[-1]:.4f}s, linked={linked_times[-1]:.4f}s")

    # Plot results
    plt.figure(figsize=(8, 5))
    plt.plot(tols, linear_times, marker='o', label='Linear Search')
    plt.plot(tols, array_times, marker='o', label='Array BK Tree')
    plt.plot(tols, linked_times, marker='o', label='Pointer BK Tree')
    plt.xlabel('Tolerance (tol)')
    plt.ylabel(f'Total retrieval time for {sample_k} searches (seconds)')
    plt.title('Retrieval time vs tolerance')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # plt.show()
    plt.savefig(f"{FIGURE_PATH}/time_tol_{datetime.now().strftime(DATE_FORMAT)}.png")
    
def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created folder: {path}")
    
MAXN = 1
MAX_DIST = 50
TOL = 2
FIGURE_PATH = "./figs"
DATE_FORMAT = "%Y-%m-%d_%H-%M-%S"
random.seed(123)

if __name__ == "__main__":
    create_folder(FIGURE_PATH)
    dictionary = dataLoader.extract_unique_words_from_csv("./datasets/airline.csv", "content")

    test_search_time_against_dict_size(dictionary)
    test_search_time_against_tolerance(dictionary, 1, 10)
    