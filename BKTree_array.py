#python 3 program to demonstrate working of BK-Tree
import time
import dataLoader

MAXN = 100000
TOL = 2

class Array_BKTree:
    class Node:
        def __init__(self, x=None):
            self.word = x
            self.next = [0] * 20

    def __init__(self, maxn=100000, tol=2):
        self.MAXN = maxn
        self.TOL = tol
        self.root = self.Node()
        self.tree = [self.Node() for _ in range(self.MAXN)]
        self.ptr = 0

    def add(self, word):
        curr = self.Node(word)
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
                raise IndexError("Tree capacity exceeded")
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
        while start <= dist + self.TOL:
            tmp = self.get_similar_words_helper(self.tree[curr.next[start]], s)
            ret += tmp
            start += 1
        return ret

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
arrayTree = Array_BKTree(MAXN, TOL)

if __name__ == "__main__":
    dictionary = dataLoader.extract_unique_words_from_csv(r"C:\Users\rayne\repo\CS201LocalRepo\CS201\datasets\airline.csv", "content")
    sz = len(dictionary)
    #adding dict[] words on to tree
    for i in range(sz):
        arrayTree.add(dictionary[i])

    search_list = ["ops", "botk", "haha", "ooc"]
    for word in search_list:
        print("-"*20 + f"\n{word}:")

        start = time.perf_counter()
        match = baseline_linear_search(dictionary, word)
        end = time.perf_counter()
        time_taken = end - start
        print(f"Linear Search: {time_taken:.4f} seconds")
        
        start = time.perf_counter()
        match = arrayTree.get_similar_words(word)
        end = time.perf_counter()
        time_taken = end - start
        print(f"BK Tree: {time_taken:.4f} seconds")





