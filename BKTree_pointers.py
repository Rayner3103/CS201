import time
import dataLoader



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

class Pointer_BKTree:
    class Node:
        def __init__(self, x=None):
            self.word = x
            self.children = {}  # distance -> Node

    def __init__(self, tol=2, distance_func=None):
        self.root = self.Node()
        self.tol = tol
        self.dist = distance_func or edit_distance

    def _add_node(self, root, node):
        if not root.word:
            root.word = node.word
            root.children = node.children
            return

        d = self.dist(node.word, root.word)
        child = root.children.get(d)
        if not child or not child.word:
            root.children[d] = node
        else:
            self._add_node(child, node)

    def add(self, word):
        self._add_node(self.root, self.Node(word))

    def _search_node(self, root, s, results):
        if not root or not root.word:
            return
        d = self.dist(root.word, s)
        if d <= self.tol:
            results.append(root.word)

        low = max(0, d - self.tol)
        high = d + self.tol
        for dist_key, child in root.children.items():
            if low <= dist_key <= high:
                self._search_node(child, s, results)

    def search(self, s):
        results = []
        self._search_node(self.root, s, results)
        return results

def baseline_linear_search(dictionary, target, tol=2):
    result = []
    for word in dictionary:
        if edit_distance(word, target) <= tol:
            result.append(word)
    return result

if __name__ == "__main__":
    TOL = 2
    dictionary = dataLoader.extract_unique_words_from_csv(
        r"C:\Users\rayne\repo\CS201LocalRepo\CS201\datasets\airline.csv", "content"
    )

    tree = Pointer_BKTree(tol=TOL)
    for w in dictionary:
        tree.add(w)

    search_list = ["ops", "botk", "haha", "ooc"]
    for word in search_list:
        print("-" * 20 + f"\n{word}:")

        start = time.perf_counter()
        match = baseline_linear_search(dictionary, word, tol=TOL)
        end = time.perf_counter()
        print(f"Linear Search: {(end - start):.4f} seconds")

        start = time.perf_counter()
        match = tree.search(word)
        end = time.perf_counter()
        print(f"BK Tree: {(end - start):.4f} seconds")