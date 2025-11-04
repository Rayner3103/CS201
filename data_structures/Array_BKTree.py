from utils import default_edit_distance

class Array_BKTree:
    class Node:
        def __init__(self, max_dist=20, x=None):
            self.word = x
            self.MAX_DIST = max_dist
            self.next = [0] * self.MAX_DIST

    def __init__(self, maxn=1, tol=2, max_dist=20, edit_distance=default_edit_distance):
        self.MAXN = maxn
        self.TOL = tol
        self.max_dist = max_dist
        self.root = self.Node(self.max_dist)
        self.tree = [self.Node(self.max_dist) for _ in range(self.MAXN)]
        self.ptr = 0
        self.edit_distance = edit_distance

    def add(self, word):
        curr = self.Node(self.max_dist, word)
        if not self.root.word:
            self.root.word = curr.word
            self.root.next = curr.next
            return
        self.add_helper(self.root, curr)

    def add_helper(self, node, curr):
        # ensure node.next is large enough for the distance index
        dist = self.edit_distance(curr.word, node.word)
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

        dist = self.edit_distance(curr.word, s)

        if dist <= self.TOL:
            ret.append(curr.word)
        start = dist - self.TOL if dist - self.TOL > 0 else 1
        while start <= dist + self.TOL and start < self.max_dist:
            tmp = self.get_similar_words_helper(self.tree[curr.next[start]], s)
            ret += tmp
            start += 1
        return ret