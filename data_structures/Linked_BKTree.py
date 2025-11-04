from utils import default_edit_distance

class Linked_BKTree:
    class Node:
        def __init__(self, x=None):
            self.word = x
            self.children = {}  # distance -> Node

    def __init__(self, tol=2, edit_distance=default_edit_distance):
        self.root = self.Node()
        self.tol = tol
        self.edit_distance = edit_distance

    def add_helper(self, curr, node):
        if not curr.word:
            curr.word = node.word
            curr.children = node.children
            return

        d = self.edit_distance(node.word, curr.word)
        child = curr.children.get(d)
        if not child or not child.word:
            curr.children[d] = node
        else:
            self.add_helper(child, node)

    def add(self, word):
        self.add_helper(self.root, self.Node(word))

    def get_similar_words_helper(self, curr, s, results):
        if not curr or not curr.word:
            return
        
        d = self.edit_distance(curr.word, s)
        if d <= self.tol:
            results.append(curr.word)

        low = max(0, d - self.tol)
        high = d + self.tol
        for i in range(low, high + 1):
                self.get_similar_words_helper(curr.children.get(i, None), s, results)

    def get_similar_words(self, s):
        results = []
        self.get_similar_words_helper(self.root, s, results)
        return results